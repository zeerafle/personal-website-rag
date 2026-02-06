from functools import lru_cache

from langchain.agents import create_agent

from app.services.llm import get_llm
from app.tools.pinecone_tool import get_pinecone_tool

SYSTEM_PROMPT = """You are a personal assistant of Sam.
Your job is answer visitor question regarding Sam's personal website.
When visitor ask questions, search the knowledge base to find relevant information.
Always cite the sources you use and be honest if you don't find relevant information.

Be conversational and helpful. Always respond in Markdown format."""


@lru_cache()
def setup_agent():
    llm = get_llm()
    tools = [get_pinecone_tool()]
    agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)

    return agent
