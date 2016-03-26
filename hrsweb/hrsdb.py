"""
Wrapper around the REST api for HRSDB


"""
import logging
import requests

# Log adapter
logs = logging.getLogger(__name__)


class HRSDB(object):

    GET  = 0
    POST = 1
    PUT  = 2

    def __init__(self, base_url):
        self.base_url = base_url


    def getPatient(self, patient_id):
        """Get a single patient record
        :param int patient_id:  ID of the patient to get
        """

        url = "%s/patient/%d" % (self.base_url, patient_id)
        return self._call(url, self.GET)


    def getPatients(self):
        """Get all patients in the database"""

        url = "%s/patients" % (self.base_url)
        return self._call(url, self.GET)


    def getBiometrics(self, patient_id, biometric_type_id):
        """Get all biometrics in the database for a patient"""

        url = "%s/biometrics" % (self.base_url)
        data = {
            'patient_id': patient_id,
            'biometric_type_id': biometric_type_id
        }

        return self._call(url, self.GET, data=data)
        

    def _call(self, url, method, data=None):
        """Call the request and handle errors"""
        
        if method is self.GET:
            req = requests.get(url, data=data)
        elif method is self.POST:
            req = requests.post(url, data=data)
        elif method is self.PUT:
            req = requests.put(url, data=data)

        print(req.text)

        json = req.json()
        return json['response']
            
        

