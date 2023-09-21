import os
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
# from langchain.chat_models import ChatOpenAI
from langchain.chat_models import JinaChat
from langchain.chains import ConversationalRetrievalChain

# from langchain import HuggingFaceHub
# from langchain import PromptTemplate, LLMChain
# from langchain.chains.qa_with_sources import load_qa_with_sources_chain
# import requests
# from langchain.document_loaders import TextLoader
import pathlib
import subprocess
import tempfile


# get a token: https://huggingface.co/docs/api-inference/quicktour#get-your-api-token

# from getpass import getpass
# HUGGINGFACEHUB_API_TOKEN = getpass()

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
# repo_id = "google/flan-t5-xxl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
os.environ["JINACHAT_API_KEY"] = "fgKakGlX5AHil5DsoINy:dd35aea4ea25aa103044555bebbf95f1e58a722dce559097280df11eb223b077"
embeddings = HuggingFaceEmbeddings()


def get_github_docs(repo_owner, repo_name):
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(
            f"git clone --depth 1 https://github.com/{repo_owner}/{repo_name}.git .",
            cwd=d,
            shell=True,
        )
        git_sha = (
            subprocess.check_output("git rev-parse HEAD", shell=True, cwd=d)
            .decode("utf-8")
            .strip()
        )

        repo_path = pathlib.Path(d)

        files = [x for x in list(repo_path.glob('**/*')) if x.is_file()]
        for file in files:
            with open(file, "r", errors='ignore') as f:
                relative_path = file.relative_to(repo_path)
                github_url = f"https://github.com/{repo_owner}/{repo_name}/blob/{git_sha}/{relative_path}"
                print(github_url)
                yield Document(page_content=f.read(), metadata={"source": github_url})


def chunk_docs(sources):
    # could try different source_splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    source_chunks = text_splitter.split_documents(sources)
    return source_chunks


def index_docs(source_chunks, embeddings):
    print('start indexing')
    db = Chroma.from_documents(source_chunks, embeddings)
    return db


def construct_retriever(db):
    retriever = db.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8}
    )
    return retriever


def construct_convo_chain(retriever):
    model = JinaChat()
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
    return qa


sources = get_github_docs("karpathy", "micrograd")
source_chunks = chunk_docs(sources)
db = index_docs(source_chunks, embeddings)
retriever = construct_retriever(db)
qa = construct_convo_chain(retriever)


questions = [
    "what is the purpose of the engine.py file"
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
