import random
import asyncio
import aiohttp
import json
import requests
from discord import Game
from discord.ext.commands import Bot

try:
    fp = open('C:/Users/Lawrence/Desktop/token.txt','r')
    TOKEN = fp.read()
finally:
    fp.close()

BOT_PREFIX = (".")

client = Bot(command_prefix=BOT_PREFIX)

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
        await client.send_message(channel,"Happy Birthday!!!")

    if message.author.id == '96746583445475328': #Mark
        author = message.author
        content = message.content
        channel = message.channel
        await client.send_message(channel,"I support breast cancer")
    
    if message.author.id == '97590532380827648': #Law
        author = message.author
        content = message.content
        channel = message.channel
        #emoji = '\:slight_smile: '
        #await client.send_message(channel,"I support breast cancer")
        #await client.add_reaction(message,':yikes:589332576909525012')
        #await client.add_reaction(message,'a:hc:659191821506838528')
        return

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



client.run(TOKEN)
