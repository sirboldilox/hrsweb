"""
Wrapper around the REST api for HRSDB


"""
import logging
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError

# Log adapter
logs = logging.getLogger(__name__)


class HRSDB(object):

    GET  = 0
    POST = 1
    PUT  = 2

    DEFAULT_TIMEOUT = 2

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


    def getBiometrics(self, patient_id, type_id):
        """Get all biometrics in the database for a patient"""

        url = "%s/biometrics" % (self.base_url)
        data = {
            'patient_id': patient_id,
            'biometric_type_id': type_id
        }

        return self._call(url, self.GET, data=data)

    def getBiometricTypes(self):
        """Get all biometric types in the database"""

        url = "%s/biometric_types" % (self.base_url)

        return self._call(url, self.GET)

    def getECGs(self, patient_id):
        """Get all ecg records (without raw data) for a patient"""

        url = "%s/ecg" % (self.base_url)
        data = {
            'patient_id': patient_id
        }

        return self._call(url, self.GET, data=data)

    def getECGData(self, data_id):
        """Get raw ECG data for graphing for a given id"""

        url = "%s/ecgdata" % (self.base_url)
        data = {
            'id': data_id
        }

        return self._call(url, self.GET, data=data)

    def _call(self, url, method, data=None):
        """Call the request and handle errors"""
        print(url)
        print(data)
        try:
            if method is self.GET:
                req = requests.get(url, data=data, timeout=self.DEFAULT_TIMEOUT)
            elif method is self.POST:
                req = requests.post(url, data=data, timeout=self.DEFAULT_TIMEOUT)
            elif method is self.PUT:
                req = requests.put(url, data=data, timeout=self.DEFAULT_TIMEOUT)

            # Check status code
            req.raise_for_status()
        except ConnectionError as error:
            raise APIError("Failed to connect to remote database")
        except Timeout as error:
            raise APIError("Failed to connect to remote database (T)")
        except HTTPError as error:
            raise APIError("Unknown record")

        json = req.json()
        return json['response']
            
        
class APIError(Exception):
    """Generic exception class for erros thrown by the database interface"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
        
