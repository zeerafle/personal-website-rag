import os
from git import Repo
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def clone_and_load_repo(github_url, local_dir):
    if os.path.exists(local_dir):
        Repo(local_dir).remotes.origin.pull()
    else:
        Repo.clone_from(github_url, local_dir)

    documents = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith((".md")):
                loader = TextLoader(os.path.join(root, file))
                documents.extend(loader.load())

    return documents


def save_vector_store(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # using google gen ai embeddings
    model_name = "models/embedding-001"
    embeddings = GoogleGenerativeAIEmbeddings(model=model_name)

    # store in FAISS
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local("vector_store/faiss_index")
    print("Vector store saved to vector_store/faiss_index")


if __name__ == "__main__":
    docs = clone_and_load_repo(
        github_url="https://github.com/zeerafle/zeerafle.github.io",
        local_dir="./github_data",
    )
    save_vector_store(docs)
