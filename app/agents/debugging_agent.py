from crewai import Agent
from app.config.llm_config import llm

debugging_agent = Agent(
    role = "Bug Detective",

    goal = ("Diagnose bugs, suggest fixes, and improve stability"),

    backstory = ("An expert debugger with deep experience in identifying and resolving software issues."),

    llm=llm,
    
    verbose=False
)