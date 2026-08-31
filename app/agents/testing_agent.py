from crewai import Agent
from app.config.llm_config import llm

testing_agent = Agent(
    role = "Test Engineer",

    goal = "design test cases and user stories for given requirments",

    backstory = "An expert in software testing and QA",

    llm=llm,

    verbose=False
    
)