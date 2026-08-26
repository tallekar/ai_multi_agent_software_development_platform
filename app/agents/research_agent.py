from crewai import Agent

from app.config.llm_config import llm


research_agent = Agent(

    role="Requirements Analyst",

    goal=(
        "Extract only the technical "
        "requirements needed to implement "
        "the project."
    ),

    backstory=(
        "An efficient software analyst "
        "who produces short, structured "
        "technical plans."
    ),

    llm=llm,

    verbose=False
)