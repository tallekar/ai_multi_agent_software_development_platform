
from crewai import Task
from app.agents.coding_agent import coding_agent
from app.tasks.research_task import research_task
from app.tasks.architecture_task import architecture_task


coding_task = Task(
    description="""
    Build or fix the requested software project.

    PROJECT REQUEST:
    {project_request}

    Use the research and architecture provided by the
    previous agents when available.

    If this is a NEW project:
    - Generate the required working project files.
    - Follow the architecture provided by the Architecture Agent.

    If this is a FIX request:
    - Review the existing generated code.
    - Apply only the fixes identified by the Debugging Agent.
    - Do not remove working functionality.
    - Do not redesign the entire project.

    IMPORTANT RULES:

    1. Generate real working code.
    2. Keep the implementation focused on the user's request.
    3. Do not add unnecessary features.
    4. Generate all important files required to run the project.
    5. For every file, use this format:

       FILE: filename.py

       Then write the complete code for that file.

    6. You can generate multiple files.
    7. Do not explain the code.
    8. Do not write unnecessary text.
    9. Keep the generated code concise.
    10. Make sure the generated code is syntactically correct.
    11. When fixing code, preserve all functionality that is already working.
    """,

    expected_output="""
    Complete working project files with filenames and their code.
    """,

    agent=coding_agent,

    context=[
        research_task,
        architecture_task
    ]
)

