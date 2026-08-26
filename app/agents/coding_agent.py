from crewai import Agent

from app.config.llm_config import llm


coding_agent = Agent(

    role="Software Developer",

    goal=(
        "Generate clean, working code "
        "for the requested project."
    ),

    backstory=(
        "A practical software developer "
        "focused on producing concise, "
        "usable implementations."
    ),

    llm=llm,

    verbose=False
)