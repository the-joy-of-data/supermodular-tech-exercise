from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path

from solution_architects.utils.get_paths import get_project_path, get_analysis_path, get_desired_sequence_diagram_path
from solution_architects.tools.code_analysis_tool import CodeAnalysisTool
from solution_architects.tools.sequence_diagram_tool import SequenceDiagramTool
from solution_architects.tools.compliance_validation_tool import ComplianceValidationTool

@CrewBase
class SolutionArchitects():
	"""SolutionArchitects crew"""

	"""Agents and tasks configuration"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, project_path: str, output_dir: str = "output"):
		super().__init__()
		self.project_path = project_path
		self.output_dir = Path(output_dir)
		self.output_dir.mkdir(exist_ok=True)

	@agent
	def code_analyst(self) -> Agent:
		"""Code Analyst Agent"""
		return Agent(
			config=self.agents_config['code_analyst'],
			verbose=True,
			tools=[CodeAnalysisTool(project_path=self.project_path)]
		)

	@agent
	def sequence_diagrammer(self) -> Agent:
		"""Sequence Diagrammer Agent"""
		return Agent(
			config=self.agents_config['sequence_diagrammer'],
			verbose=True
		)

	@agent
	def compliance_validator(self) -> Agent:
		"""Compliance Validator Agent"""
		return Agent(
			config=self.agents_config['compliance_validator'],
			verbose=True
		)

	@task
	def code_analysis_task(self) -> Task:
		"""Analyzes the codebase and saves the result"""
		task = Task(
			config=self.tasks_config['code_analysis_task'],
			output_file=str(self.output_dir / "code_analysis_result.txt")
		)
		return task

	@task
	def sequence_diagram_task(self) -> Task:
		"""Creates sequence diagram using the code analysis results"""
		task = Task(
			config=self.tasks_config['sequence_diagram_task'],
			context_file=str(self.output_dir / "code_analysis_result.txt"),
			output_file=str(self.output_dir / "sequence_diagram.mmd")
		)
		return task

	@task
	def compliance_validation_task(self) -> Task:
		"""Validates the generated sequence diagram against a reference"""
		task = Task(
			config=self.tasks_config['compliance_validation_task'],
			context_file=str(self.output_dir / "sequence_diagram.mmd"),
			output_file=str(self.output_dir / "compliance_validation_result.txt")
		)
		return task

	@crew
	def crew(self) -> Crew:
		"""Creates the SolutionArchitects crew"""

		# Define the project path
		project_path = get_project_path()

		# Define the analysis output path
		analysis_path = get_analysis_path()

		# Create tools
		code_analysis_tool = CodeAnalysisTool(project_path=project_path)
		sequence_diagram_tool = SequenceDiagramTool(analysis_path=analysis_path)
		compliance_validation_tool = ComplianceValidationTool(reference_diagram_path=get_desired_sequence_diagram_path())

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			tools=[code_analysis_tool, sequence_diagram_tool, compliance_validation_tool],
			process=Process.sequential,
			verbose=True,
		)
