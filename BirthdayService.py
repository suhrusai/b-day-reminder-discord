import random
import discord
from Constants import BIRTHDAY_MESSSAGE_THUMBNAIL, EMBED_COLORS, TIMEZONE
from FirebaseConnect import FirebaseConnect
from Helpers.TimeHelper import todayInTZ
from Models.Birthday import Birthday
from datetime import date
from Helpers.TimeHelper import todayInTZ
from datetime import datetime, date
import re
def downloadAllBirthdays():
    db = FirebaseConnect().getDbReference()
    query = db.collection('birthdays')
    docs = query.stream()
    birthdays = list(map(generateBirthdayObject,docs))
    return birthdays
def generateBirthdayObject(document):
    documentDict = document.to_dict()
    return Birthday(
        name = documentDict['name'],
        gender = documentDict['gender'],
        date = documentDict['date'],
        images = documentDict['images'],
        imageUrl = documentDict.get('imageUrl'),
        id = document.id,
        servers = documentDict['servers']
        )
class BirthdayService():
    birthdays = None
    def __init__(self,refresh=False):
        if(BirthdayService.birthdays == None or refresh):
            BirthdayService.birthdays = downloadAllBirthdays()
    def todayBdays(self):
        regex = todayInTZ().strftime('%d-%m')+'-\d{4}'
        return list(filter(lambda x: re.findall(regex,x.date),self.birthdays))
    def monthBdays(self):
        regex = '\d{2}-'+todayInTZ().strftime('%m')+'-\d{4}'
        return list(filter(lambda x: re.findall(regex,x.date),self.birthdays))
    def getAgeString(age):
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
        return agestring

    def calculateAge(born):
        today = todayInTZ()
        age_in_years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        
        return age_in_years