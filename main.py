# bot.py
import os
from asyncio import Task
import random
from discord.ext import commands, tasks
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
from discord.ext import commands, tasks
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import requests
import discord
import json
from datetime import datetime
import pytz
import platform
import asyncio
import os
import discord
from dotenv import load_dotenv

load_dotenv()

target_channel_id = int(os.getenv("TARGET_CHANNEL"))


def download_image(url):
    r = requests.get(url, allow_redirects=True)
    open("temp.png", 'wb').write(r.content)
    cnt = 0
    while (r.content == 0 and cnt < 5):
        open("temp.png", 'wb').write(r.content)
        cnt += 1


# Fetch the service account key JSON file contents
cred = credentials.Certificate(os.getenv("CERTIFICATE_PATH"))
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(
    cred, {
        'databaseURL': os.getenv('DATABASE_URL'),
        'storageBucket': os.getenv('STORAGE_BUCKET')
    })

ref = db.reference(os.getenv('DB_REFERENCE'))
embed_colors = [0xff31ba, 0xb7f205, 0x00f2d6, 0xf1c40f]
random.shuffle(embed_colors)
timezone = 'Antarctica/Vostok'
today = datetime.now(pytz.timezone(timezone))

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
    today = datetime.now(pytz.timezone(timezone))
    baseDirectory = ""
    LogStatement = today.strftime(
        "%d-%m-%y %H:%M:%S") + "  :  `" + ActionToBeLogged + "`\n"
    try:
        log_channel = client.get_channel(int(os.getenv('LOG_CHANNEL_ID')))
        await log_channel.send(LogStatement)
        try:
            f = open(baseDirectory + today.strftime('%d-%m-%y'), "a+")
            f.write(LogStatement)
            f.close()
        except:
            print("Unable to write log statement")
    except Exception as e:
        print("LogPrint Error")
        print(e)


async def deletemessages(a):

    message_channel = client.get_channel(target_channel_id)
    print("Messages to be Deleted:", a)
    for msg_id in a:
        try:
            print("Delete Messages Invoked")
            msg = await message_channel.fetch_message(msg_id)
            await msg.delete()
        except Exception as e:
            print("Exception Raised", e.message)


async def TodayBday():
    today = datetime.now(pytz.timezone(timezone))
    """
        First part of the below code generates the monthly bdays
        Second part sends notification in case of birthday 
    """
    # await asyncio.sleep(waitTime)
    message_channel = client.get_channel(target_channel_id)
    daily_sent_messages = []
    try:
        await deletemessages(
            json.loads(open(os.getenv("DAILY_SENT_FILE_NAME"), "r").read()))
    except:
        await LogPrint('deletemessages(json.loads(open(r"' +
                       os.getenv("DAILY_SENT_FILE_NAME") + ',", "r").read()))')
    if (today.strftime("%d") == "01" or True):
        try:
            await deletemessages(
                json.loads(
                    open(os.getenv("DAILY_SENT_FILE_NAME"), "r").read()))
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
        message_channel = client.get_channel(target_channel_id)
        url = month_labels[int(today.strftime("%m")) - 1]
        download_image(url)
        monthly_birthday_messages.append(
            await message_channel.send(file=discord.File("temp.png")))
        i = 0
        for value in temparray:
            name = value["Name"]
            dob = value["DOB"]
            age = int(today.strftime("%Y")) - int(value['DOB'][-4:])
            color = embed_colors[i % (len(embed_colors))]
            embed = discord.Embed(color=color)
            embed.add_field(name="Name", value="{}".format(name), inline=False)
            embed.add_field(name="Date of Birth", value="{}".format(dob))
            embed.add_field(name="Age(To be)",
                            value="{} Years".format(age),
                            inline=True)
            embed.set_footer(text="{}({}).  Developed by Sai Suhrut".format(
                today.strftime(" %d/%m/%Y, %H:%M:%S"), timezone))
            if int(today.strftime("%m")) == int(value["DOB"][3:5]):
                try:
                    url = value['Image']
                    download_image(url)
                    monthly_birthday_messages.append(
                        await
                        message_channel.send(file=discord.File("temp.png"),
                                             embed=embed))
                except:
                    print(value)
                    monthly_birthday_messages.append(
                        await message_channel.send(embed=embed))
                await LogPrint("BDAY BOT (This months bday): " + str(value))
            i += 1
        monthly_birthday_messages = [i.id for i in monthly_birthday_messages]
        open(os.getenv("MONTHLY_SENT_FILE_NAME"),
             "w").write(json.dumps(monthly_birthday_messages))
    message_channel = client.get_channel(target_channel_id)
    image_printed = False
    i = 0
    print(f"Got channel {message_channel}")
    for key, value in bdays.items():
        # print(value["DOB"])
        # print(today.strftime("%d-%m"),value["DOB"][0:5])
        if (today.strftime("%d-%m") == value["DOB"][0:5]):
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
            name = value["Name"]
            dob = value["DOB"]
            color = embed_colors[i % len(embed_colors)]
            gender_string = " on her " if value["Gender"] == "F" else " on his "
            embed = discord.Embed(title="Wish {}{}{}{} Birthday🎂".format(
                name, gender_string, age, agestring), color=color)
            embed.add_field(name="Name", value="{}".format(name), inline=False)
            embed.add_field(name="Date of Birth", value="{}".format(dob))
            embed.add_field(name="Age",
                            value="{} Years".format(age),
                            inline=True)
            embed.set_footer(text="{}({}).  Developed by Sai Suhrut".format(
                today.strftime(" %m/%d/%Y, %H:%M:%S"), timezone))
            embed.set_thumbnail(
                url="https://jooinn.com/images/birthday-cake-clipart.jpg")
            try:
                url = value['Image']
                download_image(url)
                daily_sent_messages.append(await message_channel.send(
                    file=discord.File("temp.png"), embed=embed))
                await LogPrint("BDAY BOT (Today's Bday): " + "Key: " +
                               str(key) + "Value : " + str(value))
            except Exception as e:
                print("Exception :", e)
                daily_sent_messages.append(
                    await message_channel.send(embed=embed), )
                await LogPrint("BDAY BOT (Today's Bday): " + "Key: " +
                               str(key) + "Value : " + str(value))
            finally:
                pass
        i += 1
    daily_sent_messages = [i.id for i in daily_sent_messages]
    open(os.getenv("DAILY_SENT_FILE_NAME"),
         "w").write(json.dumps(daily_sent_messages))
    try:
        print("Trying deletion og temp.png")
        os.remove("temp.png")
        print("temp.png deletion successful")
    except:
        print("Temporary image file deletion failed")

client = discord.Client()

TOKEN = os.getenv("BOT_TOKEN")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await TodayBday()
client.run()
