import instaloader
from instaloader import Profile
import os
import os.path
import logging
import shutil
import psutil
from instaloader.instaloadercontext import RateController
import requests
import pandas as pd
from telegram.ext.dispatcher import run_async
from itertools import dropwhile, takewhile
from datetime import datetime
from math import ceil
from itertools import islice
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
logging.basicConfig(level=logging.DEBUG)
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.57 Safari/537.36 Edg/91.0.864.27'
updater = Updater("", # enter your API TOKEN
                  use_context=True)
dispatcher: Dispatcher = updater.dispatcher
def login(update: Update, context: CallbackContext): # login stuff /login [user] [password]
    try:
        global L
        L = instaloader.Instaloader(download_pictures=True,
        download_videos=False, 
        download_video_thumbnails=False,
        compress_json=False, 
        download_geotags=False,
        post_metadata_txt_pattern=None, 
        max_connection_attempts=0,
        download_comments=False,
        save_metadata=False,
        storyitem_metadata_txt_pattern=None,
        user_agent=agent)
        bot: Bot = context.bot
        user = context.args[0].lower()
        passw = context.args[1]
        L.login(user, passw)
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡Welcome!, '@{}', READY?".format(user))
    except IndexError:
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U000026D4 ¡A USERNAME and a PASSWORD is required, CHECK IT! \U000026D4")

    except:
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F534 ¡Incorrect user/password, CHECK IT, and, TRY AGAIN!, '@{}'".format(user))
def postsdate(update: Update, context: CallbackContext): # gets the PICS of an USER by DATE /postsdate [user] [nº] [since(d/m/y)] [until(d/m/y)] [(a)sc/(d)sc], always since > until
    try:
        bot: Bot = context.bot
        n = int(context.args[1])
        user = context.args[0].lower()
        n2 = n
        ty = context.args[4].lower()
        s = list(context.args[2].split("/"))
        u = list(context.args[3].split("/"))
        SINCE = datetime(int(s[2]), int(s[1]), int(s[0]))
        UNTIL = datetime(int(u[2]), int(u[1]), int(u[0]))
        if n == 0:
            n2 = "ALL"
        posts = instaloader.Profile.from_username(L.context, user).get_posts()
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡Getting {} PICS, from {} to {}! of '@{}', this may take a WHILE...".format(n2, SINCE, UNTIL, user))
        y = 1
        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
            if n != 0:
                if y > n:
                    break
                else:
                    pass
                L.download_post(post, "{}date".format(user))
                y = y + 1
            else:
                L.download_post(post, "{}date".format(user))

        for file in os.listdir("{}date".format(user)):
            if file.endswith(".txt"):
                os.remove("{}date/{}".format(user, file))
            else:
                pass
        if ty == 'a':
            x = 1
            for file in sorted(os.listdir("{}date".format(user)), reverse=False):
                if n == 0:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}date/{}".format(user, file), 'rb'))

                elif n >= x:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}date/{}".format(user, file), 'rb'))
                    x = x + 1
                else:
                    break
        elif ty == 'd':
            x = 1
            for file in sorted(os.listdir("{}date".format(user)), reverse=True):
                if n == 0:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}date/{}".format(user, file), 'rb'))

                elif n >= x:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}date/{}".format(user, file), 'rb'))
                    x = x + 1
                else:
                    break
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} POSTED PICS of '@{}' from {} to {}".format(n2, user, SINCE, UNTIL))
    except Exception:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting POSTED PICS \U000026D4")
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting POSTED PICS \U000026D4")
def profilepics(update: Update, context: CallbackContext): # gets the PICS of an USER /profilepics [user] [nº] [(a)sc/(d)sc]
    try:
        bot: Bot = context.bot
        n = int(context.args[1])
        user = context.args[0].lower()
        n2 = n
        ty = context.args[2].lower()
        if n == 0:
            n2 = "ALL"
        profile = Profile.from_username(L.context, user).get_posts()
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡Getting {} PICS! of '@{}', this may take a WHILE...".format(n2, user))
        y = 1
        for pic in profile:
            if n != 0:
                if y > n:
                    break
                else:
                    pass
                L.download_post(pic, "{}".format(user))
                y = y + 1
            else:
                L.download_post(pic, "{}".format(user))
        for file in os.listdir("{}".format(user)):
            if file.endswith(".txt"):
                os.remove("{}/{}".format(user, file))
            else:
                pass
        if ty == 'a':
            x = 1
            for file in sorted(os.listdir("{}".format(user)), reverse=False):
                if n == 0:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(user, file), 'rb'))

                elif n >= x:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(user, file), 'rb'))
                    x = x + 1
                else:
                    break
        elif ty == 'd':
            x = 1
            for file in sorted(os.listdir("{}".format(user)), reverse=True):
                if n == 0:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(user, file), 'rb'))

                elif n >= x:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(user, file), 'rb'))
                    x = x + 1
                else:
                    break
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} POSTED PICS of '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting POSTED PICS \U000026D4")
def highlights(update: Update, context: CallbackContext): # gets the HIGHLIGHTS of an USER /highlights [user] [nº]
    try:
        bot: Bot = context.bot
        n = int(context.args[1])
        user = context.args[0].lower()
        n2 = n
        if n == 0:
            n2 = "ALL"
        profile = Profile.from_username(L.context, user)
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F916 ¡Getting {} HIGHLIGHTS! of '@{}', this may take a WHILE...".format(n2, user))
        y = 0
        s = True
        for highlight in L.get_highlights(user=profile):
            for item in highlight.get_items():
                if n != 0:
                    if y > n: 
                        s = False
                        break
                    else:
                        pass
                    L.download_storyitem(item, '{}stories'.format(highlight.owner_username))
                    y = y + 1
                elif n == 0:
                    L.download_storyitem(item, '{}stories'.format(highlight.owner_username))
            if s == False:
                break
        x = 1
        for file in sorted(os.listdir('{}stories'.format(user)), reverse=True):
            if n == 0:
                bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open("{}stories/{}".format(user, file), 'rb'))

            elif n >= x:
                bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open("{}stories/{}".format(user, file), 'rb'))
                x = x + 1
            else:
                break
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} HIGHLIGHTS of '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting HIGHLIGHTS \U000026D4")
def stories(update: Update, context: CallbackContext): # gets the stories of a CURRENT USER /stories [nº]
    try:
        bot: Bot = context.bot
        n = int(context.args[0])
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F916 ¡Getting STORIES!, this may take a WHILE...")
        y = 1
        for story in L.get_stories():
            for item in story.get_items():
                if n != 0:
                    if y > n:
                        break
                    else:
                        pass
                    L.download_storyitem(item, 'story')
                    y = y + 1
                else:
                    L.download_storyitem(item, 'story')
        x = 1
        for file in sorted(os.listdir('story'), reverse=True):
            if n == 0:
                bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open('story/{}'.format(file), 'rb'))

            elif n >= x:
                bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open('story/{}'.format(file), 'rb'))
                x = x + 1
            else:
                break
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} STORIES from USER".format(n))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting STORIES from USER \U000026D4")
def feed(update: Update, context: CallbackContext): # gets the USER FEED /feed [nº]
    try:
        bot: Bot = context.bot
        n = int(context.args[0])
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F916 ¡Getting FEED!, this may take a WHILE...")
        y = 0
        for item in L.get_feed_posts():
            if n != 0:
                if y > n: 
                    break
                else:
                    pass
                L.download_storyitem(item, 'feed')
                y = y + 1
            else:
                L.download_storyitem(item, 'feed')
        x = 1
        for file in sorted(os.listdir('feed'), reverse=True):
            if n == 0:
                bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open('feed/{}'.format(file), 'rb'))

            elif n >= x:
                bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open('feed/{}'.format(file), 'rb'))
                x = x + 1
            else:
                break
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} FEED from USER".format(n))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting FEED from USER \U000026D4")
def followers(update: Update, context: CallbackContext): # gets the FOLLOWERS of an USER /followers [user] [nº]
    try:
        bot: Bot = context.bot
        n = int(context.args[1])
        n2 = n
        if n == 0:
            n2 = "ALL"
        user = context.args[0].lower()
        profile = Profile.from_username(L.context, user)
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡Getting USER FOLLOWERS! of '@{}', this may take a WHILE...".format(user))
        x = 1
        for followee in profile.get_followers():
            if n != 0:
                if x > n:
                    break
                bot.send_message(chat_id=update.effective_chat.id,
                                        text="\U0001F916 [{}] '{}'".format(x, followee.username))
                x = x + 1
            else:
                bot.send_message(chat_id=update.effective_chat.id,
                                        text="\U0001F916 [{}] '{}'".format(x, followee.username))
                x = x + 1
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} USER FOLLOWERS from '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting USER FOLLOWERS \U000026D4")
def following(update: Update, context: CallbackContext): # gets the FOLLOWEES of an USER /following [user] [nº]
    try:
        bot: Bot = context.bot
        n = int(context.args[1])
        n2 = n
        if n == 0:
            n2 = "ALL"
        user = context.args[0].lower()
        profile = Profile.from_username(L.context, user)
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡Getting USER FOLLOWING! of '@{}', this may take a WHILE...".format(user))
        x = 1
        for followee in profile.get_followees():
            if n != 0:
                if x > n:
                    break
                bot.send_message(chat_id=update.effective_chat.id,
                                        text="\U0001F916 [{}] '{}'".format(x, followee.username))
                x = x + 1
            else:
                bot.send_message(chat_id=update.effective_chat.id,
                                        text="\U0001F916 [{}] '{}'".format(x, followee.username))
                x = x + 1
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} USER FOLLOWEES from '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting USER FOLLOWEES \U000026D4")
def mutual(update: Update, context: CallbackContext): # gets the mutual followers /mutual [user] [nº]
    try:
        bot: Bot = context.bot
        n = int(context.args[1])
        n2 = n
        if n == 0:
            n2 = "ALL"
        user = context.args[0].lower()
        profile = Profile.from_username(L.context, user)
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡Getting USER MUTUAL! of '@{}', this may take a WHILE...".format(user))
        followees = set()
        for followee in profile.get_followers():
            followees.add(followee.username)

        followers = set()
        for follower in profile.get_followees():
            followers.add(follower.username)

        mutual = set.intersection(followees, followers)
        z = 1
        for m in mutual:
            if n != 0:
                if z > n:
                    break
                bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 [{}] '@{}'".format(z, m))
                z = z + 1
            elif n == 0:
                bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 [{}] '@{}'".format(z, m))
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} USER MUTUALS from '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting USER MUTUAL \U000026D4")
def profilepic(update: Update, context: CallbackContext): # gets the profile pic of an USER /profilepic [user]
    try:
        bot: Bot = context.bot
        user = context.args[0].lower()
        profile = Profile.from_username(L.context, user).profile_pic_url
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡Getting PROFILE PIC! of '@{}', this may take a WHILE...".format(user))
        r = requests.get(profile, stream=True)
        if not os.path.exists("{}profile".format(user)):
            os.mkdir("{}profile".format(user))
            with open('{}profile/{}_profilepic.jpg'.format(user, user), 'wb') as f:
                shutil.copyfileobj(r.raw, f) 
            bot.send_photo(chat_id=update.effective_chat.id,
                                    photo=open('{}profile/{}_profilepic.jpg'.format(user, user), 'rb'))
        else:
            bot.send_photo(chat_id=update.effective_chat.id,
                                    photo=open('{}profile/{}_profilepic.jpg'.format(user, user), 'rb'))      
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted PROFILE PIC from '@{}'".format(user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting PROFILE PIC \U000026D4")
def story(update: Update, context: CallbackContext): # gets stories of an USER /stories [user] [nº]
    try:
        bot: Bot = context.bot
        user = context.args[0].lower()
        profile = L.check_profile_id(user)
        bot.send_message(chat_id=update.effective_chat.id,
                        text="\U0001F916 ¡Getting STORIES! of '@{}', this may take a WHILE...".format(user))
        L.download_stories(userids=[profile], filename_target='{}story'.format(user))
        if os.path.exists("{}/id".format(user)):
            os.remove("{}/id".format(user))
        for file in sorted(os.listdir('{}story'.format(user)), reverse=True):
            if file.endswith(".xz"):
                    os.remove("{}story/{}".format(user, file))
            else:
                bot.send_photo(chat_id=update.effective_chat.id,
                                        photo=open('{}story/{}'.format(user, file), 'rb'))
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted STORIES from '@{}'".format(user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting STORIES \U000026D4")
def tagged(update: Update, context: CallbackContext): # get TAGGED PICS of an USER /tagged [user] [nº]
    try:
        bot: Bot = context.bot
        user = context.args[0].lower()
        n = int(context.args[1])
        n2 = n
        if n == 0:
            n2 = "ALL"
        bot.send_message(chat_id=update.effective_chat.id,
                        text="\U0001F916 ¡Getting {} TAGGED! of '@{}', this may take a WHILE...".format(n2, user))
        profile = L.check_profile_id(user)   
        L.download_tagged(profile, target='{}tagged'.format(user))
        if os.path.exists("{}/id".format(user)):
            os.remove("{}/id".format(user))
        x = 1
        for file in sorted(os.listdir('{}tagged'.format(user)), reverse=True):
            if file.endswith(".xz"):
                os.remove("{}tagged/{}".format(user, file))
            elif file.endswith(".txt"):
                os.remove("{}tagged/{}".format(user, file))
            elif file.endswith(".mp4"):
                os.remove("{}tagged/{}".format(user, file))
            else:
                if n != 0:
                    if x > n:
                        break
                    bot.send_photo(chat_id=update.effective_chat.id,
                                            photo=open('{}tagged/{}'.format(user, file), 'rb'))
                    x = x + 1
                else:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                            photo=open('{}tagged/{}'.format(user, file), 'rb'))
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} TAGGED from '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting TAGGED \U000026D4")
def top(update: Update, context: CallbackContext): # gets TOP PICS of an USER /top [user] [nº]
    try:
        bot: Bot = context.bot
        user = context.args[0].lower()
        n = int(context.args[1])
        X_percentage = n    
        profile = Profile.from_username(L.context, user)
        posts_sorted_by_likes = sorted(profile.get_posts(),
                                    key=lambda p: p.likes + p.comments,
                                    reverse=True)

        bot.send_message(chat_id=update.effective_chat.id,
                        text="\U0001F916 ¡Getting {}% MOST LIKED! of '@{}', this may take a WHILE...".format(n, user))
        for post in islice(posts_sorted_by_likes, ceil(profile.mediacount * X_percentage / 100)):
            L.download_post(post, "{}top".format(user))
        for file in sorted(os.listdir('{}top'.format(user)), reverse=True):
            if file.endswith(".xz"):
                os.remove("{}top/{}".format(user, file))
            elif file.endswith(".txt"):
                os.remove("{}top/{}".format(user, file))
            elif file.endswith(".mp4"):
                os.remove("{}top/{}".format(user, file))
            else:
                bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open('{}top/{}'.format(user, file), 'rb'))
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} % MOST LIKED from '@{}'".format(n, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting % MOST LIKED \U000026D4")
def similar(update: Update, context: CallbackContext): # gets similar ACCOUNTS /similar [user] [nº]
    try:
        bot: Bot = context.bot
        user = context.args[0].lower()
        n = int(context.args[1])
        n2 = n
        if n == 0:
            n2 = "ALL"
        bot.send_message(chat_id=update.effective_chat.id,
                        text="\U0001F916 ¡Getting {} SIMILAR USERS! of '@{}', this may take a WHILE...".format(n2, user))
        profile = Profile.from_username(L.context, user)
        x = 1
        for followee in profile.get_similar_accounts():
            if n != 0:
                if x > n:
                    break
                bot.send_message(chat_id=update.effective_chat.id,
                                        text="\U0001F916 [{}] '{}'".format(x, followee.username))
                x = x + 1
            else:
                bot.send_message(chat_id=update.effective_chat.id,
                                        text="\U0001F916 [{}] '{}'".format(x, followee.username))
                x = x + 1
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} SIMILAR from '@{}'".format(n2, user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting SIMILAR USERS \U000026D4")
def clear(update: Update, context: CallbackContext): # ¡CAUTION! erase all directories in the script.py, by /clear [nameofile]
    try:
        bot: Bot = context.bot
        user = context.args[0].lower()
        if user == "0":
            dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
            for dir in dirs:
                shutil.rmtree(dir)
            bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡ALL FILES ERASED!...")
        elif user != "0":
            shutil.rmtree('{}'.format(user))
            bot.send_message(chat_id=update.effective_chat.id,
                                text="\U0001F916 ¡ALL FILES ERASED! from '{}'...".format(user))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while CLEANING \U000026D4")
