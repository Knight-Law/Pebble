import random
import asyncio
import aiohttp
import json
import requests
import os
import time
import sys
import urllib.request
import discord
import psycopg2
import re
import textwrap
from io import BytesIO
from discord import Game
from discord.ext.commands import Bot
from config import config
from PIL import Image, ImageColor, ImageDraw, ImageSequence, ImageFont


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

    #Bot will give a reaction or message depending on the userID paramters
    @client.event
    async def on_message(message):
        cur, conn = getConnect()
        await client.process_commands(message)

        if message.author == client.user:
            return

        channel = message.channel
        ##print (message.guild.id)
        #cur.execute('SELECT * FROM users WHERE "userID"=\'{}\''.format(message.author.id))
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

        #Examples
        #emoji = '\:slight_smile: '
        #await client.send_message(channel,"I support breast cancer")
        #await client.add_reaction(message,':yikes:589332576909525012')
        #await client.add_reaction(message,'a:hc:659191821506838528')
        
    #Grabs a random response 
    @client.command(name='showme',
                    description="Pebble will answer a question by shattering itself",
                    brief="Pebble will answer your questions",
                    pass_context=True,
                    aliases =['sm'])
    async def ballresponse(context):
        newMSG = await context.send(file=discord.File('PebbleShatter.gif'))#delete_after = 0.1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT "response" FROM answers')
        user = cur.fetchall()
        m = re.search('\'(.+?)\'',str(random.choice(user)))
        if m:
           found = m.group(1)
        #embed = discord.Embed(title="\u200b", color=0xDBC4C4)
        #embed.add_field(name="\u200b", value=found, inline=False)
        #await context.send(embed=embed)
        time.sleep(3)
        await newMSG.delete()
        await context.send("*Pebble shatters itself to reveal...*\n**{}**".format(found))
        return

    #Suggest a random game
    @client.command(name='playwhat',
                    description="Pebble will decide a random game for you",
                    brief="Pebble will decide a random game for you",
                    pass_context=True,
                    aliases =['pw'])
    async def whatGame(context, gameType):
        cur, conn = getConnect()
        cur = conn.cursor()
        
        # if (gameType[0]=='-'):
        #     include = "false"
        # else:
        #     include = "true"
        
        if (gameType == 'tts'):
            cur.execute('SELECT "name","description","url" FROM games WHERE "TTS" = true')
        elif (gameType == 'all'):
            cur.execute('SELECT "name","description","url" FROM games')
        elif (gameType == '-tts'):
            cur.execute('SELECT "name","description","url" FROM games WHERE "TTS" = false')
        else:
            await context.send("*Pebble deems you have chosen an invalid mode and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        user = cur.fetchall()
        conn.close()
        m = re.findall('\'(.+?)\'',str(random.choice(user)))
        if m:
           nameFound = m[0]
           descriptionFound = m[1]
           urlFound = m[2]
        embed = discord.Embed(title=nameFound,description = descriptionFound,url = urlFound)
        await context.send(embed=embed)

    #Adds a new game to the list
    @client.command(name='newgame',
                description="Add a new game to Pebble\'s recommended games",
                brief="Pebble wants a new game",
                pass_context=True,
                aliases =['ng'])
    async def newGame(context, message):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this')
            return
        if (message == None):
            return
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('INSERT INTO games ("name") VALUES (\'{}\')'.format(message))
        conn.commit()
        conn.close()
        embed = discord.Embed(title="\u200b", color=0xDBC4C4)
        embed.add_field(name="\u200b", value='{} has been added to the list'.format(message), inline=False)
        await context.send(embed=embed)
        return

    #Outputs all the games 
    @client.command(name='allgames',
                description="Pebble will display all the games it knows.",
                brief="Pebble will display all the games it knows.",
                pass_context=True,
                aliases =['ag'])
    async def allGames(context, gameType):
        cur, conn = getConnect()
        cur = conn.cursor()
        if (gameType == 'tts'):
            cur.execute('SELECT * from games WHERE "TTS" = true')
            embed = discord.Embed(title="All Table Top Simulator Games", color=0xDBC4C4)
        elif (gameType == 'all'):
            cur.execute('SELECT * from games')
            embed = discord.Embed(title="All Games", color=0xDBC4C4)
        else:
            await context.send("*Pebble deems you have chosen an invalid mode and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        games = cur.fetchall()
        conn.close()
        gameOutput = ""
        games.sort(key = lambda x: x[1])
        for i in range (len(games)):
            gameOutput += ('[{}] '.format(i+1)+games[i][1])
            if (gameType != 'tts'):
                if (games[i][4]):
                    gameOutput += " : *TTS* \n"
                else:
                    gameOutput += "\n"
            else:
                gameOutput += "\n"
        #embed = discord.Embed(title="All the games", color=0xDBC4C4)
        embed.add_field(name="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", value=gameOutput, inline=False)
        await context.send(embed=embed)
        return

    #Showcase
    @client.command(name='color',
                description="Pebble will print a color from the hex color code given",
                brief="Pebble will print a color from the hex color code given",
                pass_context=True)
    async def printColor(context,hue):
        match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hue) #Checks for valid hex color code
        if match:
            im = Image.new(mode = "RGB", size = (25, 25), color = ('#{}'.format(hue)))
            pixel = im.save('simplePixel.png') 
            await context.send(file=discord.File('simplePixel.png'))
        else:
            await context.send('Invalid Hex Color Code')
        return

    #Overlays a gif over a targetted user's avatar
    @client.command(name='pet',
                description="Pebble will give a friendly petting to a user of your choice",
                brief="Pebble gives pets",
                pass_context=True)
    async def printColor(context,target:discord.User):
        response = requests.get(target.avatar_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((50,50))

        gifFrames = 10
        avatar = Image.new('RGBA',(100,100),(255, 105, 180, 255))
        avatar.paste (img.convert('RGBA'),(34,21))

        output = []

        for x in range(gifFrames):
            output.append(avatar.copy())
            im = Image.open("Hands\\{}.png".format(str(x+1))).convert('RGBA')
            output[x].paste(im,(0,0), mask = im)

        final = output[0]
        final.save('out.gif','GIF',save_all=True, append_images= output, optimize=True, duration=70, loop=0, transparency = 0, disposal = 2)
        await context.send(file=discord.File('out.gif'))
        return

    #sign
    @client.command(name='sign',
                    description="Select a color such as red and a message in \"\" ",
                    brief="Pebble forces an astronaut to hold a sign",
                    pass_context=True)
    async def messageToggle(context, colorChoice, message):
        if (len(message)>75):
            await context.send("*Pebble deems your message too long and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return

        sign = Image.open("AmongUs\\Sign.png").convert('RGBA')
        player = Image.open("AmongUs\\{}.png".format(colorChoice)).convert('RGBA')
        player.paste(sign,(0,0), mask = sign)

        draw = ImageDraw.Draw(player)
        font = ImageFont.truetype("arial.ttf", 16)
        #draw.text((24, 191),message,(0,0,0),font=font)
        h = 180
        w = 240 
        lines = textwrap.wrap(message, width=25)
        y_text = h
        for line in lines:
            width, height = font.getsize(line)
            draw.text(((w - width) / 2, y_text), line, (0,0,0),font=font)
            y_text += height
        
        player = player.resize ((180,180))
        player.save('sign.png')

        await context.send(file=discord.File('sign.png'))
        return

    #Flips the message parameter to True/False
    @client.command(name='messagetoggle',
                    description="Flips the user\'s toggle for messages",
                    brief="Pebble flips the user\'s toggle for messages",
                    pass_context=True,
                    aliases =['mt'])
    async def messageToggle(context, target):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this```')
            return
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
            embed = discord.Embed(title="\u200b", color=0xDBC4C4)
            embed.add_field(name="\u200b", value="Message disabled for {}".format(target), inline=False)
            await context.send(embed=embed)
        elif (user[0][4]==False):  #messageToggle
            cur.execute('UPDATE users SET "messageToggle"= true WHERE "userID"={}'.format('\''+userID+'\''))
            conn.commit()
            embed = discord.Embed(title="\u200b", color=0xDBC4C4)
            embed.add_field(name="\u200b", value="Message enabled for {}".format(target), inline=False)
            await context.send(embed=embed)
        conn.close()
        return
        
    #Flips the react parameter to True/False
    @client.command(name='reactiontoggle',
                    description="Flips the user\'s toggle for messages reactions",
                    brief="Pebble flips the user\'s toggle for messages reactions",
                    pass_context=True,
                    aliases =['rt'])
    async def reactToggle(context, target):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this')
            return
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
            conn.close()
            embed = discord.Embed(title="\u200b", color=0xDBC4C4)
            embed.add_field(name="\u200b", value="Reaction disabled for {}".format(target), inline=False)
            await context.send(embed=embed)
        elif (user[0][5]==False):  #reactToggle
            cur.execute('UPDATE users SET "reactToggle"= true WHERE "userID"={}'.format('\''+userID+'\''))
            conn.commit()
            conn.close()
            embed = discord.Embed(title="\u200b", color=0xDBC4C4)
            embed.add_field(name="\u200b", value="Reaction enabled for {}".format(target), inline=False)
            await context.send(embed=embed)
        return
    
    #Changes the message of the targeted user
    @client.command(name='changemessage',
                    description="Change Pebble\'s message of the targeted user",
                    brief="Pebble wants to change its message",
                    pass_context=True,
                    aliases =['cm'])
    async def changeMessage(context, target, message):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this')
            return
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
        conn.close()
        embed = discord.Embed(title="\u200b", color=0xDBC4C4)
        embed.add_field(name="\u200b", value="Message updated for {}".format(target), inline=False)
        await context.send(embed=embed)
        return
    
    #Changes the reaction of the targeted user
    @client.command(name='changereaction',
                description="Change Pebble\'s reaction of the targeted user",
                brief="Pebble wants to change its reaction",
                pass_context=True,
                aliases =['cr'])
    async def changeReaction(context, target, message):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this')
            return
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
        conn.close()
        embed = discord.Embed(title="\u200b", color=0xDBC4C4)
        embed.add_field(name="\u200b", value="Reaction updated for {}".format(target), inline=False)
        await context.send(embed=embed)
        return

    #Gets the current message of the targeted user  
    @client.command(name='getmessage',
                description="See Pebble\'s message for the user",
                brief="Pebble will show you the message for the user",
                pass_context=True,
                aliases =['gm'])
    async def getMessage(context, target):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this')
            return
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()
        conn.close()
        embed = discord.Embed(title="\u200b", color=0xDBC4C4)
        embed.add_field(name="\u200b", value="Message for {} is {}".format(target,user[0][6]), inline=False)
        await context.send(embed=embed)
        return

    #Gets the current reaction of the targeted user  
    @client.command(name='getreaction',
                description="See Pebble\'s reaction for the user",
                brief="Pebble will show you the reaction for the user",
                pass_context=True,
                aliases =['gr'])
    async def getReaction(context, target):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this')
            return
        if (target == None):
            return
        m = re.search('<@!(.+?)>', target)
        if m:
            userID = m.group(1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE "userID"={}'.format('\''+userID+'\''))
        user = cur.fetchall()
        conn.close()
        embed = discord.Embed(title="\u200b", color=0xDBC4C4)
        embed.add_field(name="\u200b", value="Reaction for {} is <{}>".format(target,user[0][7]), inline=False)
        await context.send(embed=embed)
        return

    #Exit 
    @client.command(name='exit',
                    description="Pebble goes bye",
                    brief="Pebble goes bye",
                    pass_context=True)
    async def endProgram(context):
        #client.close()
        #sys.exit()
        return

    client.run(TOKEN)



if __name__ == '__main__':
    testConnect()
    initilizeBot()