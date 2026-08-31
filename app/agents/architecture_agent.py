from crewai import Agent
from app.config.llm_config import llm


architecture_agent = Agent(
    role = "system architect",
    goal = (
        "Design the software architecture using best practices and patterns."
    ),
    backstory = (
        "An expert software architect with deep expertise"
    ),
    llm=llm,
    verbose=False

)