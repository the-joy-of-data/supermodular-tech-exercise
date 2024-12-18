from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import json

from solution_architects.tools.code_analysis_tool import CodeAnalysisTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SolutionArchitects():
	"""SolutionArchitects crew"""

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
		return Agent(
			config=self.agents_config['sequence_diagrammer'],
			verbose=True
		)

	# @agent
	# def compliance_validator(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['compliance_validator'],
	# 		verbose=True
	# 	)

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

	# @task
	# def compliance_validation_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['compliance_validation_task'],
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the SolutionArchitects crew"""

		code_analysis_tool = CodeAnalysisTool(project_path=self.project_path)

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			tools=[code_analysis_tool],
			process=Process.sequential,
			verbose=True,
		)
