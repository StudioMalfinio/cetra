"""
Pytest tests for CETRA workflow parser.

This module contains tests that validate the YAML parser works correctly
by loading the demo workflow and verifying its parsed contents.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cetra.parser import WorkflowParser, WorkflowParserError
from cetra.models import WorkflowConfig


class TestWorkflowParser:
    """Test suite for WorkflowParser functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.parser = WorkflowParser()
        self.demo_file = Path(__file__).parent.parent / "demo_workflow.yaml"
    
    def test_demo_workflow_exists(self):
        """Test that the demo workflow file exists."""
        assert self.demo_file.exists(), f"Demo workflow file not found: {self.demo_file}"
        assert self.demo_file.is_file(), f"Demo workflow path is not a file: {self.demo_file}"
    
    def test_load_demo_workflow(self):
        """Test loading and parsing the demo workflow."""
        # Load the workflow
        config = self.parser.load_workflow(self.demo_file)
        
        # Verify it returns a WorkflowConfig instance
        assert isinstance(config, WorkflowConfig)
        
        # Verify basic workflow properties
        assert config.name == "hello_agent_demo"
        assert config.description == "Démonstration basique d'un agent conversationnel"
    
    def test_demo_workflow_agents(self):
        """Test that demo workflow agents are correctly parsed."""
        config = self.parser.load_workflow(self.demo_file)
        
        # Verify agents exist
        assert "greeter" in config.agents
        assert "helper" in config.agents
        
        # Verify agent configurations
        greeter = config.agents["greeter"]
        assert greeter.instructions == "Tu es un assistant amical et professionnel. Réponds de manière chaleureuse et personnalisée."
        assert greeter.temperature == 0.7
        
        helper = config.agents["helper"]
        assert helper.instructions == "Tu es un assistant serviable qui aime aider les utilisateurs."
        assert helper.temperature == 0.5
    
    def test_demo_workflow_steps(self):
        """Test that demo workflow steps are correctly parsed."""
        config = self.parser.load_workflow(self.demo_file)
        
        # Verify number of steps
        assert len(config.steps) == 3
        
        # Verify step details
        steps = config.steps
        
        assert steps[0].name == "welcome"
        assert steps[0].agent == "greeter"
        assert steps[0].ask == "Dis bonjour à {name} et présente-toi brièvement"
        
        assert steps[1].name == "offer_help"
        assert steps[1].agent == "helper"
        assert steps[1].ask == "Demande à {name} comment tu peux l'aider aujourd'hui"
        
        assert steps[2].name == "farewell"
        assert steps[2].agent == "greeter"
        assert steps[2].ask == "Remercie {name} et dis au revoir poliment"
    
    def test_nonexistent_file_error(self):
        """Test that loading a nonexistent file raises appropriate error."""
        nonexistent_file = "nonexistent_workflow.yaml"
        
        with pytest.raises(WorkflowParserError) as excinfo:
            self.parser.load_workflow(nonexistent_file)
        
        assert "not found" in str(excinfo.value).lower()
    
    def test_display_parsed_workflow(self, capsys):
        """Test displaying the parsed workflow in a readable format."""
        config = self.parser.load_workflow(self.demo_file)
        
        # Display formatted output (similar to original script)
        print(f"🚀 Loading workflow: {self.demo_file.name}")
        print(f"📋 Workflow: {config.name}")
        
        if config.description:
            print(f"📄 Description: {config.description}")
        
        print("\n👥 Agents:")
        for agent_name, agent_config in config.agents.items():
            # Truncate instructions if too long
            instructions = agent_config.instructions
            if len(instructions) > 50:
                instructions = instructions[:47] + "..."
            
            print(f"  - {agent_name}: \"{instructions}\" (temp: {agent_config.temperature})")
        
        print("\n⚡ Steps:")
        for i, step in enumerate(config.steps, 1):
            # Truncate ask if too long
            ask = step.ask
            if len(ask) > 50:
                ask = ask[:47] + "..."
            
            print(f"  {i}. {step.name} → {step.agent}: \"{ask}\"")
        
        print("\n✅ Parsing successful!")
        
        # Capture output and verify key elements are present
        captured = capsys.readouterr()
        assert "🚀 Loading workflow" in captured.out
        assert "hello_agent_demo" in captured.out
        assert "greeter" in captured.out
        assert "helper" in captured.out
        assert "✅ Parsing successful!" in captured.out