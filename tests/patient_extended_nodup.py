from wcunittest import wcElement, wcDBRecord

def insertReport(d, data):
    sql = "REPLACE INTO system_reports (%s) VALUES (%s)" %(','.join(data.keys()),
        ','.join(['%s'] * len(data)))
    d.miedb.dbExec(sql, *data.values())
    d.wcutils.SetSystemSetting('System', 'Reports', 'Max Threads', '10', False)

def editPermission(d, value):
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
        "WHERE module_name='Control' AND category_name='Manage System Reports' "\
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
        "username=%s)", value, d.getUserData('selenium_username'))

def executeReport(d, data):
    cgi = ''
    if isinstance(data, str):
        name = data
    elif isinstance(data, dict):
        name = data.get('name')
        cgi = data.get('cgi')
    d.navigate('?f=admin&s=system_report&opp=query&submit_query&report_name={0}&{1}'.format(
        name, cgi))

def doPerform(d, data):
    d.clickElement(text='Perform')
    d.clickElement(value='Perform All')

def main(d, WCURL):
    reportName = 'Insert Pat Ext'

    u = d.getWCUnitTest('Perform report to insert patient extended threaded to duplicate name')

    u.setup(insertReport, {'name': reportName, 'sql_query': "SELECT pat_id, '?f=ajaxpost&s=patextadd&name=duplicatename&value=1' AS `URL` FROM patients"})
    u.setup(editPermission, 2)
    u.setup(executeReport, reportName)

    u.verifyElements([
        wcElement('xpath', "//div[text()='Perform operation completed']"),
        wcElement('xpath', "//div[contains(., '( 1 ) Performed action')]"),
        wcElement('xpath', "//div[contains(., 'records from system report ({0})')]".format(reportName))
    ], reason='Make sure report performed', timeout=30)

    u.verifyDB(wcDBRecord("FROM patient_extended_index WHERE name='duplicatename'", {
        'count(*)': 1,
    }), reason='Expect 1 row')

    u.test(doPerform)
