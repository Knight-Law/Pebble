import random
import asyncio
import aiohttp
import json
import requests
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = (".")
STEAMAPI = '?'
TOKEN = '?'

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='whosucks',
                description="TBD",
                brief="TBD",
                aliases=['TBD'],
                pass_context=True)
async def suckList(context):
    possible_responses = [
        'Mark Sucks',
        'Hy Sucks',
        'Michael Sucks',
        'Jen Sucks',
        'Everyone is awesome',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

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
        'Dont starve together',
        'Monaco',
        'Left 4 Dead',
        'Black Desert Online',
    ]
    await client.say(random.choice(possible_responses))
#dasdsadsa
@client.command(name='steamTest',
                description="TBD",
                brief="TBD",
                pass_context=True)
async def steamAPI(context, arg):
    id = arg
    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=%s&count=3&maxlength=300&format=json' % id
    response = requests.get(url)
    await client.say(id)
    await client.say(url)
    await client.say(response.json())

@client.command(name='boredom',
                description="TBD",
                brief="TBD",
                pass_context=True)
async def boredom(context, arg):
    number = int (arg)
    number = number*number
    await client.say(number)


#@client.command()
#async def square(number):
#    squared_value = int(number) * int(number)
#    await client.say(str(number) + " squared is " + str(squared_value))


#@client.event
#async def on_ready():
#    await client.change_presence(game=Game(name="with humans"))
#    print("Logged in as " + client.user.name)


#@client.command()
#async def bitcoin():
#    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
#    async with aiohttp.ClientSession() as session:  # Async HTTP request
#        raw_response = await session.get(url)
#        response = await raw_response.text()
#        response = json.loads(response)
#        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


#async def list_servers():
#    await client.wait_until_ready()
#    while not client.is_closed:
#        print("Current servers:")
#        for server in client.servers:
#            print(server.name)
#        await asyncio.sleep(600)


#client.loop.create_task(list_servers())
client.run(TOKEN)
