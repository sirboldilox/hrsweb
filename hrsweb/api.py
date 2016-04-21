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

        # Sort by name for lookup.
        # name: {
        #  "id": 0
        #  "units": m 
        # }
        bio_types = { rbio_type['name']: { 
                            "id":    rbio_type['id'],
                            "units": rbio_type['units']
                        }
                        for rbio_type in rbio_types
                    }

        # Invalid biometric type
        if not args.type in bio_types.keys():
            return jsonify({})      

        # Fetch biometrics for this patient and biometric type
        bio_type = bio_types[args.type]
        print(bio_type)
        biometrics = hrsdb.getBiometrics(
            args.patient_id, bio_type['id']

        )

        graph_biometrics = {
            "value": [],
            "time" : [],
            "units": bio_type['units']
        }

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


class ECGAPI(Resource):
    """
    API handler for returning basic ECG data for a patient
        GET    /api/ecg

    """
    parser = reqparse.RequestParser()
    parser.add_argument('patient_id', type=int, required=True)

    def get(self):
        """Fetch a list of ECG timestamps with id's for this patient"""
        args = self.parser.parse_args(strict=True)

        hrsdb = HRSDB(base_url)
        ecg_records = hrsdb.getECGs(args.patient_id)

        # Return JSON response
        response = {
            'response': [
                {
                    'id': record['id'],
                    'timestamp': record['timestamp']
                }
            for record in ecg_records]
        }

        print("Sending: %s" % str(response))
        return jsonify(response)

    @staticmethod
    def add(api):
        api.add_resource(ECGAPI, '/api/ecg')


class ECGDataAPI(Resource):
    """
    API handler for returning ECG graph data for a patient
        GET    /api/ecgdata

    """
    parser = reqparse.RequestParser()
    parser.add_argument('data_id', type=int, required=True)

    def get(self):
        """Fetch a data set for a given id"""
        args = self.parser.parse_args(strict=True)

        hrsdb = HRSDB(base_url)
        ecgdata = hrsdb.getECGData(args.data_id)

        # Return JSON response
        response = {
            'response': ecgdata
        }

        print("Sending: %s" % str(response))
        return jsonify(response)

    @staticmethod
    def add(api):
        api.add_resource(ECGDataAPI, '/api/ecgdata')

# Load the api
def load_api(app):
    api = Api(app)
    for resource in Resource.__subclasses__():
        resource.add(api)
