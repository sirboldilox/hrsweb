"""
Webserver
"""
from collections import OrderedDict
from flask import Flask, url_for, redirect, render_template, request

from hrsweb.api import load_api
from hrsweb.hrsdb import HRSDB, APIError


# Global web app
webapp = Flask(__name__)
load_api(webapp)

# Move this to the CONFIG
HRSDB_BASE_URL = 'http://localhost:8080'

# Dummy patient list
dummy_patients = {
    1 : "Test 1",
    2 : "Test 2",
    3 : "Test 3"
}

# Error page
def error(msg):
    return render_template('error.html', error=msg)

# Default page
@webapp.route('/')
def patients_list():
    base_url = HRSDB_BASE_URL
    hrsdb = HRSDB(base_url)
        
    patients = None
    try:
        patients = hrsdb.getPatients()
    except APIError as exc:
        return error(repr(exc))

    return render_template('patient_list.html', patients=patients)


# Route for search receipts page
@webapp.route('/patient')
def patient():
    patient_id = int(request.args.get('id'))
    base_url = HRSDB_BASE_URL
    hrsdb = HRSDB(base_url)

    error = None
    patient = None
    try:
        patient = hrsdb.getPatient(patient_id)
    except APIError as exc:
        error = str(exc)

    print(patient)

    # Convert gender int to string
    if patient['gender'] == 0:
        patient['gender'] = 'Male'
    else:
        patient['gender'] = 'Female'

    return render_template('patient.html', patient=patient, error=error)

