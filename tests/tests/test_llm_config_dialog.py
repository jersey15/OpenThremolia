import pytest
from streamlit.testing.v1 import AppTest

from thremolia.llm_interfaces import (
    ChatGPTInterface,
    OllamaInterface,
    OpenAICompatibleInterface,
)
from thremolia.llm_interfaces.llm_utils import UnknownInterfaceError
from thremolia.llm_interfaces.openai_interface import OpenAIInterface
from thremolia.streamlit_gui.llm_config_dialog import switch_llm_interface


@pytest.mark.parametrize(
    ("selected_llm"),
    [
        "Cat",
    ],
)
def test_switch_llm_interface_wrong(selected_llm):
    at = AppTest.from_file("streamlit_gui.py").run()

    with pytest.raises(UnknownInterfaceError) as excinfo:
        at.session_state.llm_interface = switch_llm_interface(selected_llm)

    assert f"Unknown client type: {selected_llm.lower()}" in str(excinfo.value)
    assert excinfo.type is UnknownInterfaceError


@pytest.mark.parametrize(
    ("selected_llm", "correct_type"),
    [
        ("chatGPT", ChatGPTInterface),
        ("Ollama", OllamaInterface),
        ("openaicompatible", OpenAICompatibleInterface),
    ],
)
def test_switch_llm_interface(selected_llm, correct_type, monkeypatch):
    # These interfaces require secrets normally supplied via .env; dummy
    # values are sufficient since only object construction is asserted on.
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("THIRD_PARTY_HOST", "http://localhost:0/v1")
    # Avoid real network calls (and their flakiness/timeouts in sandboxed
    # environments) from check_api(), which the app calls on every startup.
    # A False result also skips init_default_embeddings(), which would
    # otherwise try to generate real embeddings against the dummy key/host.
    monkeypatch.setattr(OpenAIInterface, "check_api", lambda self: (False, "stubbed"))
    monkeypatch.setattr(OllamaInterface, "check_api", lambda self: (False, "stubbed"))

    at = AppTest.from_file("streamlit_gui.py").run()

    at.session_state.llm_interface = switch_llm_interface(selected_llm)

    assert isinstance(at.session_state.llm_interface, correct_type)
