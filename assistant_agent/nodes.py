from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_google_vertexai import ChatVertexAI, VertexAI

from assistant_agent._html_for_mail import _populate_bag_email
from assistant_agent.state import AssistantAgentState
from db_setup import db

load_dotenv()
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

llm = ChatVertexAI(model_name="gemini-1.5-flash-preview-0514", location="me-west1")


@tool
def send_email(bag_data: Optional[Dict[str, Any]]) -> None:
    """
    "This function sends an email letting the recipient know that someone is looking for a bag to buy them
    :return: None
    """
    print("@@@@@@@@@@")
    print(bag_data)
    html_content2 = _populate_bag_email(bag_data=bag_data)
    message = Mail(
        from_email=os.environ["FROM_EMAIL"],
        to_emails=os.environ["TO_EMAIL"],
        subject="Cool bag to buy",
        html_content=html_content2,
    )

    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


@tool
def get_user_information(user_id: str = "emKszv8xjISy446FJNmK") -> Dict[str, Any]:
    """
    :param user_id: the user id to get information on
    :return: a dictionary containing the information about the user such as: first_name, last_name, age, email, time_browsing
    """

    document = db.collection("Users").document(user_id).get()
    print(document.to_dict)
    return {"user_data": document.to_dict()}


@tool
def get_information_about_bag(bag_name: str):
    """

    :param bag_name: the name of the bag to search
    :return: all the information relevant for a bag
    """
    document = db.collection("Bags").where("name", "==", bag_name).get()[0]
    return {"bag_data": document.to_dict()}


TOOLS = [get_user_information, send_email, get_information_about_bag]


def assistant_node(state: AssistantAgentState):
    print(state)
    primary_assistant_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful customer support assistant for Cymbal- an e-commerece specializing in womens bag . "
                " Use the provided tools to search for user information, bag information, send email, and other information to assist the user's queries. "
                "\n\nCurrent user:\n<User>\n{user_id}\n</User>"
                "\nCurrent time: {time}.",
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now())

    chain = primary_assistant_prompt | llm.bind_tools(TOOLS)
    res = chain.invoke(state)
    print(res)
    return {"messages": res}
