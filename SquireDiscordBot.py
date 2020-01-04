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
import re
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
            #cur.execute('INSERT INTO users VALUES (\'122867560210235392\',\'Jen\',true, false, false, true, \'Happy Birthday\',\':JensCake:662156604270968843\')')
            cur.execute('INSERT INTO users VALUES ({},{},false, false, false, false, \'None\',\':JensCake:662156604270968843\')'.format('\''+message.author.id+'\'','\''+message.author.name+'\''))
            conn.commit()
            conn.close()
            return

        if (user[0][4]==True):
            await client.send_message(channel,user[0][6])
        if (user[0][5]==True):
            await client.add_reaction(message,user[0][7])
        conn.close()
        return

        #Examples
        #emoji = '\:slight_smile: '
        #await client.send_message(channel,"I support breast cancer")
        #await client.add_reaction(message,':yikes:589332576909525012')
        #await client.add_reaction(message,'a:hc:659191821506838528')
        

    #Command to suggest a random game from a list
    @client.command(name='playwhat',
                    description="TBD",
                    brief="TBD",
                    pass_context=True)
    async def whatGame(context):
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT "name" FROM games')
        user = cur.fetchall()
        m = re.search('\'(.+?)\'',str(random.choice(user)))
        if m:
           found = m.group(1)
        await client.say(found)

    @client.command(name='ng',
                description="TBD",
                brief="TBD",
                pass_context=True)
    async def newGame(context, message):
        if (message == None):
            return

        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('INSERT INTO games ("name") VALUES (\'{}\')'.format(message))
        conn.commit()
        await client.say('{} has been added to the list'.format(message))
        return

    @client.command(name='ag',
                description="TBD",
                brief="TBD",
                pass_context=True)
    async def allGames(context):
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * from games')
        games = cur.fetchall()
        gameOutput = ""
        for i in range (len(games)):
            gameOutput += (games[i][1]+'\n')
        await client.say(gameOutput)
        #embed = discord.Embed(title="List of Games", color=0x00ff00)
        #embed.add_field(name=" ", value=gameOutput, inline=False)
        #await client.say(embed=embed)
        return

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

    @client.command(name='mt',
                    description="TBD",
                    brief="TBD",
                    pass_context=True)
    async def messageToggle(context, target):
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
    
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()
        if (user[0][4]==True):  #messageToggle
            cur.execute('UPDATE users SET "messageToggle"= false WHERE "userID"={}'.format('\''+userID+'\''))
            conn.commit()
            await client.say("Message disabled for{}".format(target))
        elif (user[0][4]==False):  #messageToggle
            cur.execute('UPDATE users SET "messageToggle"= true WHERE "userID"={}'.format('\''+userID+'\''))
            conn.commit()
            await client.say("Message enabled for{}".format(target))
        conn.close()
        return
    
    @client.command(name='rt',
                    description="TBD",
                    brief="TBD",
                    pass_context=True)
    async def reactToggle(context, target):
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
    
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()
        if (user[0][5]==True):  #reactToggle
            cur.execute('UPDATE users SET "reactToggle"= false WHERE "userID"={}'.format('\''+userID+'\''))
            conn.commit()
            await client.say("Reaction disabled for{}".format(target))
        elif (user[0][5]==False):  #reactToggle
            cur.execute('UPDATE users SET "reactToggle"= true WHERE "userID"={}'.format('\''+userID+'\''))
            conn.commit()
            await client.say("Reaction enabled for{} ".format(target))
        return
        
    @client.command(name='cm',
                    description="TBD",
                    brief="TBD",
                    pass_context=True)
    async def changeMessage(context, target, message):
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
    
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()

        cur.execute('UPDATE users SET "message"= {} WHERE "userID"={}'.format('\''+message+'\'','\''+userID+'\''))
        conn.commit()
        await client.say("Message updated for{}".format(target))
        return
    

    
    @client.command(name='cr',
                description="TBD",
                brief="TBD",
                pass_context=True)
    async def changeReaction(context, target, message):
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
        m = re.search('<(.+?)>', message)
        if m:
            emoji = m.group(1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()

        cur.execute('UPDATE users SET "reaction"= {} WHERE "userID"={}'.format('\''+emoji+'\'','\''+userID+'\''))
        conn.commit()
        await client.say("Reaction updated for{}".format(target))
        return

    @client.command(name='gm',
                description="TBD",
                brief="TBD",
                pass_context=True)
    async def getMessage(context, target):
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()
        await client.say("Message for{} is {}".format(target,user[0][6]))
        return

    
    @client.command(name='gr',
                description="TBD",
                brief="TBD",
                pass_context=True)
    async def getReaction(context, target):
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()
        await client.say("Reaction for{} is <{}>".format(target,user[0][7]))
        return

    
    

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