from discord.ext import commands
import discord
import json
from loguru import logger
import asyncio
from utils.firebase import *
from utils.nlp import *



with open('data/config.json') as d:
    config = json.load(d)



class Setup(commands.Cog):



    def __init__(self, client):
        self.client = client
        self.db = Firebase()
        self.nlp = NLP()



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def viewQA(self, ctx):
        questionData = self.db.getQA()

        # check if questions channel has been set up
        guildID = str(ctx.guild.id)
        if not guildID in questionData:
            return await ctx.send("```You have not added a channel for me to watch. You can do so by running q!addchannel```")
        
        def whosent(m):
            return m.author == ctx.author
    
        try:
            # set the channel if needed
            if len(list(questionData[guildID])) > 1:
                await ctx.send("```You have more than one channel being watched in this server. Please reply with the ID of the channel you wish to view questions for.```")
                channelID = await self.client.wait_for('message', check=whosent, timeout=300)
                channelID = channelID.content
                if not channelID in questionData[guildID]:
                    return await ctx.send("```This channel has not been added to the database yet. Add it with q!addchannel and try this command again.```")
            else:
                channelID = list(questionData[guildID])[0]

        except asyncio.TimeoutError:
            return await ctx.send("```You took too long \:( Please try the command again.```")

        # send the API link
        await ctx.send(f"https://slingshot-bot-default-rtdb.firebaseio.com/qa/{guildID}/{channelID}.json")



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addChannel(self, ctx):
        """
        Adds channels to watch.
        """
        questionData = self.db.getQA()

        guildID = str(ctx.guild.id)

        def whosent(m):
            return m.author == ctx.author

        try:
            # get channel id
            await ctx.send("```Please reply with the channel id for a channel to watch:```")
            channelID = await self.client.wait_for('message', check=whosent, timeout=300)
            channelID = channelID.content
            try:
                channel = ctx.guild.get_channel(int(channelID))
                if channel is None:
                    return await ctx.send("```Invalid channel ID. Please check and try again.```")
            except:
                return await ctx.send("```Invalid channel ID. Please check and try again.```")

        except asyncio.TimeoutError:
            return await ctx.send("```You took too long \:( Please try the command again.```")

        # confirm channel
        message = await ctx.send(f"```Please react to confirm that you would like this bot to watch #{channel.name} in {ctx.guild.name}.```")
        await message.add_reaction("✅")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id

        try: 
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=300)
            await message.clear_reactions()

            # add channel and guild to database
            if not guildID in questionData:
                questionData.update(
                    {
                        guildID : {
                            channelID : [{"placeholder": "placeholder"}]    
                        }
                    }
                )
            else:
                if not channelID in questionData[guildID]:
                    questionData[guildID][channelID] = [{"placeholder": "placeholder"}]  
                else:
                    return await message.edit(content="```This channel has already been added previously.```")
            self.db.updateQA(questionData)

            await message.edit(content="```The channel has been added.```")
        except asyncio.TimeoutError:
            return await ctx.send("```You took too long \:( Please try the command again.```")
            return await message.clear_reactions()



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeChannel(self, ctx):
        """
        Removes channels from watch list.
        """
        questionData = self.db.getQA()

        guildID = str(ctx.guild.id)

        def whosent(m):
            return m.author == ctx.author

        try:
            # get channel id
            await ctx.send("```Please reply with the channel id to remove from the bot's watch list:```")
            channelID = await self.client.wait_for('message', check=whosent, timeout=300)
            channelID = channelID.content
            try:
                channel = ctx.guild.get_channel(int(channelID))
                if channel is None:
                    return await ctx.send("```Invalid channel ID. Please check and try again.```")
            except:
                return await ctx.send("```Invalid channel ID. Please check and try again.```")

        except asyncio.TimeoutError:
            return await ctx.send("```You took too long \:( Please try the command again.```")

        # remove channel from the database
        if not guildID in questionData:
            return await ctx.send("```This channel is not in the database for this guild.```")
        if not channelID in questionData[guildID]:
            return await ctx.send("```This channel is not in the database for this guild.```")
        else:
            questionData[guildID].pop(channelID)
            if questionData[guildID] == {}:
                questionData.pop(guildID)

        self.db.updateQA(questionData)

        await ctx.send("```The channel has been removed.```")



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addQA(self, ctx):
        """
        Adds questions to the database.
        """
        questionData = self.db.getQA()

        # check if questions channel has been set up
        guildID = str(ctx.guild.id)
        if not guildID in questionData:
            return await ctx.send("```You have not added a channel for me to watch. You can do so by running q!addchannel```")
        
        def whosent(m):
            return m.author == ctx.author
    
        try:
            # set the question
            await ctx.send("```Please reply with the question you would like to add:```")
            question = await self.client.wait_for('message', check=whosent, timeout=300)
            question = question.content
        
            # set the answer
            await ctx.send("```Please reply with the answer to this question:```")
            answer = await self.client.wait_for('message', check=whosent, timeout=300)
            answer = answer.content
            
            # set the channel if needed
            if len(list(questionData[guildID])) > 1:
                await ctx.send("```You have more than one channel being watched in this server. Please reply with the ID of the channel you wish to associate this question and answer with.```")
                channelID = await self.client.wait_for('message', check=whosent, timeout=300)
                channelID = channelID.content
                if not channelID in questionData[guildID]:
                    return await ctx.send("```This channel has not been added to the database yet. Add it with !addchannel and try this command again.```")
            else:
                channelID = list(questionData[guildID])[0]
            try:
                int(channelID)
            except:
                return await ctx.send("```Invalid channel ID. Please check and try again.```")

        except asyncio.TimeoutError:
            return await ctx.send("```You took too long \:( Please try the command again.```")

        # confirmation message
        text = f"```Please react with a check to confirm that you would like to add this for #{self.client.get_channel(int(channelID))}.\n\nQuestion: {question}\n\nAnswer: {answer}```"
        message = await ctx.send(text)
        await message.add_reaction("✅")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id
        try: 
            reaction, user = await self.client.wait_for('reaction_add', check=check, timeout=300)
            await message.clear_reactions()

            # add question, answer, and keywords to database
            keywords = self.nlp.getKeywords(question)
            data = {"q": question, "a": answer, "k": keywords}
            questionData = self.db.getQA()
            
            if "placeholder" in questionData[guildID][channelID][0]:
                questionData[guildID][channelID] = []
            questionData[guildID][channelID].append(data)

            self.db.updateQA(questionData)

            await message.edit(content="```This question and answer has been added.```")
        except asyncio.TimeoutError:
            return await message.clear_reactions()



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeQA(self, ctx):
        """
        Removes questions from the database.
        """
        questionData = self.db.getQA()

        # check if questions channel has been set up
        guildID = str(ctx.guild.id)
        if not guildID in questionData:
            return await ctx.send("```This bot doesn't watch any channels in this guild.```")
        
        def whosent(m):
            return m.author == ctx.author
    
        try:
            # set the question
            await ctx.send("```Please reply with the question you would like to remove:```")
            question = await self.client.wait_for('message', check=whosent, timeout=300)
            question = question.content
        
            # set the channel if needed
            if len(list(questionData[guildID])) > 1:
                await ctx.send("```You have more than one channel being watched in this server. Please reply with the ID of the channel this question is associated with.```")
                channelID = await self.client.wait_for('message', check=whosent, timeout=300)
                channelID = channelID.content
                if not channelID in questionData[guildID]:
                    return await ctx.send("```This channel is not in the database.```")
            else:
                channelID = list(questionData[guildID])[0]

        except asyncio.TimeoutError:
            return await ctx.send("```You took too long \:( Please try the command again.```")

        # check if the question is there and remove it
        channelqa = questionData[guildID][channelID]
        if channelqa == [{"placeholder": "placeholder"}]:
            return await ctx.send("```There are no questions/answers added for this channel.```")
        for qa in channelqa:
            if qa["q"] == question:
                channelqa.remove(qa)
                questionData[guildID][channelID] = channelqa
                if channelqa == []:
                    questionData[guildID][channelID] = [{"placeholder": "placeholder"}]
                self.db.updateQA(questionData)
                await ctx.send("```Question has been removed from the database.```")
                return
        await ctx.send("```The question given is not in the database. If you need help finding the question, try !viewqa.```")



def setup(client):
    client.add_cog(Setup(client))
