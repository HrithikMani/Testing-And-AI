"""
    @owner: sgrider
    @filedep: src/wccron*.c, include/wccron*.h
"""
from wcunittest import wcElement, wcJSCode, wcDBRecord

jobsListview = wcElement('xpath', "//span[@class='LVTitle'][contains(.,'Scheduled Jobs')]", exists=True)

def checkSource(d, data):
    d.reportCommandStatus('Check Source', data, data in d.getWebDriver().page_source, '', '')

def listJobs(d):
    d.navigate('?f=admin&s=cron')

def enable(d, value):
    d.miedb.dbExec("UPDATE system_settings SET value=%s WHERE module='System' "\
        "AND section='Cron' AND item='Enable Cron Manager'", value)

def editPermission(d, value):
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
        "WHERE module_name='Control' AND category_name='Manage Scheduled Jobs' "\
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
        "username=%s)", value, d.getUserData('selenium_username'))

def setDefaultUser(d, username):
    d.miedb.dbExec("UPDATE system_settings SET value=(SELECT user_id FROM users WHERE "\
        "username=%s) WHERE module='System' AND section='Cron' AND item='Default User'", username)

def addDB(d, data, table, exclude=[]):
    return d.miedb.dbExec("REPLACE INTO {0} ({1}) VALUES ({2})".format(table,
        ','.join(["{0}".format(k) for k, v in data.items() if k not in exclude]),
        ','.join(["'{0}'".format(v.replace("'", "\\'") if isinstance(v, str) else v) for k, v in data.items() if k not in exclude])))

def addJob(d, data):
    res = addDB(d, data, 'cron', ['email_address'])
    cron_id = res.lastrowid
    if cron_id:
        d.miedb.dbExec('DELETE FROM cron_ext_options WHERE id=%s', cron_id)
        if 'email_address' in data.keys():
            if isinstance(data['email_address'], str):
                data['email_address'] = [data['email_address']]
            for e in data['email_address']:
                addDB(d, {
                    'id': cron_id,
                    'type': 'EMAIL',
                    'value': e
                }, 'cron_ext_options')

def addSystemReport(d, data):
    addDB(d, data, 'system_reports')

def enterJob(d, data):
    dates = ('MONTH', 'DAY', 'YEAR', 'TIME')
    rctypes = ('', 'Minutely', 'Hourly', 'Daily', 'Weekly', 'Monthly')
    if 'name' in data:
        d.enterFormData(data.get('name'), id='name')
    if 'description' in data:
        d.enterFormData(data.get('description'), id='description')
    if 'type' in data:
        d.enterFormData(data.get('type'), id='type')
    if 'operation' in data:
        d.enterFormData(data.get('operation'), id='operation')
    if 'cgi' in data:
        d.enterFormData(data.get('cgi'), id='cgi')
    if 'method' in data:
        d.enterFormData(data.get('method'), id='method')
    if 'firstrun' in data:
        for idx, val in enumerate(data.get('firstrun')):
            d.enterFormData(val, id='firstrun{0}'.format(dates[idx]))
    if 'endrun' in data:
        for idx, val in enumerate(data.get('endrun')):
            d.enterFormData(val, id='endrun{0}'.format(dates[idx]))
    if 'recurrence' in data:
        d.enterFormData(data.get('recurrence'), id='rc_type')
        if 'recurrence_options' in data:
            for x in data.get('recurrence_options'):
                d.enterFormData(True,
                    xpath="//div[@id='recurrence_{0}']//input[@value='{1}']".format(
                        rctypes.index(data.get('recurrence')), x))
    if 'logic' in data:
        d.enterFormData(data.get('logic'), id='recurrence_logic')
    if 'active' in data:
        d.enterFormData(data.get('active'), id='active')
        
def executeJob(d, name):
    res = d.miedb.dbQuery("SELECT id FROM cron WHERE name=%s", name)
    if res and res.numRows():
        d.navigate('?f=admin&s=cron&opp=execute&id={0}'.format(res.getRow(0)['id']))
    else:
        d.reportCommandStatus('Failed to query job', name, False, res.dbError(), '')

