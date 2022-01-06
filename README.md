# instaloaderbot
A telegram bot who gets some informations and pics from Instagram. It can dowload everything like posts, highlights, stories and even more.

# Getting Started
First of all, you should dowload de repo, or even de script, 'instaloader.py' and put it in an empty folder. Later, you should install the needed modules, via 'pip/pip3 install'
* pip/pip3 install instaloader
* pip/pip3 install logging
* pip/pip3 install os
* pip/pip3 install requests
* pip/pip3 install shutil
* pip/pip3 install instaloader
* pip/pip3 install pandas
* pip/pip3 install itertools
* pip/pip3 install python-telegram-bot

# Telegram BOT
You need to create a BOT on TELEGRAM, for this, you can chat to 'BotFather', then '/newbot', and follow the instructions, then, when you have created it, you need to copy the API KEY that BotFather gives to you and put it on the script, in the part of 'Updater('' #insert your BOT API KEY)'.
Later, you have to add commands, for this, return to 'BotFather', '/mybots', select your bot, 'Edit Bot', 'Edit Commands', then you paste this list:
"""
login - LOGIN [user] [password]
posts - Get USER'S POSTS [user] [nº] [a/d](ascendent/descentent)
postsdate -Get USER'S POSTS by DATE [user] [nº] [since(d/m/y)] [until(d/m/y)] [asc/desc](ascendent/descentent)
top - Get TOP POST of USER [user] [nº]
profilepic -Get PROFILE PIC of an USER [user]
stories -Get an USER STORY [user]
highlights - Get USER'S HIGHLIGHTS [user] [nº]
tagged - Get tagged POSTS of an USER [user] [nº]
story - Get USER'S STORIES [nº]
feed - Get USER'S FEED [nº]
followers - Get USER'S FOLLOWERS [user] [nº]
following - Get USER'S FOLLOWING [user] [nº]
mutual - Get MUTUAL FOLLOWERS/FOLLOWING [user] [nº]
similar - Get similar ACCOUNTS [user] [nº]
clear- CLEAR all FILES
"""
# Functions and Examples
For all the functions except 'login' you have to be logged before. Then, there are some examples of using.
*login - Auth on your account by the command, for example, '/login danielaceros 1234 (Login on user 'danielaceros' with password '1234')
*posts - Get an USER'S POSTS by te command, for example, '/posts dani 10 a' (Get 10 posts of the user 'dani' by ascendent way)
*postsdate - Get an USER'S POSTS by DATE by the command, for example
