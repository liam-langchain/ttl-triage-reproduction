"""Simple React agent 2 for TTL testing."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime


class Context(TypedDict):
    """Context parameters for agent2."""
    extraction_mode: str


@dataclass  
class State:
    """State for agent2."""
    input_data: str = "agent2_input"
    extracted_result: str = ""


async def extract_data(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Simple extraction function for agent2."""
    mode = runtime.context.get('extraction_mode') if runtime.context else 'basic'
    
    return {
        "extracted_result": f"Agent2 extracted: {state.input_data} using mode: {mode}"
    }


# Define the graph
graph = (
    StateGraph(State, context_schema=Context)
    .add_node("extract", extract_data)
    .add_edge("__start__", "extract") 
    .add_edge("extract", "__end__")
    .compile()
)