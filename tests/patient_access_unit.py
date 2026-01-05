"""
    Unit tests for all WebChart permission/security related to patient access
    @owners: sgrider
"""
from wcunittest import wcElement, wcDBRecord

def dropPatientRestrictions(d, pat_id):
    d.miedb.dbExec('''DELETE FROM patient_restrictions WHERE pat_id=%s''', pat_id)

def getUserID(d, data):
    if 'user_id' in data:
        return data['user_id']
    elif 'username' in data:
        return d.miedb.dbQuery('''SELECT user_id FROM users WHERE username=%s''',
            data['username']).getRes()[0]['user_id']
    else:
        d.reportCommandStatus('user_id or username key required', '', False, '', '')

def addPatientRestriction(d, data):
    # This inserts an ALLOWED user to a restricted patient chart
    user_id = getUserID(d, data)
    d.miedb.dbExec('''INSERT INTO patient_restrictions (user_id, pat_id) VALUES (%s, %s)''',
        user_id, data['pat_id'])

def unrestrictPartition(d, wc_partition):
    d.miedb.dbExec('''UPDATE patient_partitions SET restricted=0 WHERE wc_partition=%s''',
        wc_partition)
    d.miedb.dbExec('''DELETE FROM patient_partition_restricted WHERE wc_partition=%s''',
        wc_partition)

def getRoleID(d, data):
    if 'role_id' in data:
        return data['role_id']
    elif 'role_name' in data:
        return d.miedb.dbQuery('''SELECT role_id FROM user_roles WHERE name=%s''',
            data['role_name']).getRes()[0]['role_id']
    elif 'role_description' in data:
        return d.miedb.dbQuery('''SELECT role_id FROM user_roles WHERE description=%s''',
            data['role_description']).getRes()[0]['role_id']
    else:
        d.reportCommandStatus('role_id, role_name or role_description key required', '',
            False, '', '')

def restrictPartitionToUser(d, data):
    user_id = getUserID(d, data)
    if user_id:
        d.miedb.dbExec('''UPDATE patient_partitions SET restricted=1 WHERE wc_partition=%s''',
            data['wc_partition'])
        d.miedb.dbExec('''INSERT INTO patient_partitions_restricted (id_type, wc_partition,'''\
            '''allowed_id) VALUES ('user', %s, %s) ON DUPLICATE KEY UPDATE id_type='user' ''',
            data['wc_partition'], user_id)

def dropUserPatientUser(d, data):
    user_id = getUserID(d, data)
    if user_id:
        d.miedb.dbExec('''DELETE FROM user_patients WHERE pat_id=%s AND id_type='user' '''\
            'AND id=%s''', data['pat_id'], user_id)

def insertUserPatientUser(d, data):
    user_id = getUserID(d, data)
    role_id = getRoleID(d, data)
    if user_id and role_id:
        d.miedb.dbExec('''INSERT INTO user_patients (id, id_type, pat_id, role_id) '''\
            '''VALUES (%s, 'user', %s, %s) ON DUPLICATE KEY UPDATE id_type='user' ''',
            user_id, data['pat_id'], role_id)

def setRestrictByPartition(d, data):
    user_id = getUserID(d, data)
    if user_id:
        d.miedb.dbExec('''INSERT INTO security_exception (user_id, module_name, '''\
            '''category_name, security_value) VALUES (%s, 'E-Chart','''\
            ''' 'Restrict Access by Partition', %s) ON DUPLICATE KEY UPDATE '''\
            '''security_value=%s''',
            user_id, data['value'], data['value'])

def goToChart(d, pat_id):
    d.navigate('?f=chart&s=pat&pat_id={0}'.format(str(pat_id)))

NOACCESS_MSG = [
    wcElement('xpath', '''//*[contains(text(), 'You currently do not have access to')]'''),
]
CHART_RESTRICTION_MSG = [
    wcElement('xpath', '''//*[contains(text(), 'The chart is restricted')]'''),
]
PARTITION_RESTRICTION_MSG = [
    wcElement('xpath', '''//*[contains(text(), 'Partition Restrictions')]'''),
]
PATIENT_HEADERS = [
    wcElement('id', 'wc_pat_bar'),
    wcElement('id', 'wc_patextended_bar'),
    wcElement('id', 'wc_alert_bar'),
]

