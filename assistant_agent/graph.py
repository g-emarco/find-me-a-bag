from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from assistant_agent.nodes import TOOLS, assistant_node
from assistant_agent.state import AssistantAgentState

builder = StateGraph(AssistantAgentState)


builder.add_node("assistant", assistant_node)
builder.set_entry_point("assistant")

builder.add_node("action", ToolNode(TOOLS))
builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {"action": "action", END: END},
)
builder.add_edge("action", "assistant")

graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="assistant_graph.png")
