from xml.dom import minidom
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
try:
    import StringIO
except ImportError:
    import io as StringIO
import json
import os.path
import urllib
try:
    import urllib2
except ImportError:
    import urllib.parse
import os
import time

from wcunittest import wcElement
from wcunittest import wcDBRecord

LOGFILE = 'csvFile.log'
SYSTEM_NAME = 'wctest'

TESTGROUPS = [
    {
        'name': 'Appointments Tests',
        'description': 'Appointments Tests',
        'src': 'appointments_CSV_tests.json'
    },
    {
        'name': 'Asset Import Tests',
        'description': 'Asset Import Tests',
        'src': 'asset_import_tests.json'
    },
    {
        'name': 'Chart Data Tests',
        'description': 'Chart Data Tests',
        'src': 'chartdata_tests.json'
    },
    {
        'name': 'Audiometric Tests',
        'description': 'Audiometric Tests',
        'src': 'audiometric_tests.json'
    },
    {
        'name': 'Chart Relations Tests',
        'description': 'Chart Relations Tests',
        'src': 'chart_relations_tests.json'
    },
    {
        'name': 'Clinical Encounter Tests',
        'description': 'Clinical Encounter Tests',
        'src': 'clinical_encounter_tests.json'
    },
    {
        'name': 'Completed Orders Tests',
        'description': 'Completed Orders Tests',
        'src': 'completed_orders_tests.json'
    },
    {
        'name': 'Fee Schedule Tests',
        'description': 'Fee Schedule Tests',
        'src': 'fee_schedule_tests.json'
    },
    {
        'name': 'Injections Tests',
        'description': 'Injections Tests',
        'src': 'injections_tests.json'
    },
    {
        'name': 'Lab Results Tests',
        'description': 'Lab Results Tests',
        'src': 'lab_results_tests.json'
    },
    {
        'name': 'Observation Codes',
        'description': 'Observation Codes',
        'src': 'observation_codes.json'
    },
    {
        'name': 'Observations Tests',
        'description': 'Observations Tests',
        'src': 'observations_tests.json'
    },
    {
        'name': 'Order Compendium Tests',
        'description': 'Order Compendium Tests',
        'src': 'order_compendium_tests.json'
    },
    {
        'name': 'Order Questions Tests',
        'description': 'Order Questions Tests',
        'src': 'order_questions_tests.json'
    },
    {
        'name': 'Panel Membership Tests',
        'description': 'Panel Membership Tests',
        'src': 'panel_membership_tests.json'
    },
    {
        'name': 'Patient Panel Status Tests',
        'description': 'Patient Panel Status Tests',
        'src': 'patient_panel_status_tests.json'
    },
    {
        'name': 'PFT Data Tests',
        'description': 'PFT Data Tests',
        'src': 'pft_data_tests.json'
    },
    {
        'name': 'Pharmacy Filter Tests',
        'description': 'Pharmacy Filter Tests',
        'src': 'pharmacy_filter_tests.json'
    },
    {
        'name': 'Respirator Fit Test Data Tests',
        'description': 'Respirator Fit Test Data Tests',
        'src': 'respirator_fit_tests.json'
    },
    {
        'name': 'Summary Documents Tests',
        'description': 'Summary Documents Tests',
        'src': 'summary_documents_tests.json'
    },
    {
        'name': 'Encounter Injury Tests',
        'description': 'Encounter Injury Tests',
        'src': 'cases_tests.json'
    }
]

if 0:
    TESTGROUPS.append(
        {
            'name': '1k CSV Tests',
            'description': '1k Row CSV file tests; Long runtime.',
            'src': '1k_csv_tests.json'
        }
    )

def addTrans(d, trans):
    d.miedb.dbExec("INSERT INTO translate (name, trans_from, trans_to) VALUES ("\
        "'{name}', '{trans_from}', '{trans_to}') ON DUPLICATE KEY UPDATE name = "\
        "VALUES(name), trans_from = VALUES(trans_from), trans_to = VALUES(trans_to);".format(**trans))

def doSQL(d, statement):
    d.miedb.dbExec(statement)

