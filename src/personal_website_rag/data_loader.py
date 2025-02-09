import os
from git import Repo
# from langchain.document_loaders import TextLoader

def clone_and_load_repo(github_url, local_dir):
    if os.path.exists(local_dir):
        Repo(local_dir).remotes.origin.pull()
    else:
        Repo.clone_from(github_url, local_dir)

    documents = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(('.md')):
                print(os.path.join(root, file))


if __name__ == '__main__':
    clone_and_load_repo(
        github_url='https://github.com/zeerafle/zeerafle.github.io',
        local_dir='./github_data'
    )
