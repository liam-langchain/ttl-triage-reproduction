"""Simple React agent 1 for TTL testing."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime


class Context(TypedDict):
    """Context parameters for agent1."""
    config_param: str


@dataclass
class State:
    """State for agent1."""
    message: str = "agent1_input"
    result: str = ""


async def process_request(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Simple processing function for agent1."""
    context_value = runtime.context.get('config_param') if runtime.context else 'default'
    
    return {
        "result": f"Agent1 processed: {state.message} with config: {context_value}"
    }


# Define the graph
graph = (
    StateGraph(State, context_schema=Context)
    .add_node("process", process_request)
    .add_edge("__start__", "process")
    .add_edge("process", "__end__")
    .compile()
)