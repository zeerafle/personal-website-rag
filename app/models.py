from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
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
