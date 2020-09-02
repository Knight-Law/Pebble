import discord
import re
from discord.ext import commands
from main import*

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin Cog is good.')

    @commands.command(name='messagetoggle',
                    description="Flips the user\'s toggle for messages",
                    brief="Pebble flips the user\'s toggle for messages",
                    pass_context=True,
                    aliases =['mt'])
    async def messageToggle(self, context, target):
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
    @commands.command(name='reactiontoggle',
                    description="Flips the user\'s toggle for messages reactions",
                    brief="Pebble flips the user\'s toggle for messages reactions",
                    pass_context=True,
                    aliases =['rt'])
    async def reactToggle(self, context, target):
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
    @commands.command(name='changemessage',
                    description="Change Pebble\'s message of the targeted user",
                    brief="Pebble wants to change its message",
                    pass_context=True,
                    aliases =['cm'])
    async def changeMessage(self, context, target, message):
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
    @commands.command(name='changereaction',
                description="Change Pebble\'s reaction of the targeted user",
                brief="Pebble wants to change its reaction",
                pass_context=True,
                aliases =['cr'])
    async def changeReaction(self, context, target, message):
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


        
    #Adds a new game to the list
    @commands.command(name='newgame',
                description="Add a new game to Pebble\'s recommended games",
                brief="Pebble wants a new game",
                pass_context=True,
                aliases =['ng'])
    async def newGame(self, context, message):
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

def setup(client):
    client.add_cog(Admin(client))

