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

from wcunittest import wcDBRecord
from datetime import datetime, timedelta, time


TESTGROUPS = [
    {
        'name': 'HL7 Inbound labs',
        'description': 'Lab reports',
        'src': 'hl7inbound_tests.json'
    },
    {
        'name': 'HL7 Inbound Order Requests',
        'description': 'Incoming order requests',
        'src': 'inbound_order_requests.json'
    },
    {
        'name': 'Rad Orders',
        'description': 'Radiology order/encounter workflow',
        'src': 'rad_orders_hl7.json'
    },
    {
        'name': 'Demographics',
        'description': 'Demographics workflows',
        'src': 'demographics.json'
    },
    {
        'name': 'Appointments',
        'description': 'Appointments workflows',
        'src': 'appointments.json'
    },
    {
        'name': 'Documents',
        'description': 'Documents, Documents, and more documents!',
        'src': 'documents.json'
    },
    {
        'name': 'VXU Tests',
        'description': 'Tests for running HL7 Messages with VXU elements',
        'src': 'hl7_vxu_tests.json'
    },
    {
        'name': 'MFN Tests',
        'description': 'EO Updates with MFN message type',
        'src': 'hl7_mfn_tests.json'
    }
]

def updateConf(d, data):
    if 'conf' in data.keys() and 'name' in data['conf'].keys() and 'vars' in data['conf'].keys():
        wccurl = data['_curl']
        res = wccurl.get('?f=ajaxget&s=layout&active=1&module=hl7&module_exact=1&name={name}'.format(**data['conf']))
        if not res:
            d.reportCommandStatus('Ajax query for conf layout returned no response', '', False, '', '')
            return
        try:
            dom = minidom.parse(StringIO.StringIO(res))
        except Exception as e:
            d.reportCommandStatus('Failed to parse layout XML', '', False, res, e)
            return
        layouts = dom.getElementsByTagName('LAYOUT')
        if len(layouts) > 1:
            d.reportCommandStatus('Found > 1 Layout', len(layouts), False, '', '')
            return
        elif len(layouts) == 0:
            d.reportCommandStatus('Layout not found', data['conf']['name'], False, '', '')
            return
        source = layouts[0].attributes['layout_html'].value
        for key, value in data['conf']['vars'].items():
            source = source.replace(key, value)
        d.reportHTML('pre', source, 'Modified Conf Data')
        d.miedb.dbExec("REPLACE INTO layout (name, module, layout_html, active) VALUES ("\
            "'{name}', 'hl7', '{html}', 1)".format(**{
                'name': data['conf']['name'],
                'html': source,
            }))

def isAckSuccess(d, msg):
    msgValues = msg.split(b'|')
    msaIndex = msgValues.index(b'\rMSA')
    return msgValues[msaIndex + 1] == b'AA'

def uploadHL7(d, data):
    wccurl = data['_curl']
    # Normalize hl7 message
    data['message'] = data['message'].replace('\r\n', '\r').replace('\n', '\r')
    d.reportHTML('pre', data['message'], 'HL7 Message')
    ret = wccurl.post(data={
        'f': 'wchl7',
        'interface': data['interface'],
        'message': data['message']
    })
    d.reportHTML('pre', ret, 'WebChart Response')
    if not isAckSuccess(d, ret):
        # This is only a failure if the test data doesn't expect an error ack
        if 'expectErrorAck' in data and data['expectErrorAck']:
            d.reportCommandStatus('Caught Webchart Unsuccessful Ack', '', True, '', 'MSA.1 was not \'AA\'')
        else:
            d.reportCommandStatus('ERROR: Received Unsuccessful Ack', '', False, '', 'MSA.1 was not \'AA\'')

def addTrans(d, trans):
    d.miedb.dbExec("INSERT INTO translate (name, trans_from, trans_to) VALUES ("\
        "'{name}', '{trans_from}', '{trans_to}') ON DUPLICATE KEY UPDATE name = "\
        "VALUES(name), trans_from = VALUES(trans_from), trans_to = VALUES(trans_to);".format(**trans))

def doSQL(d, statement):
    d.miedb.dbExec(statement)

