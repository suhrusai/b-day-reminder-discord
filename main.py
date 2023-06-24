from Constants import TOKEN
from Helpers.TimeHelper import today_in_tz

from Services.DiscordService import DiscordService
from Services.BirthdayService import BirthdayService

client = DiscordService.client
embedIndex = 0

BirthdayService()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    if today_in_tz().day == 1 and True:
        await DiscordService.send_birthday_notifications("monthly")
        await DiscordService.delete_recent_notifications("monthly")
    await DiscordService.send_birthday_notifications("daily")
    await DiscordService.delete_recent_notifications("daily")
    exit()


client.run(TOKEN)
