<html>
<div align="center">
<img src="https://camo.githubusercontent.com/48b5c67f0baa5b41fc98c96dad8de4771b0fc583d6b3dda417c7f8e01e801028/68747470733a2f2f692e696d6775722e636f6d2f734a7a665a734c2e6a7067" alt="alt text" width="250" height="250"></img>
</div>
<h1 align="center">@danielaceros
<div align="center">
<a href=https://github.com/danielaceros><img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=@danielaceros&color=%230076D6&style=flat&logo=google-chrome&logoColor=%230076D6" alt="website"/></a>
<img src="https://img.shields.io/github/followers/danielaceros?style=social" alt="Star Badge"/>
<a><img src="https://img.shields.io/github/last-commit/danielaceros/instaloaderbot" alt="Join Community Badge"/></a>
<a><img src="https://img.shields.io/github/repo-size/danielaceros/instaloaderbot" />
</div>
</html>

# instaloaderbot
A telegram bot who gets some informations and pics from Instagram. It can dowload everything like posts, highlights, stories and even more.
## Getting Started
First of all, you should dowload de repo, or even de script, 'instaloader.py' and put it in an empty folder. Later, you should install the needed modules, via 'pip/pip3 install'
```bash
pip/pip3 install instaloader
pip/pip3 install logging
pip/pip3 install os
pip/pip3 install requests
pip/pip3 install shutil
pip/pip3 install instaloader
pip/pip3 install pandas
pip/pip3 install itertools
pip/pip3 install python-telegram-bot
```
## Telegram BOT
You need to create a BOT on TELEGRAM, for this, you can chat to 'BotFather', then '/newbot', and follow the instructions, then, when you have created it, you need to copy the API KEY that BotFather gives to you and put it on the script, in the part of 'Updater('' #insert your BOT API KEY)'.
Later, you have to add commands, for this, return to 'BotFather', '/mybots', select your bot, 'Edit Bot', 'Edit Commands', then you paste this list:
```
login - LOGIN [user] [password]
posts - Get USER'S POSTS [user] [nº] [a/d](ascendent/descentent)
postsdate -Get USER'S POSTS by DATE [user] [nº] [since(d/m/y)] [until(d/m/y)] [asc/desc](ascendent/descentent)
top - Get TOP POST of USER [user] [nº]
profilepic - Get PROFILE PIC of an USER [user]
stories -Get an USER STORY [user]
highlights - Get USER'S HIGHLIGHTS [user] [nº]
tagged - Get tagged POSTS of an USER [user] [nº]
story - Get USER'S STORIES [nº]
feed - Get USER'S FEED [nº]
followers - Get USER'S FOLLOWERS [user] [nº]
following - Get USER'S FOLLOWING [user] [nº]
mutual - Get MUTUAL FOLLOWERS/FOLLOWING [user] [nº]
similar - Get similar ACCOUNTS [user] [nº]
clear - CLEAR all FILES
```
## Running CODE
When you have created the BOT, installed the packages, and gived to the '.py' your API TOKEN, you can run the code by an IDE or PowerShell/CommandPrompt by:
```bash
python instaloaderbot.py
python3 instaloaderbot.py
```
## Functions and Examples
For all the functions except 'login' you have to be logged before. Then, there are some examples of the usage of Telegram Commands.
* login - Auth on your account by the command, for example, ```/login danielaceros 1234``` (Login on user 'danielaceros' with password '1234')
* posts - Get an USER'S POSTS by te command, for example, ```/posts dani 10 a``` (Get 10 posts of the user 'dani' by ascendent way)
* postsdate - Get an USER'S POSTS by DATE by the command, for example, ```/postsdate dani 10 1/1/2022 1/1/2020 a``` (Get 10 posts of the user 'dani' from 2022 to 2020 by ascendent). Important that since > until, instead, first date > second date.
* top - Get TOP POSTS of an USER by the command, for example ```/top dani 20``` (Get the 20% photos more liked from user 'dani')
* profilepic - Get the PROFILE PIC of an USER by the command, for example ```/profilepic dani``` (Get the profile pic of 'dani)
* stories - Get the STORIES of an USER by the command, for example ```/stories dani``` (Gets the stories of the user 'dani')
* highlights - Get the HIGHLIGHTS of an USER by the command, for example ```/highlights dani 10``` (Get 10 highlights of the user 'dani')
* tagged - Get the TAGGED PHOTOS of an USER by the command, for example ```/tagged dani 10``` (Get 10 tagged photos of the user 'dani')
* story - Get the STORIES from the FEED of LOGGED USER by the command, for example ```/story 10``` (Get 10 stories of feed)
* feed - Get the FEED of LOGGED USER by the command, for example ```/feed 10``` (Get 10 feed posts of feed)
* followers - Get the LIST of FOLLOWERS of an USER by the command, for example ```/followers dani 10``` (Get 10 followers of the user 'dani')
* following - Get the LIST of FOLLOWING of an USER by the command, for example ```/following dani 10``` (Get 10 followees of the user 'dani')
* mutual - Get the LIST of FOLLOWERS - FOLLOWING of an USER by the command, for example ```/mutual dani 10``` (Get 10 mutual followings of the user 'dani')
* similar - Get the LIST of SIMILAR ACCOUNT of an USER by the command, for example ```/similar dani 10``` (Get 10 accounts similar to the user 'dani')
* clear - Clear all DIRECTORIES of the FOLDER where the script is placed by the command, ```/clear```
## License
[GPL](https://choosealicense.com/licenses/gpl-3.0/)
