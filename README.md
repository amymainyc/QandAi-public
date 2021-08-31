## 🚀 Slingshot Bot
A discord bot that checks for previously answered questions using natural language processing and answers them (made with [discord.py](https://discordpy.readthedocs.io/en/stable/api.html#) and [spaCy](https://spacy.io/)). Made for open-source sunday on the Slingshot Discord Server. 

### Invite
You can invite this bot to your server using [this link](https://discord.com/oauth2/authorize?client_id=843968680680488980&scope=bot&permissions=85056)!

### Commands
<details>
<summary>Click to expand!</summary>

Use `s!help` for access the commands list.
<br>
<img src="https://i.imgur.com/mIP3LdN.png" width=600><br>
<br>

Use `s!addchannel` to select a channel for the bot to watch.
<br>
<img src="https://i.imgur.com/obw8xbB.png" width=600><br>
<br>

Use `s!removechannel` to select a channel for the bot to watch.
<br>
<img src="https://i.imgur.com/Ns0fbEw.png" width=600><br>
<br>

Use `s!addqa` to add questions and answers.
<br>
<img src="https://i.imgur.com/HVYrJEI.png" width=600><br>
<br>

Use `s!removeqa` to remove questions and answers.
<br>
<img src="https://i.imgur.com/i7Nw2pR.png" width=600><br>
<br>

Use `s!viewqa` to get a link to the questions/answers in the database.
<br>
<img src="https://i.imgur.com/NUqBXo7.png" width=600><br>
<br>

Once you've added a channel and some questions, the bot will answer questions in that channel!
<br>
<img src="https://i.imgur.com/dzjXgXP.png" width=600><br>
</details>

### Hosting
This bot is hosted on Heroku and is free for everyone to use. However, if you'd like to run a version of this bot on your machine, follow the instructions below.
<br>
- Open the "data/config.json" and replace the fields in indicated in [brackets].
- Set up a [firebase database](https://console.firebase.google.com/) and download the service account credentials to "data/firebase.json".
- Run the following commands in your terminal.
```
> pip install -r requirements.txt 
> python3 bot.py
```

### Changelog
##### v1.2 - 8/25/2021
- Allow adding multiple channels.
- Changed the prefix to `s!`
- Minor bug fixes.

##### v1.1 - 5/22/2021
- Expanded bot to work in different guilds.
- Renamed `!setchannel` to `!addchannel`.
- Added `!help`, `!removechannel`,`!removeqa`, and `!viewqa`.
- Set up a firebase database.
- Listed the bot on [TopGG](https://top.gg/bot/843968680680488980) (awaiting approval so the link does not work yet).

##### v1.0 - 5/17/2021
- Initial release!
