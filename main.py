import dotenv
from app import discord
from app import flask
import os

dotenv.load_dotenv()

flask.run_keep_alive()
discord.client.run(os.getenv("botKey"))
