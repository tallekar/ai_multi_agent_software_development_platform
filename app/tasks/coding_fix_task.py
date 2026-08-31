
from crewai import Task
from app.agents.coding_agent import coding_agent


coding_fix_task = Task(
    description="""
    Fix the existing generated software project based on the
    debugging report.

    PROJECT REQUEST:
    {project_request}

    EXISTING GENERATED CODE:
    {coding_output}

    DEBUGGING REPORT:
    {debugging_output}

    Your job is to apply the fixes identified by the Debugging Agent.

    IMPORTANT RULES:

    1. Fix only the identified problems.
    2. Do not redesign the entire project.
    3. Do not remove working functionality.
    4. Do not add unnecessary features.
    5. Return the complete corrected files.
    6. Preserve files that do not require changes.
    7. Make sure the corrected code is syntactically valid.
    8. Use this format for every file:

       FILE: filename.py

       <complete corrected code>

    9. Do not explain the code.
    10. Do not include unnecessary text.
    """,

    expected_output="""
    Complete corrected project files with filenames and their
    updated code.
    """,

    agent=coding_agent
)

