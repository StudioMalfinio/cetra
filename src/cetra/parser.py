"""
YAML flow parser for CETRA.

Provides functionality to parse YAML flow files and convert them
into validated Pydantic models.
"""

import yaml
from pathlib import Path
from typing import Union
from pydantic import ValidationError

from .models import FlowConfig


class FlowParserError(Exception):
    """Base exception for flow parsing errors."""
    pass


class FlowFileError(FlowParserError):
    """Raised when there's an issue reading the flow file."""
    pass


class FlowValidationError(FlowParserError):
    """Raised when flow validation fails."""
    pass


class FlowParser:
    """Parser for YAML flow files.
    
    Converts YAML flow definitions into validated FlowConfig objects.
    Handles file reading, YAML parsing, and Pydantic validation with clear error messages.
    """
    
    def load_flow(self, filepath: Union[str, Path]) -> FlowConfig:
        """Load and parse a YAML flow file.
        
        Args:
            filepath: Path to the YAML flow file
            
        Returns:
            FlowConfig: Validated flow configuration object
            
        Raises:
            FlowFileError: If the file cannot be read or doesn't exist
            FlowValidationError: If the YAML structure is invalid or doesn't match the schema
        """
        filepath = Path(filepath)
        
        # Check if file exists
        if not filepath.exists():
            raise FlowFileError(f"Flow file not found: {filepath}")
        
        if not filepath.is_file():
            raise FlowFileError(f"Path is not a file: {filepath}")
        
        try:
            # Read and parse YAML file
            with open(filepath, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                
        except FileNotFoundError:
            raise FlowFileError(f"Flow file not found: {filepath}")
        except PermissionError:
            raise FlowFileError(f"Permission denied reading file: {filepath}")
        except yaml.YAMLError as e:
            raise FlowValidationError(f"Invalid YAML format in {filepath}: {e}")
        except Exception as e:
            raise FlowFileError(f"Error reading flow file {filepath}: {e}")
        
        # Validate YAML data is not empty
        if yaml_data is None:
            raise FlowValidationError(f"Flow file is empty: {filepath}")
        
        # Validate structure
        if not isinstance(yaml_data, dict):
            raise FlowValidationError(f"Flow file must contain a YAML object, got {type(yaml_data).__name__}: {filepath}")
        
        # Check for flow section
        flow_data = yaml_data.get('flow')
        if flow_data is None:
            raise FlowValidationError(f"Flow file must contain a 'flow' section: {filepath}")
        
        try:
            # Create and validate FlowConfig
            return FlowConfig(flow=flow_data)
            
        except ValidationError as e:
            error_details = []
            for error in e.errors():
                field = '.'.join(str(loc) for loc in error['loc'])
                msg = error['msg']
                error_details.append(f"{field}: {msg}")
            
            raise FlowValidationError(
                f"Flow validation failed in {filepath}:\n" + 
                '\n'.join(f"  - {detail}" for detail in error_details)
            )
        except Exception as e:
            raise FlowValidationError(f"Error validating flow in {filepath}: {e}")