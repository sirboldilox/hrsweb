"""
Plain models of database records
"""

class Patient(object):
    """
    Patitent object

    :param id:              Uniquie identifier for the patient
    :param first_name:      First name of the patient
    :param last_name:       Last name of the patient
    :param gender:          Gender of the patient - Male(0) Female(1)
    :param date_of_birth:   Date of birth of the patient
    """
    fields = ['id', 'first_name', 'last_name',
              'gender', 'date_of_birth']

    def __init__(self, id, first_name, last_name, gender, date_of_birth):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth


    def from_json(self, json_obj):
        return Patient(**json_obj)


class BiometricType(object):
    pass
