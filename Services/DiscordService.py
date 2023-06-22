import datetime
import random
import discord
from BirthdayService import BirthdayService
from Constants import BIRTHDAY_MESSSAGE_THUMBNAIL, EMBED_COLORS, TIMEZONE
from datetime import date
from Services.ImageCache import ImageCache
from Models.ServerRunRecord import ServerRunRecord

from Services.NotificationService import NotificationService
from Services.ServerRunRecordService import ServerRunRecordService
from Services.ServerService import ServerCache
from Helpers.EmbedGenerator import getBirthdayNotificationEmbed, getMonthlyBirthdayEmbed
from Models.Notification import Notification
from Helpers.TimeHelper import todayInTZ
class DiscordService():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    async def deleteRecentNotifications(notificationType):
        #get latest run record of either month or daily notification type
        latestRunRecord = NotificationService().getLatestNotificationRecord(notificationType);
        if latestRunRecord is not None:
            for serverRunRecordId in latestRunRecord.serverRunRecords:
                serverRunRecord = ServerRunRecordService().getServerRunRecordById(serverRunRecordId)
                channelId = ServerCache().get(serverRunRecord.serverId).channelId
                message_channel = DiscordService.client.get_channel(int(channelId))
                for messageId in serverRunRecord.messageIds:
                    try:
                        msg = await message_channel.fetch_message(messageId)
                        await msg.delete()
                    except Exception as e:
                        print("Failed to delete message in server:"+serverRunRecord.serverId)
                        print(e)
    async def sendBirthdayNotifications(actionType):
        birthdays = None
        if(actionType == "monthly"):
            birthdays = BirthdayService().monthBdays()
        else:
            birthdays = BirthdayService().todayBdays()
        if(actionType == "monthly"):
            birthdays = sorted(birthdays, key=lambda bday: datetime.datetime.strptime(bday.date, "%d-%m-%Y").date().replace(year=todayInTZ().year))
        notificationDict = {}
        for birthday in birthdays:
            for serverId in birthday.servers:
                if(notificationDict.get(serverId) is None):
                    notificationDict[serverId] = ServerRunRecord(serverId,[],[])
                if(actionType == "monthly"):
                    embed = getMonthlyBirthdayEmbed(birthday)
                else:
                    embed = getBirthdayNotificationEmbed(birthday)
                channelId = ServerCache().get(serverId).channelId
                message_channel = None
                while(message_channel is None):
                    message_channel = DiscordService.client.get_channel(int(channelId))
                sentMessageId = None
                if(birthday.imageUrl and len(birthday.imageUrl) > 0):
                    imageFileName = ImageCache.getImage(birthday.imageUrl)
                    sentMessageId = await message_channel.send(embed=embed,file=discord.File(imageFileName))
                else:
                    sentMessageId = await message_channel.send(embed=embed)
                notificationDict[serverId].messageIds.append(sentMessageId.id)
                notificationDict[serverId].birthdayIds.append(birthday.id)
        notificationObj = Notification([],actionType)
        for serverId in notificationDict.keys():
            val = ServerRunRecordService().addServerRunRecord(notificationDict[serverId])
            notificationObj.serverRunRecords.append(val)
        NotificationService().addNotification(notificationObj)
        


