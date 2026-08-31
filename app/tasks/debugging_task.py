

from crewai import Task
from app.agents.debugging_agent import debugging_agent


debugging_task = Task(
    description="""
    Diagnose problems in the generated software project.

    PROJECT REQUEST:
    {project_request}

    GENERATED CODE:
    {coding_output}

    VALIDATION RESULTS:
    {validation_summary}

    TESTING RESULTS:
    {testing_output}

    Your job is to identify the exact problems and provide
    actionable fixes for the Coding Agent.

    For each problem, provide:

    1. Problem
    2. Root cause
    3. Affected file
    4. Why the problem occurred
    5. Exact fix required
    6. Corrected code when necessary

    IMPORTANT:
    - Do not redesign the entire project.
    - Do not remove working functionality.
    - Fix only the identified problems.
    - Keep the solution practical.
    - The Coding Agent will use your output to implement the fixes.
    - Do not generate unnecessary changes.

    If no problem is found, clearly state that no debugging
    changes are required.
    """,

    expected_output="""
    A precise debugging report containing:

    - Problem
    - Root cause
    - Affected file
    - Required fix
    - Corrected code or implementation instructions
    - Whether another attempt is required
    """,

    agent=debugging_agent
)

