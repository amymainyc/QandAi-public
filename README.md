## 🚀 Slingshot Bot
A discord bot that checks for commonly asked questions and answers them (made with [discord.py](https://discordpy.readthedocs.io/en/stable/api.html#) and [spaCy](https://spacy.io/)).

### Setup
Invite the bot to the server using [this link](https://discord.com/oauth2/authorize?client_id=843968680680488980&scope=bot&permissions=8). This bot will only work on the official Slingshot server.
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

#### Hosting
This bot is hosted for free on Heroku but if you'd like to run a version of it on your machine, follow the following instructions.
<br>

```
> pip install -r requirements.txt 
> python3 bot.py
```