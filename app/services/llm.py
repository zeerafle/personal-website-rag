from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache()
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        # google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.5,
    )
