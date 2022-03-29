from datetime import timedelta
from datetime import time
from discord.ext import commands, tasks
import requests
from requests.packages import urllib3
import requests
from requests.packages import urllib3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
from PIL import Image
import shutil
from discord.ext import commands, tasks
from requests.packages import urllib3
from requests.packages import urllib3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
from PIL import Image
import shutil
import wget
import requests
import re
import discord
import os
import json
from datetime import datetime
import pytz
import asyncio
"""
Testing_channel_id=831911965643112489
Main Channel id=831833834671702086
"""
target_channel_id = 831935935255543828
"""
Iitilizing Firebase Credentials and getting the database information
Also Setting up discord Bot
"""


def download_image(url):
    r = requests.get(url, allow_redirects=True)
    open("temp.png", 'wb').write(r.content)
    cnt = 0
    while (r.content == 0 and cnt < 5):
        open("temp.png", 'wb').write(r.content)
        cnt += 1


# Fetch the service account key JSON file contents
cred = credentials.Certificate(
    r'certificate.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://birthday-reminder-bb6f8-default-rtdb.europe-west1.firebasedatabase.app/',
    'storageBucket': 'gs://birthday-reminder-bb6f8.appspot.com'
})
ref = db.reference('birthday-reminder-bb6f8-default-rtdb')

today = datetime.now(pytz.timezone('Asia/Kolkata'))

ref = db.reference("/")
bdays = ref.get()
bot = commands.Bot("!")
month_labels = [
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide1.JPG?alt=media&token=64277866-8c5b-40e3-9e2a-d05428777af2',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide2.JPG?alt=media&token=56d1540d-304f-4dfe-9527-897bf880e25e',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide3.JPG?alt=media&token=5a8f36a5-4d03-4c48-9e91-6c53c09b3bd1',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide4.JPG?alt=media&token=06c8cec9-2f71-4109-acbf-103435cf9fd4',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide5.JPG?alt=media&token=126ebb2e-593e-4ba7-885b-ae7ffa0ece32',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide6.JPG?alt=media&token=29b26d7b-d865-4945-a358-040e115bab32',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide7.JPG?alt=media&token=f76a30a8-882b-4285-86bb-2e8fcf921589',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide8.JPG?alt=media&token=d0e69650-6432-46be-a1d5-f294ed055620',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide9.JPG?alt=media&token=e7ba6ca4-3cde-4d1f-868a-936fe3b80520',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide10.JPG?alt=media&token=c647231c-0e25-4dbf-84cd-3d319c0b19c2',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide11.JPG?alt=media&token=86c35f54-ea08-4ffc-9cc0-ebfdb2d069ee',
    'https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2FSlide12.JPG?alt=media&token=46591047-83ec-4329-a364-40e1699bb366',
]
bday_wish_pic = "https://firebasestorage.googleapis.com/v0/b/firebaseauthsuhrut.appspot.com/o/Month_labels%2Fbday_wish.png?alt=media&token=a056e178-d4eb-4172-9de1-403dc758e17a"
message_channel = None


async def LogPrint(ActionToBeLogged):
    today = datetime.now(pytz.timezone('Asia/Kolkata'))
    baseDirectory = "Logs/"
    LogStatement = today.strftime(
        "%d-%m-%y %H:%M:%S") + "  :  `" + ActionToBeLogged + "`\n"
    log_channel = bot.get_channel(876070119867031592)
    # await log_channel.send(LogStatement)
    try:
        f = open(baseDirectory + today.strftime('%m-%y'), "a+")
        f.write(LogStatement)
        f.close()
    except:
        pass


@tasks.loop(hours=24)
async def deletemessages(a):
    try:
        message_channel = bot.get_channel(target_channel_id)
        print(a)
        for msg_id in a:
            print("Delete Messages Invoked")

            msg = await message_channel.fetch_message(msg_id)
            await msg.delete()
    except Exception as e:
        print(e.message)
        

