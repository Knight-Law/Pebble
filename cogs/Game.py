import discord
import random
from discord.ext import commands
from main import*
from discord.ext import tasks
from datetime import datetime

gamesList = []

class Game(commands.Cog):

    description = "Pebble's commands related for game activities"

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Game Cog is good.')
        cleanUp.start()

  

    @commands.command(name='playwhat',
                    description="Pebble will decide a random game for you",
                    brief="Pebble will decide a random game for you",
                    pass_context=True,
                    aliases =['pw'])
    async def whatGame(self, context, gameType):
        cur, conn = getConnect()
        cur = conn.cursor()
        gameType = gameType.lower()

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



    #Outputs all the games 
    @commands.command(name='allgames',
                description="Pebble will display all the games it knows.",
                brief="Pebble will display all the games it knows.",
                pass_context=True,
                aliases =['ag'])
    async def allGames(self, context, gameType):
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
        
        for i in range (len(gamesList)):
            if gamesList[i][0] == context.author.id:
                del gamesList[i]
                
        gamesList.append([context.author.id,datetime.now(),games])
        embed.add_field(name="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", value=gameOutput, inline=False)
        await context.send(embed=embed)
        return

    @commands.command(name='info',
                        description="Pebble will give you information on a game from the list",
                        brief="Pebble will give you information on a game from the list",
                        pass_context=True)
    async def gameInfo(self, context, number:int):
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
        return

@tasks.loop(seconds=21)
async def cleanUp():
    global gamesList
    amountDeleted = 0
    copyList = gamesList.copy()
    i = 0
    for i in range(len(gamesList)):
        d1 = gamesList[i][1]
        d2 = datetime.now()
        d2 = d2-d1
        if (d2.total_seconds()>20):
            del copyList[i-amountDeleted]
    gamesList = copyList.copy()
    return

def setup(client):
    client.add_cog(Game(client))

