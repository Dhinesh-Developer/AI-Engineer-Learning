from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import web_search

load_dotenv()

def create_research_agent():
    model = ChatGroq(model="openai/gpt-oss-120b",temperature=0)
    tools = [web_search]

    system_prompt = """
You are an autonomous web research agent.
Your job is to research the user's topic using web search.
Follow these rules:

1. Understand the research topic.
2. Break the topic into smaller research questions.
3. Generate useful search queries.
4. Use the web_search tool to search the internet.
5. Search multiple times when necessary.
6. Prefer recent and reliable information.
7. Do not invent facts.
8. Use information from the search results.
9. Keep track of the source URLs.
10. After collecting enough information, write a structured Markdown report.

The final report must contain:

# Title
## Executive Summary
## Key Findings
## Detailed Analysis
## Benefits / Opportunities
## Risks / Limitations
## Conclusion
## Sources
In the Sources section, include the URLs used during research.
Do not give a final answer until you have performed web research.
"""

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )

    return agent