@tasks.loop(minutes=30)
async def TodayBday():
    today = datetime.now(pytz.timezone('Asia/Kolkata'))
    """
        First part of the below code generates the monthly bdays
        Second part sends notification in case of birthday 
    """
    # await asyncio.sleep(waitTime)
    message_channel = bot.get_channel(target_channel_id)
    daily_sent_messages = []
    try:
        await deletemessages(
            json.loads(open(r"daily_sent_messages.json", "r").read()))
    except:
        await LogPrint('deletemessages(json.loads(open(r"daily_sent_messages.json", "r").read()))')
    if (today.strftime("%d") == "30"):
        try:
            await deletemessages(
                json.loads(open(r"montly_birthday_messages.json", "r").read()))
        except:
            pass
        monthly_birthday_messages = []
        temparray = []
        await LogPrint("Today Bday method run")
        # print(bdays)
        for key, value in bdays.items():
            temparray.append(value)
        temparray = sorted(temparray,
                           key=lambda x:
                           (int(x["DOB"][3:5]), int(x["DOB"][:2])))
        message_channel = bot.get_channel(target_channel_id)
        url = month_labels[int(today.strftime("%m")) - 1]
        download_image(url)
        monthly_birthday_messages.append(
            await message_channel.send(file=discord.File("temp.png")))
        for value in temparray:
            if int(today.strftime("%m")) == int(value["DOB"][3:5]):
                try:
                    url = value['Image']
                    download_image(url)
                    monthly_birthday_messages.append(
                        await message_channel.send(
                            "**Name: " + value["Name"] + "**\n" + "**DOB: " +
                            value["DOB"] + "**",
                            file=discord.File("temp.png")))
                except:
                    print(value)
                    monthly_birthday_messages.append(
                        await message_channel.send("**Name: " + value["Name"] +
                                                   "**\n" + "**DOB: " +
                                                   value["DOB"] + "**"))
                await LogPrint("BDAY BOT (This months bday): " + str(value))
        monthly_birthday_messages = [i.id for i in monthly_birthday_messages]
        open(r"montly_birthday_messages.json",
             "w").write(json.dumps(monthly_birthday_messages))
    message_channel = bot.get_channel(target_channel_id)
    image_printed = False
    print(f"Got channel {message_channel}")
    for key, value in bdays.items():
        # print(value["DOB"])
        # print(today.strftime("%d-%m"),value["DOB"][0:5])
        if (today.strftime("%d-%m") == value["DOB"][0:5]):
            if (not (image_printed)):
                url = bday_wish_pic
                download_image(url)
                daily_sent_messages.append(
                    await message_channel.send(file=discord.File("temp.png")))
                image_printed = True
            age = int(today.strftime("%Y")) - int(value['DOB'][-4:])
            agestring = ""
            if (age % 10 == 1):
                agestring = "st "
            elif (age % 10 == 2):
                agestring = "nd "
            elif (age % 10 == 3):
                agestring = "rd "
            elif (age == 11 or age == 12 or age == 12):
                agestring = " th "
            elif (age):
                agestring = "th "
            gender_string = " on her " if value["Gender"] == "F" else " on his "
            try:
                url = value['Image']
                download_image(url)
                daily_sent_messages.append(await message_channel.send(
                    '**Wish ' + value["Name"] + gender_string + str(age) +
                    agestring + "Birthday🎂✨🎉🎂✨🎉🎁🎁**\n",
                    file=discord.File("temp.png")))
                await LogPrint("BDAY BOT (Today's Bday): " + "Key: " +
                               str(key) + "Value : " + str(value))
            except:
                daily_sent_messages.append(
                    await
                    message_channel.send('**Wish ' + value["Name"] +
                                         gender_string + str(age) + agestring +
                                         "Birthday🎂✨🎉🎂✨🎉🎁🎁**\n"))
                await LogPrint("BDAY BOT (Today's Bday): " + "Key: " +
                               str(key) + "Value : " + str(value))
            finally:
                pass

    daily_sent_messages = [i.id for i in daily_sent_messages]
    open(r"daily_sent_messages.json",
         "w").write(json.dumps(daily_sent_messages))
    exit()


@TodayBday.before_loop
async def before():
    await bot.wait_until_ready()


TodayBday.start()
bot.run("ODMxNTMyMTQ1NDUzMzAxNzcw.YHWmqA.X3k3mfLzhewi3iJg2OL_upD-OTE")
