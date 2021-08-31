from discord.ext import commands
import discord
import json
from loguru import logger
from datetime import date
from utils.firebase import *



with open('data/config.json') as d:
    config = json.load(d)



class General(commands.Cog):



    def __init__(self, client):
        self.client = client
        self.db = Firebase()


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Bot startup tasts.
        """
        questionData = self.db.getQA()
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"over {len(list(questionData))} servers!")
        await self.client.change_presence(activity=activity)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        """
        Error handling.
        """
        if isinstance(exception, commands.CommandNotFound):
            return await ctx.send("```Command not found! Check q!help for usage instructions.```")
        if isinstance(exception, commands.MemberNotFound):
            return await ctx.send('```Invalid user! Make sure you are tagging the right user.```')
        if isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.send("```You are missing required arguments! Check q!help for usage instructions.```")
        if isinstance(exception, commands.BadArgument):
            return await ctx.send("```Invalid arguments! Check q!help for usage instructions.```")
        if isinstance(exception, commands.TooManyArguments):
            return await ctx.send("```Too many arguments! Check q!help for usage instructions.```")
        else:
            logger.exception(exception)
            return await ctx.send("```An error occurred while performing this action. Please contact Moonflower#8861.```")



    @commands.command()
    async def help(self, ctx):
        """
        Help command.
        """
        embed = discord.Embed(
            title="Q&Ai's Commands (q!)"
        )
        embed.add_field(
            name="**q!help**",
            value="Responds with this message!",
            inline=False
        )
        embed.add_field(
            name="**q!addchannel / q!removechannel**",
            value="Adds/removes a channel for the bot to watch. \n`(server admin only)`",
            inline=False
        )
        embed.add_field(
            name="**q!addqa / q!removeqa**",
            value="Adds/removes a question and answer pair that the bot will look out for. \n`(server admin only)`",
            inline=False
        )
        embed.add_field(
            name="**q!viewqa**",
            value="Sends the API link to view the question/answer database. \n`(server admin only)`",
            inline=False
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {str(date.today().strftime('%m/%d/%Y'))}", icon_url=ctx.author.avatar_url)
        await ctx.message.reply(embed=embed)
    


    @commands.command()
    async def invite(self, ctx):
        """
        Invite command.
        """
        await ctx.send(config["inviteLink"])



def setup(client):
    client.add_cog(General(client))
