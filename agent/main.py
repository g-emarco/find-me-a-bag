from dotenv import load_dotenv
from langchain.output_parsers import EnumOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
from langgraph.graph import END, StateGraph

from agent.nodes import (
    Searches,
    hybrid_search,
    keyword_search,
    semantic_search,
    update_session_state,
)
from agent.state import AgentState

load_dotenv()

llm = VertexAI(model_name="gemini-1.5-flash-preview-0514", location="me-west1")


def router(state: AgentState) -> str:
    thread_id = state["thread_id"]
    update_session_state(session_id=thread_id, state="router")

    router_prompt_template = """
    You are a router, your task is make a decision between 3 possible action paths based on the human message:

    "SEMANTIC_SEARCH" Take this path if the query/image can be answered by running a semantic / similarity search query to the vectordb.
                      For example: cute bag to go to the beach
                      For example: only an image_file_path (without a 'query' in the state)
                      
    "HYBRID_SEARCH" Take this path if the query should be a result of a combined  similarity search query to the vectordb with a keywords query.
                    For example, you have in state['image_file_path']  an image_file_path and in state['query'] you have a query like: 'Cymbal Bag'
        
    "KEYWORD_SEARCH" Take this path if you have only a query that requires a simple keyword search, for example "a blue bag" can be translated into a keyword search. 
                      Do not take this path if you have an image in the state
    
    Rule 1 : You should never infer information if it does not appear in the context of the query
    Rule 2 : You can only answer with the type of query that you choose based on why you choose it.
    Rule 3: if you have image_file_path and query- it is a hybrid search
    
    Answer only with the type of query that you choose, just one word.
    {input}
    {image_file_path}
    Instructions: {instructions}
    """

    parser = EnumOutputParser(enum=Searches)

    router_prompt = PromptTemplate.from_template(
        template=router_prompt_template
    ).partial(instructions=parser.get_format_instructions())
    chain = router_prompt | llm | parser

    query = state["query"]
    image_file_path = state.get("image_file_path")

    res = chain.invoke({"input": query, "image_file_path": image_file_path})

    match res:
        case Searches.SEMANTIC_SEARCH:
            return str(Searches.SEMANTIC_SEARCH.value)
        case Searches.HYBRID_SEARCH:
            return str(Searches.HYBRID_SEARCH.value)
        case Searches.KEYWORD_SEARCH:
            return str(Searches.KEYWORD_SEARCH.value)

    raise ValueError(f"Could not determine next node for {input=}")


def start_dummy(state):
    return {}


flow = StateGraph(AgentState)
flow.add_node("classify_query", start_dummy)
flow.set_entry_point("classify_query")
flow.add_conditional_edges("classify_query", router)
flow.add_node(Searches.SEMANTIC_SEARCH.value, semantic_search)  # type: ignore
flow.add_node(Searches.HYBRID_SEARCH.value, hybrid_search)  # type: ignore
flow.add_node(Searches.KEYWORD_SEARCH.value, keyword_search)  # type: ignore
flow.add_edge(Searches.KEYWORD_SEARCH.value, END)  # type: ignore
flow.add_edge(Searches.HYBRID_SEARCH.value, END)  # type: ignore
flow.add_edge(Searches.SEMANTIC_SEARCH.value, END)  # type: ignore


compiled_graph = flow.compile()
# compiled_graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    compiled_graph.invoke({"query": "find me a bag similar to this bag"})
    compiled_graph.invoke({"query": "find me a a black bag"})
    compiled_graph.invoke({"query": "find me a a black bag similar to my bag"})
