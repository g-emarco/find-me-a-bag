from datetime import datetime
from typing import Any, Dict

from dotenv import load_dotenv
from google.cloud import firestore_v1
from google.cloud.firestore_v1 import FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_google_vertexai import ChatVertexAI, VertexAI

from assistant_agent.state import AssistantAgentState
from db_setup import db

load_dotenv()
import os

from langgraph.prebuilt import ToolNode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

llm = ChatVertexAI(model_name="gemini-1.5-pro-preview-0409")

html_content = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    /* Some basic styling to make the email look nice */
    body { font-family: sans-serif; max-width: 100%; width: auto; }
    img { max-width: 100%; height: auto; }
    @media (min-width: 600px) { /* Adjusts the size for screens wider than 600px */
      img { max-width: 25%; } /* Limits image width to 25% of the container on desktop */
    }
  </style>
</head>
<body>

  <h2>Hi!</h2>

  <p>I was thinking about you and saw this beautiful bag. What do you think?</p>

  <img src="https://storage.googleapis.com/984298407984_bucket-summit-tlv-24-public/bag-dataset/greenclassic2.png" alt="Green Classic Bag">

  <p>I love the rich green color, and it seems like the perfect size for everyday use. It looks so stylish and classic, just like you! 😉</p>

  <p>Let me know if you like it, and we can get it for you!</p>

  <p>Love,<br>
  [Your Name]</p>

</body>
</html>

"""


@tool
def send_email() -> None:
    """
    "This function sends an email letting the recipient know that someone is looking for a bag to buy them
    :return: None
    """
    print("@@@@@@@@@@@@@@@@@@@@@@@@")
    message = Mail(
        from_email="e75686682@gmail.com",
        to_emails="emarco@google.com",
        subject="Cool bag to buy",
        html_content=html_content,
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


TOOLS = [get_user_information, send_email]


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
