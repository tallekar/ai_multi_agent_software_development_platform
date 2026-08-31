from crewai import Agent

from app.config.llm_config import llm

code_review_agent = Agent(
    role="Code Reviewer",

    goal=("Ensure high-quality, maintainable, and efficient code"),

    backstory=("A meticulous code reviewer who spots issues with logic, performance, and standards."),

    llm=llm,

    verbose=False
)
