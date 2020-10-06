import asyncio
import os
import time
import sys
import discord
import psycopg2
import re
from datetime import datetime
from discord import Game
from discord.ext import tasks
from discord.ext.commands import Bot
from config import config


BOT_PREFIX = (">")
client = Bot(command_prefix=BOT_PREFIX)


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

#Segment to load and unload cogs
@client.command(hidden = True)
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')

@client.command(hidden = True)
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir("cogs/"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

def initilizeBot():
    try:
        fp = open(os.path.join(sys.path[0], 'config.txt'), 'r')
        TOKEN = fp.read()
    finally:
        fp.close()
    client.run(TOKEN)
    return

    

#Bot will give a reaction or message depending on the userID paramters
@client.event
async def on_message(message):
    cur, conn = getConnect()
    await client.process_commands(message)

    if message.author == client.user:
        return

    channel = message.channel
    cur.execute('SELECT * FROM users WHERE "userID"=\'{}\'AND"server"=\'{}\''.format(message.author.id,message.guild.id))
    user = cur.fetchall()
    if not user:
        print("{} has been aded to the database".format(message.author.name))
        cur.execute('INSERT INTO users VALUES ({},{},false, false, false, false, \'None\',\':JensCake:662156604270968843\', {})'.format('\''+str(message.author.id)+'\'','\''+message.author.name+'\'','\''+str(message.guild.id)+'\''))
        conn.commit()
        conn.close()
        return

    if (user[0][4]==True):
        embed = discord.Embed(title=user[0][6], color=0xDBC4C4)
        await message.channel.send(embed=embed)
    if (user[0][5]==True):
        await message.add_reaction(user[0][7])
    conn.close()
    return



#Exit 
@client.command(name='exit',
                description="Pebble goes bye",
                brief="Pebble goes bye",
                pass_context=True,
                hidden = True)
async def endProgram(context):
    #client.close()
    #sys.exit()
    return



if __name__ == '__main__':
    testConnect()
    initilizeBot()