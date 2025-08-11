"""
Cetra - Contextual Execution Through Reactive Agents

YAML flow orchestration for AI agents.
"""

__version__ = "0.1.0"

from .parser import FlowParser, FlowParserError, FlowFileError, FlowValidationError
from .models import FlowConfig, FlowStep, ToolCall, FlowAction, ToolParameter, ToolOutput

__all__ = [
    "FlowParser",
    "FlowParserError", 
    "FlowFileError",
    "FlowValidationError",
    "FlowConfig",
    "FlowStep",
    "ToolCall",
    "FlowAction",
    "ToolParameter",
    "ToolOutput",
]

def hello() -> str:
    return "Hello from cetra!"