def status(update: Update, context: CallbackContext): # gets INSTAGRAM status logged/not logged in
    try:
        bot: Bot = context.bot
        status = L.test_login()
        if status != None:
            bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡LOGGED IN! as '@{}'".format(status))
        else:
            bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F534 ¡NOT LOGEED IN, CHECK IT, and TRY AGAIN!")
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F534 ¡NOT LOGEED IN, CHECK IT, and TRY AGAIN!")
def dir(update: Update, context: CallbackContext): # list dirs on the SERVER and gets FREE DISK SPACE
    try:
        bot: Bot = context.bot
        dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
        x = 1
        sizes = []
        for dir in dirs:
            filesize = []
            for file in os.listdir('{}'.format(dir)):
                filesize.append(os.path.getsize('{}/{}'.format(dir, file)))
            size = round(float(sum(filesize))/float(1024*1024), 2)
            sizes.append(size)
            bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F916 [{}] '{}' | {} MB".format(x, dir, size))
            x = x + 1

        path = '/'
        ava = (psutil.disk_usage(path).free) / 1024 / 1024
        to = (psutil.disk_usage(path).total) / 1024 / 1024
        us = (psutil.disk_usage(path).used) / 1024 / 1024
        
        bot.send_message(chat_id=update.effective_chat.id,
                            text="""\U0001F916 TOTAL: {} MB
      USED: {} MB
      FREE: {} MB
      DIR: {} MB""".format(round(to,2), round(us,2), round(ava,2), round(sum(sizes),2)))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while LISTING DIRS \U000026D4")
