from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv
import os


load_dotenv()


def setup_rag():
    # load vector store
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    vectorstore = FAISS.load_local('vector_store/faiss_index',
                                   embeddings,
                                   allow_dangerous_deserialization=True)

    # initialize gemini
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash-lite-preview-02-05',
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        temperature=0.5
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    rag_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain)

    return rag_chain

qa = setup_rag()
