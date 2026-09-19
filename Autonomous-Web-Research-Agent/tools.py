import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool

load_dotenv()

@tool
def web_search(query:str) ->str:
    """
    Search the internet for information about a topic.

    Use this tool when you need current or factual
    information from the web.
    """

    tavily = TavilyClient(
        api_key=os.getenv("TAVILY_API_KEY")
    )

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )
    results = response.get("results", [])
    if not results:
        return "No search results found."

    formatted_results = []
    for index, result in enumerate(results, start=1):

        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")

        formatted_results.append(
            f"""
SOURCE {index}

Title:
{title}

URL:
{url}

Content:
{content}
"""
        )
    return "\n".join(formatted_results)