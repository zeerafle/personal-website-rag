import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from pinecone import Pinecone

load_dotenv()


# load vector store
pc = Pinecone()
index_name = os.environ.get("INDEX_NAME", "personal-website")
index = pc.Index(index_name)
embeddings = PineconeEmbeddings(model="multilingual-e5-large")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


def setup_rag():
    # initialize gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        # google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.5,
    )

    tools = [retrieve_context]
    prompt = (
        "You have access to a tool that retrieves context from Sam's posts. "
        "Use the tool to help answer user queries"
    )
    agent = create_agent(llm, tools, system_prompt=prompt)

    return agent


qa = setup_rag()
