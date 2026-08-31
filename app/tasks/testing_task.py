
from crewai import Task
from app.agents.testing_agent import testing_agent


testing_task = Task(
    description="""
    Analyze the generated software project and design appropriate
    test cases.

    PROJECT REQUEST:
    {project_request}

    ARCHITECTURE:
    {architecture_output}

    GENERATED CODE:
    {coding_output}

    Create tests that verify:
    1. Core functionality
    2. API behavior where applicable
    3. Important edge cases
    4. Invalid inputs
    5. Expected failures

    Do not rewrite the application code.
    Focus only on testing.
    """,

    expected_output="""
    A concise testing plan containing:
    - Test cases
    - Expected results
    - Important edge cases
    - Potential failures
    """,

    agent=testing_agent
)

