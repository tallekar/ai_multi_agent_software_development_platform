from crewai import Task
from app.agents.architecture_agent import architecture_agent
from app.tasks.research_task import research_task


architecture_task = Task(
    description="""
    Design the software architecture for the following project:

    PROJECT REQUEST:
    {project_request}

    Use the research findings from the Research Agent.

    Provide:
    1. Application architecture
    2. Main components
    3. Project folder structure
    4. Data flow
    5. Important technologies

    Do not generate implementation code.
    Keep the architecture practical and concise.
    """,

    expected_output="""
    A concise technical architecture containing:
    - Application architecture
    - Components
    - Folder structure
    - Data flow
    - Technologies
    """,

    agent=architecture_agent,
    context=[research_task]
)