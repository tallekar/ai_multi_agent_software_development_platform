from crewai import Task

from app.agents.coding_agent import coding_agent


coding_task = Task(
    description="""
Build the requested software project.

PROJECT REQUEST:
{project_request}

TECHNICAL PLAN:
{research_output}

IMPORTANT RULES:

1. Generate real working code.

2. Keep the implementation focused on the user's request.

3. Do not add unnecessary features.

4. Generate all important files required to run the project.

5. For every file, use this format:

FILE: filename.py

Then write the complete code for that file.

For example:

FILE: app.py

print("Hello World")


FILE: requirements.txt

fastapi
uvicorn

6. You can generate multiple files.

7. Do not explain the code.

8. Do not write unnecessary text.

9. Keep the generated code concise.

10. Make sure the generated code is syntactically correct.
""",

    expected_output="""
Complete working project files with filenames and their code.
""",

    agent=coding_agent
)