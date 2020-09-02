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
import math
import textwrap
from io import BytesIO
from datetime import datetime
from discord import Game
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import Bot
from config import config
from PIL import Image, ImageColor, ImageDraw, ImageSequence, ImageFont


gamesList = []

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
            #print(row)
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

    @tasks.loop(seconds=21)
    async def cleanUp():
        global gamesList
        amountDeleted = 0
        copyList = gamesList.copy()
        #print (gamesList[0][2][0][1])
        #print(len(gamesList))
        i = 0
        for i in range(len(gamesList)):
            #print (testList[i][1].time())
            #print (datetime.now().time())
            d1 = gamesList[i][1]
            d2 = datetime.now()
            d2 = d2-d1
            #print (d2.total_seconds())
            if (d2.total_seconds()>20):
                del copyList[i-amountDeleted]
        gamesList = copyList.copy()
        return

    @client.event
    async def on_ready():
        cleanUp.start()

    #Bot will give a reaction or message depending on the userID paramters
    @client.event
    async def on_message(message):
        cur, conn = getConnect()
        await client.process_commands(message)

        if message.author == client.user:
            return

        channel = message.channel
        #print (message.guild.id)
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

    @client.command(name='signList',
                    description="Pebble will show all the choices for the sign command",
                    brief="Pebble will show all the choices for the sign command",
                    pass_context=True)
    async def files(context):
        characterList = (os.listdir("AmongUs\\"))
        output = ''
        characterList.remove('Sign.png')
        for i in range(len(characterList)):
            if ".png" in characterList[i]:
                output += "{}\n".format(characterList[i].replace('.png',''))
        if output == '':
            output = 'No Files'
        await context.send("```{}```".format(output))
        return

    @client.command(name='soulmate',
                    description="Pebble will see the compatibility between two people",
                    brief="Pebble will see the compatibility between two people",
                    pass_context=True)
    async def soulMate(context, target1:discord.User, target2:discord.User):
        random.seed(target1.id+target2.id)
        result = random.randint(0,10)
        heartString = ""
        description = ""
        for i in range(result):
            heartString += '❤️'
        for i in range(10-result):
            heartString += '🖤'


        if (result == 0):
            description = "Pebble deems your souls aren\'t meant to spend even a second much less eternity together"
        elif (result >= 1 and result <=2):
            description = "Pebble sees no love between you two "
        elif (result >= 3 and result <=4):
            description = "Pebble knows the love you feel is brief"    
        elif (result >= 5 and result <=7):
            description = "Pebble sees you are fond of each other, but unsure if the love will last"
        elif (result >= 8 and result <=9):
            description = "Pebble knows your love is true and will last"
        elif (result == 10):
            description = "Pebble sees you were created in the beginning to spend eternity with each other"
        
        #await context.send(heartString)
        embed = discord.Embed(title=heartString,description = " ")
        embed.add_field(name="Soulmate Results", value="{}".format(description), inline=False)
        await context.send(embed=embed)
        return

    @client.command(name='allchannels',
                    description="Pebble goes bye",
                    brief="Pebble goes bye",
                    pass_context=True,
                    aliases =['ac'])
    async def allchannels(context, type):
        #test = context.message.author.guild.channels[1].type
        #print (test)

        if (type != "text" and type != "voice"):
            await context.send("*Pebble deems your mode choice invalid and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return

        voiceChanneList = []
        for i in context.message.author.guild.channels:
            if (i.type.name == type):
                voiceChanneList.append((i.id,i.type.name,i.name,i.members))
            #print (i.type)
        #print(voiceChanneList)
        if (type == 'voice'):
            output = '**#. Name : ID : People in Call**\n'
        elif (type == 'text'):
            output = '**#. Name : ID : People with Accessed**\n'

        for i in range(len(voiceChanneList)):
            output += "{}. {} : {} : {}\n".format(i+1,voiceChanneList[i][2],voiceChanneList[i][0],len(voiceChanneList[i][3]))
            #output += "{:<3}{:-^30}{:-18}{:-^3}\n".format(str(i+1)+'.',voiceChanneList[i][2],voiceChanneList[i][0],len(voiceChanneList[i][3]))
        cycles = None
        if (len(output)>2000):
            cycles = math.ceil(len(output)/2000) 
            for i in range (cycles):
                await context.send(output[0+(i*2000):1999+(i*2000)])
                #await context.send(output[0:1999])
                #print (5)
        else:
            await context.send(output)
        return

    #async def select(context,voice: discord.VoiceChannel, teams, members):
    #Showcase
    @client.command(name='select',
                description="Pebble will print a color from the hex color code given",
                brief="Pebble will print a color from the hex color code given",
                pass_context=True)
    async def select(context,voiceID, teams, members):
        #Get all server voice channels and select voice to the discord voice channel that matches the id to simplify call
        voice = None
        for i in context.message.author.guild.channels:
            if (i.id == int(voiceID)):
                voice = i
        if voice == None:
            await context.send("*Pebble deems the channel id invalid and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        
        voiceList = voice.members
        memberList = []
        teamList = []
        output = ''
        #voiceList:discord.VoiceChannel = '<#542558448194289666>'
        for i in range(len(voiceList)):
            #print (voiceList[i].name)
            memberList.append(voiceList[i].name)
        chosenOne = ""
        # for i in range(int(teams)):
        #     output += '**Team {}**\n'.format(str(i+1))
        #     if (len(memberList)==0):
        #         break
        #     for j in range(int(members)):
                # chosenOne = random.choice(memberList)
                # output += '{}\n'.format(chosenOne)
                # memberList.remove(chosenOne)
                # if (len(memberList)==0):
                #     break

        # CREATE EDGE CASE FOR 1  TEAM
        for i in range(int(teams)):
            teamList.append([])

        for i in range(int(members)):
            for j in range(int(teams)):
                if (len(memberList)==0):
                    chosenOne ="*Empty*"
                else:
                    chosenOne = random.choice(memberList)
                    memberList.remove(chosenOne)
                teamList[j].append(chosenOne+'\n')
                

        for i in range(len(teamList)):
            output += '**Team {}**\n'.format(str(i+1))
            for j in range(len(teamList[i])):
                output += teamList[i][j]
            output += '\n'

        #print (teamList)
        await context.send(output)
        return



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
        await context.send ('```Currently disabled```')
        return
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this```')
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
        global gamesList
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

        gameOutput += "**\nUse \'info #\' for more details**"
        #embed = discord.Embed(title="All the games", color=0xDBC4C4)
        #if context.author.id in gamesList:
        
        for i in range (len(gamesList)):
            if gamesList[i][0] == context.author.id:
                del gamesList[i]
                
        gamesList.append([context.author.id,datetime.now(),games])
        embed.add_field(name="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", value=gameOutput, inline=False)
        await context.send(embed=embed)
        return

    @client.command(name='info',
                        description="Pebble will give you information on a game from the list",
                        brief="Pebble will give you information on a game from the list",
                        pass_context=True)
    async def whatGame(context, number:int):
        global gamesList
        hasIt = False
        for i in range (len(gamesList)):
            if gamesList[i][0] == context.author.id:
                gameList = gamesList[i][2]
                hasIt = True

        if (not hasIt):
            await context.send("*Pebble sees you have no recent list and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        

        total = len(gameList)
        if (number>total or number<1):
            await context.send("*Pebble deems your choice invalid and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        number -= 1
        nameFound = gameList[number][1]
        descriptionFound = gameList[number][2]
        urlFound = gameList[number][3]

        embed = discord.Embed(title=nameFound,description = descriptionFound,url = urlFound)
        await context.send(embed=embed)
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

    #Overlays a gif over a targetted user's avatar
    @client.command(name='flatten',
                description="Pebble will sit on a person of your choice",
                brief="Pebble will sit",
                pass_context=True)
    async def flatten(context,target:discord.User):
        response = requests.get(target.avatar_url)

        #random.seed(target.id)
        result = random.randint(1,4)

        img = Image.open(BytesIO(response.content))
        img = img.resize((256,50))

        sign = Image.open("PebbleOptions\\{}.png".format(str(result))).convert('RGBA')
        avatar = img.copy().convert('RGBA')
        avatar.paste(sign,(0,0), mask = sign)

        output = Image.new('RGBA',(256,256),(0, 0, 0, 0))
        output.paste(avatar,(0,226), mask = avatar)
        output.paste(sign,(0,0), mask = sign)
        output = output.resize ((180,180))
        output.save('squashed.png')
        
        await context.send("*Pebble sits on {}*".format(target.name))
        await context.send(file=discord.File('squashed.png'))
        return

    #Overlays a gif over a targetted user's avatar
    # @client.command(name='resize',
    #             description="Pebble will take an image of your choice and resize it",
    #             brief="Pebble will take an image of your choice and resize its",
    #             pass_context=True)
    # async def resize(context,imageType, imageUrl, width, height):
    #     if (not context.message.author.guild_permissions.administrator):
    #         await context.send ('```You do not have permission to use this```')
    #         return
    #     size = (int(width),int(height))
    #     if (size[0] > 300 or size[1] > 300):
    #         await context.send("*Pebble deems resolution is too big and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
    #         return

    #     response = requests.get(imageUrl)
    #     img = Image.open(BytesIO(response.content))
        

    #     #print(Image.MIME[img.format])
    #     #final.save('out.gif','GIF',save_all=True, append_images= output, optimize=True, duration=70, loop=0, transparency = 0, disposal = 2)
    #     if (imageType == 'png'):
    #         img = img.resize(size)
    #         img.save('resize.{}'.format('png'))
    #         await context.send(file=discord.File('resize.{}'.format('png')))
    #     elif (imageType == 'gif'):
    #         # Get sequence iterator
    #         frames = ImageSequence.Iterator(img)

    #         # Wrap on-the-fly thumbnail generator
    #         def thumbnails(frames):
    #             for frame in frames:
    #                 thumbnail = frame.copy()
    #                 thumbnail.thumbnail(size)
    #                 yield thumbnail

    #         frames = thumbnails(frames)

    #         # Save output
    #         om = next(frames) # Handle first frame separately
    #         om.info = img.info # Copy sequence info
    #         om.save("resize.gif", save_all=True, append_images=list(frames), loop = 0)         
    #         await context.send(file=discord.File('resize.{}'.format('gif')))   
    #     else:
    #         await context.send("*Pebble deems your image type invalid and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
    #         return
    #     return
    

    #sign
    @client.command(name='sign',
                    description="Select a character and a message in \"\" ",
                    brief="Pebble forces a character to hold a sign",
                    pass_context=True)
    async def messageToggle(context, colorChoice, message):
        if (len(message)>75):
            await context.send("*Pebble deems your message too long and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return

        sign = Image.open("AmongUs\\Sign.png").convert('RGBA')
        player = Image.open("AmongUs\\{}.png".format(colorChoice)).convert('RGBA')
        player = player.resize ((256,256))
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