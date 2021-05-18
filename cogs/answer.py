from discord.ext import commands
import discord
import json
from loguru import logger
import spacy
from datetime import date



nlp = spacy.load("en_core_sci_md")

with open('config.json') as d:
    config = json.load(d)



class Answer(commands.Cog):



    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_message(self, message):
        # checking messages in questions channel
        channelID = config["channel"]
        if message.channel.id == channelID:
            m = message.content
            if "?" in m:
                channel = self.client.get_channel(channelID)
                with open("questions.json") as f:
                    questionData = json.load(f)["q&a"]
                mostSimilar = {}
                mostSimilarNum = 0
                for q in questionData:
                    question = q["question"]
                    keywordSimilarity = self.getKeywordSimilarity(question, m)
                    if keywordSimilarity > 0.5:
                        similarity = self.getOverallSimilarity(question, m)
                        if similarity > mostSimilarNum:
                            mostSimilarNum = similarity
                            mostSimilar = q
                if mostSimilarNum > 0.5:
                    question = mostSimilar["question"]
                    answer = mostSimilar["answer"]
                    embed = discord.Embed(
                        title="Thanks for your interest in Slingshot!",
                        description="Your question is similar to the previously answered question below. If this is irrelevant, feel free to disregard this message."
                    )
                    embed.add_field(name=f"**Q: **{question}", value=f"**A: **{answer}", inline=False)
                    embed.set_footer(text=f"{message.guild.name} • {str(date.today().strftime('%d/%m/%Y'))}", icon_url=self.client.user.avatar_url)
                    await channel.send(embed=embed)
            


    def getKeywords(self, question):
        return nlp(question).ents



    def getKeywordSimilarity(self, q1, q2):
        k1 = self.getKeywords(q1)
        match = 0
        for keyword in k1:
            if str(keyword).lower() in q2.lower():
                match += 1
        if len(k1) > 0:
            return match / len(k1)
        else:
            return 0



    def getOverallSimilarity(self, q1, q2):
        q1 = nlp(q1)
        q2 = nlp(q2)
        return q2.similarity(q1)



def setup(client):
    client.add_cog(Answer(client))