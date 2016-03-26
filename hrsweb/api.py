"""
Rest API for webrecords AJAX requests

Internal API:
    /api/biometrics/<patient_id>
"""
from flask import jsonify, request, current_app
from flask_restful import Api, Resource, reqparse

from webrecords.hrsdb import HRSDB


# Move this to the CONFIG
HRSDB_BASE_URL = 'http://hrsdb0:8080'
base_url = HRSDB_BASE_URL


class BiometricsAPI(Resource):
    """
    API handler for returning biometric data for a patient
        GET    /api/biometrics

    """
    parser = reqparse.RequestParser()
    parser.add_argument('patient_id')
    parser.add_argument('type_id')

    def get(self):

        # Parse arguments
        args = self.parser.parse_args(strict=True)

        hrsdb = HRSDB(base_url)
        biometrics = hrsdb.getBiometrics(
            args.patient_id, args.type_id
        )

        graph_biometrics = {
            "value": [],
            "time" : []
        }

        print("Got back this: %s" % str(biometrics))
        for biometric in biometrics:
            graph_biometrics["value"].append(biometric['value'])
            graph_biometrics["time"].append(biometric['timestamp'])


        # Return JSON response
        response = { 
            'response': graph_biometrics        
        }

        print("Sending: %s" % str(response))
        return jsonify(response)
    
    @staticmethod
    def add(api):
        api.add_resource(BiometricsAPI, '/api/biometrics')


# Load the api
def load_api(app):
    api = Api(app)
    for resource in Resource.__subclasses__():
        resource.add(api)
