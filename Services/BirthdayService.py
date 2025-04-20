import re

from FirebaseConnect import FirebaseConnect
from Helpers.TimeHelper import today_in_tz
from Models.Birthday import Birthday


def download_all_birthdays():
    db = FirebaseConnect().get_db_reference()
    query = db.collection('birthdays')
    docs = query.stream()
    birthdays = list(map(generate_birthday_object, docs))
    return birthdays


def generate_birthday_object(document):
    document_dict = document.to_dict()
    return Birthday(
        name=document_dict['name'],
        gender=document_dict['gender'],
        date=document_dict['date'],
        images=document_dict['images'],
        image_url=document_dict.get('imageUrl'),
        firebase_id=document.id,
        servers=document_dict['servers']
    )


class BirthdayService:
    birthdays = None

    def __init__(self, refresh=False):
        if BirthdayService.birthdays is None or refresh:
            BirthdayService.birthdays = download_all_birthdays()

    def today_bdays(self):
        regex = today_in_tz().strftime(r'%d-%m') + r'-\d{4}'
        return list(filter(lambda x: re.findall(regex, x.date), self.birthdays))

    def month_bdays(self):
        regex = r'\d{2}-' + today_in_tz().strftime('%m') + r'-\d{4}'
        return list(filter(lambda x: re.findall(regex, x.date), self.birthdays))

    @staticmethod
    def get_age_string(age):
        age_string = ""
        if age % 10 == 1:
            age_string = "st "
        elif age % 10 == 2:
            age_string = "nd "
        elif age % 10 == 3:
            age_string = "rd "
        elif age == 11 or age == 12 or age == 12:
            age_string = " th "
        elif age:
            age_string = "th "
        return age_string

    @staticmethod
    def calculate_age(born):
        today = today_in_tz()
        age_in_years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        return age_in_years
