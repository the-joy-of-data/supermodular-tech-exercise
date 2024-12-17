from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

import ast
import os
import networkx as nx

def call_graph_tool(project_path: str) -> str:
    """
    A custom CrewAI tool to parse a Python codebase and generate Mermaid sequence diagram syntax.

    Args:
        project_path (str): The directory path of the Python project to analyze.

    Returns:
        str: Mermaid-compatible sequence diagram syntax representing function call relationships.
    """
    class CallGraphGenerator(ast.NodeVisitor):
        """
        Extracts function calls and relationships between functions in a Python codebase.
        """
        def __init__(self):
            self.graph = nx.DiGraph()
            self.current_function = None

        def visit_FunctionDef(self, node):
            """Visit function definitions."""
            self.current_function = node.name
            self.graph.add_node(self.current_function)
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node):
            """Visit function calls."""
            if isinstance(node.func, ast.Name) and self.current_function:
                called_function = node.func.id
                self.graph.add_edge(self.current_function, called_function)
            elif isinstance(node.func, ast.Attribute) and self.current_function:
                called_function = f"{node.func.value.id}.{node.func.attr}"
                self.graph.add_edge(self.current_function, called_function)
            self.generic_visit(node)

    def analyze_codebase(path):
        """Analyzes all Python files in a codebase."""
        generator = CallGraphGenerator()
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            tree = ast.parse(f.read(), filename=file)
                            generator.visit(tree)
                        except SyntaxError:
                            pass  # Ignore syntax errors in files
        return generator.graph

    def generate_mermaid_sequence(graph):
        """Generates Mermaid sequence diagram syntax from the call graph."""
        mermaid_output = ["sequenceDiagram"]
        for source, target in graph.edges:
            mermaid_output.append(f"    {source} ->> {target}: calls")
        return "\n".join(mermaid_output)

    # Analyze the codebase and generate the Mermaid syntax
    call_graph = analyze_codebase(project_path)
    mermaid_code = generate_mermaid_sequence(call_graph)

    return mermaid_code