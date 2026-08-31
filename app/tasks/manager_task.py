from crewai import Task
from app.agents.manager_agent import manager_agent


manager_task = Task(
    description="""
    Analyze the following software development request:

    {project_request}

    Determine which specialized development activities are required.

    Available agents:
    - Research Agent
    - Architecture Agent
    - Coding Agent
    - Testing Agent
    - Debugging Agent
    - Code Review Agent

    Create a short execution plan specifying:
    1. Required agents
    2. Order of execution
    3. Whether testing is required
    4. Whether code review is required

    Do not generate code.
    """,

    expected_output="""
    A concise software development execution plan.
    """,

    agent=manager_agent
)