"""
YAML workflow parser for CETRA.

Provides functionality to parse YAML workflow files and convert them
into validated Pydantic models.
"""

import yaml
from pathlib import Path
from typing import Union
from pydantic import ValidationError

from .models import WorkflowConfig


class WorkflowParserError(Exception):
    """Base exception for workflow parsing errors."""
    pass


class WorkflowFileError(WorkflowParserError):
    """Raised when there's an issue reading the workflow file."""
    pass


class WorkflowValidationError(WorkflowParserError):
    """Raised when workflow validation fails."""
    pass


class WorkflowParser:
    """Parser for YAML workflow files.
    
    Converts YAML workflow definitions into validated WorkflowConfig objects.
    Handles file reading, YAML parsing, and Pydantic validation with clear error messages.
    """
    
    def load_workflow(self, filepath: Union[str, Path]) -> WorkflowConfig:
        """Load and parse a YAML workflow file.
        
        Args:
            filepath: Path to the YAML workflow file
            
        Returns:
            WorkflowConfig: Validated workflow configuration object
            
        Raises:
            WorkflowFileError: If the file cannot be read or doesn't exist
            WorkflowValidationError: If the YAML structure is invalid or doesn't match the schema
        """
        filepath = Path(filepath)
        
        # Check if file exists
        if not filepath.exists():
            raise WorkflowFileError(f"Workflow file not found: {filepath}")
        
        if not filepath.is_file():
            raise WorkflowFileError(f"Path is not a file: {filepath}")
        
        try:
            # Read and parse YAML file
            with open(filepath, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                
        except FileNotFoundError:
            raise WorkflowFileError(f"Workflow file not found: {filepath}")
        except PermissionError:
            raise WorkflowFileError(f"Permission denied reading file: {filepath}")
        except yaml.YAMLError as e:
            raise WorkflowValidationError(f"Invalid YAML format in {filepath}: {e}")
        except Exception as e:
            raise WorkflowFileError(f"Error reading workflow file {filepath}: {e}")
        
        # Validate YAML data is not empty
        if yaml_data is None:
            raise WorkflowValidationError(f"Workflow file is empty: {filepath}")
        
        # Extract workflow section
        if not isinstance(yaml_data, dict):
            raise WorkflowValidationError(f"Workflow file must contain a YAML object, got {type(yaml_data).__name__}: {filepath}")
        
        workflow_data = yaml_data.get('workflow')
        if workflow_data is None:
            raise WorkflowValidationError(f"Workflow file must contain a 'workflow' section: {filepath}")
        
        try:
            # Create and validate WorkflowConfig
            return WorkflowConfig(**workflow_data)
            
        except ValidationError as e:
            error_details = []
            for error in e.errors():
                field = '.'.join(str(loc) for loc in error['loc'])
                msg = error['msg']
                error_details.append(f"{field}: {msg}")
            
            raise WorkflowValidationError(
                f"Workflow validation failed in {filepath}:\n" + 
                '\n'.join(f"  - {detail}" for detail in error_details)
            )
        except Exception as e:
            raise WorkflowValidationError(f"Error validating workflow in {filepath}: {e}")