def uploadData(d, udata):
    test = udata['test']
    cgi = { 'f' : 'admin', 
            's' : 'wc_data_import', 
            'opp' : test['csv_api'].encode('utf-8'), 
            'process' : '1', 
            'import_go' : 'Upload' }
    for key, value in test['vars'].items():
        cgi[key.encode('utf-8')] = value.encode('utf-8')
    fileData = {}

    for key, value in test['files'].items():
        if value.endswith(".csv"):
            script_dir = os.path.dirname(__file__)
            rel_path = "../upload/" + value
            abs_file_path = os.path.join(script_dir, rel_path)
            if os.path.exists(abs_file_path):
                try:
                    fileData[key] = open(abs_file_path, 'r')
                except Exception as e:
                    d.reportCommandStatus('Failed to open data file: ' + abs_file_path, e, False, '', '')   
            else:
                d.reportCommandStatus('File Could Not Be Found: ' + value, '', False, '', '')
        else:
            fileData[key] = (key, value)

    udata['res'] = udata['wccurl'].multiPartPost(data=cgi, 
                                                files=fileData)
    for key, value in test['files'].items():
        if value.endswith(".csv"):
            script_dir = os.path.dirname(__file__)
            rel_path = "../upload/" + value
            abs_file_path = os.path.join(script_dir, rel_path)
            if os.path.exists(abs_file_path):
                d.reportHTML('pre', '', section='CSV File')
                d.initSubComment("<a target='_blank' href='{0}'>View CSV File</a>".format(os.path.join("..", "upload", value)))
        else:
            d.reportHTML('pre', value, section='CSV Data')

    if "Successfully imported file" in udata['res'].decode():
        d.reportHTML('pre', 'File Processed Successfully')
    else:
        d.reportCommandStatus('File Failed to Process', '', False, '', '')
        d.reportHTML('pre', udata['res'], section='WC Ouput')


    for key in fileData.keys():
        if type(fileData[key]) != tuple and not fileData[key].closed:
            fileData[key].close()

def runTestGroup(d, tests, udata):
    wccurl = udata['wccurl']
    res = udata['res']

    for test in tests:
        if len(test['files'].keys()) == 0:
            d.reportCommandStatus('Skipping test without any csv files', '', False, '', '')
        else:
            unit = d.getWCUnitTest(test['name'] if 'name' in test else 'Unnamed Test', coreCheck=False, errorScreens=False)

            for statement in test.get('setupSQL', []):
                unit.setup(doSQL, statement, reason='Modify data before test: {}'.format(statement))

            for statement in test.get('tearDownSQL', []):
                unit.teardown(doSQL, statement, reason='Modify data after test: {}'.format(statement))

            if 'verifydata' in test:
                for v in test['verifydata']:
                    # Convert the values from unicode to str
                    fieldvalues = []
                    fieldvalues.append(wcDBRecord(v['query'], v['fieldvalues']))
                    unit.verifyDB(fieldvalues, reason='DB Verification')
            unit.test(uploadData, { 'wccurl' : wccurl, 'res' : res, 'test' : test })

def main(d, _):
    base = d._base_urls[-1]
    if not base.endswith('webchart.cgi'):
        base = '{0}{1}webchart.cgi'.format(base, '' if base[-1] == '/' else '/')
    wccurl = d.getWCCurl(base)
    wccurl.setWCCookie('WCTESTSESSION')
    res = ""
    data = {}

    for group in TESTGROUPS:
        name = group.get('name')
        desc = group.get('description')
        filename = group.get('src')
        
        try:
            file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testlib', filename)
            data = open(file, 'r')
            d.startSection('{0} | {1}'.format(name, filename), comments=desc)
            if (os.path.isfile(file)):
                try:   
                    tests = json.load(data)
                    runTestGroup(d, tests, { 'wccurl' : wccurl, 'res' : res })
                except Exception as e:
                    d.reportCommandStatus('Failed to open file: ' + file, e, False, '', '')               
            else:
                d.reportCommandStatus('Failed to open test file: ' + file, '', False, '', '')
        except Exception as e:
            d.reportCommandStatus('Failed to import test list', e, False, '', '')
        d.endSection()

        if not data.closed:
            data.close()
