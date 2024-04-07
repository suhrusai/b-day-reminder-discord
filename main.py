from Helpers.TimeHelper import today_in_tz
import os
from Services.DiscordService import DiscordService
from Services.BirthdayService import BirthdayService
from dotenv import load_dotenv
client = DiscordService.client
embedIndex = 0

BirthdayService()
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    if today_in_tz().day == 1 and True:
        try:
            await DiscordService.delete_recent_notifications("monthly")
        except Exception as e:
            print(e)
        try:
            await DiscordService.send_birthday_notifications("monthly")
        except Exception as e:
            print(e)
    try:
        await DiscordService.delete_recent_notifications("daily")
    except Exception as e:
        print(e)
    try:
        await DiscordService.send_birthday_notifications("daily")
    except Exception as e:
        print(e)
    client.close()
    exit()


client.run(TOKEN)
