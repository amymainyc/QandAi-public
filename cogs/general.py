from discord.ext import commands
import discord
import json
from loguru import logger
import aiohttp
import base64
import asyncio
import spacy
import scispacy



with open('config.json') as d:
    config = json.load(d)



class General(commands.Cog):



    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        # bot startup tasks
        channelID = config["channel"]
        channelName = self.client.get_channel(channelID).name
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"#{channelName}")
        await self.client.change_presence(activity=activity)
        await asyncio.sleep(43200)
        await self.pushToGitHub()



    @commands.Cog.listener()
    async def on_command_error(self, ctx : commands.Context, exception):
        # error handling
        if isinstance(exception, commands.MissingRequiredArgument):
            return await ctx.send("```You are missing required arguments! Check !help for usage instructions.```")
        if isinstance(exception, commands.BadArgument):
            return await ctx.send("```Invalid arguments! Check !help for usage instructions.```")
        if isinstance(exception, commands.TooManyArguments):
            return await ctx.send("```Too many arguments! Check !help for usage instructions.```")
        else:
            logger.exception(exception)



    async def pushToGitHub(self):
        # push files to GitHub
        logger.info("Pushing latest files to GitHub.")
        filenames = ["config.json"]
        for filename in filenames: 
            try:
                token = config["githubOath"]
                repo = "amymainyc/slingshot-bot"
                branch = "main"
                url = "https://api.github.com/repos/" + repo + "/contents/" + filename

                base64content = base64.b64encode(open(filename, "rb").read())

                async with aiohttp.ClientSession() as session:
                    async with session.get(url + '?ref=' + branch, headers={"Authorization": "token " + token}) as data:
                        data = await data.json()
                sha = data['sha']

                if base64content.decode('utf-8') + "\n" != data['content']:
                    message = json.dumps(
                        {"message": "Automatic data update.",
                            "branch": branch,
                            "content": base64content.decode("utf-8"),
                            "sha": sha}
                    )

                    async with aiohttp.ClientSession() as session:
                        async with session.put(
                            url, data=message, headers={"Content-Type": "application/json", "Authorization": "token " + token}
                        ) as resp:
                            print(resp)

            except Exception as e:
                logger.exception(e)



    @commands.command()
    async def gitPush(self, ctx):
        # push files to GitHub
        if ctx.author.id == 430079880353546242:
            await ctx.send("Pushing latest files to GitHub.")
            await self.pushToGitHub()



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setChannel(self, ctx):
        if ctx.guild.id == config["guild"]:
            def whosent(m):
                return m.author == ctx.author
            
            await ctx.send("```Please reply with the channel id for the questions channel:```")
            try:
                channelID = await self.client.wait_for('message', check=whosent, timeout=300)
                channelID = int(channelID.content)
            except asyncio.TimeoutError:
                return await ctx.send('You took too long \:( Please try the command again.')
            
            channel = self.client.get_channel(channelID)
            message = await ctx.send(f"```Please react to confirm that you would like this bot to check over #{channel.name}```")
            await message.add_reaction("✅")

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == "✅"
            try: 
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=300)
                await message.clear_reactions()
                config["channel"] = channelID
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)
                await message.edit(content="```The questions channel has been set.```")
            except asyncio.TimeoutError:
                return await message.clear_reactions()



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addQA(self, ctx):
        if ctx.guild.id == config["guild"]:
            def whosent(m):
                return m.author == ctx.author
            
            await ctx.send("```Please reply with the question you would like to add:```")
            try:
                question = await self.client.wait_for('message', check=whosent, timeout=300)
                question = question.content
            except asyncio.TimeoutError:
                return await ctx.send('You took too long \:( Please try the command again.')
            
            await ctx.send("```Please reply with the answer to this question:```")
            try:
                answer = await self.client.wait_for('message', check=whosent, timeout=300)
                answer = answer.content
            except asyncio.TimeoutError:
                return await ctx.send('You took too long \:( Please try the command again.')

            text = f"```Please react with a check to confirm that you would like to add this: \nQuestion: {question} \nAnswer: {answer}```"
            message = await ctx.send(text)
            await message.add_reaction("✅")

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == "✅"
            try: 
                reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=300)
                await message.clear_reactions()
                data = {"question": question, "answer": answer}
                with open("questions.json") as f:
                    questionData = json.load(f)
                questionData["q&a"].append(data)
                with open("questions.json", "w") as f:
                    json.dump(questionData, f, indent=4)
                await message.edit(content="```This question and answer has been added.```")
            except asyncio.TimeoutError:
                return await message.clear_reactions()


def setup(client):
    client.add_cog(General(client))