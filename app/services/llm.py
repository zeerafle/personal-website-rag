import os
from functools import lru_cache

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI


@lru_cache()
def get_llm():
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.167  # 10 RPM (1 request per 6 seconds)
    )
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "auto"),
        base_url=os.getenv("LLM_BASE_URL", "https://zeerafle-llm.duckdns.org/v1"),
        api_key=os.environ["FREELLMAPI_KEY"],
        temperature=0.5,
        rate_limiter=rate_limiter,
    )
