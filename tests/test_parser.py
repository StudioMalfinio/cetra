"""
Pytest tests for CETRA flow parser.

This module contains tests that validate the YAML parser works correctly
by loading flow files and verifying their parsed contents.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cetra.parser import FlowParser, FlowParserError
from cetra.models import FlowConfig


class TestFlowParser:
    """Test suite for FlowParser functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.parser = FlowParser()
        self.test_flow_file = Path(__file__).parent.parent / "resources/yaml_flow/0.yaml"
    
    def test_flow_file_exists(self):
        """Test that the test flow file exists."""
        assert self.test_flow_file.exists(), f"Test flow file not found: {self.test_flow_file}"
        assert self.test_flow_file.is_file(), f"Test flow path is not a file: {self.test_flow_file}"
    
    def test_load_flow(self):
        """Test loading and parsing a flow file."""
        # Load the flow
        config = self.parser.load_flow(self.test_flow_file)
        
        # Verify it returns a FlowConfig instance
        assert isinstance(config, FlowConfig)
        
        # Verify flow structure
        assert hasattr(config, 'flow')
        assert isinstance(config.flow, list)
        assert len(config.flow) > 0
    
    def test_flow_steps_structure(self):
        """Test that flow steps have the correct structure."""
        config = self.parser.load_flow(self.test_flow_file)
        
        # Check first step
        first_step = config.flow[0]
        assert hasattr(first_step, 'id')
        assert first_step.id == "start"
        assert hasattr(first_step, 'prompt')
        assert first_step.prompt is not None
        assert hasattr(first_step, 'next_step')
    
    def test_flow_with_tool_calls(self):
        """Test that flows with tool calls are parsed correctly."""
        config = self.parser.load_flow(self.test_flow_file)
        
        # Find a step with tool_call
        tool_steps = [step for step in config.flow if step.tool_call is not None]
        assert len(tool_steps) > 0
        
        # Verify tool_call structure
        tool_step = tool_steps[0]
        assert hasattr(tool_step.tool_call, 'name')
        assert hasattr(tool_step.tool_call, 'description')
        assert hasattr(tool_step.tool_call, 'parameters')
        assert hasattr(tool_step.tool_call, 'output')
    
    def test_flow_with_actions(self):
        """Test that flows with conditional actions are parsed correctly."""
        config = self.parser.load_flow(self.test_flow_file)
        
        # Find a step with actions
        action_steps = [step for step in config.flow if step.actions is not None]
        assert len(action_steps) > 0
        
        # Verify action structure
        action_step = action_steps[0]
        assert isinstance(action_step.actions, list)
        
        first_action = action_step.actions[0]
        assert hasattr(first_action, 'condition')
        assert hasattr(first_action, 'next_step')
    
    def test_multiple_flow_files(self):
        """Test parsing multiple flow files."""
        flow_dir = Path(__file__).parent.parent / "resources/yaml_flow"
        flow_files = list(flow_dir.glob("*.yaml"))[:3]  # Test first 3 files
        
        for flow_file in flow_files:
            config = self.parser.load_flow(flow_file)
            assert isinstance(config, FlowConfig)
            assert len(config.flow) > 0
            
            # Each flow should have a starting step
            step_ids = [step.id for step in config.flow]
            assert len(step_ids) > 0
    
    def test_nonexistent_file_error(self):
        """Test that loading a nonexistent file raises appropriate error."""
        nonexistent_file = "nonexistent_flow.yaml"
        
        with pytest.raises(FlowParserError) as excinfo:
            self.parser.load_flow(nonexistent_file)
        
        assert "not found" in str(excinfo.value).lower()
    
    def test_display_parsed_flow(self, capsys):
        """Test displaying the parsed flow in a readable format."""
        config = self.parser.load_flow(self.test_flow_file)
        
        # Display formatted output
        print(f"🚀 Loading flow: {self.test_flow_file.name}")
        print(f"📋 Flow with {len(config.flow)} steps")
        
        print("\n⚡ Steps:")
        for i, step in enumerate(config.flow, 1):
            prompt_preview = ""
            if step.prompt:
                prompt_preview = step.prompt[:50] + "..." if len(step.prompt) > 50 else step.prompt
            
            tool_info = f" [Tool: {step.tool_call.name}]" if step.tool_call else ""
            action_info = f" [Actions: {len(step.actions)}]" if step.actions else ""
            
            print(f"  {i}. {step.id}: {prompt_preview}{tool_info}{action_info}")
        
        print("\n✅ Flow parsing successful!")
        
        # Capture output and verify key elements are present
        captured = capsys.readouterr()
        assert "🚀 Loading flow" in captured.out
        assert "✅ Flow parsing successful!" in captured.out
        assert "steps" in captured.out.lower()