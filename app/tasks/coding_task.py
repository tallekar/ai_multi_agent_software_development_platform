
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
        - Unless the request explicitly asks for a single-file script, generate
            both a backend and a frontend as separate parts of the project.
        - Unless the request explicitly asks for a single-file script, generate
            both a backend and a frontend as separate parts of the project.

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
     5. For a full-stack request, include at least:
         - backend/main.py (or the backend entry point)
         - backend/requirements.txt
         - frontend/package.json
         - frontend/index.html
         - frontend/src/App.jsx (or the frontend entry point)
         Do not combine frontend and backend into one file.
     5. For every file, use exactly this format, including END_FILE:

         FILE: path/to/filename.py

         <complete file content>
         END_FILE

    7. You can generate multiple files.
    8. Do not explain the code.
    9. Do not write unnecessary text.
    10. Keep the generated code concise.
    11. Make sure the generated code is syntactically correct.
    12. When fixing code, preserve all functionality that is already working.
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

