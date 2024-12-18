#!/usr/bin/env python
import sys

from solution_architects.utils.get_paths import get_project_path
from solution_architects.crew import SolutionArchitects

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    inputs = {
        "topic": "supermodular.ai"
    }
    architects = SolutionArchitects(project_path=get_project_path())
    architects.crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "supermodular.ai"
    }
    try:
        architects = SolutionArchitects(project_path="/path/to/your/project")
        architects.crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        architects = SolutionArchitects(project_path="/path/to/your/project")
        architects.crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "supermodular.ai"
    }
    try:
        architects = SolutionArchitects(project_path="/path/to/your/project")
        architects.crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
