
import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()


async def main():

    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    tools = await client.get_tools()

    model = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
    )

    math_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What's (3 + 5) * 12?",
                }
            ]
        }
    )

    print("Math response:")
    print(math_response["messages"][-1].content)

    weather_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What's the weather in India?",
                }
            ]
        }
    )

    print("\nWeather response:")
    print(weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())


### output
#   agent = create_react_agent(
# Math response:
# (3 + 5) × 12 = 8 × 12 = **96**

# Weather response:
# I’d be happy to give you the current weather—but India covers a huge range of climates.
#  Could you let me know which city or region you’re interested in? 
# If you just want a general overview, I can describe the typical weather patterns across the country.  
# 
# 
# INFO:     Started server process [23454]
# INFO:     Waiting for application startup.
# [09/19/26 18:19:41] INFO     StreamableHTTP session manager started                                          streamable_http_manager.py:164
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# [09/19/26 18:19:54] INFO     Created new transport with session ID: f0df193685604286889cfa93cb9f9f59         streamable_http_manager.py:330
# INFO:     127.0.0.1:35272 - "POST /mcp HTTP/1.1" 200 OK
# INFO:     127.0.0.1:35282 - "POST /mcp HTTP/1.1" 202 Accepted
# INFO:     127.0.0.1:35298 - "GET /mcp HTTP/1.1" 200 OK
# INFO:     127.0.0.1:35310 - "POST /mcp HTTP/1.1" 200 OK
#                     INFO     Processing request of type ListToolsRequest                                                      server.py:733
#                     INFO     Terminating session: f0df193685604286889cfa93cb9f9f59                                   streamable_http.py:831
# INFO:     127.0.0.1:35324 - "DELETE /mcp HTTP/1.1" 200 OK
# [09/19/26 18:20:27] INFO     Created new transport with session ID: 93fdb6736b6249a8b824ab8a451af065         streamable_http_manager.py:330
# INFO:     127.0.0.1:42068 - "POST /mcp HTTP/1.1" 200 OK
# INFO:     127.0.0.1:42076 - "POST /mcp HTTP/1.1" 202 Accepted
# INFO:     127.0.0.1:42092 - "GET /mcp HTTP/1.1" 200 OK
# INFO:     127.0.0.1:42100 - "POST /mcp HTTP/1.1" 200 OK
#                     INFO     Processing request of type ListToolsRequest                                                      server.py:733
#                     INFO     Terminating session: 93fdb6736b6249a8b824ab8a451af065                                   streamable_http.py:831
# INFO:     127.0.0.1:42114 - "DELETE /mcp HTTP/1.1" 200 OK  