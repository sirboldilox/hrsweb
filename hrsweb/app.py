"""
Webserver
"""
from collections import OrderedDict
from flask import Flask, url_for, redirect, render_template, request

from webrecords.api import load_api
from webrecords.hrsdb import HRSDB


# Global web app
webapp = Flask(__name__)
load_api(webapp)

# Move this to the CONFIG
HRSDB_BASE_URL = 'http://hrsdb0:8080'

# Dummy patient list
dummy_patients = {
    1 : "Test 1",
    2 : "Test 2",
    3 : "Test 3"
}


# Default page
@webapp.route('/')
def index():
    base_url = HRSDB_BASE_URL
    hrsdb = HRSDB(base_url)
    patients = hrsdb.getPatients()
    return render_template('index.html', patients=patients)


# Route for search receipts page
@webapp.route('/patient')
def patient():
    patient_id = int(request.args.get('id'))
    base_url = HRSDB_BASE_URL
    hrsdb = HRSDB(base_url)
    patient = hrsdb.getPatient(patient_id)

    print(patient_id)
    return render_template('patient.html', patient=patient)
