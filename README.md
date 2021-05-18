## 🚀 Slingshot Bot
A discord bot that checks for commonly asked questions using natural language processing and answers them. (made with [discord.py](https://discordpy.readthedocs.io/en/stable/api.html#) and [spaCy](https://spacy.io/)). Made for open-source sunday on the Slingshot Discord Server.

### Hosting
I could not host this bot on Heroku due to their memory limit. If you'd like to run a version of this bot on your machine, follow the instructions below.
<br>
- Open the "config.json" file and insert the bot token, client id, and guild id.
- Run the following commands in your terminal.
```
> pip install -r requirements.txt 
> python3 bot.py
```
<br>

### Setup
Invite the bot to the server using the link in "config.json". This bot will only work on the official Slingshot server.
<br>

Use `!setchannel` to select a channel for the bot to watch over.
<img src="https://i.imgur.com/OpgTkLy.png"><br>
<br>

Use `!addqa` to add questions and answers.
<img src="https://i.imgur.com/J3D370B.png"><br>
<br>

The bot will now answer questions in that channel!
<img src="https://i.imgur.com/lvbqM12.png"><br>
<img src="https://i.imgur.com/OcK7rxX.png"><br>

### Improvements
Given the time, I would:
- Host the bot
- Add a command to remove questions and answers
- Tweak/improve the NLP system to make it more accurate
