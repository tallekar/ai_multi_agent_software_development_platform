
from crewai import Task
from app.agents.debugging_agent import debugging_agent


debugging_task = Task(
    description="""
    Diagnose the problems found during validation or testing.

    PROJECT REQUEST:
    {project_request}

    GENERATED CODE:
    {coding_output}

    VALIDATION RESULTS:
    {validation_summary}

    Identify:
    1. The root cause of each problem
    2. The affected file
    3. The required fix
    4. Any additional stability concerns

    Do not rewrite the entire project.
    Focus only on problems that need to be fixed.
    """,

    expected_output="""
    A concise debugging report containing:
    - Problem
    - Root cause
    - Affected file
    - Recommended fix
    """,

    agent=debugging_agent
)
