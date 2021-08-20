import discord
import data
from flask import Flask,request
from threading import Thread
import flask_cors
import json
import os
import dotenv

client = discord.Client()

dotenv.load_dotenv()
app = Flask('')
flask_cors.CORS(app)

@app.route('/')
def main():
  return "Your Bot Is Ready"

@app.route('/score',methods=['GET'])
def scoreboard():
    season = request.args.get('season')
    return json.dumps(data.getScore(int(season)))

@app.route('/last-score',methods=['GET'])
def last_score():
    return data.getLastScore()

def run():
  app.run(port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

keep_alive()

##############################################################
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user:
        return

    if msg.startswith('-test'):
        await message.channel.send('Hello!')
        return
    
    if msg.startswith('-pc'):
        if msg.split()[1] == 'list':
            await message.channel.send('"ปาล์มมาตั้งแต่เมื่อไหร่นี่" scoreboard')
            if len(msg.split()) >= 3:
              send = generateTable(int(msg.split()[2]))
            else:
              send = generateTable(2)
            await message.channel.send(embed=send)
        elif len(msg.split()) > 1:
            name = msg.split()[1]
            result = data.add(name)

            if result == "Invalid name":
                await message.channel.send(result)
                return
            if result.startswith("Duplicated date"):
                khinged = "<:khinged:812167089712005190>"
                name = result.split()[2]
                await message.channel.send("You're too late, วันนี้ "+ name +" ได้คะแนนไปแล้ว")
                await message.channel.send(khinged)
                return
            
            #add success 
            await message.channel.send(f'add {result} to scoreboard successfully')
            send = generateTable(2)
            await message.channel.send(embed=send)
        return

def generateTable(season):
    stats = data.listScore(season)
    send = discord.Embed(title='scordboard S'+str(season),description=stats,color=0x5865F2)
    send.set_thumbnail(url = 'https://firebase.google.com/downloads/brand-guidelines/PNG/logo-built_white.png')
    return send

##############################################################
client.run(os.getenv("botKey"))