from google.adk.agents import Agent
from common import models
from tools import geeknews
from . import prompts

root_agent = Agent(
    model=models.GEMINI_2_5_FLASH_PREVIEW_04_17,
    name="assistant_agent",
    description="A versatile AI assistant that answers queries and uses tools for specific information like GeekNews.",
    instruction=prompts.ROOT_PROMPT,
    tools=[
        geeknews.get_geeknews_articles,
        geeknews.get_geeknews_article_content
    ]
)
