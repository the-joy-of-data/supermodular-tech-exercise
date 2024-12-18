from langchain.tools import BaseTool

import difflib

class ComplianceValidationTool(BaseTool):
    """Tool for comparing sequence diagrams and calculating similarity."""
    name: str = "Compliance Validation Tool"
    description: str = "Compares two sequence diagrams in MMD format and calculates their similarity index"
    reference_diagram_path: str

    def __init__(self, reference_diagram_path:str):
        """Initialize the tool with path to reference diagram."""
        super().__init__(reference_diagram_path=reference_diagram_path)

    def _process_diagram(self, content):
        """Process diagram content to extract relevant comparison elements."""
        # Remove whitespace and comments
        lines = [
            line.strip()
            for line in content.split('\n')
            if line.strip() and not line.strip().startswith('%')
        ]
        return lines

    def _calculate_similarity(self, diagram1, diagram2):
        """Calculate similarity ratio between two diagrams."""
        matcher = difflib.SequenceMatcher(None, diagram1, diagram2)
        return matcher.ratio()

    def _get_detailed_comparison(self, diagram1, diagram2):
        """Generate detailed comparison metrics."""
        total_lines1 = len(diagram1)
        total_lines2 = len(diagram2)

        # Find common lines
        common_lines = set(diagram1) & set(diagram2)

        return {
            "similarity_ratio": self._calculate_similarity(diagram1, diagram2),
            "common_elements": len(common_lines),
            "reference_elements": total_lines1,
            "current_elements": total_lines2,
            "missing_elements": total_lines1 - len(common_lines),
            "extra_elements": total_lines2 - len(common_lines)
        }

    def _run(self, diagram_path):
        """Compare the given diagram with the reference diagram."""
        if not self.reference_diagram_path:
            return "Error: Reference diagram path not set"

        try:
            # Read both diagrams
            with open(self.reference_diagram_path, 'r') as f:
                reference_content = f.read()

            with open(diagram_path, 'r') as f:
                current_content = f.read()

            # Process diagrams
            reference_processed = self._process_diagram(reference_content)
            current_processed = self._process_diagram(current_content)

            # Get detailed comparison
            comparison = self._get_detailed_comparison(reference_processed, current_processed)

            # Format output
            return f"""Sequence Diagram Comparison Results:
- Similarity Index: {comparison['similarity_ratio']:.2%}
- Common Elements: {comparison['common_elements']}
- Reference Elements: {comparison['reference_elements']}
- Current Elements: {comparison['current_elements']}
- Missing Elements: {comparison['missing_elements']}
- Extra Elements: {comparison['extra_elements']}"""

        except Exception as e:
            return f"Error comparing diagrams: {str(e)}"

    async def _arun(self, diagram_path):
        """Async version of _run."""
        return self._run(diagram_path)