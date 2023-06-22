import random
from datetime import datetime
import discord
from BirthdayService import BirthdayService
from Constants import BIRTHDAY_MESSSAGE_THUMBNAIL, EMBED_COLORS, TIMEZONE
from Helpers.TimeHelper import todayInTZ

def getMonthlyBirthdayEmbed(birthday):
    today = todayInTZ()
    bdayDate = datetime.strptime(birthday.date, "%d-%m-%Y").date()
    age = BirthdayService.calculateAge(bdayDate)
    embed=None
    color = EmbedGenerator.getEmbedColor()
    embed = discord.Embed(color=color)
    embed.add_field(name="Name", value="{}".format(birthday.name), inline=False)
    embed.add_field(name="Date of Birth", value="{}".format(birthday.date))
    embed.add_field(name="Age(To be)",
                    value="{} Years".format(age),
                    inline=True)
    embed.set_footer(text="{}({}).  Developed by Sai Suhrut".format(
        today.strftime(" %d/%m/%Y, %H:%M:%S"), TIMEZONE))
    return embed

def getBirthdayNotificationEmbed(birthday):
    today = todayInTZ()
    bdayDate = datetime.strptime(birthday.date, "%d-%m-%Y").date()
    age = BirthdayService.calculateAge(bdayDate)
    color = EmbedGenerator.getEmbedColor()
    ageString = BirthdayService.getAgeString(age)
    gender_string = " on her " if birthday.gender == "F" else " on his "
    embed = discord.Embed(title="Wish {}{}{}{} Birthday🎂".format(
        birthday.name, gender_string, age, ageString), color=color)
    embed.add_field(name="Name", value="{}".format(birthday.name), inline=False)
    embed.add_field(name="Date of Birth", value="{}".format(birthday.date))
    embed.add_field(name="Age",
                    value="{} Years".format(age),
                    inline=True)
    embed.set_footer(text="{}({}).  Developed by Sai Suhrut".format(
        today.strftime(" %m/%d/%Y, %H:%M:%S"), TIMEZONE))
    embed.set_thumbnail(
        url=BIRTHDAY_MESSSAGE_THUMBNAIL)
class EmbedGenerator():
    embedColorIndex = 0
    def getEmbedColor():
        totalEmbedColors = len(EMBED_COLORS)
        color= EMBED_COLORS[EmbedGenerator.embedColorIndex]
        EmbedGenerator.embedColorIndex = (EmbedGenerator.embedColorIndex + 1 ) % totalEmbedColors
        return color