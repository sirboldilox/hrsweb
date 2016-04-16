"""
Rest API for webrecords AJAX requests

Internal API:
    /api/biometrics/<patient_id>
"""
from flask import jsonify, request, current_app
from flask_restful import Api, Resource, reqparse

from hrsweb.hrsdb import HRSDB


# Move this to the CONFIG
HRSDB_BASE_URL = 'http://localhost:8080'
base_url = HRSDB_BASE_URL


class BiometricsAPI(Resource):
    """
    API handler for returning biometric data for a patient
        GET    /api/biometrics

    """
    parser = reqparse.RequestParser()
    parser.add_argument('patient_id', type=int)
    parser.add_argument('type')

    bio_types = None


    def get(self):

        # Parse arguments
        args = self.parser.parse_args(strict=True)

        hrsdb = HRSDB(base_url)
        rbio_types = hrsdb.getBiometricTypes()
        bio_types = { rbio_type['type']: rbio_type['id'] for rbio_type in rbio_types}
        print(bio_types)

        # Invalid biometric type
        if not args.type in bio_types.keys():
            return jsonify({})      


        biometrics = hrsdb.getBiometrics(
            args.patient_id, bio_types[args.type]
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
