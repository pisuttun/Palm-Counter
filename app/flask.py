from app.db import DB
from flask import Flask, request
import flask_cors
import json
import os
from threading import Thread
import dotenv

dotenv.load_dotenv()

app = Flask('')
flask_cors.CORS(app)


@app.route('/')
def main():
    return "Your Bot Is Ready"


@app.route('/score', methods=['GET'])
def scoreboard():
    db = DB(os.getenv("dbPath"), os.getenv("seasonName"), os.getenv("timezone"))
    season = request.args.get('season')
    return json.dumps(db.getScore(int(season)))


@app.route('/last-score', methods=['GET'])
def last_score():
    db = DB(os.getenv("dbPath"), os.getenv("seasonName"), os.getenv("timezone"))
    return db.getLastScore()


def run():
    app.run(port=8000)


def run_keep_alive():
    server = Thread(target=run)
    server.start()
