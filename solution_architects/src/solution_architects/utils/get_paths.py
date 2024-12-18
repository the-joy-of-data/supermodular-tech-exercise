import os

def get_project_path() -> str:
    """Get the project path from command line arguments or environment variable"""
    # Try to get from environment variable first
    project_path = os.getenv('PROJECT_PATH')
    if not project_path:
        raise ValueError("PROJECT_PATH environment variable is not set")
    return project_path

def get_analysis_path() -> str:
    """Get the analysis path from command line arguments or environment variable"""
    # Try to get from environment variable first
    analysis_path = os.getenv('ANALYSIS_PATH')
    if not analysis_path:
        raise ValueError("ANALYSIS_PATH environment variable is not set")
    return analysis_path

def get_sequence_diagram_path() -> str:
    """Get the sequence diagram path from command line arguments or environment variable"""
    # Try to get from environment variable first
    sequence_diagram_path = os.getenv('SEQUENCE_DIAGRAM_PATH')
    if not sequence_diagram_path:
        raise ValueError("SEQUENCE_DIAGRAM_PATH environment variable is not set")
    return sequence_diagram_path

def get_desired_sequence_diagram_path() -> str:
    """Get the desired sequence diagram path from command line arguments or environment variable"""
    # Try to get from environment variable first
    desired_sequence_diagram_path = os.getenv('DESIRED_SEQUENCE_DIAGRAM_PATH')
    if not desired_sequence_diagram_path:
        raise ValueError("DESIRED_SEQUENCE_DIAGRAM_PATH environment variable is not set")
    return desired_sequence_diagram_path