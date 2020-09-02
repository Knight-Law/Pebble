import discord
import requests
import os
import math
from io import BytesIO
from PIL import Image, ImageSequence
from discord.ext import commands
from main import*

class Useful(commands.Cog):

    description = "Pebble's commands that will prove useful to the user"

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Useful Cog is good.')

    @commands.command(name='resize',
                description="Pebble will take an image of your choice and resize it",
                brief="Pebble will take an image of your choice and resize its",
                pass_context=True)
    async def resize(self, context,imageType, imageUrl, width, height):
        if (not context.message.author.guild_permissions.administrator):
            await context.send ('```You do not have permission to use this```')
            return
        size = (int(width),int(height))
        if (size[0] > 300 or size[1] > 300):
            await context.send("*Pebble deems resolution is too big and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return

        response = requests.get(imageUrl)
        img = Image.open(BytesIO(response.content))
        

        if (imageType == 'png'):
            img = img.resize(size)
            img.save('resize.{}'.format('png'))
            await context.send(file=discord.File('resize.{}'.format('png')))
        elif (imageType == 'gif'):
           
            frames = ImageSequence.Iterator(img)

            def thumbnails(frames):
                for frame in frames:
                    thumbnail = frame.copy()
                    thumbnail.thumbnail(size)
                    yield thumbnail

            frames = thumbnails(frames)

            # Save output
            om = next(frames) # Handle first frame separately
            om.info = img.info # Copy sequence info
            om.save("resize.gif", save_all=True, append_images=list(frames), loop = 0)         
            await context.send(file=discord.File('resize.{}'.format('gif')))   
        else:
            await context.send("*Pebble deems your image type invalid and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return
    

    @commands.command(name='signList',
                    description="Pebble will show all the choices for the sign command",
                    brief="Pebble will show all the choices for the sign command",
                    pass_context=True)
    async def files(self, context):
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

    @commands.command(name='allchannels',
                    description="Pebble will list all of the channels of type",
                    brief="Pebble will list all of the channels of type",
                    pass_context=True,
                    aliases =['ac'])
    async def allchannels(self, context, type):

        if (type != "text" and type != "voice" and type!= "all"):
            await context.send("*Pebble deems your mode choice invalid and rolls away*. <a:PebbleIconAnimation:746859796585513040>")
            return

        voiceChanneList = []
        if (type == 'voice' or type =='text'):
            for i in context.message.author.guild.channels:
                if (i.type.name == type):
                    voiceChanneList.append((i.id,i.type.name,i.name,i.members))
        else: 
            for i in context.message.author.guild.channels:
                if (i.type.name == 'text' or i.type.name == 'voice'):
                    voiceChanneList.append((i.id,i.type.name,i.name,i.members))
                    
        if (type == 'voice'):
            output = '**#. Name : ID : People in Call**\n'
        elif (type == 'text'):
            output = '**#. Name : ID : People with Accessed**\n'
        elif (type == 'all'):
            output = '**#. Name : ID : People with Accessed : Type**\n'

        if (type == 'voice' or type =='text'):
            for i in range(len(voiceChanneList)):
                output += "{}. {} : {} : {}\n".format(i+1,voiceChanneList[i][2],voiceChanneList[i][0],len(voiceChanneList[i][3]))
        elif (type == 'all'):
            for i in range(len(voiceChanneList)):
                output += "{}. {} : {} : {} : {}\n".format(i+1,voiceChanneList[i][2],voiceChanneList[i][0],len(voiceChanneList[i][3]),voiceChanneList[i][1])

        cycles = None
        if (len(output)>2000):
            cycles = math.ceil(len(output)/2000) 
            for i in range (cycles):
                await context.send(output[0+(i*2000):1999+(i*2000)])
        else:
            await context.send(output)
        return

    #Takes a hexcolor code and draw an image of the color
    @commands.command(name='color',
                description="Pebble will print a color from the hex color code given",
                brief="Pebble will print a color from the hex color code given",
                pass_context=True)
    async def printColor(self, context,hue):
        match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hue) #Checks for valid hex color code
        if match:
            im = Image.new(mode = "RGB", size = (25, 25), color = ('#{}'.format(hue)))
            pixel = im.save('simplePixel.png') 
            await context.send(file=discord.File('simplePixel.png'))
        else:
            await context.send('Invalid Hex Color Code')
        return

    #Pebble will randomly assign team from people currently connected in a voice channel
    @commands.command(name='select',
                description="Pebble will select your teams",
                brief="Pebble will select your teams",
                pass_context=True)
    async def select(self,context,voiceID, teams, members):
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
        for i in range(len(voiceList)):
            memberList.append(voiceList[i].name)
        chosenOne = ""

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

        await context.send(output)
        return


def setup(client):
    client.add_cog(Useful(client))

