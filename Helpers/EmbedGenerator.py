from datetime import datetime
import discord
from Services.BirthdayService import BirthdayService
from Constants import BIRTHDAY_MESSAGE_THUMBNAIL, EMBED_COLORS, TIMEZONE
from Helpers.TimeHelper import today_in_tz


def get_monthly_birthday_embed(birthday):
    today = today_in_tz()
    bday_date = datetime.strptime(birthday.date, "%d-%m-%Y").date()
    age = BirthdayService.calculate_age(bday_date)
    embed = None
    color = EmbedGenerator.get_embed_color()
    embed = discord.Embed(color=color)
    embed.add_field(name="Name", value="{}".format(birthday.name), inline=False)
    embed.add_field(name="Date of Birth", value="{}".format(birthday.date))
    embed.add_field(name="Age(To be)",
                    value="{} Years".format(age),
                    inline=True)
    embed.set_footer(text="{}({}).  Developed by Sai Suhrut".format(
        today.strftime(" %d/%m/%Y, %H:%M:%S"), TIMEZONE))
    return embed


def get_birthday_notification_embed(birthday):
    today = today_in_tz()
    bday_date = datetime.strptime(birthday.date, "%d-%m-%Y").date()
    age = BirthdayService.calculate_age(bday_date)
    color = EmbedGenerator.get_embed_color()
    age_string = BirthdayService.get_age_string(age)
    gender_string = " on her " if birthday.gender == "F" else " on his "
    embed = discord.Embed(title="Wish {}{}{}{} Birthday🎂".format(
        birthday.name, gender_string, age, age_string), color=color)
    embed.add_field(name="Name", value="{}".format(birthday.name), inline=False)
    embed.add_field(name="Date of Birth", value="{}".format(birthday.date))
    embed.add_field(name="Age",
                    value="{} Years".format(age),
                    inline=True)
    embed.set_footer(text="{}({}).  Developed by Sai Suhrut".format(
        today.strftime(" %m/%d/%Y, %H:%M:%S"), TIMEZONE))
    embed.set_thumbnail(
        url=BIRTHDAY_MESSAGE_THUMBNAIL)
    return embed


class EmbedGenerator:
    embedColorIndex = 0

    @staticmethod
    def get_embed_color():
        total_embed_colors = len(EMBED_COLORS)
        color = EMBED_COLORS[EmbedGenerator.embedColorIndex]
        EmbedGenerator.embedColorIndex = (EmbedGenerator.embedColorIndex + 1) % total_embed_colors
        return color
