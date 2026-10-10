from typing import Literal

from pydantic import BaseModel, Field


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    history: list[HistoryMessage] = Field(
        default_factory=list,
        max_length=12,
        description="Earlier turns of this conversation, oldest first",
    )
    conversation_id: str | None = Field(
        None, description="Optional conversation ID for context"
    )


class ChatResponse(BaseModel):
    message: str = Field(..., description="Agent's responses")
    conversation_id: str | None = Field(
        None, description="Optional conversation ID for context"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Based on your previous conversation, I recommend...",
                "conversation_id": "1234567890",
            }
        }
