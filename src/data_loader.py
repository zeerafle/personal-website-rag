import os
from git import Repo
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()


pc = Pinecone()
index_name = os.getenv("INDEX_NAME", "personal-website")
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
        }
    )

index = pc.Index(index_name)

def clone_and_load_repo(github_url, local_dir):
    if os.path.exists(local_dir):
        Repo(local_dir).remotes.origin.pull()
    else:
        Repo.clone_from(github_url, local_dir)

    documents = []
    excludes = ["README.md", "LICENSE"]
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith((".md")) and file not in excludes:
                file_path = os.path.join(root, file)
                loader = UnstructuredMarkdownLoader(file_path)
                docs = loader.load()

                for doc in docs:
                    if "_portfolio" in root:
                        doc.metadata["document_type"]= "portfolio"
                        doc.metadata["category"] = "portfolio"
                    elif "_posts" in root:
                        doc.metadata["document_type"]= "post"
                        doc.metadata["category"] = "post"
                    else:
                        doc.metadata["document_type"] = "general"
                        doc.metadata["category"] = "general"

                    doc.metadata["file_name"] = os.path.splitext(file)[0]
                    doc.metadata["file_path"] = file_path

                documents.extend(docs)

    return documents


def save_vector_store(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # store in Pinecone
    records = []
    for i, doc in enumerate(splits):
        unique_id = f"{doc.metadata.get('file_name', 'doc')}_{i}"
        record = {
            "_id": unique_id,
            "text": doc.page_content,
            "document_type": doc.metadata.get("document_type", ""),
            "category": doc.metadata.get("category", ""),
            "file_name": doc.metadata.get("file_name", ""),
            "file_path": doc.metadata.get("file_path", ""),
        }
        records.append(record)

    for batch in range(0, len(records), 96):
        batch_records = records[batch:batch+96]
        index.upsert_records(namespace="__default__", records=batch_records)
    print("Documents saved to Pinecone.")


if __name__ == "__main__":
    docs = clone_and_load_repo(
        github_url="https://github.com/zeerafle/zeerafle.github.io",
        local_dir="./github_data",
    )
    save_vector_store(docs)
