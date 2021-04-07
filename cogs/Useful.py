import discord
import requests
import os
import math
import random
from io import BytesIO
from PIL import Image, ImageSequence
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from main import*
from datetime import datetime,timedelta

clientReference = client

class Useful(commands.Cog):

    description = "Pebble's commands that will prove useful to the user"

    def __init__(self, client):
        self.client = client
        global clientReference
        clientReference = client

    @commands.Cog.listener()
    async def on_ready(self):
        reminder.start()
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
        if (size[0] > 2000 or size[1] > 2000):
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
        characterList = (os.listdir("Assets/Sign/"))
        output = ''
        characterList.remove('sign.png')
        for i in range(len(characterList)):
            if ".png" in characterList[i]:
                output += "{}\n".format(characterList[i].replace('.png',''))
        if output == '':
            output = 'No Files'
        await context.send("```{}```".format(output))
        return

    @commands.command(name='HDEmojiList',
                    description="Pebble will show all the choices for the sign command",
                    brief="Pebble will show all the choices for the sign command",
                    pass_context=True,
                    aliases =['emojilist'])
    async def HDEmojiList(self, context):
        characterList = (os.listdir("Assets/HDEmoji/"))
        characterList = characterList.sort()
        output = ''
        for i in range(len(characterList)):
            if ".png" in characterList[i]:
                output += "{}\n".format(characterList[i].replace('.png',''))
            elif ".gif" in characterList[i]:
                output += "{}\n".format(characterList[i].replace('.gif',''))
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
        type = type.lower()
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
            output = ['**#. Name : ID : People in Call**\n']
        elif (type == 'text'):
            output = ['**#. Name : ID : People with Accessed**\n']
        elif (type == 'all'):
            output = ['**#. Name : ID : People with Accessed : Type**\n']


        if (type == 'voice' or type =='text'):
            for i in range(len(voiceChanneList)):
                if (len(output[-1])>1900):
                    output.append('')
                output[-1] += "{}. {} : {} : {}\n".format(i+1,voiceChanneList[i][2],voiceChanneList[i][0],len(voiceChanneList[i][3]))
        elif (type == 'all'):
            for i in range(len(voiceChanneList)):
                if (len(output[-1])>1900):
                    output.append('')
                output[-1] += "{}. {} : {} : {} : {}\n".format(i+1,voiceChanneList[i][2],voiceChanneList[i][0],len(voiceChanneList[i][3]),voiceChanneList[i][1])

        for i in output:
            await context.send(i)
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

    
    @commands.command(name='truecolor',
                description="Pebble will give a random color based on your user id",
                brief="Pebble will give a random color based on your user id",
                pass_context=True)
    async def truecolor(self, context, target:discord.User):
        random.seed(target.id)
        r = random.randint(0,255)
        random.seed(target.id-255)
        g = random.randint(0,255)
        random.seed(target.id+255)
        b = random.randint(0,255)
        im = Image.new(mode = "RGB", size = (25, 25), color = (r,g,b))
        pixel = im.save('simplePixel.png') 
        await context.send("#{:02x}{:02x}{:02x}".format(r,g,b),file=discord.File('simplePixel.png'))


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
        
    #Send user the first Google result
    @commands.command(name='google',
                description="Pebble will give you the first link of your Google search",
                brief="Pebble will give you the first link of your Google search",
                pass_context=True)
    async def google(self, context,*, search):
        #search = search.replace(" ","+")
        embed = discord.Embed(title=search, url="https://www.google.com/search?q={}&btnI".format(search.replace(" ","+")))
        await context.send(embed=embed)
        return

    @commands.command(name='colorlist',
                description="Pebble will print out all the colors of the roles",
                brief="Pebble will print out all the colors of the role",
                pass_context=True)
    async def colorList(self, context):  
        colorArr = []
        countArr = []
        nameArr = []
        for i in context.message.author.guild.roles:
            if i.color in colorArr:
                countArr[colorArr.index(i.color)] += 1
                nameArr[colorArr.index(i.color)].append (i.name)
            else:
                colorArr.append(i.color)
                countArr.append(1)
                nameArr.append([])
                if (i.name=="@everyone"):
                    nameArr[-1].append('everyone')
                else:
                    nameArr[-1].append(i.name)

        # output = ''

        # for i in range(len(colorArr)):
        #     output += (str(nameArr[i]) + " "+ str(colorArr[i]) +" "+ str(countArr[i]) + '\n')

        # cycles = None
        # if (len(output)>2000):
        #     cycles = math.ceil(len(output)/2000) 
        #     for i in range (cycles):
        #         await context.send(output[0+(i*2000):1999+(i*2000)])
        # else:
        #     await context.send(output)

        output=[]
        output.append('')
        for i in range(len(colorArr)):
            if (len(output[-1])>1900):
                output.append('')
            output[-1] += (str(nameArr[i]) + " : "+ str(colorArr[i]) +" : "+ str(countArr[i]) + 'x\n')
        for i in output:
            await context.send(i)
        

        return

    #Will reminder the user after a specificied amount of time
    @commands.command(name='remind',
                description="Pebble will remind you about something",
                brief="Pebble will remind you about something",
                pass_context=True)
    async def remind(self, context, targetToRemind, timeAmount, timeType, *, message):  
        now = datetime.now()
        timeType = timeType.lower()
        try:
            timeAmount = int(timeAmount)
        except:
            await context.send("Invalid amount of time")
            return

        if (timeType == 'sec' or timeType == 'second' or timeType == "seconds"):
            timeToRemind = now + timedelta(0,timeAmount)
        elif (timeType == 'min' or timeType == 'minute' or timeType == "minutes"):
            timeToRemind = now + timedelta(0,0,0,0,timeAmount)
        elif (timeType == 'hour' or timeType == 'hours'):
            timeToRemind = now + timedelta(0,0,0,0,0,timeAmount)
        elif (timeType == 'day' or timeType == 'days'):
            timeToRemind = now + timedelta(timeAmount)
        else:
            await context.send("Wrong Time Type")
            return

        cur, conn = getConnect()
        cur.execute('INSERT INTO reminders VALUES ({},{},{},{},{})'.format('\''+str(context.message.author.id)+'\'', '\''+targetToRemind+'\'','\''+str(timeToRemind)+'\'', '\''+message+'\'', '\''+str(context.message.channel.id)+'\''))
        conn.commit()
        conn.close()
        
        await context.send("Pebble will remind you when it is time")
        return

    # @commands.command(name='remindat',
    #             description="Pebble will remind you about something",
    #             brief="Pebble will remind you about something",
    #             pass_context=True)
    # async def remindAt(self, context, targetToRemind, timeToRemind, *, message):  
    #     print(context.message.created_at)
    #     newTime = context.message.created_at + timedelta(0,3)
    #     print(newTime)
    #     return