def main(d, WCURL):
    d.startSection('Configuration / Permissions')
    wcunit = d.getWCUnitTest('Verify Disabled')
    wcunit.setup(enable, 0)
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='warning'][contains(.,'Scheduled jobs are not yet enabled on this system')]"),
        wcElement('xpath', "//span[@class='warning'][contains(.,'Scheduled jobs will not run until the configuration is corrected')]"),
        jobsListview,
], reason='Ensure the message about being disabled shows up')
    wcunit.test()

    wcunit = d.getWCUnitTest('Verify Enabled')
    wcunit.setup(enable, 1)
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='warning'][contains(.,'Scheduled jobs are not yet enabled on this system')]", exists=False),
        wcElement('xpath', "//span[@class='warning'][contains(.,'Scheduled jobs will not run until the configuration is corrected')]", exists=False),
        jobsListview,
    ], reason='Ensure the message about being disabled does not show up')
    wcunit.test()

    wcunit = d.getWCUnitTest('Verify Missing Default User')
    wcunit.setup(setDefaultUser, '')
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='warning'][contains(text(), 'The system does not have a valid default user set')]"),
    ], reason='Ensure the warning shows up when no default user is set')
    wcunit.test()

    wcunit = d.getWCUnitTest('Verify Invalid Default User (For inactive user)')
    wcunit.setup(lambda d: d.miedb.dbExec("UPDATE users SET status=2 WHERE username='dave'"))
    wcunit.teardown(lambda d: d.miedb.dbExec("UPDATE users SET status=1 WHERE username='dave'"))
    wcunit.setup(setDefaultUser, 'dave')
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='warning'][contains(., 'The specified user [ dave ] is not an active user and cannot login')]"),
        wcElement('xpath', "//span[@class='warning'][contains(., 'Scheduled jobs will not run until the configuration is corrected')]"),
    ], reason='Ensure the warning shows up when an invalid user is set as the default')
    wcunit.test()

    wcunit = d.getWCUnitTest('Verify Invalid Default User (For expired password)')
    wcunit.setup(lambda d: d.miedb.dbExec("UPDATE users SET pwd_expire=DATE_SUB(CURDATE(), INTERVAL 100 YEAR) WHERE username='dave'"))
    wcunit.teardown(lambda d: d.miedb.dbExec("UPDATE users SET pwd_expire=DATE_ADD(CURDATE(), INTERVAL 50 YEAR) WHERE username='dave'"))
    wcunit.setup(setDefaultUser, 'dave')
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='warning'][contains(., 'The specified user [ dave ] has a password that has expired')]"),
        wcElement('xpath', "//span[@class='warning'][contains(., 'Scheduled jobs will not run until the configuration is corrected')]")
    ], reason='Ensure the warning shows up when an invalid user is set as the default')
    wcunit.test()

    wcunit = d.getWCUnitTest('Verify Valid Default User')
    wcunit.setup(setDefaultUser, d.getUserData('selenium_username'))
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='warning'][contains(text(), 'The system does not have a valid default user set')]", exists=False)
    ], reason='Ensure no warning shows up when a valid default user is set')
    wcunit.test()

    wcunit = d.getWCUnitTest('Permission (None)')
    wcunit.setup(editPermission, 0)
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        wcElement('xpath', """//*[contains(., "A permission level of 'View' is required")]"""),
        wcElement(jobsListview, None, exists=False),
    ], reason='Look for non-existent listview and a permission message')
    wcunit.test()

    wcunit = d.getWCUnitTest('Permission (View)')
    wcunit.setup(editPermission, 1)
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        jobsListview,
        wcElement('text', 'Add Scheduled Job', exists=False),
        wcElement('text', 'Manage Settings', exists=False),
        wcElement('text', 'List Scheduled Jobs', exists=True),
    ], reason='Look for listview present, but no links to manage or add')
    wcunit.test()

    wcunit = d.getWCUnitTest('Permission (Execute)')
    wcunit.setup(editPermission, 2)
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        jobsListview,
        wcElement('text', 'Add Scheduled Job', exists=False),
        wcElement('text', 'Manage Settings', exists=False),
        wcElement('text', 'List Scheduled Jobs', exists=True),
    ], reason='Look for listview present but no links to manage or add')
    wcunit.test()

    wcunit = d.getWCUnitTest('Permission (Manage)')
    wcunit.setup(editPermission, 3)
    wcunit.setup(listJobs)
    wcunit.verifyElements([
        jobsListview,
        wcElement('text', 'Add Scheduled Job', exists=True),
        wcElement('text', 'Manage Settings', exists=True),
        wcElement('text', 'List Scheduled Jobs', exists=True),
    ], reason='Look for listview present and manage/add links')
    wcunit.test()
    d.endSection()

    d.startSection('Add / Edit Functionality')
    wcunit = d.getWCUnitTest('Validate Add Form')
    wcunit.setup(lambda d: d.clickElement(text='Add Scheduled Job'))
    wcunit.verifyElements([
        wcElement('id', 'name', name='name', size='50', maxlength='128', type='text'),
        wcElement('id', 'description', name='description', rows='4', cols='50'),
        wcElement('id', 'type', name='type'),
        wcElement('xpath', "//option[@value='' and text()='Select Job Type']"),
        wcElement('xpath', "//option[@value='1' and text()='URL']"),
        wcElement('xpath', "//option[@value='2' and text()='Email Report']"),
        wcElement('xpath', "//option[@value='3' and text()='Perform Report']"),
        wcElement('xpath', "//option[@value='4' and text()='Automatic Checkout']"),
        wcElement('id', 'cgi', name='cgi', size='50', maxlength='1023', type='text'),
        wcElement('id', 'method', name='method'),
        wcElement('xpath', "//option[@value='2' and text()='POST']"),
        wcElement('xpath', "//option[@value='1' and text()='GET']"),
        wcElement('id', 'firstrunMONTH', name='firstrunMONTH'),
        wcElement('id', 'firstrunDAY', name='firstrunDAY'),
        wcElement('id', 'firstrunYEAR', name='firstrunYEAR'),
        wcElement('id', 'firstrunTIME', name='firstrunTIME'),
        wcElement('id', 'endrunMONTH', name='endrunMONTH'),
        wcElement('id', 'endrunDAY', name='endrunDAY'),
        wcElement('id', 'endrunYEAR', name='endrunYEAR'),
        wcElement('id', 'endrunTIME', name='endrunTIME'),
        wcElement('id', 'rc_type', name='rc_type'),
        wcElement('xpath', "//option[@value='0' and text()='No Recurrence']"),
        wcElement('xpath', "//option[@value='1' and text()='Minutely']"),
        wcElement('xpath', "//option[@value='2' and text()='Hourly']"),
        wcElement('xpath', "//option[@value='3' and text()='Daily']"),
        wcElement('xpath', "//option[@value='4' and text()='Weekly']"),
        wcElement('xpath', "//option[@value='5' and text()='Monthly']"),
        wcElement('xpath', "//option[@value='6' and text()='Yearly']"),
        wcElement('id', 'active', name='active', type='checkbox', value='1'),
    ], reason='Ensure the basic inputs are present')
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate URL Options')
    wcunit.setup(lambda d: d.enterFormData('URL', id='type'))
    wcunit.verifyElements([
        wcElement('id', 'operation', name='operation', size='50', type='text'),
    ], reason='Check the URL options')
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Email Report Options')
    wcunit.setup(lambda d: d.enterFormData('Email Report', id='type'))
    wcunit.verifyElements([
        wcElement('xpath', "//option[@value='' and text()='Select System Report']"),
        wcElement('id', 'cron_ext_cgi_email_userid_ac_txt', name='cron_ext_cgi_email_userid_ac_txt'),
        wcElement('id', 'ext_address', name='ext_address', rows='4', cols='30'),
    ], reason='Check the URL options')
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Perform Report Options')
    wcunit.setup(lambda d: d.enterFormData('Perform Report', id='type'))
    wcunit.verifyElements([
        wcElement('xpath', "//option[@value='' and text()='Select System Report']"),
    ], reason='Check the URL options')
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Automatic Checkout Options')
    wcunit.setup(lambda d: d.enterFormData('Automatic Checkout', id='type'))
    wcunit.verifyElements([
    ], reason='Check the URL options')
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Minutely Recurrence Options')
    wcunit.setup(lambda d: d.enterFormData('Minutely', id='rc_type'))
    wcunit.verifyElements([
        wcElement('xpath', "//input[@name='rc_min' and @value='1']",),
        wcElement('xpath', "//input[@name='rc_min' and @value='5']",),
        wcElement('xpath', "//input[@name='rc_min' and @value='10']"),
        wcElement('xpath', "//input[@name='rc_min' and @value='15']"),
        wcElement('xpath', "//input[@name='rc_min' and @value='20']"),
        wcElement('xpath', "//input[@name='rc_min' and @value='30']"),
        wcElement('xpath', "//input[@name='rc_min' and @value='45']"),
    ])
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Hourly Recurrence Options')
    wcunit.setup(lambda d: d.enterFormData('Hourly', id='rc_type'))
    wcunit.verifyElements([
        wcElement('xpath', "//input[@name='rc_hour' and @value='1']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='2']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='3']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='4']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='5']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='6']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='7']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='8']"),
        wcElement('xpath', "//input[@name='rc_hour' and @value='12']"),
    ])
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Daily Recurrence Options')
    wcunit.setup(lambda d: d.enterFormData('Daily', id='rc_type'))
    wcunit.verifyElements([
    ])
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Weekly Recurrence Options')
    wcunit.setup(lambda d: d.enterFormData('Weekly', id='rc_type'))
    wcunit.verifyElements([
        wcElement('xpath', "//input[@name='rc_dow' and @value='1']"),
        wcElement('xpath', "//input[@name='rc_dow' and @value='2']"),
        wcElement('xpath', "//input[@name='rc_dow' and @value='4']"),
        wcElement('xpath', "//input[@name='rc_dow' and @value='8']"),
        wcElement('xpath', "//input[@name='rc_dow' and @value='16']"),
        wcElement('xpath', "//input[@name='rc_dow' and @value='32']"),
        wcElement('xpath', "//input[@name='rc_dow' and @value='64']"),
    ])
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Monthly Recurrence Options')
    wcunit.setup(lambda d: d.enterFormData('Monthly', id='rc_type'))
    wcunit.verifyElements([
        wcElement('xpath', "//input[@name='rc_month' and @value='1']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='2']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='4']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='8']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='16']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='32']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='64']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='128']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='256']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='512']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='1024']"),
        wcElement('xpath', "//input[@name='rc_month' and @value='2048']"),

    ])
    wcunit.test()

    wcunit = d.getWCUnitTest('Validate Yearly Recurrence Options')
    wcunit.setup(lambda d: d.enterFormData('Yearly', id='rc_type'))
    wcunit.verifyElements([
    ])
    wcunit.test()

    wcunit = d.getWCUnitTest('Add a job and ensure it saves correctly in the DB')
    wcunit.setup(enterJob, {
        'name': 'Job Unit Test',
        'description': 'This job was created from a WCUnitTest',
        'type': 'URL',
        'operation': '?f=wcversion',
        'cgi': '&test=1',
        'method': 'POST',
        'firstrun': ('01', '01', '2050', '08:00'),
        'endrun': ('12', '31', '2050', '23:00'),
        'recurrence': 'Weekly',
        'recurrence_options': ('2','4','8','16','32'),
        'logic': 'SELECT 1',
        'active': True
    })
    wcunit.verifyElements([
        wcElement('xpath', "//span[@class='information'][contains(.,'Scheduled Job Saved')]"),
    ])
    wcunit.verifyDB([
        wcDBRecord("FROM cron WHERE name='Job Unit Test'", {
            'description': 'This job was created from a WCUnitTest',
            'operation_type': 'URL',
            'operation': '?f=wcversion',
            'cgi': '&test=1',
            'method': 'POST',
            'firstrun': '2050-01-01 08:00:00',
            'endrun': '2050-12-31 23:00:00',
            'rc_type': 'WEEK',
            'recurrence': 62,
            'recurrence_logic': 'SELECT 1',
            'active': 1,
        }),
    ])
    wcunit.test(lambda d: d.clickElement(value='Schedule'), reason='Click Schedule')
    d.endSection()

    d.startSection('Preview Mode')
    u = d.getWCUnitTest('Verify Preview Mode Works')
    u.verifyFunc(checkSource, udata='The following jobs are what would be executed were you not in preview mode',
        reason='Ensure the preview message appears')
    u.verifyFunc(checkSource, udata='preview: 1', reason='Ensure preview mode is enabled')
    u.verifyFunc(checkSource, udata='cgitimestamp: 0', reason='Ensure the cgitimestamp is unset')
    u.test(lambda d: d.navigate('?f=cron'), reason='Go to f=cron')

    u = d.getWCUnitTest('Verify Preview Mode Works with an invalid timestamp')
    d.wcErrorLog.ignore('Scheduled jobs daemon invoked with an invalid timestamp*')
    u.verifyFunc(checkSource, udata='The following jobs are what would be executed were you not in preview mode',
        reason='Ensure the preview message appears')
    u.verifyFunc(checkSource, udata='preview: 1', reason='Ensure preview mode is enabled')
    u.verifyFunc(checkSource, udata='cgitimestamp: 1', reason='Ensure the cgitimestamp is set')
    u.test(lambda d: d.navigate('?f=cron&timestamp=1'), reason='Go to f=cron&timestamp=1')

    d.endSection()

    d.startSection('Execute Behavior')
    u = d.getWCUnitTest('Verify Asbolute URL')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'URL',
        'operation': '{0}{1}?f=wcrelease'.format(d._base_urls[-1],
            '/' if not d._base_urls[-1].endswith('/') else ''),     # This url for some reason must have a before the querystring
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
    }, reason='Create a job that hits this system\'s wcrelease page')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [SUCCESS]']"),
        reason='Absolute URLs should always return success if the response code is 200')
    u.verifyElements(
        wcElement('xpath', "//span//pre[contains(., 'SYSTEM_HANDLE: {0}')]".format(d.getUserData('handle'))),
        reason='The url should have returned the wcrelease page for this system')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Verify Relative URL (that doesn\'t require a login)')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'URL',
        'operation': '?f=wcrelease',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
    }, reason='Create a job that hits this system\'s wcrelease page')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [SUCCESS]']"),
        reason='Absolute URLs should always return success if the response code is 200')
    u.verifyElements(
        wcElement('xpath', "//span//pre[contains(., 'SYSTEM_HANDLE: {0}')]".format(d.getUserData('handle'))),
        reason='The url should have returned the wcrelease page for this system')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Verify Relative URL (that requires a login)')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'URL',
        'operation': '?f=wcversion',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
    }, reason='Create a job that hits this system\'s wcversion page')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [SUCCESS]']"),
        reason='We should get success if the server determined that we logged in and there were no cron errors')
    u.verifyElements([
        wcElement('xpath', "//pre[contains(., 'Dependency Versions')]"),
        wcElement('xpath', "//pre[contains(., 'Product Release')]"),
        wcElement('xpath', "//pre[contains(., 'Git Status')]"),
    ], reason='Look for elements from the wcversion page')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Verify Automatic Checkout Failure (due to system setting)')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'CHECKOUT',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
    }, reason='Create a job that checks out all patients')
    u.setup(lambda d: d.wcutils.SetSystemSetting('Checkin', 'Settings', 'Allow Auto Checkout After This Hour', '25', False))
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [ERROR]']"),
        reason='We should get an error message because the system setting Checkin|Settings|Allow Auto Checkout After This Hour')
    u.verifyElements([
        wcElement('xpath', "//pre[contains(., 'Checkout Body Start')]"),
    ], reason='Look for the checkout page (this could still not technically allow checkout based on the "Allow Auto Checkout After This Hour" system setting')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Verify Automatic Checkout Success')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'CHECKOUT',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
    }, reason='Create a job that checks out all patients')
    u.setup(lambda d: d.wcutils.SetSystemSetting('Checkin', 'Settings', 'Allow Auto Checkout After This Hour', '0', False))
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [SUCCESS]']"),
        reason='We should get the success message')
    u.verifyElements([
        wcElement('xpath', "//pre[contains(., 'Checkout Body Start')]"),
    ], reason='Look for the checkout page (this could still not technically allow checkout based on the "Allow Auto Checkout After This Hour" system setting')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Verify Email Report')
    u.setup(addSystemReport, {
        'name': 'SeleniumReport',
        'sql_query': 'SELECT 1',
        'active': '1',
        'run_counter': '0',
    }, reason='Create a report to be emailed')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'REPORT EMAIL',
        'operation': 'SeleniumReport',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
        'email_address': 'selenium@mieweb.com'
    }, reason='Create a job that emails a system report')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [SUCCESS]']"),
        reason='We should get success if the server determined that we logged in and there were no cron errors')
    u.verifyElements([
        wcElement('xpath', "//pre[contains(., 'Successfully sent email')]"),
    ], reason='Look for success message in the output')
    u.verifyDB(wcDBRecord("FROM system_reports WHERE name='SeleniumReport'", {
        'run_counter': 1
    }), reason='Ensure the run count on the system report incremented by 1')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Verify Perform Report')
    u.setup(addSystemReport, {
        'name': 'SeleniumReport',
        'sql_query': "SELECT pat_id, 'Pat Portal Message Notification' AS 'layout_name','?f=chart&s=pat&opp=email&send=send' AS 'URL' FROM patients WHERE pat_id=18",
        'active': '1',
        'run_counter': '0',
    }, reason='Create a report to be performed')
    u.setup(addJob, {
        'name': 'SeleniumJob',
        'operation_type': 'REPORT PERFORM',
        'operation': 'SeleniumReport',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'GET',
        'active': '1',
    }, reason='Create a job that performs a system report')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ SeleniumJob ] reports [SUCCESS]']"),
        reason='We should get success if the server determined that we logged in and there were no cron errors')
    u.verifyElements([
        wcElement('xpath', "//pre[contains(., 'Performed action on 1/1 records from system report')]"),
    ], reason='Look for success message in the output')
    u.verifyDB(wcDBRecord("FROM system_reports WHERE name='SeleniumReport'", {
        'run_counter': 1
    }), reason='Ensure the run count on the system report incremented by 1')
    u.test(executeJob, 'SeleniumJob', reason='Execute this job')

    u = d.getWCUnitTest('Testing the scheduled jobs max records threshold check for success case')
    u.setup(addJob, {
        'name': 'MaxRecordSuccess',
        'max_records': '15',
        'operation_type': 'REPORT PERFORM',
        'operation': 'max_records_test',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'POST',
        'active': '1',
    }, reason='Testing the scheduled jobs max records threshold check for success case')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ MaxRecordSuccess ] reports [SUCCESS]']"),
        reason='We should get success if the no. of records returned are within the threshold')
    u.test(executeJob, 'MaxRecordSuccess', reason='Execute this job')

    u = d.getWCUnitTest('Testing the scheduled jobs max records threshold check for failure case')
    u.setup(addJob, {
        'name': 'MaxRecordFailure',
        'max_records': '5',
        'operation_type': 'REPORT PERFORM',
        'operation': 'max_records_test',
        'firstrun': '2000-01-01 00:00:00',
        'method': 'POST',
        'active': '1',
    }, reason='Testing the scheduled jobs max records threshold check for failure case')
    u.verifyElements(
        wcElement('xpath', "//span[text()='Scheduled Job [ MaxRecordFailure ] reports [ERROR]']"),
        reason='We should get error if the no. of records returned are greater than the threshold')
    u.test(executeJob, 'MaxRecordFailure', reason='Execute this job')

    d.endSection()



