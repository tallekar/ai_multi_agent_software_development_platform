
from crewai import Crew, Process

# Agents
from app.agents.research_agent import research_agent
from app.agents.architecture_agent import architecture_agent
from app.agents.coding_agent import coding_agent
from app.agents.testing_agent import testing_agent
from app.agents.debugging_agent import debugging_agent
from app.agents.code_review_agent import code_review_agent
from app.agents.manager_agent import manager_agent

# Tasks
from app.tasks.research_task import research_task
from app.tasks.architecture_task import architecture_task
from app.tasks.coding_task import coding_task
from app.tasks.testing_task import testing_task
from app.tasks.debugging_task import debugging_task
from app.tasks.coding_fix_task import coding_fix_task
from app.tasks.code_review_task import code_review_task
from app.tasks.manager_task import manager_task


def build_coding_crew():
    """
    Simple path:

    Coding
    """
    return Crew(
        agents=[coding_agent],
        tasks=[coding_task],
        process=Process.sequential,
        verbose=False
    )


def build_research_coding_crew():
    """
    Complex path:

    Research
        ↓
    Architecture
        ↓
    Coding
    """
    return Crew(
        agents=[
            research_agent,
            architecture_agent,
            coding_agent
        ],
        tasks=[
            research_task,
            architecture_task,
            coding_task
        ],
        process=Process.sequential,
        verbose=False
    )


def build_testing_crew():
    """
    Testing-only path.

    Uses already generated code.
    """
    return Crew(
        agents=[testing_agent],
        tasks=[testing_task],
        process=Process.sequential,
        verbose=False
    )


def build_debugging_crew():
    """
    Debugging-only path.

    Uses existing code, validation results
    and testing results.
    """
    return Crew(
        agents=[debugging_agent],
        tasks=[debugging_task],
        process=Process.sequential,
        verbose=False
    )


def build_coding_fix_crew():
    """
    Coding Fix path.

    Uses existing generated code
    and debugging report.
    """
    return Crew(
        agents=[coding_agent],
        tasks=[coding_fix_task],
        process=Process.sequential,
        verbose=False
    )


def build_code_review_crew():
    """
    Code Review-only path.

    Reviews the already generated project.

    Does NOT run:
    Research
    Architecture
    Coding
    Testing
    """
    return Crew(
        agents=[code_review_agent],
        tasks=[code_review_task],
        process=Process.sequential,
        verbose=False
    )


def build_full_development_crew():
    """
    Full development path:

    Research
        ↓
    Architecture
        ↓
    Coding
        ↓
    Testing
        ↓
    Code Review
    """
    return Crew(
        agents=[
            research_agent,
            architecture_agent,
            coding_agent,
            testing_agent,
            code_review_agent
        ],
        tasks=[
            research_task,
            architecture_task,
            coding_task,
            testing_task,
            code_review_task
        ],
        process=Process.sequential,
        verbose=False
    )


def build_manager_crew():
    """
    Manager-only path.
    """
    return Crew(
        agents=[manager_agent],
        tasks=[manager_task],
        process=Process.sequential,
        verbose=False
    )