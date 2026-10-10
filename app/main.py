import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langgraph.errors import GraphRecursionError
from openai import APIError, RateLimitError

from app.agent import setup_agent
from app.tools.pinecone_tool import get_vector_store
from app.models import ChatRequest, ChatResponse
from app.utils import extract_agent_response

load_dotenv()


def warm_up():
    setup_agent()
    get_vector_store()

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Fly scales this machine to zero. The port only opens once startup returns, so build
    # everything the first /chat needs here: /health (the site's wake-up ping) then means "ready".
    await asyncio.to_thread(warm_up)
    yield


app = FastAPI(lifespan=lifespan)

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
            {
                "messages": [
                    *(m.model_dump() for m in request.history),
                    {"role": "user", "content": request.message},
                ]
            },
            config={"recursion_limit": 7},
        )
        message = extract_agent_response(result)
        return ChatResponse(message=message, conversation_id=request.conversation_id)
    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Daily rate limit exceeded. Please try again later.",
        )
    except APIError as e:
        # Upstream LLM gateway failure (auth, overload, bad gateway, ...)
        print(str(e))
        raise HTTPException(status_code=502, detail="The language model is unavailable.")
    except GraphRecursionError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
