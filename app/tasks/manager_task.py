from crewai import Task
from app.agents.manager_agent import manager_agent

manager_task = Task(
    description="""
    Review this project briefly:

    {project_request}

    STRICT RULES:
    - Maximum 50 words
    - Keep it simple
    - Beginner-friendly language

    FORMAT:

    STRENGTHS:
    - ...

    IMPROVEMENTS:
    - ...
    """,

    expected_output="""
    Short simple review.
    """,

    agent=manager_agent
)