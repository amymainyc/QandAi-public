from discord.ext import commands
import discord
import json
from loguru import logger
import spacy
from datetime import date



nlp = spacy.load("en_core_sci_sm")

with open('data/config.json') as d:
    config = json.load(d)



class Answer(commands.Cog):



    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Checking messages in questions channels for matches.
        """
        with open("data/database.json") as f:
            questionData = json.load(f)
        for guildID in questionData:
            channelID = str(message.channel.id)
            if channelID in questionData[guildID]:
                msg = message.content
                if "?" in msg:
                    channel = self.client.get_channel(channelID)
                    questionData = questionData[guildID][channelID]
                    similar = []
                    for qa in questionData:
                        keywordSimilarity = self.getKeywordSimilarity(qa["k"], msg)
                        if keywordSimilarity > 0.5:
                            similarity = self.getOverallSimilarity(qa["q"], msg)
                            if similarity > 0.5:
                                similar.append(qa)
                    if similar:
                        embed = discord.Embed(
                            title="Hey there!",
                            description="Your question is similar to the previously answered questions below. If this is irrelevant, feel free to disregard this message."
                        )
                        embed.set_footer(text=f"{message.guild.name} • {str(date.today().strftime('%d/%m/%Y'))}", icon_url=self.client.user.avatar_url)
                        for qa in similar:
                            embed.add_field(name=f"**Q: **{qa['q']}", value=f"**A: **{qa['a']}", inline=False)
                        return await message.reply(embed=embed)
            


    def getKeywordSimilarity(self, keywords, message):
        match = 0
        for keyword in keywords:
            if str(keyword).lower() in message.lower():
                match += 1
        if len(keywords) > 0:
            return match / len(keywords)
        else:
            return 0



    def getOverallSimilarity(self, question, message):
        question = nlp(question)
        message = nlp(message)
        return message.similarity(question)



def setup(client):
    client.add_cog(Answer(client))