def exit(update: Update, context: CallbackContext): # exits
    try:
        bot: Bot = context.bot
        profilepics.terminate()
        highlights.terminate()
        stories.terminate()
        feed.terminate()
        clear.terminate()
        login.terminate()
        followers.terminate()
        following.terminate()
        profilepic.terminate()
        stories.terminate()
        tagged.terminate()
        top.terminate()
        similar.terminate()
        postsdate.terminate()
        status.terminate()
        dir.terminate()
    except:
        pass
def saved(update: Update, context: CallbackContext): # gets files DOWNLOADED YET /status [nameofile] [nº/0] [(a)sc/(d)esc]
    try:
        bot: Bot = context.bot
        name = context.args[0].lower()
        n = int(context.args[1])
        n2 = n
        rev = context.args[2].lower()
        if n == 0:
            n2 = "ALL"
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F916 ¡Getting {} SAVED PICS!, on {}, this may take a WHILE...".format(n2, name))
        x = 1
        if rev == "a":
            for file in sorted(os.listdir('{}'.format(name)), reverse=False):
                if n == 0:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(name, file), 'rb'))

                elif n >= x:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(name, file), 'rb'))
                    x = x + 1
                else:
                    break
        elif rev == "d":
            for file in sorted(os.listdir('{}'.format(name)), reverse=True):
                if n == 0:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(name, file), 'rb'))

                elif n >= x:
                    bot.send_photo(chat_id=update.effective_chat.id,
                                photo=open("{}/{}".format(name, file), 'rb'))
                    x = x + 1
                else:
                    break
        bot.send_message(chat_id=update.effective_chat.id,
                            text="\U0001F7E2 ¡FINISHED!, getted {} SAVED PICS from '@{}'".format(n2, name))
    except:
        bot.send_message(chat_id=update.effective_chat.id,
                                text="\U000026D4 FATAL ERROR, while getting SAVED PICS \U000026D4")
