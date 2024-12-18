# SolutionArchitects Crew

Welcome to the SolutionArchitects Crew project, powered by [crewAI](https://crewai.com).

SolutionArchitect is a tool for generating sequence diagrams from Python codebases and comparing them to desired diagrams.

This repository automates the process of parsing code, analyzing function call relationships, and producing sequence diagrams in Mermaid-compatible format.

Designed with CrewAI and uv, it integrates seamlessly into workflows for software architects and developers.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

We are building this with a local ollama model

```
ollama/mistral
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**


## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the SolutionArchitects Crew, assembling the agents and assigning them tasks as defined in your configuration.

This will run the **code_analyst** agent to analyze the codebase, the **sequence_diagrammer** agent to create a sequence diagram and the **compliance_validator** agent to validate the sequence diagram against a desired diagram.

The first output will be a sequence diagram of the original codebase in Mermaid format, saved in the output directory as a .mmd file.

```
output/sequence_diagram.mmd
```

The second output will be a similarity index between the generated diagram and the desired diagram, saved in the output directory as a .txt file.

```
output/compliance_validation_result.txt
```

## Understanding Your Crew

The SolutionArchitects Crew is composed of multiple AI agents, each with unique roles, goals, and tools.
- **code_analyst**
    - Analyzes the codebase, extracting method calls and interactions.
    - Outputs a text-based representation of the code analysis.
- **sequence_diagrammer**
    - Creates a sequence diagram based on the code analysis output.
    - Outputs a Mermaid-compatible sequence diagram.
- **compliance_validator**
    - Validates the sequence diagram against a desired diagram.
    - Outputs a similarity index between the generated diagram and the desired diagram.

These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives.

The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the SolutionArchitects Crew or crewAI.
- Ping me on [LinkedIn](https://www.linkedin.com/in/thejoyofdata/)
