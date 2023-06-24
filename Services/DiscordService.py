import datetime
import discord
from Services.BirthdayService import BirthdayService
from Services.ImageCache import ImageCache
from Models.ServerRunRecord import ServerRunRecord

from Services.NotificationService import NotificationService
from Services.ServerRunRecordService import ServerRunRecordService
from Services.ServerService import ServerCache
from Helpers.EmbedGenerator import get_birthday_notification_embed, get_monthly_birthday_embed
from Models.Notification import Notification
from Helpers.TimeHelper import today_in_tz


class DiscordService:
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @staticmethod
    async def delete_recent_notifications(notification_type):
        # get latest run record of either month or daily notification type
        latest_run_record = NotificationService().get_latest_notification_record(notification_type);
        if latest_run_record is not None:
            for serverRunRecordId in latest_run_record.serverRunRecords:
                server_run_record = ServerRunRecordService().getServerRunRecordById(serverRunRecordId)
                channel_id = ServerCache().get(server_run_record.serverId).channelId
                message_channel = DiscordService.client.get_channel(int(channel_id))
                for messageId in server_run_record.messageIds:
                    try:
                        msg = await message_channel.fetch_message(messageId)
                        await msg.delete()
                    except Exception as e:
                        print("Failed to delete message in server:" + server_run_record.serverId)
                        print(e)

    @staticmethod
    async def send_birthday_notifications(action_type):
        birthdays = None
        if action_type == "monthly":
            birthdays = BirthdayService().month_bdays()
        else:
            birthdays = BirthdayService().today_bdays()
        if action_type == "monthly":
            birthdays = sorted(birthdays,
                               key=lambda x: datetime.datetime.strptime(x.date, "%d-%m-%Y").date().replace(
                                   year=today_in_tz().year))
        notification_dict = {}
        for birthday in birthdays:
            for serverId in birthday.servers:
                if notification_dict.get(serverId) is None:
                    notification_dict[serverId] = ServerRunRecord(serverId, [], [])
                if action_type == "monthly":
                    embed = get_monthly_birthday_embed(birthday)
                else:
                    embed = get_birthday_notification_embed(birthday)
                channel_id = ServerCache().get(serverId).channelId
                message_channel = None
                while message_channel is None:
                    message_channel = DiscordService.client.get_channel(int(channel_id))
                sent_message_id = None
                if birthday.imageUrl and len(birthday.imageUrl) > 0:
                    image_file_name = ImageCache.get_image(birthday.imageUrl)
                    sent_message_id = await message_channel.send(embed=embed, file=discord.File(image_file_name))
                else:
                    sent_message_id = await message_channel.send(embed=embed)
                notification_dict[serverId].messageIds.append(sent_message_id.id)
                notification_dict[serverId].birthdayIds.append(birthday.id)
        notification_obj = Notification([], action_type)
        for serverId in notification_dict.keys():
            val = ServerRunRecordService().addServerRunRecord(notification_dict[serverId])
            notification_obj.serverRunRecords.append(val)
        NotificationService().add_notification(notification_obj)
