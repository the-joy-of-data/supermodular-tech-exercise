from crewai.tools import BaseTool
from typing import Optional

class SequenceDiagramTool(BaseTool):
    name: str = "Sequence Diagram Tool"
    description: str = "Generates a sequence diagram from code analysis results"
    analysis_path: str

    def __init__(self, analysis_path: str):
        super().__init__(analysis_path=analysis_path)

    def _run(self, query: Optional[str] = None) -> str:
        """
        Creates a sequence diagram in Mermaid format based on code analysis.

        Args:
            query (Optional[str]): Optional query parameter (not used in this implementation)

        Returns:
            str: Mermaid sequence diagram
        """
        try:
            with open(self.analysis_path, 'r') as f:
                analysis_content = f.read()

            # Start the Mermaid sequence diagram
            diagram = ["sequenceDiagram", "    title Function Call Sequence"]

            # Parse the analysis content and create sequence
            current_caller = None
            for line in analysis_content.split('\n'):
                if line.strip().endswith("calls:"):
                    current_caller = line.replace(" calls:", "").strip()
                elif line.strip().startswith("└─>") and current_caller:
                    callee = line.replace("└─>", "").strip()
                    diagram.append(f"    {current_caller}->>+{callee}: call")
                    diagram.append(f"    {callee}-->>-{current_caller}: return")

            return "\n".join(diagram)

        except FileNotFoundError:
            return f"Error: Analysis file not found at {self.analysis_path}"
        except Exception as e:
            return f"Error generating sequence diagram: {str(e)}"