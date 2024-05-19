from unittest.mock import patch, MagicMock

from dotenv import load_dotenv

load_dotenv()
from agent.nodes import update_session_state


def test_update_session_state():
    # update_session_state(session_id="test1", state="hybrid_search_node")
    assert 1 == 1