def patientRestrictions(d):
    # Patient restrictions work by seeing that a chart has a record in patient_restrictions AND the user
    # attempting to access the chart in question is not allowed in patient_restrictions
    # So the absence of chart 18 in the table means he is not restricted, the presence means he is
    # and only visible to the records listed in the table
    t = d.getWCUnitTest('Verify that a patient restriction locks a user out')
    t.setup(dropPatientRestrictions, 18, reason='Clear out any existing allowances')
    t.setup(addPatientRestriction, reason='Grant a single allowance to a user (who doesn\'t even exist)',
        userdata={
            'pat_id': 18,
            'user_id': 1
        })
    t.verifyElements(NOACCESS_MSG, exists=True, reason='Expect no access message')
    t.verifyElements(CHART_RESTRICTION_MSG, exists=True, reason='Expect chart restriction message')
    t.verifyElements(PATIENT_HEADERS, exists=False, reason='Ensure the patient header bars are NOT present')
    t.test(goToChart, userdata=18, reason='Try to access the chart')

    t = d.getWCUnitTest('Verify that removing patient restrictions allows access')
    t.setup(dropPatientRestrictions, 18, reason='Clear out any existing allowances')
    t.verifyElements(NOACCESS_MSG, exists=False, reason='Expect access')
    t.verifyElements(CHART_RESTRICTION_MSG, exists=False, reason='Expect access')
    t.verifyElements(PATIENT_HEADERS, exists=True, reason='Ensure the patient header bars ARE present')
    t.test(goToChart, userdata=18, reason='Try to access the chart')

def partitionRestrictions(d):
    t = d.getWCUnitTest('Verify that a partition restriction locks a user out of a given chart')
    t.setup(restrictPartitionToUser, {
        'pat_id': 18,
        'username': 'dave',
        'wc_partition': 'mie',
    }, reason='Only dave has access to this chart')
    t.setup(dropUserPatientUser, {
        'pat_id': 18,
        'username': 'selenium'
    }, reason='Ensure selenium has no user relationship to the patient')
    t.setup(setRestrictByPartition, {
        'username': 'selenium',
        'value': 1,
    }, reason='Ensure selenium respects restricted partitions')
    t.verifyElements(NOACCESS_MSG, exists=True, reason='Expect no access message')
    t.verifyElements(PARTITION_RESTRICTION_MSG, exists=True, reason='Expect partition message')
    t.verifyElements(PATIENT_HEADERS, exists=False, reason='No access') 
    t.test(goToChart, 18)

    t = d.getWCUnitTest('Verify that a partition restrictions allow a user-patient relationship')
    t.setup(restrictPartitionToUser, {
        'pat_id': 18,
        'username': 'dave',
        'wc_partition': 'mie',
    }, reason='Only dave has access to this chart')
    t.setup(insertUserPatientUser, {
        'pat_id': 18,
        'role_name': 'Family Medicine',
        'username': 'selenium',
    }, reason='Add a relationship of Family Medicine for selenium -> Hart, William')
    t.setup(setRestrictByPartition, {
        'username': 'selenium',
        'value': 1,
    }, reason='Ensure selenium respects restricted partitions')
    t.verifyElements(NOACCESS_MSG, exists=False, reason='Do not expect no access message')
    t.verifyElements(PARTITION_RESTRICTION_MSG, exists=False, reason='Do not expect partition message')
    t.verifyElements(PATIENT_HEADERS, exists=True, reason='Expect patient access') 
    t.test(goToChart, 18)

def main(d, WCURL):
    d.startSection('Patient Restrictions')
    patientRestrictions(d)
    d.endSection()

    d.startSection('Partition Restrictions')
    partitionRestrictions(d)
    d.endSection()
