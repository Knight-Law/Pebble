import discord
import random
import textwrap
import requests
import re
import math
from discord.ext import commands
from PIL import Image, ImageColor, ImageDraw, ImageSequence, ImageFont
from io import BytesIO
from main import*

class Fun(commands.Cog):
    description = "Pebble's commands that will gift the user with entertainment"

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun Cog is good.')

    @commands.command(name='soulmate',
                    description="Pebble will see the compatibility between two people",
                    brief="Pebble will see the compatibility between two people",
                    pass_context=True)
    async def soulMate(self, context, target1:discord.User, target2:discord.User):
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
        
        embed = discord.Embed(title=heartString,description = " ")
        embed.add_field(name="Soulmate Results", value="{}".format(description), inline=False)
        await context.send(embed=embed)
        return

    #Take user's avatar and Pebble alter it to sit on the picture
    @commands.command(name='flatten',
                description="Pebble will sit on a person of your choice",
                brief="Pebble will sit on someone",
                pass_context=True)
    async def flatten(self,context,target:discord.User):
        response = requests.get(target.avatar_url)


        result = random.randint(1,4)

        img = Image.open(BytesIO(response.content))
        img = img.resize((256,50))

        sign = Image.open("Assets/PebbleOptions/{}.png".format(str(result))).convert('RGBA')
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

    @commands.command(name='sign',
                    description="Select a character and a message in \"\" ",
                    brief="Pebble forces a character to hold a sign",
                    pass_context=True)
    async def messageToggle(self, context, signChoice, *,message):
        if (len(message)>75):
            await context.send("*Pebble deems your message too long and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        signChoice = signChoice.lower()
        sign = Image.open("Assets/Sign/Sign.png").convert('RGBA')
        player = Image.open("Assets/Sign/{}.png".format(signChoice)).convert('RGBA')
        player = player.resize ((256,256))
        player.paste(sign,(0,0), mask = sign)

        draw = ImageDraw.Draw(player)
        font = ImageFont.truetype("arial.ttf", 16)
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

#Overlays a gif over a targetted user's avatar
    @commands.command(name='pet',
                description="Pebble will give a friendly petting to a user of your choice",
                brief="Pebble gives pets",
                pass_context=True)
    async def printColor(self, context,target:discord.User):
        response = requests.get(target.avatar_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((50,50))

        gifFrames = 10
        avatar = Image.new('RGBA',(100,100),(255, 105, 180, 255))
        avatar.paste (img.convert('RGBA'),(34,21))

        output = []

        for x in range(gifFrames):
            output.append(avatar.copy())
            im = Image.open("Assets/Hands/{}.png".format(str(x+1))).convert('RGBA')
            output[x].paste(im,(0,0), mask = im)

        final = output[0]
        final.save('out.gif','GIF',save_all=True, append_images= output, optimize=True, duration=70, loop=0, transparency = 0, disposal = 2)
        await context.send(file=discord.File('out.gif'))
        return

    #Grabs a random response 
    @commands.command(name='showme',
                    description="Pebble will answer a question by shattering itself",
                    brief="Pebble will answer your questions",
                    pass_context=True,
                    aliases =['sm'])
    async def ballresponse(self, context):
        newMSG = await context.send(file=discord.File('Assets/PebbleOptions/PebbleShatter.gif'))#delete_after = 0.1)
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute('SELECT "response" FROM answers')
        user = cur.fetchall()
        m = re.search('\'(.+?)\'',str(random.choice(user)))
        if m:
           found = m.group(1)
        time.sleep(3)
        await newMSG.delete()
        await context.send("*Pebble shatters itself to reveal...*\n**{}**".format(found))
        return

    #Gets the current reaction of the targeted user  
    @commands.command(name='getreaction',
                description="See Pebble\'s reaction for the user",
                brief="Pebble will show you the reaction for the user",
                pass_context=True,
                aliases =['gr'])
    async def getReaction(self, context, target):
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

    #Gets the current message of the targeted user  
    @commands.command(name='getmessage',
                description="See Pebble\'s message for the user",
                brief="Pebble will show you the message for the user",
                pass_context=True,
                aliases =['gm'])
    async def getMessage(self, context, target):
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

    #Take user's avatar and multiple parameters to create a Yu-Gi-OH card 
    @commands.command(name="summon",
            description="Pebble will summon the target",
            brief = 'Pebble will summon the target',
            pass_context = True)
    async def summon(self, context, target:discord.User, *,effect):
        if (len(effect)>210):
            await context.send("*Pebble deems your message too long and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
        response = requests.get(target.avatar_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((199,201))

        random.seed(target.id)
        element = Image.open("Assets/Summon/{}.png".format(str(random.randint(1,6)))).convert('RGBA')
        card = Image.open("Assets/Summon/card.png").convert('RGBA')
        star = Image.open("Assets/Summon/star.png").convert('RGBA') 
        avatar = img.copy().convert('RGBA')
        

        random.seed(target.id+1)
        attack = str(100*random.randint(0,50))
        random.seed(int(str(target.id+1)[::-1]))
        defense = str(100*random.randint(0,50))

        stars = math.floor((int(attack)+int(defense))/1000)
        if (target.id == 658872372140441602):
            stars = 11
            attack = '∞'
            defense = '∞'
            effect = 'Having this card in your deck automatically grants you victory'
            element = Image.open("Assets/Summon/pebble.png").convert('RGBA')
            #star = Image.open("Assets/Summon/pebble.png").convert('RGBA')
        

        card.paste(avatar,(38,89), mask = avatar)
        card.paste(element,(219,22), mask = element)


        draw = ImageDraw.Draw(card)
        nameFont = ImageFont.truetype("arial.ttf", 16)
        statFont = ImageFont.truetype("arial.ttf", 10)
        draw.text((28, 28),target.display_name,(0,0,0),font=nameFont)
        draw.text((146, 369),'ATK/{}'.format(attack),(0,0,0),font=statFont)
        draw.text((200, 369),'DEF/{}'.format(defense),(0,0,0),font=statFont)
        for i in range(stars):
            card.paste(star,(225+(i*-20),62), mask = star)

        h = 308
        w = 275 
        lines = textwrap.wrap(effect, width=45)
        y_text = h
        for line in lines:
            width, height = statFont.getsize(line)
            draw.text(((w - width) / 2, y_text), line, (0,0,0),font=statFont)
            y_text += height


        card.save('output.png')
        await context.send(file=discord.File('output.png'))



def setup(client):
    client.add_cog(Fun(client))

