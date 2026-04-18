import pytest
from nodes.summarizer import SummarizerNode
from nodes.email_generator import EmailGeneratorNode
from nodes.base_node import WorkflowState
from schemas import SummarizerOutput, EmailOutput

def test_workflow_state_initialization():
    state = WorkflowState("Initial input")
    assert state.input == "Initial input"
    assert state.output == ""
    assert len(state.history) == 0

def test_summarizer_node_logic(mocker):
    # Mock the LLM service to return a structured Pydantic object
    mock_response = SummarizerOutput(
        summary="This is a test summary",
        key_points=["Point 1", "Point 2"],
        word_count=5,
        confidence=0.9
    )
    mocker.patch("nodes.summarizer.generate_response", return_value=mock_response)
    
    node = SummarizerNode()
    state = WorkflowState("Test large text " * 10)
    new_state = node.execute(state)
    
    assert "This is a test summary" in new_state.output
    assert "summarizer_data" in new_state.variables
    assert new_state.variables["summarizer_data"]["word_count"] == 5

def test_state_passes_between_nodes(mocker):
    # Setup mocks
    mock_sum = SummarizerOutput(summary="Sum1", key_points=[], word_count=0, confidence=1.0)
    mock_email = EmailOutput(subject="Sub1", body="Body1", tone="formal", suggested_recipients=[])
    
    mocker.patch("nodes.summarizer.generate_response", return_value=mock_sum)
    mocker.patch("nodes.email_generator.generate_response", return_value=mock_email)
    
    state = WorkflowState("raw input")
    
    # Run sequence
    state = SummarizerNode().execute(state)
    state = EmailGeneratorNode().execute(state)
    
    assert len(state.history) == 2
    assert state.history[0]["node"] == "Summarizer"
    assert state.history[1]["node"] == "Email Generator"
    assert "Sub1" in state.output
