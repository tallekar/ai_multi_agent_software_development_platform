
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

    REAL PROJECT PATH:
    {project_path}

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
     7. If the existing project has frontend and backend parts, return both
         parts in the corrected output, including unchanged files.
         Do not collapse a full-stack project into one file.
     8. Make sure the corrected code is syntactically valid.
     8. Use exactly this format for every file, including END_FILE:

         FILE: path/to/filename.py

       <complete corrected code>
         END_FILE

    10. Do not explain the code.
    11. Do not include unnecessary text.
    12. The backend writes your returned FILE blocks into REAL PROJECT PATH.
        Only return files that belong inside that generated project.
    """,

    expected_output="""
    Complete corrected project files with filenames and their
    updated code.
    """,

    agent=coding_agent
)

