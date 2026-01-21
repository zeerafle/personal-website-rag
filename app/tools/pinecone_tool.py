from langchain_core.tools import Tool
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore

from app.services.vectorstore import get_pinecone_index


def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    try:
        embeddings = PineconeEmbeddings(model="multilingual-e5-large")
        vector_store = PineconeVectorStore(
            index=get_pinecone_index(), embedding=embeddings
        )
        retrieved_docs = vector_store.similarity_search(query, k=3)

        # Format results
        results = "\n\n".join(
            [
                f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}"
                for doc in retrieved_docs
            ]
        )

        return (
            results
            if results
            else "No relevant information found in the knowledge base."
        )

    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"


def get_pinecone_tool() -> Tool:
    return Tool(
        name="retrieve_context",
        description="Search the knowledge base to for getting context to answer user questions. Use this when you need to find specific information or context.",
        func=retrieve_context,
    )
