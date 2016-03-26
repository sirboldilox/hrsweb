"""
Database REST service handler
"""
import requests

class DBHandler(object):
    """
    Handles access to the health record database via
    the REST API
    """
    GET  = 0
    POST = 1
    PUT  = 2

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = "http://%s:%s" % (self.host, self.port)


    def get_patient(self, id):
        url = self.url + '/patients'
        rdata = self._call(url, self.GET)
        return rdata

    def get_patients(self):
        url = self.url + '/patients'
        rdata = self._call(url, self.GET)
        return rdata

        
    def _call(self, url, method):
        """
        Wrappper for calls to the DB API
        """
        response = None
        if method == self.GET:
            response = requests.get(url)
        if method == self.POST:
            response = requests.post(url)
        if method == self.PUT:
            response = requests.put(url)
        
        # Check for errors
        print(response.text)
        rdata = response.json()['data']

        return rdata


class ResquestError(Exception):
    pass