if __name__ == '__main__': # starting stuff and commands for TELEGRAM BOT
    try:
        dispatcher.add_handler(
            CommandHandler("posts", profilepics, run_async=True))
        dispatcher.add_handler(
            CommandHandler("highlights", highlights, run_async=True))
        dispatcher.add_handler(
            CommandHandler("story", stories, run_async=True))
        dispatcher.add_handler(
            CommandHandler("feed", feed, run_async=True))
        dispatcher.add_handler(
            CommandHandler("clear", clear, run_async=True))
        dispatcher.add_handler(
            CommandHandler("login", login, run_async=True))
        dispatcher.add_handler(
            CommandHandler("followers", followers, run_async=True))
        dispatcher.add_handler(
            CommandHandler("following", following, run_async=True))
        dispatcher.add_handler(
            CommandHandler("mutual", mutual, run_async=True))
        dispatcher.add_handler(
            CommandHandler("profilepic", profilepic, run_async=True))
        dispatcher.add_handler(
            CommandHandler("stories", stories, run_async=True))
        dispatcher.add_handler(
            CommandHandler("tagged", tagged, run_async=True))
        dispatcher.add_handler(
            CommandHandler("top", top, run_async=True))
        dispatcher.add_handler(
            CommandHandler("similar", similar, run_async=True))
        dispatcher.add_handler(
            CommandHandler("postsdate", postsdate, run_async=True))
        dispatcher.add_handler(
            CommandHandler("status", status, run_async=True))
        dispatcher.add_handler(
            CommandHandler("dir", dir, run_async=True))
        dispatcher.add_handler(
            CommandHandler("exit", exit, run_async=True))
        dispatcher.add_handler(
            CommandHandler("saved", saved, run_async=True))
        updater.start_polling()
    except:
        pass
