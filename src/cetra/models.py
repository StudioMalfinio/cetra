"""
Pydantic models for CETRA flow and workflow configuration.

These models define the structure for YAML flow definitions
that will be parsed and executed by CETRA agents.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    """Parameter definition for tool calls."""
    type: str = Field(..., description="Parameter type (e.g., 'string')")
    description: str = Field(..., description="Parameter description")
    required: bool = Field(False, description="Whether the parameter is required")


class ToolOutput(BaseModel):
    """Output definition for tool calls."""
    type: str = Field(..., description="Output type (e.g., 'string')")
    description: str = Field(..., description="Output description")


class ToolCall(BaseModel):
    """Tool call configuration for a flow step."""
    name: str = Field(..., description="Name of the tool to call")
    description: str = Field(..., description="Description of what the tool does")
    parameters: Dict[str, ToolParameter] = Field(..., description="Tool parameters")
    output: Optional[Dict[str, ToolOutput]] = Field(None, description="Expected tool outputs")


class FlowAction(BaseModel):
    """Action to take based on conditions."""
    condition: str = Field(..., description="Condition to evaluate")
    next_step: Optional[str] = Field(None, description="Next step ID to execute")


class FlowStep(BaseModel):
    """A single step in a flow execution.
    
    Each step can contain a prompt, tool call, response template,
    and conditional actions to determine the next step.
    """
    id: str = Field(..., description="Unique ID for this flow step")
    prompt: Optional[str] = Field(None, description="Prompt to display or process")
    tool_call: Optional[ToolCall] = Field(None, description="Tool to call in this step")
    response: Optional[str] = Field(None, description="Response template")
    actions: Optional[List[FlowAction]] = Field(None, description="Conditional actions")
    next_step: Optional[str] = Field(None, description="Default next step ID")


class FlowConfig(BaseModel):
    """Complete configuration for a CETRA flow.
    
    Represents the entire flow definition that will be parsed
    from YAML and executed by the CETRA engine.
    """
    flow: List[FlowStep] = Field(..., description="List of flow steps to execute")


