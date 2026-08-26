from crewai import Agent

from app.config.llm_config import llm


manager_agent = Agent(

    role="Engineering Reviewer",

    goal=(
        "Review the project using the "
        "supplied validation summary and "
        "identify important issues."
    ),

    backstory=(
        "A senior engineering reviewer "
        "focused on concrete risks and "
        "actionable improvements."
    ),

    llm=llm,

    verbose=False
)