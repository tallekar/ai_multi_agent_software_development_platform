from crewai import Task

from app.agents.research_agent import research_agent


research_task = Task(
    description="""
Analyze this software request:

{project_request}

Return ONLY this format:

STACK:
...

ARCHITECTURE:
...

REQUIREMENTS:
...

Rules:
- Maximum 60 words
- Use bullet points where useful
- Do not generate code
- Do not explain anything else
""",

    expected_output="""
A short technical plan containing:
STACK, ARCHITECTURE, and REQUIREMENTS.
""",

    agent=research_agent
)
