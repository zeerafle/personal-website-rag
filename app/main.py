import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langgraph.errors import GraphRecursionError

from app.agent import setup_agent
from app.models import ChatRequest, ChatResponse
from app.utils import extract_agent_response

load_dotenv()

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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that uses the LangChain agent
    to query Pinecone and respond to user messages.
    """
    try:
        agent = setup_agent()
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config={"recursion_limit": 5},
        )
        message = extract_agent_response(result)
        return ChatResponse(message=message, conversation_id=request.conversation_id)
    except ChatGoogleGenerativeAIError as e:
        # Catch Gemini errors (rate limiting, quota exceeded, etc.)
        error_msg = str(e)
        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
            raise HTTPException(
                status_code=429,
                detail="Daily rate limit exceeded. Please try again later.",
            )
        # For other Gemini errors, return 500
        raise HTTPException(status_code=500, detail=error_msg)
    except GraphRecursionError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
