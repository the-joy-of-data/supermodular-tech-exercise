from crewai.tools import BaseTool

from solution_architects.utils.callgraphgenerator import call_graph_tool

class CodeAnalysisTool(BaseTool):
    name: str = "Code Analysis Tool"
    description: str = "Generates a call graph from a Python codebase."
    project_path: str

    def __init__(self, project_path: str):
        super().__init__(project_path = project_path)

    def _run(self) -> str:
        """
        Executes the code analysis by generating a call graph for the project.

        Returns:
            str: The generated call graph representation
        """

        return call_graph_tool(self.project_path)