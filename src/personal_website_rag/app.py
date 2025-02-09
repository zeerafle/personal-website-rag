from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .rag_chain import qa
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    try:
        result = qa.invoke({'input': query.question})
        return {
            "answer": result['answer'],
            "sources": [doc.metadata['source'] for doc in result['context']]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
