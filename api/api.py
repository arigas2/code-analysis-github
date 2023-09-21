from flask import Flask, request, redirect, url_for
import time
import langchain_bot
from urllib.parse import urlparse
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world!'


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/newrepo', methods=['POST'])
def input_repo():
    parse_json = request.get_json()
    url = parse_json['url']
    path = urlparse(url).path
    path_split = path.split('/')
    repo_owner = path_split[1]
    repo_name = path_split[2]
    langchain_bot.add_new_repo(repo_owner, repo_name)
    return redirect(url_for('qa'))


@app.route('/qa')
def qa():
    # show the post with the given id, the id is an integer
    return 'ready to answer'


@app.route('/repos')
def get_repos():
    repo_names = langchain_bot.get_collection_names()
    print(repo_names)
    return {'repo_names': repo_names}


@app.route('/repos/<repo_name>', methods=['PUT'])
def ask_question(repo_name):
    parse_json = request.get_json()
    question = parse_json['question']
    answer = langchain_bot.ask_question(repo_name, question)
    return {'answer': answer}

