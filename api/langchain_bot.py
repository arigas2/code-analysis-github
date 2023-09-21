import os
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import chromadb
from langchain.llms import Ollama
# from langchain.chat_models import ChatOllama
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
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = './db'


def get_github_docs(repo_owner, repo_name):
    print('start get github docs')
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
                yield Document(page_content=f.read(), metadata={"source": github_url})


def chunk_docs(sources):
    print('start chunk docs')
    # could try different source_splitter
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    source_chunks = text_splitter.split_documents(sources)
    return source_chunks


def index_docs(source_chunks, embeddings, repo_owner, repo_name):
    print("start index docs")
    collection_name = repo_owner+"-"+repo_name
    # vectordb = Chroma.from_documents(source_chunks, embeddings)
    vectordb = Chroma.from_documents(collection_name=collection_name,
                                     persist_directory=persist_directory,
                                     documents=source_chunks,
                                     embedding=embeddings)
    return vectordb


def construct_retriever(db):
    print('start construct retriever')
    retriever = db.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8}
    )
    return retriever


def construct_convo_chain(retriever):
    print('start construct convo chain')
    # model = ChatOllama(model="llama2:7b-chat")
    model = Ollama(base_url="http://localhost:11434",
                   model="orca-mini")
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
    return qa


def add_new_repo(repo_owner, repo_name):
    sources = get_github_docs(repo_owner, repo_name)
    source_chunks = chunk_docs(sources)
    db = index_docs(source_chunks, embeddings, repo_owner, repo_name)
    retriever = construct_retriever(db)
    qa = construct_convo_chain(retriever)
    return qa


def get_collection_names():
    client = chromadb.PersistentClient(path="./db")
    names = []
    for collection in client.list_collections():
        names.append(collection.name)
    print(names)
    return names


def ask_question(repo_name, question):
    client = chromadb.PersistentClient(path="./db")
    db = Chroma(
        client=client,
        collection_name=repo_name,
        embedding_function=embeddings,
    )
    retriever = construct_retriever(db)
    qa = construct_convo_chain(retriever)
    chat_history = []
    result = qa({"question": question, "chat_history": chat_history})
    return result['answer']





# qa = add_new_repo("karpathy", "micrograd")
# qa = create_new_convo("karpathy", "nanoGPT")
# qa = create_new_convo("karpathy", "micrograd")

# questions = [
#     "what is the purpose of the engine.py file"
# ]
# chat_history = []

# for question in questions:
#     result = qa({"question": question, "chat_history": chat_history})
#     chat_history.append((question, result["answer"]))
#     print(f"-> **Question**: {question} \n")
#     print(f"**Answer**: {result['answer']} \n")
