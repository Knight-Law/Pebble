import random
import asyncio
import aiohttp
import json
import requests
import os
import sys
import urllib.request
import discord
import psycopg2
from discord import Game
from discord.ext.commands import Bot
from config import config

def testConnect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute('SELECT "name" FROM users')
        print(cur.rowcount)
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
def getConnect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def initilizeBot():
    try:
        fp = open(os.path.join(sys.path[0], 'config.txt'), 'r')
        TOKEN = fp.read()
    finally:
        fp.close()

    BOT_PREFIX = (".")
    client = Bot(command_prefix=BOT_PREFIX)

    @client.event
    async def on_message(message):
        cur, conn = getConnect()
        await client.process_commands(message)

        if message.author == client.user:
            return

        channel = message.channel
        cur.execute('SELECT * FROM users WHERE "userID"=\'{}\''.format(message.author.id))
        user = cur.fetchall()
        if not user:
            print("User does exist in database")
            return
        if (user[0][4]==True):
            await client.send_message(channel,user[0][6])
        if (user[0][5]==False):
            await client.add_reaction(message,user[0][7])
        conn.close()
        return

        #Examples
        #emoji = '\:slight_smile: '
        #await client.send_message(channel,"I support breast cancer")
        #await client.add_reaction(message,':yikes:589332576909525012')
        #await client.add_reaction(message,'a:hc:659191821506838528')
        

    #Command to suggest a random game from a list
    #Move list to a table later
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


    @client.command(name='exit',
                    description="TBD",
                    brief="TBD",
                    pass_context=True)
    async def endProgram(context):
        client.close()
        sys.exit()

    client.run(TOKEN)


 
if __name__ == '__main__':
    testConnect()
    initilizeBot()