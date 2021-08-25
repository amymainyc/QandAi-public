from discord.ext import commands
import discord
import json
from loguru import logger
from datetime import date
from utils.firebase import *
from utils.nlp import *



with open('data/config.json') as d:
    config = json.load(d)



class Answer(commands.Cog):



    def __init__(self, client):
        self.client = client
        self.db = Firebase()
        self.nlp = NLP()



    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Checking messages in questions channels for matches.
        """
        msg = message.content
        if "?" in msg:
            questionData = self.db.getQA()
            for guildID in questionData:
                channelID = str(message.channel.id)
                if channelID in questionData[guildID]:
                    channel = self.client.get_channel(channelID)
                    questionData = questionData[guildID][channelID]
                    if questionData != [{"placeholder": "placeholder"}]:
                        similar = []
                        for qa in questionData:
                            keywordSimilarity = self.nlp.getKeywordSimilarity(qa["k"], msg)
                            if keywordSimilarity > 0.5:
                                similarity = self.nlp.getOverallSimilarity(qa["q"], msg)
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



def setup(client):
    client.add_cog(Answer(client))