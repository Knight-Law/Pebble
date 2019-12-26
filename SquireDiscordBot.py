import random
import asyncio
import aiohttp
import json
import requests
import os
import sys
import urllib.request
import discord
from discord import Game
from discord.ext.commands import Bot

try:
    fp = open(os.path.join(sys.path[0], 'config.txt'), 'r')
    TOKEN = fp.read()
finally:
    fp.close()

BOT_PREFIX = (".")

client = Bot(command_prefix=BOT_PREFIX)
#Specialize message responding based on userID
#Note to self. Add message to an SQL table that's adjustable by command
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    if message.author.id == '124969272698077184': #HY
        author = message.author
        content = message.content
        channel = message.channel
        await client.send_message(channel,"SUP HY!")

    if message.author.id == '148338773887811587': #Chi
        author = message.author
        content = message.content
        channel = message.channel
        await client.add_reaction(message,':yikes:589332576909525012')

    if message.author.id == '136297703029080065': #CB
        author = message.author
        content = message.content
        channel = message.channel
        await client.send_message(channel,"Phanpy stuff I guess")

    if message.author.id == '102636726811389952': #Anthony
        author = message.author
        content = message.content
        channel = message.channel
        await client.add_reaction(message,'a:hc:659191821506838528')

    if message.author.id == '137291885130678272': #Mike
        author = message.author
        content = message.content
        channel = message.channel
        await client.send_message(channel,"1 gift for 2 days")

    if message.author.id == '122867560210235392': #Jen
        author = message.author
        content = message.content
        channel = message.channel
        await client.add_reaction(message,'🎂')
        #await client.send_message(channel,"Happy Birthday!!!")

    if message.author.id == '96746583445475328': #Mark
        author = message.author
        content = message.content
        channel = message.channel
        await client.send_message(channel,"************")
    
    if message.author.id == '97590532380827648': #Law
        author = message.author
        content = message.content
        channel = message.channel
        #emoji = '\:slight_smile: '
        #await client.send_message(channel,"I support breast cancer")
        #await client.add_reaction(message,':yikes:589332576909525012')
        #await client.add_reaction(message,'a:hc:659191821506838528')
        return

#Command to suggest a random game from a list
@client.command(name='playwhat',
                description="TBD",
                brief="TBD",
                pass_context=True)
async def whatGame(context):
    possible_responses = [
        'Risk of Rain 2',
        'League of Legends',
        'Smash',
        'Draw Something',
        'MHW',
        'Wizard of Legends',
        'Terraria',
        'Minecraft',
        'Stardew Valley',
        'Outward',
        'Brawlhalla',
        'Mabinogi',
        'Pokemon',
        'Dont Starve Together',
        'Monaco',
        'Left 4 Dead',
    ]
    await client.say(random.choice(possible_responses))
#showcases the current server status of Mabinogi's Nao server using an API
@client.command(name='naoStatus',
                description="TBD",
                brief="TBD",
                pass_context=True)
async def mabiServerStatus(context):
    with urllib.request.urlopen("http://mabi.world/mss/status.json") as url:
        data = json.loads(url.read().decode())
    total = []
    combine = ""
    size = (len(data['game']['servers'][0]['channels']))
    for i in range (size):
        total.append(json.dumps(data['game']['servers'][0]['channels'][i]['name'] ) + " : " + json.dumps(data['game']['servers'][0]['channels'][i]['stress']) + '%')
        combine += total[i] +'\n'
    embed = discord.Embed(title="Nao Server Status", color=0x00ff00)
    embed.add_field(name="Channels", value=combine, inline=False)
    await client.say(embed=embed)
client.run(TOKEN)
