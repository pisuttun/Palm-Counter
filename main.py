import os
from app import flask
from app import discord
import dotenv


dotenv.load_dotenv()

flask.run_keep_alive()
discord.client.run(os.getenv("botKey"))
