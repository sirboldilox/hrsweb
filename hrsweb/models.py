"""
Plain models of database records
"""
from datetime import datetime


# Dateformat used across apps
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


class Patient(object):
    """
    Patitent object

    :param id:              Uniquie identifier for the patient
    :param first_name:      First name of the patient
    :param last_name:       Last name of the patient
    :param gender:          Gender of the patient - Male(0) Female(1)
    :param date_of_birth:   Date of birth of the patient
    """
    GENDER_MALE = 1
    GENDER_FEMALE = 2

    def __init__(self, id, first_name, last_name, gender, date_of_birth):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = datetime.strptime(date_of_birth, DATE_FORMAT)

    @classmethod
    def from_dict(cls, pdict):
        return Patient(
            pdict['id'],
            pdict['first_name'],
            pdict['last_name'],
            pdict['gender'],
            pdict['date_of_birth']
        )

    def get_name(self):
        """Returns the patient full name"""
        return "%s %s" % (
            self.first_name,
            self.last_name
        )

    def get_age(self):
        """Returns the patient age as a string"""
        today = datetime.now()
        return today.year \
            - self.date_of_birth.year \
            - ((today.month, self.date_of_birth.day) \
            < (self.date_of_birth.month, self.date_of_birth.day)) \

    def get_gender(self):
        """Returns the patient gender as a string"""
        if self.gender == self.GENDER_MALE:
            return 'Male'
        else:
            return 'Female'


class BiometricType(object):
    pass
