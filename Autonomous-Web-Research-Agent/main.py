from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_research_agent


app = FastAPI(
    title="Autonomous Web Research Agent",
    description="AI agent that researches topics using web search",
    version="1.0.0"
)

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str

@app.get("/")
def home():
    return {
        "message": "Autonomous Web Research Agent API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/research")
def research(request: ResearchRequest):
    agent = create_research_agent()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.topic
                }
            ]
        }
    )

    final_message = result["messages"][-1]
    return ResearchResponse(
        topic=request.topic,
        report=final_message.content
    )