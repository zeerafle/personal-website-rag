import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .rag_chain import setup_rag

app = FastAPI()

if os.getenv("ENV") == "production":
    origins = ["https://samfareez.is-a.dev"]
else:
    origins = ["*", "null"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str


@app.get("/")
def index():
    return {"message": "Chatbot API"}


@app.post("/ask")
async def ask(query: Query):
    try:
        agent = setup_rag()
        result = agent.invoke(
            {"messages": [{"role": "user", "content": query.question}]}
        )
        tool_calls = [
            message
            for message in result["messages"]
            if message.__class__.__name__ == "ToolMessage"
        ]
        return {
            "answer": result["messages"][-1].content,
            "sources": [tool_call.artifact for tool_call in tool_calls],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
