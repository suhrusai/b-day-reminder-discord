from Constants import TOKEN
import sys

from Services.DiscordService import DiscordService
from TimeHelper import todayInTZ
client = DiscordService.client
embedIndex = 0
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    if(todayInTZ().day == 1):
        await DiscordService.sendBirthdayNotifications("monthly")
        await DiscordService.deleteRecentNotifications("monthly")
    await DiscordService.sendBirthdayNotifications("daily")
    await DiscordService.deleteRecentNotifications("daily")
    exit()
client.run(TOKEN)