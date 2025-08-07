"""
Pydantic models for CETRA workflow configuration.

These models define the structure for YAML workflow definitions
that will be parsed and executed by CETRA agents.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an AI agent in a workflow.
    
    Defines the behavior and parameters for agents that will
    execute workflow steps.
    """
    instructions: str = Field(..., description="Instructions for the agent's behavior")
    temperature: float = Field(0.7, description="Temperature parameter for AI generation", ge=0.0, le=2.0)


class WorkflowStep(BaseModel):
    """A single step in a workflow execution.
    
    Each step is executed by a specific agent with a prompt template.
    """
    name: str = Field(..., description="Unique name for this workflow step")
    agent: str = Field(..., description="Name of the agent to execute this step")
    ask: str = Field(..., description="Prompt template for the agent to execute")


class WorkflowConfig(BaseModel):
    """Complete configuration for a CETRA workflow.
    
    Represents the entire workflow definition that will be parsed
    from YAML and executed by the CETRA engine.
    """
    name: str = Field(..., description="Name of the workflow")
    description: Optional[str] = Field(None, description="Optional description of the workflow")
    agents: Dict[str, AgentConfig] = Field(..., description="Dictionary of agent configurations")
    steps: List[WorkflowStep] = Field(..., description="List of workflow steps to execute")