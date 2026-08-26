from crewai import Crew, Process

from app.agents.research_agent import research_agent
from app.agents.coding_agent import coding_agent
from app.agents.manager_agent import manager_agent

from app.tasks.research_task import research_task
from app.tasks.coding_task import coding_task
from app.tasks.manager_task import manager_task


def build_coding_crew():
    """Cheap path: only coding agent."""
    return Crew(
        agents=[coding_agent],
        tasks=[coding_task],
        process=Process.sequential,
        verbose=False
    )


def build_research_coding_crew():
    """Complex path: research followed by coding."""
    return Crew(
        agents=[
            research_agent,
            coding_agent
        ],
        tasks=[
            research_task,
            coding_task
        ],
        process=Process.sequential,
        verbose=False
    )


def build_manager_crew():
    """Only used when a review is actually required."""
    return Crew(
        agents=[manager_agent],
        tasks=[manager_task],
        process=Process.sequential,
        verbose=False
    )