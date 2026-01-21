import os
from functools import lru_cache

from pinecone import Pinecone


@lru_cache()
def get_pinecone_client():
    return Pinecone()


@lru_cache()
def get_pinecone_index():
    pc = get_pinecone_client()

    index = pc.Index(os.environ.get("INDEX_NAME", "personal-website"))
    return index
