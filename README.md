# Integrated Task and Knowledge Assistant with Programmable Policies

Genie is a programmable framework for creating task-oriented conversational agents that are designed to handle complex user interactions.
Unlike LLMs, Genie provides reliable grounded responses, with controllable agent policies through its expressive specification, Genie Worksheet.
In contrast to dialog trees, it is resilient to diverse user queries, helpful with knowledge sources, and offers ease of programming policies through its declarative paradigm.

Note: This is not the complete codebase for Genie. This doesn't support knowledge bases and is a simplified version of Genie.

## Installation

To install Genie, you can use pip:

```bash
git clone https://github.com/stanford-oval/worksheets_assignment.git
cd worksheets
pip install -r requirements.txt
pip install -e .
```

## Creating Agents

You can use Genie to create a Genie agents by writing a dialogue specification in a spreadsheet (We are working on a python-like syntax for writing specification). 


### Spreadsheet Specification

To create a new agent, you should have a Google Service Account and create a new spreadsheet. 
You can follow the instructions [here](https://cloud.google.com/iam/docs/service-account-overview) to create a Google Service Account.
Share the created spreadsheet with the service account email.

You should save the service_account key as `service_account.json` in the `worksheets/` directory.

Here is a sample spreadsheet for a restaurant agent: [Restaurant Agent](https://docs.google.com/spreadsheets/d/1ejyFlZUrUZiBmFP3dLcVNcKqzAAfw292-LmyHXSFsTE/edit#gid=699205925)

Please note that we only use the specification defined in the first sheet of the spreadsheet.

### Defining a New Agent

To add a new agent, you should create a folder under `worksheets/agents` and add the following files:
- `prompts/`: This folder contains the prompts for the agent. There are three required prompt files: `response_generator.prompt`, `semantic_parser_stateful.prompt`, and `semantic_parser_stateless.prompt`.
- `api.py`: This file contains the API for the agent. 
- `common.py`: This file contains the common details for the agent such as name, prompt directory, etc.
- `custom_suql.py`: A small wrapper around SUQL to provide custom functions for the agent.
- `spreadsheet.py`: This file imports the specifications and defines the spreadsheet id.

To run the dialogue system in the command line, you can use the following command:

### Running the Agent (CLI)

```bash
python src/main.py --domain [agent_name] --spec_type [spec_type]
```

The `agent_name` is the folder name under `worksheets/agents`. We only support spreadsheet as the spec_type for now.

### Running the Agent (Web Interface)

Create a folder under `frontend/<agent_name>` and create a `app_*` file.

You can run the agent in a web interface by running:

**NOTE:** You should run the agent in the `frontend` directory to preserve the frontend assets.

For restaurant agent:
```bash
cd frontend/restaurant
chainlit run app_restaurant.py
```