#Set this as an SQL database to grab all the ones I need

    @commands.command(name='changemycolor',
                        description="Pebble will show all the choices for the sign command",
                        brief="Pebble will show all the choices for the sign command",
                        pass_context=True,
                        aliases =['cmc'],
                        hidden = True)
    async def changemycolor(self, context,hue):
            match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hue) #Checks for valid hex color code
            if not match:
                await context.send('Invalid Hex Color Code')
                return
     
            user = context.author
            guild = context.guild
            role = ''
            for i in context.message.author.guild.roles:
                if i.name == str(user.id):
                    role = i
            if not role:
                role = await guild.create_role(name="{}".format(user.id),colour=discord.Colour(0xffffff))
                total = len(context.message.author.guild.roles)
                await user.add_roles(role)
                await role.edit(position=total-2)
            await role.edit(color=int('0x'+hue,0))
            await context.send('Pebble has changed your color')
            return
    
            
    @commands.command(name='role',
                        description="Pebble will give or take away the role of your choice",
                        brief="Pebble will give or take away the role of your choice",
                        pass_context=True,
                        hidden=True)
    async def role(self, context,choice):
        choice = choice.lower()
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute("SELECT * from roles where command = '{}'".format(choice))
        role = cur.fetchall()
        conn.close()
        if not role:
            await context.send("Pebble deems your role choice invalid")
            return

        roleID = role[0][0]
        member = context.message.author
        role = get(member.guild.roles, id=int(roleID))
        hasTheRole = False
        for i in context.message.author.roles:
                if i.name == role.name:
                    hasTheRole = True
        if hasTheRole:
            await discord.Member.remove_roles(member, role)
            await context.send("Pebble has taken away from you the role, {}".format(role.name))
        else:
            await discord.Member.add_roles(member, role)
            await context.send("Pebble has given you the role, {}".format(role.name))
       
    @commands.command(name='uid',
                description="Pebble will add your Genshin Impact UID to the server list",
                brief="Pebble will add your Genshin Impact UID to the server list",
                pass_context=True)
    async def uid(self, context, uid, name):
        member = context.message.author
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute("select * from genshin where id = \'{}\' AND server = \'{}\'".format(member.id,member.guild.id))
        result = cur.fetchall()
        print (result)
        if not result:
            cur.execute('INSERT INTO genshin VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(member.id,uid,name,member.guild.id,member))
            conn.commit()
            await context.send("Pebble has added your UID to the Genshin Impact List")
        else:
            cur.execute("UPDATE genshin SET uid = \'{}\', name = \'{}\', username = \'{}\' WHERE id = \'{}\' AND server = \'{}\' ".format(uid,name,member,member.id,member.guild.id))
            conn.commit()
            await context.send("Pebble has updated your UID and Name in the List")
        conn.close()

        return

    @commands.command(name='uidlist',
                description="Pebble will print out the server's list of UID for Genshin Impact",
                brief="Pebble will print out the server's list of UID for Genshin Impact",
                pass_context=True)
    async def uidlist(self, context):
        member = context.message.author
        cur, conn = getConnect()
        cur = conn.cursor()
        cur.execute("SELECT * from genshin WHERE server = \'{}\'".format(member.guild.id))
        result = cur.fetchall()
        conn.close()
        if not result:
            await context.send("Pebble sees there are no UIDs in this server")
        else:
            output = 'UID LIST\n'
            output += 'User : UID : In-Game Name\n'
            for i in range(len(result)):
                output += "{} : {} : {}\n".format(result[i][4],result[i][1],result[i][2])
        await context.send("```{}```".format(output))

    @commands.command(name='genshininfo',
                description="Pebble will give you an info card for the character",
                brief="Pebble will give you an info card for the character",
                pass_context=True,
                aliases=['gi'])
    async def genshininfo(self, context, character):     
        character = character.lower()
        await context.send(file=discord.File("Assets/Genshin/Characters/{}.jpg".format(character)))
    
    @commands.command(name='genshininfolist',
                    description="Pebble will show all the choices for the genshininfo command",
                    brief="Pebble will show all the choices for the genshininfo command",
                    pass_context=True,
                    aliases=['gil'])
    async def genshininfolist(self, context):
        characterList = (os.listdir("Assets/Genshin/Characters/"))
        output = ''
        for i in range(len(characterList)):
            if ".jpg" in characterList[i]:
                output += "{}\n".format(characterList[i].replace('.jpg','').title())
        if output == '':
            output = 'No Files'
        await context.send("```{}```".format(output))
        return

      

    @commands.command(name='genshinadventurerank',
                    description="Pebble will calculate how much exp you need to get to your Adventure Rank Goal",
                    brief="Pebble will calculate how much exp you need to get to your Adventure Rank Goal",
                    pass_context=True,
                    aliases=['gar'])
    async def genshinadventurerank(self, context, currentAdventureRank:int, currentAdventureExp: int, targetedAdventureRank: int):
        adventureRankChart = [0,375,500,625,725,850,950,1075,1175,1300,1425,1525,1650,1775,1875,2000,2375,2500,2625,2775,2825,3425,
        3725,4000,4300,4575,4875,5150,5450,5725,6025,6300,6600,6900,7175,7475,7750,8050,8325,8625,10550,11525,12475,13450,14400,15350,16325,17275,
        18250, 19200, 26400, 28800, 31200, 33600, 36000, 232350] #AR 50

        max = len(adventureRankChart)
        if currentAdventureRank >= targetedAdventureRank:
            await context.send('Pebble says you cannot go backwards in Adventure Ranks!')
            return
        elif targetedAdventureRank > max:
            await context.send('Pebble does not how much experience is required for that rank yet')
            return
        totalExp = currentAdventureExp
        for i in range(currentAdventureRank):
            totalExp += adventureRankChart[i]

        expNeeded = -(currentAdventureExp)
        for i in range(currentAdventureRank, targetedAdventureRank):
            expNeeded += adventureRankChart[i]

        resin = math.ceil((expNeeded/100)*20)

        
        await context.send('```Total Current Adventure Rank EXP: {}\nCurrent Adventure Rank: {}\nTargeted Adventure Rank: {}\nAdventure Rank EXP Required: {}\nResin Required: {}```'.format(totalExp, currentAdventureRank, targetedAdventureRank, expNeeded, resin))

    @commands.command(name='advancedgenshinadventurerank',
                    description="Pebble will calculate how much exp you need to get to your Adventure Rank Goal",
                    brief="Pebble will calculate how much exp you need to get to your Adventure Rank Goal",
                    pass_context=True,
                    aliases=['agar'])
    async def advancedgenshinadventurerank(self, context, currentAdventureRank:int, currentAdventureExp: int, targetedAdventureRank: int, resinrefills: int):
        adventureRankChart = [0,375,500,625,725,850,950,1075,1175,1300,1425,1525,1650,1775,1875,2000,2375,2500,2625,2775,2825,3425,
        3725,4000,4300,4575,4875,5150,5450,5725,6025,6300,6600,6900,7175,7475,7750,8050,8325,8625,10550,11525,12475,13450,14400,15350,16325,17275,
        18250, 19200, 26400, 28800, 31200, 33600, 36000, 232350] #AR 50

        max = len(adventureRankChart)
        if currentAdventureRank >= targetedAdventureRank:
            await context.send('Pebble says you cannot go backwards in Adventure Ranks!')
            return
        elif targetedAdventureRank > max:
            await context.send('Pebble does not how much experience is required for that rank yet')
            return
        totalExp = currentAdventureExp
        for i in range(currentAdventureRank):
            totalExp += adventureRankChart[i]

        expNeeded = -(currentAdventureExp)
        for i in range(currentAdventureRank, targetedAdventureRank):
            expNeeded += adventureRankChart[i]

        resin = math.ceil((expNeeded/100)*20)

        days = math.ceil(expNeeded / ((((180+(60*resinrefills))/20)*100)+1500))


        
        
        await context.send('```Total Current Adventure Rank EXP: {}\nCurrent Adventure Rank: {}\nTargeted Adventure Rank: {}\nAdventure Rank EXP Required: {}\nResin Required: {}\nDays: {}```'.format(totalExp, currentAdventureRank, targetedAdventureRank, expNeeded, resin,days))





@tasks.loop(seconds=1)
async def reminder():
    cur, conn = getConnect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM reminders')
    user = cur.fetchall()
    now = datetime.now()

    for i in user:
        if ((datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S.%f') - now).total_seconds() <= 0 ):
            channel = clientReference.get_channel(int(i[4]))
            await channel.send("Reminder for {} : {}".format(i[1], i[3]))
            cur.execute ('DELETE FROM reminders WHERE "ID" = \'{}\' AND "timestamp" =\'{}\''.format(i[0],i[2]))
            conn.commit()
            #print ('DELETE FROM reminders WHERE "ID" = \'{}\' AND "timestamp" =\'{}\''.format(i[0],i[2]))
    conn.close()
    return


def setup(client):
    client.add_cog(Useful(client))

