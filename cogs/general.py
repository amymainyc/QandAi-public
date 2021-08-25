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
        if isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.send("```You are missing required arguments! Check !help for usage instructions.```")
        if isinstance(exception, commands.BadArgument):
            return await ctx.send("```Invalid arguments! Check !help for usage instructions.```")
        if isinstance(exception, commands.TooManyArguments):
            return await ctx.send("```Too many arguments! Check !help for usage instructions.```")
        else:
            logger.exception(exception)
            return await ctx.send("```An error occurred while performing this action. Please contact Moonflower#8861.```")



    @commands.command()
    async def help(self, ctx):
        """
        Help command.
        """
        embed = discord.Embed(
            title="Slingshot Bot's Commands (s!)"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(
            name="**s!help**",
            value="Responds with this message!",
            inline=False
        )
        embed.add_field(
            name="**s!addchannel**",
            value="Add a channel for the bot to watch. \n`(server admin only)`",
            inline=False
        )
        embed.add_field(
            name="**s!removechannel**",
            value="Remove a channel from the bot's watch list. \n`(server admin only)`",
            inline=False
        )
        embed.add_field(
            name="**s!addqa**",
            value="Add a question and answer that the bot will look out for. \n`(server admin only)`",
            inline=False
        )
        embed.add_field(
            name="**s!removeqa**",
            value="Remove a question and answer that the bot will look out for. \n`(server admin only)`",
            inline=False
        )
        embed.add_field(
            name="**s!viewqa**",
            value="Sends the API link to view the question/answer database. \n`(server admin only)`",
            inline=False
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {str(date.today().strftime('%m/%d/%Y'))}", icon_url=ctx.author.avatar_url)
        await ctx.message.reply(embed=embed)
    


def setup(client):
    client.add_cog(General(client))
