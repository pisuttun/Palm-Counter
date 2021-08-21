from app import data
from flask import Flask, request
import flask_cors
import json
from threading import Thread

app = Flask('')
flask_cors.CORS(app)


@app.route('/')
def main():
    return "Your Bot Is Ready"


@app.route('/score', methods=['GET'])
def scoreboard():
    season = request.args.get('season')
    return json.dumps(data.getScore(int(season)))


@app.route('/last-score', methods=['GET'])
def last_score():
    return data.getLastScore()


def run():
    app.run(port=8000)


def run_keep_alive():
    server = Thread(target=run)
    server.start()
