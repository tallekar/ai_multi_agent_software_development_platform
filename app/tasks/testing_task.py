
from crewai import Task
from app.agents.testing_agent import testing_agent


testing_task = Task(
    description="""
    Analyze the generated software project and create a focused
    testing report.

    PROJECT REQUEST:
    {project_request}

    GENERATED CODE:
    {coding_output}

    Check:
    1. Core functionality
    2. Important API behavior
    3. Edge cases
    4. Invalid inputs
    5. Potential runtime problems

    Do not rewrite the application.
    Keep the testing report concise.
    """,

    expected_output="""
    A concise test report containing:
    - Test cases
    - Potential failures
    - Important issues
    - Overall testing status
    """,

    agent=testing_agent
)