def runTestGroup(d, wccurl, tests, ignores):
    # These replaces the values for referenced fields in the hl7inbound test files
    for test in tests:
        test['conf']['vars']['${WCTUSER}'] = d.getUserData('developer')
        test['conf']['vars']['hl7alert@med-web.com'] = '{0}@mieweb.com'.format(d.getUserData('developer'))
        if 'verifydata' in test:
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'a.createdate' in entry['fieldvalues']:
                    entry['fieldvalues']['a.createdate'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'create_date' in entry['fieldvalues']:
                    entry['fieldvalues']['create_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'd.origin_date' in entry['fieldvalues']:
                    entry['fieldvalues']['d.origin_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'dt.origin_date' in entry['fieldvalues']:
                    entry['fieldvalues']['dt.origin_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 't.entry_date' in entry['fieldvalues']:
                    entry['fieldvalues']['t.entry_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'dt.service_date' in entry['fieldvalues']:
                    original_datetime = datetime.strptime(d.getUserData('run_datetime'), '%Y-%m-%d %H:%M:%S')
                    modified_datetime = datetime(original_datetime.year, original_datetime.month, original_datetime.day)
                    modified_datetime = datetime.combine(original_datetime.date(), time.min)
                    entry['fieldvalues']['dt.service_date'] = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'enter_date' in entry['fieldvalues']:
                    entry['fieldvalues']['enter_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'entered_date' in entry['fieldvalues']:
                    entry['fieldvalues']['entered_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'o.create_datetime' in entry['fieldvalues']:
                    entry['fieldvalues']['o.create_datetime'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'u.create_date' in entry['fieldvalues']:
                    entry['fieldvalues']['u.create_date'] = d.getUserData('run_datetime')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'observed_datetime' in entry['fieldvalues']:
                    original_datetime = datetime.strptime(d.getUserData('run_datetime'), '%Y-%m-%d %H:%M:%S')
                    modified_datetime = original_datetime + timedelta(seconds=1)
                    entry['fieldvalues']['observed_datetime'] = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')
            for entry in test['verifydata']:
                if 'fieldvalues' in entry and 'o1.observed_datetime' in entry['fieldvalues']:
                    original_datetime = datetime.strptime(d.getUserData('run_datetime'), '%Y-%m-%d %H:%M:%S')
                    modified_datetime = original_datetime + timedelta(seconds=1)
                    entry['fieldvalues']['o1.observed_datetime'] = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')

        if not 'message' in test:
            d.reportCommandStatus('Skipping test without a message object', '', False, '', '')

        # Store a reference to the curl to prevent repeated re-initializations
        test['_curl'] = wccurl
        unit = d.getWCUnitTest(test['name'] if 'name' in test else 'Unnamed Test', coreCheck=False, errorScreens=False)
        unit.setup(updateConf, test, reason='Modify conf file')

        for trans in test.get('translations', []):
            unit.setup(addTrans, trans, reason='Add custom translation: {name}:{trans_from}=>{trans_to}'.format(**trans))

        for statement in test.get('setupSQL', []):
            unit.setup(doSQL, statement, reason='Modify data before test: {}'.format(statement))

        for statement in test.get('tearDownSQL', []):
            unit.teardown(doSQL, statement, reason='Modify data after test: {}'.format(statement))

        for ignore in test.get('ignores', []):
            ignores.append(ignore)

        unit.setup(uploadHL7, test, reason='Upload the hl7 message')

        # Generate the verify section from the data in the JSON
        if 'verifydata' in test:
            # Loop array and instantiate wcdb records
            test['verify'] = []
            for v in test['verifydata']:
                test['verify'].append(wcDBRecord(v['query'], v['fieldvalues']))
            unit.verifyDB(test['verify'], reason='DB Verification')

        unit.test()

    for ignore in ignores:
        d.wcErrorLog.ignore(ignore)

def main(d, WCURL):
    base = d._base_urls[-1]
    tests = None
    if not base.endswith('webchart.cgi'):
        base = '{0}{1}webchart.cgi'.format(base, '' if base[-1] == '/' else '/')
    d.reportCommandStatus('Using Base Url', base, True, '', '')
    wccurl = d.getWCCurl(base, None, None, None)
    wccurl.setWCCookie('WCTESTSESSION')
    ignores = []

    for testgroup in TESTGROUPS:
        name = testgroup.get('name')
        desc = testgroup.get('description')
        filename = testgroup.get('src')

        try:
            d.startSection('{0} | {1}'.format(name, filename), comments=desc)
            tests = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testlib', filename)))
            runTestGroup(d, wccurl, tests, ignores)
        except Exception as e:
            d.reportCommandStatus('Failed to import test list', e, False, '', '')
            d.endSection()
            return
        d.endSection()

