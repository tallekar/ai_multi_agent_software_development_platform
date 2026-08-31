
from crewai import Task
from app.agents.code_review_agent import code_review_agent


code_review_task = Task(
    description="""
    Review the final generated software project.

    PROJECT REQUEST:
    {project_request}

    GENERATED CODE:
    {coding_output}

    VALIDATION RESULTS:
    {validation_summary}

    DEBUGGING RESULTS:
    {debugging_output}

    Review the project for:

    1. Correctness
    2. Code quality
    3. Maintainability
    4. Security concerns
    5. Performance issues
    6. Unnecessary complexity

    Identify only important issues.
    Do not rewrite the complete project.
    """,

    expected_output="""
    A concise code review containing:
    - Strengths
    - Important issues
    - Recommended improvements
    - Overall assessment
    """,

    agent=code_review_agent
)

