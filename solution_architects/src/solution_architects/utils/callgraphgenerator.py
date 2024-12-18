import ast
import os
from typing import Dict, Set, List
from collections import defaultdict

class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.current_function = None
        self.calls = defaultdict(set)
        self.functions = set()

    def visit_FunctionDef(self, node):
        previous_function = self.current_function
        self.current_function = node.name
        self.functions.add(node.name)
        # Visit all nodes inside the function
        self.generic_visit(node)
        self.current_function = previous_function

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and self.current_function:
            # Record the function call
            self.calls[self.current_function].add(node.func.id)
        self.generic_visit(node)

def analyze_file(file_path: str) -> tuple[Dict[str, Set[str]], Set[str]]:
    """
    Analyze a single Python file and return its call graph information.

    Args:
        file_path (str): Path to the Python file to analyze

    Returns:
        tuple: (Dictionary of function calls, Set of defined functions)
    """
    try:
        # Try different encodings if UTF-8 fails
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    try:
                        tree = ast.parse(file.read())
                        visitor = FunctionCallVisitor()
                        visitor.visit(tree)
                        return visitor.calls, visitor.functions
                    except SyntaxError as se:
                        print(f"Syntax error in {file_path}: {se}")
                        print(f"Line {se.lineno}, Column {se.offset}: {se.text}")
                        break  # No need to try other encodings for syntax errors
                    except Exception as e:
                        print(f"AST parsing error in {file_path}: {e}")
                        break  # No need to try other encodings for parsing errors
            except UnicodeDecodeError:
                if encoding == 'cp1252':  # Last encoding attempt
                    print(f"Failed to decode {file_path} with encodings: utf-8, latin-1, cp1252")
                continue  # Try next encoding
    except PermissionError:
        print(f"Permission denied: Unable to read {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {type(e).__name__}: {e}")

    return {}, set()  # Return empty results if any error occurred

def call_graph_tool(project_path: str) -> str:
    """
    Generate a call graph for all Python files in the project directory.

    Args:
        project_path (str): Path to the project directory

    Returns:
        str: A text representation of the call graph
    """
    all_calls = defaultdict(set)
    all_functions = set()
    error_files = []

    # Recursively find all Python files
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    calls, functions = analyze_file(file_path)
                    if not calls and not functions:
                        error_files.append(file_path)
                    else:
                        # Merge results
                        for caller, callees in calls.items():
                            all_calls[caller].update(callees)
                        all_functions.update(functions)
                except Exception as e:
                    error_files.append(file_path)
                    print(f"Error processing {file_path}: {e}")

    # Generate text representation
    result = ["Call Graph Analysis:", "=" * 50]

    # Add error summary if any
    if error_files:
        result.extend([
            "\nFiles with Errors:",
            "-" * 20
        ])
        for file in error_files:
            result.append(f"- {file}")

    # Add function definitions
    result.extend([
        "\nDefined Functions:",
        "-" * 20
    ])
    for func in sorted(all_functions):
        result.append(f"- {func}")

    # Add function calls
    result.extend([
        "\nFunction Calls:",
        "-" * 20
    ])
    for caller, callees in sorted(all_calls.items()):
        if callees:  # Only show functions that make calls
            result.append(f"\n{caller} calls:")
            for callee in sorted(callees):
                if callee in all_functions:  # Only show calls to defined functions
                    result.append(f"  └─> {callee}")

    # Add summary
    result.extend([
        "\nSummary:",
        "-" * 20,
        f"Total files with errors: {len(error_files)}",
        f"Total functions analyzed: {len(all_functions)}",
        f"Total call relationships: {sum(len(callees) for callees in all_calls.values())}"
    ])

    return "\n".join(result)