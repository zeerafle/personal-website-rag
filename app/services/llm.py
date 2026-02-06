from functools import lru_cache

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache()
def get_llm():
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.167  # 10 RPM (1 request per 6 seconds)
    )
    return ChatGoogleGenerativeAI(
        model="gemini-flash-lite-latest", temperature=0.5, rate_limiter=rate_limiter
    )
