from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from crewai.project import CrewBase, agent, crew, task

from solution_architects.tools.callgraphgenerator import call_graph_tool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SolutionArchitects():
	"""SolutionArchitects crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def code_analyst(self) -> Agent:
		"""Code Analyst Agent"""
		return Agent(
			config=self.agents_config['code-analyst'],
			verbose=True,
			tools=code_analysis_tool
		)

	# @agent
	# def sequence_diagrammer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['sequence-diagrammer'],
	# 		verbose=True
	# 	)

	# @agent
	# def compliance_validator(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['compliance-validator'],
	# 		verbose=True
	# 	)

	@task
	def code_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['code-analysis-task'],
		)

	# @task
	# def sequence_diagram_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['sequence-diagram-task'],
	# 		output_file='sequence_diagram.mmd'
	# 	)

	# @task
	# def compliance_validation_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['compliance-validation-task'],
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the SolutionArchitects crew"""

		# Define the tool
		code_analysis_tool = Tool(
			name="Code Analysis Tool",
			description="Generates a call graph from a Python codebase.",
			func=call_graph_tool,
			args_schema={
				"project_path": {
					"type": "string",
					"description": "The absolute path of the Python project directory to analyze."
				}
			}
		)

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			tools=[code_analysis_tool],
			process=Process.sequential,
			verbose=True,
		)
