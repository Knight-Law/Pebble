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

userAmount = 0
userID = list()
name = list()
responseType = list()
response = list()

try:
    fp = open(os.path.join(sys.path[0], 'config.txt'), 'r')
    TOKEN = fp.read()
finally:
    fp.close()

BOT_PREFIX = (".")
client = Bot(command_prefix=BOT_PREFIX)


try:
    fp = open(os.path.join(sys.path[0], 'users.txt'), 'r')
    userAmount = int(fp.readline())
    for x in range(userAmount):
            userID.append(fp.readline().rstrip('\n'))
            name.append(fp.readline().rstrip('\n'))
            responseType.append(fp.readline().rstrip('\n'))
            response.append(fp.readline().rstrip('\n'))
finally:
    fp.close()


users = ([userID,name,responseType,response])

print (users)





#Specialize message responding based on userID
    #Note to self. Add message to an SQL table that's adjustable by command
    #Issues with implementing a SQL database, will use a .txt file as a temporary work around
@client.event
async def on_message(message):
    await client.process_commands(message)
    choice = 99999999
    for x in range (len(userID)):
        if (message.author.id==userID[x]):
            choice = x
        else:
            return

    if message.author == client.user:
        return

    if message.author.id == userID[choice]: 
        author = message.author
        content = message.content
        channel = message.channel
        if (int(responseType[choice])==1):
            await client.send_message(channel,response[choice])
        elif (int(responseType[choice])==0):
            await client.add_reaction(message,response[choice])
        else:
            return

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
        'Buy a new game on steam',
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
        #combine += total[i] +'\n'
#---------------
    hold = '' 
    for i in range(0, len(total)): 
        if(total[i].startswith('"Ch')): 
            end = total[i].index('"', 1) 
            start = total[i].index('h', 1) + 1 
            part = total[i][start:end] 
            total[i] = total[i].partition(part) 
        else: 
            hold = i 

    hold = total.pop(hold) 

    for i in range(0, len(total)): 
        total[i] = list(total[i]) 
        total[i][1] = int(total[i][1]) 

    a = sorted(total, key=lambda x: x[1]) 
    for i in range(len(a)): 
        concat = '' 
        for c in a[i]: 
            concat += str(c) 
        a[i] = concat 
    a.append(hold) 
    for i in range (size):
        combine += a[i] +'\n'
#----------------
    embed = discord.Embed(title="Nao Server Status", color=0x00ff00)
    embed.add_field(name="Channels", value=combine, inline=False)
    await client.say(embed=embed)



@client.command(name='save',
                description="TBD",
                brief="TBD",
                pass_context=True)
async def saveToFile(context):
    fp = open(os.path.join(sys.path[0], 'configTest.txt'), 'w')
    fp.write(str(userAmount)+'\n')
    for x in range(userAmount):
        fp.write(userID[x]+'\n')
        fp.write(name[x]+'\n')
        fp.write(responseType[x]+'\n')
        fp.write(response[x]+'\n') 
    fp.close()

@client.command(name='exit',
                description="TBD",
                brief="TBD",
                pass_context=True)
async def endProgram(context):
    client.close()
    sys.exit()

client.run(TOKEN)
