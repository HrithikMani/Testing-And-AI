"""
    Unit Tests for System Reports
    @owners: sgrider
    @filedeps: src/system_report.*
"""
from wcunittest import wcElement, wcDBRecord

def deleteSecurityException(d, username):
    d.miedb.dbExec("DELETE FROM security_exception "\
                   "WHERE user_id=(SELECT user_id FROM users WHERE username=%s) "\
                   "AND category_name='Limited to Restricted Items'", username)

def editPermission(d, value):
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
        "WHERE module_name='Control' AND category_name='Manage System Reports' "\
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
        "username=%s)", value, d.getUserData('selenium_username'))

def editReport(d, name):
    d.navigate('?f=admin&s=system_report&opp=edit&report_name={0}'.format(name))

def clickPerform(d, data):
    d.clickElement(text='Perform')

def executeReport(d, data):
    cgi = ''
    if isinstance(data, str):
        name = data
    elif isinstance(data, dict):
        name = data.get('name')
        cgi = data.get('cgi')
    d.navigate('?f=admin&s=system_report&opp=query&submit_query&report_name={0}&{1}'.format(
        name, cgi))

def insertLayout(d, data):
    sql = "REPLACE INTO layout (%s) VALUES (%s)" %(','.join(data.keys()),
        ','.join(['%s'] * len(data)))
    d.miedb.dbExec(sql, *data.values())
    d.wcutils.SetSystemSetting('System', 'WebChart', 'All Layouts Table Update Time', '0', False)

def insertReport(d, data):
    sql = "REPLACE INTO system_reports (%s) VALUES (%s)" %(','.join(data.keys()),
        ','.join(['%s'] * len(data)))
    d.miedb.dbExec(sql, *data.values())


def main(d, WCURL):
    reportName = 'unitTestReport'

    # Manage System Reports: No
    u = d.getWCUnitTest('No Permission (Run)')
    u.setup(insertReport, {'name': reportName, 'sql_query': 'SELECT 1'})
    u.setup(editPermission, 0)
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=False),
        wcElement('xpath', """//*[contains(., "A permission level of 'Run only' is required")]"""),
    ], reason='Looking for non-existent listview and a permission message')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('No Permission (Edit)')
    u.verifyElements([
        wcElement('xpath', """//*[contains(., "A permission level of 'Run only' is required")]"""),
        wcElement('id', 'sysrpt_form', exists=False),
    ], reason='Looking for permission message and a missing edit form')
    u.test(editReport, reportName)

    # Manage System Reports: Run only
    u = d.getWCUnitTest('Run Only Permission (Run)')
    u.setup(editPermission, 1)
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=True),
        wcElement('text', 'Edit Report', exists=False),
    ], reason='Look for the listview and ensure the Edit Report link is not present')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Run Only Permission (Edit)')
    u.verifyElements([
        wcElement('xpath', """//*[contains(., "A permission level of 'Add/Edit' is required")]"""),
        wcElement('id', 'sysrpt_form', exists=False),
    ])
    u.test(editReport, reportName)

    # Manage System Reports: Add/Edit
    # Realtime: 0
    u = d.getWCUnitTest('Add/Edit Permission, Realtime: 0 (Run)')
    u.setup(insertReport, {'name': reportName, 'sql_query': 'SELECT 1', 'realtime':'0' })
    u.setup(editPermission, 2)
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=True),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Add/Edit Permission, Realtime: 0 (Edit)')
    u.verifyElements([
        wcElement('id', 'sysrpt_form', exists=True),
        wcElement('xpath', "//input[@disabled and @id='report_realtime']", exists=True),
        wcElement('xpath', "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=False),
    ])
    u.test(editReport, reportName)

    # Realtime: 1
    u = d.getWCUnitTest('Add/Edit Permission, Realtime: 1 (Run)')
    u.setup(insertReport, {'name': reportName, 'sql_query': 'SELECT 1', 'realtime':'1' })
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=True),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Add/Edit Permission, Realtime: 1 (Edit)')
    u.verifyElements([
        wcElement('id', 'sysrpt_form', exists=True),
        wcElement('xpath', "//input[@disabled and @id='report_realtime']", exists=True),
        wcElement('xpath', "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=True),
    ])
    u.test(editReport, reportName)

    # Manage System Reports: Add/Edit Realtime
    # Realtime: 0
    u = d.getWCUnitTest('Realtime Permission, Realtime: 0 (Run)')
    u.setup(insertReport, {'name': reportName, 'sql_query': 'SELECT 1', 'realtime':'0' })
    u.setup(editPermission, 3)
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=True),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Realtime Permission, Realtime: 0 (Edit)')
    u.verifyElements([
        wcElement('id', 'sysrpt_form', exists=True),
        wcElement('xpath', "//input[not(@disabled) and @id='report_realtime']", exists=True),
        wcElement('xpath', "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=False),
    ])
    u.test(editReport, reportName)

    # Realtime: 1
    u = d.getWCUnitTest('Realtime Permission, Realtime: 1 (Run)')
    u.setup(insertReport, {'name': reportName, 'sql_query': 'SELECT 1', 'realtime':'1' })
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=True),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Realtime Permission, Realtime: 1 (Edit)')
    u.verifyElements([
        wcElement('id', 'sysrpt_form', exists=True),
        wcElement('xpath', "//input[not(@disabled) and @id='report_realtime']", exists=True),
        wcElement('xpath', "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=False),
    ])
    u.test(editReport, reportName)

    ##
    u = d.getWCUnitTest('Listview Appears for Basic Query')
    u.setup(insertReport, {'name': reportName,
        'sql_query': 'SELECT pat_id, first_name, last_name FROM patients'})
    u.verifyElements(wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)))
    u.verifyDB(wcDBRecord("FROM system_reports WHERE name='{0}'".format(reportName), {
        'run_counter': 1
    }), reason='Run counter should increment by one after running the report')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Listview Error for Invalid Query')
    u.setup(insertReport, {'name': reportName,
        'sql_query': 'SELECT thisisbull FROM patients'})
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=False),
        wcElement('xpath', """//*[contains(., "Unknown column 'thisisbull' in 'field list'") or contains(., "Unknown column 'thisisbull' in 'SELECT'")]"""),
        wcElement('value', 'Edit Query', name='submit_fix_and_edit'),
        wcElement('name', 'cancel', value='Cancel'),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Error Message for Query That Doesn\'t Start with Select')
    u.setup(insertReport, {'name': reportName,
        'sql_query': '* FROM patients'})
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=False),
        wcElement('xpath', "//div[contains(text(), 'The report contains multiple queries, but the last query is not a SELECT statement. It must be a SELECT in order to run')]"),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Verify Multiple Statements Work Correctly')
    u.setup(insertReport, {'name': reportName,
        'sql_query': 'SET @pat_id=18;\n\nSELECT pat_id FROM patients WHERE pat_id=@pat_id'})
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)),
    ], reason='Look for a listview')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Verify a Trailing semicolon and Whitespace Do Not Break Multiple Queries')
    u.setup(insertReport, {'name': reportName,
        'sql_query': 'SET @pat_id=18;\n\nSELECT pat_id FROM patients WHERE pat_id=@pat_id;\n\t'})
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)),
    ], reason='Look for a listview')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Populates Pre-Defined SQL Variables')
    u.setup(insertReport, {'name': reportName,
        'sql_query': 'SELECT @session_id, @user_id, @practice_name'})
    u.verifyElements(wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)))
    u.verifyElements([
        wcElement('id', 'session_id', size=12, type='text', value='WCTESTSESSION'),
        wcElement('id', 'user_id', size=12, type='text'),
        wcElement('id', 'practice_name', size=12, type='text', value='WebChart Testing System'),
        wcElement('value', 'Run Report', type='submit', name='submit_query'),
    ])
    u.verifyElements([
        wcElement('xpath', "//td[text()='WCTESTSESSION']"),
        wcElement('xpath', "//td[text()='WCTESTSESSION']/following-sibling::td[1]", text=d.runJS("return user_id")),
        wcElement('xpath', "//td[text()='WCTESTSESSION']/following-sibling::td[2]", text='WebChart Testing System'),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Ensure use keyword is flagged')
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': 'use otherdatabase; SELECT 1'
    }, reason='Insert invalid report sql')
    u.verifyElements(wcElement('xpath', '''//*[contains(., "The report contains the restricted sql keyword 'use'")]'''),
        reason='Look for the error message')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Ensure a quoted "use" is not flagged')
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': 'SELECT "I like to use sql sometimes"'
    }, reason='Insert valid report sql')
    u.verifyElements(wcElement('xpath', '''//*[contains(., "The report contains the restricted sql keyword 'use'")]''', exists=False),
        reason='Look for no error message')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Ensure a quoted `use` is not flagged')
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': 'SELECT "asd" AS `I like to use sql sometimes`'
    }, reason='Insert valid report sql')
    u.verifyElements(wcElement('xpath', '''//*[contains(., "The report contains the restricted sql keyword 'use'")]''', exists=False),
        reason='Look for no error message')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Parses CGI Variables in Report')
    u.setup(insertReport, {'name': reportName,
        'sql_query': "SELECT 'static', @thisismyvar"})
    u.verifyElements(wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)))
    u.verifyElements([
        wcElement('id', 'thisismyvar', size=12, type='text', value='fromcgi'),
        wcElement('value', 'Run Report', type='submit', name='submit_query'),
    ])
    u.verifyElements([
        wcElement('xpath', "//td[text()='static']"),
        wcElement('xpath', "//td[text()='static']/following-sibling::td[1]", text='fromcgi')
    ])
    u.test(executeReport, {'name': reportName, 'cgi': 'thisismyvar=fromcgi'})

    u = d.getWCUnitTest('Parses $RXDB$')
    u.setup(insertReport, {'name': reportName,
        'sql_query': "SELECT 'testcolumn' FROM $RXDB$.zip_codes"})
    u.verifyElements(wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)))
    u.verifyElements(wcElement('xpath', "//td[text()='testcolumn']"))
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Parses $ALL_LAYOUTS$')
    u.setup(insertLayout, {'module': 'zUnitTest', 'name': 'zUnitTestLayout', 'layout_html': '', 'active': '1'})
    u.setup(insertReport, {'name': reportName,
        'sql_query': "SELECT 'testcolumn', module, name, file_date FROM $ALL_LAYOUTS$ "\
            "ORDER BY module DESC"})
    u.verifyElements(wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)))
    u.verifyElements([
        wcElement('xpath', "//td[text()='zUnitTest']", text='zUnitTest'),
        wcElement('xpath', "//td[text()='zUnitTest']/following-sibling::td[1]", text='zUnitTestLayout'),
    ], reason='Ensure we find the zUnitTest module/layout row')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Parses $WCINCLUDE$')
    u.setup(insertReport, {'name': 'wcinclude1', 'sql_query': "'this',"})
    u.setup(insertReport, {'name': 'wcinclude2', 'sql_query': "'column',"})
    u.setup(insertReport, {'name': 'wcinclude3', 'sql_query': "'is',"})
    u.setup(insertReport, {'name': 'wcinclude4', 'sql_query': "'included'"})
    u.setup(insertReport, {'name': reportName,
        'sql_query': "SELECT 'FirstColumn', "\
        "$WCINCLUDE|wcinclude1$ "\
        "$WCINCLUDE|wcinclude2$ "\
        "$WCINCLUDE|wcinclude3$ "\
        "$WCINCLUDE|wcinclude4$ "\
        ", pat_id FROM patients p"})
    u.verifyElements([
        wcElement('xpath', "//td[text()='FirstColumn']", text='FirstColumn'),
        wcElement('xpath', "//td[text()='FirstColumn']/following-sibling::td[1]", text='this'),
        wcElement('xpath', "//td[text()='FirstColumn']/following-sibling::td[2]", text='column'),
        wcElement('xpath', "//td[text()='FirstColumn']/following-sibling::td[3]", text='is'),
        wcElement('xpath', "//td[text()='FirstColumn']/following-sibling::td[4]", text='included'),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Reports Missing $WCINCLUDE$')
    u.setup(insertReport, {'name': reportName, 'sql_query': "SELECT 'asd', $WCINCLUDE|ThisIsMissing$"})
    u.verifyElements([
        wcElement('xpath', """//*[contains(., 'Failed to retrieve system report [ThisIsMissing] from WCINCLUDE')]"""),
        wcElement('value', 'Edit Query'),
    ], reason='Should get a message about a missing include instead of generic sql error')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Reports Invalid $WCINCLUDE$')
    u.setup(insertReport, {'name': 'wcinclude1', 'sql_query': 'SELECT 1'})
    u.setup(insertReport, {'name': reportName, 'sql_query': 'SELECT $WCINCLUDE|wcinclude1$'})
    u.verifyElements([
        wcElement('xpath', """//*[contains(., 'You have an error in your SQL syntax;')]"""),
        wcElement('value', 'Edit Query'),
    ])
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Allows Nested $WCINCLUDE$')
    u.setup(insertReport, {'name': 'wcinclude1', 'sql_query': "SELECT $WCINCLUDE|nested$"})
    u.setup(insertReport, {'name': 'nested', 'sql_query': "'nested_column'"})
    u.setup(insertReport, {'name': reportName,
        'sql_query': "SELECT ($WCINCLUDE|wcinclude1$), $WCINCLUDE|nested$, 'last_column'"})
    u.verifyElements([
        wcElement('xpath', "//td[text()='nested_column'][1]", text='nested_column'),
        wcElement('xpath', "//td[text()='nested_column'][1]/following-sibling::td[1]", text='nested_column'),
        wcElement('xpath', "//td[text()='nested_column'][1]/following-sibling::td[2]", text='last_column'),
    ], reason='Checks that the listview is showing all the correct columns')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Prevents Recursive $WCINCLUDE$')
    u.setup(insertReport, {'name': 'wcinclude1', 'sql_query': "SELECT $WCINCLUDE|{0}$".format(reportName)})
    u.setup(insertReport, {'name': reportName, 'sql_query': "SELECT $WCINCLUDE|wcinclude1$"})
    u.verifyElements([
        wcElement('xpath', """//*[contains(., 'Skipping include of circular reference to [ {0} ]')]""".format(reportName)),
        wcElement('value', 'Edit Query'),
    ], reason='The system should detect and prevent circular includes which would result in an endless loop')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Verify Perform Mode Detects No URL Column')
    u.setup(insertReport,
        {'name': reportName,
         'sql_query': "SELECT user_id, 'Report Perform' AS 'subject' FROM users WHERE username='{0}'".format(d.getUserData('selenium_username'))
        })
    u.setup(executeReport, reportName)
    u.verifyElements([
        wcElement('xpath', "//div[text()='This report has no URL or JSON_PATH column defined. There is nothing to perform']"),
    ])
    u.test(clickPerform)

    u = d.getWCUnitTest('Verify Perform Mode Detects URL Column')
    u.setup(insertReport,
        {'name': reportName,
         'sql_query': "SELECT user_id, 'Report Perform' AS 'subject', '?f=admin&s=users&opp=email' AS 'URL' "\
                      "FROM users WHERE username='{0}'".format(d.getUserData('selenium_username'))
        })
    u.setup(executeReport, reportName)
    u.verifyElements([
        wcElement('value', 'Perform All'),
        wcElement('value', 'Perform Selected'),
        wcElement('value', 'Cancel'),
        wcElement('text', 'Select All'),
        wcElement('text', 'Select None'),
        wcElement('text', 'Show URLs'),
        wcElement('xpath', "//input[@class='performSelect']", type='checkbox')
    ])
    u.test(clickPerform)

    u = d.getWCUnitTest('Verify Selective Perform Mode Reports No Selected Rows')
    u.setup(insertReport,
        {'name': reportName,
         'sql_query': "SELECT user_id, 'Report Perform' AS 'subject', '?f=admin&s=users&opp=email' AS 'URL' "\
                      "FROM users WHERE username='{0}'".format(d.getUserData('selenium_username'))
        })
    u.setup(executeReport, reportName)
    u.setup(clickPerform)
    u.verifyElements([
        wcElement('xpath', "//div[text()='There are no rows selected to perform']")
    ], reason='Look for no rows message')
    u.test(lambda d: d.clickElement(value='Perform Selected'), reason='Click perform selected without any checked')

    u = d.getWCUnitTest('Verify Selective Perform Mode Warns About Selecting All')
    u.setup(insertReport,
        {'name': reportName,
         'sql_query': "SELECT user_id, 'Report Perform' AS 'subject', '?f=admin&s=users&opp=email' AS 'URL' "\
                      "FROM users WHERE username='{0}'".format(d.getUserData('selenium_username'))
        })
    u.setup(executeReport, reportName)
    u.setup(clickPerform)
    u.setup(lambda d: d.enterFormData(True, xpath="//input[@class='performSelect']"), reason='Check a single row')
    u.verifyElements([
        wcElement('xpath', '''//div[contains(., "It looks like you're attempting to perform all")]''')
    ], reason='Look for warning message')
    u.test(lambda d: d.clickElement(value='Perform Selected'), reason='Click perform selected')

    u = d.getWCUnitTest('Verify Selective Perform Mode Works')
    u.setup(insertReport,
        {'name': reportName,
         'sql_query': "SELECT user_id, 'Report Perform' AS 'subject', '?f=admin&s=users&opp=email' AS 'URL' "\
                      "FROM users"
        })
    u.setup(executeReport, reportName)
    u.setup(clickPerform)
    u.setup(lambda d: d.enterFormData(True, xpath="//input[@class='performSelect']"), reason='Check a single row')
    u.verifyElements([
        wcElement('xpath', "//div[contains(., 'Perform operation completed')]")
    ], timeout=30, reason='Look for complete message')
    u.test(lambda d: d.clickElement(value='Perform Selected'), reason='Click perform selected')

    u = d.getWCUnitTest('Verify WCSystemReportView Lets All Users in Regardless of "Manage System Report" Permission')
    u.setup(editPermission, 0)
    u.teardown(editPermission, 1)
    u.setup(insertLayout, {
        'module': 'unittest',
        'name': 'unittest',
        'layout_html': '<WCSYSTEMREPORTVIEW name="{0}" title="{0}">'.format(reportName),
        'active': '1',
    })
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': 'SELECT pat_id, CONCAT(last_name, ", ", first_name) FROM patients',
    })
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0}']".format(reportName), exists=True),
    ], reason='Look for a valid listview')
    u.test(lambda d: d.navigate('?f=layout&module=unittest&name=unittest'))

    u = d.getWCUnitTest('Verify WCSystemReportView Respects Explicitly Restricted System Reports')
    u.setup(editPermission, 0)
    u.teardown(editPermission, 1)
    u.setup(insertLayout, {
        'module': 'unittest',
        'name': 'unittest',
        'layout_html': '<WCSYSTEMREPORTVIEW name="{0}" title="{0}">'.format(reportName),
        'active': '1',
    })
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': 'SELECT pat_id, CONCAT(last_name, ", ", first_name) FROM patients',
        'restricted': '1',
    })
    u.setup(lambda d: d.miedb.dbExec("REPLACE INTO system_reports_restricted (rep_id, allowed_id, id_type) VALUES ((SELECT report_id FROM system_reports WHERE name='{0}'), 0, 'user')".format(reportName)),
        reason='Insert the restricted record that doesnt allow this user')
    u.teardown(deleteSecurityException, d.getUserData('selenium_username'))
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=False),
        wcElement('xpath', "//div[contains(., 'You lack permission to run this report')]", exists=True),
    ], reason='Ensure a listview does not show and a message does instead')
    u.test(lambda d: d.navigate('?f=layout&module=unittest&name=unittest'))

    u = d.getWCUnitTest('Verify WCSystemReportView Shows Reports Even with "Limited to Restricted Items" enabled')
    u.setup(lambda d: d.miedb.dbExec("REPLACE INTO system_reports_restricted (rep_id, allowed_id, id_type) VALUES ((SELECT report_id FROM system_reports WHERE name='{0}'), 0, 'user')".format(reportName)),
        reason='Insert the restricted record that doesnt allow this user')
    u.setup(lambda d: d.miedb.dbExec("REPLACE INTO security_exception (user_id, module_name, category_name, security_value) VALUES ((SELECT user_id FROM users WHERE username=%s), 'E-Chart', 'Limited to Restricted Items', 1)", d.getUserData('selenium_username')),
        reason="Enable 'Limited to Restricted Items' for Selenium User")
    u.teardown(deleteSecurityException, d.getUserData('selenium_username'))
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName), exists=False),
        wcElement('xpath', "//div[contains(., 'You lack permission to run this report')]", exists=True),
    ], reason='Ensure a listview does not show and a message does instead')
    u.test(lambda d: d.navigate('?f=layout&module=unittest&name=unittest'))

    u = d.getWCUnitTest('Verify query parsing does not care about leading space')
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': '   SELECT pat_id FROM patients'
    }, reason='Insert a report that starts with whitespace')
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)),
        wcElement('xpath', "//a[text()='Show All']")
    ], reason='Ensure the listview Show All link is present. This means that listview did not append a default limit clause')
    u.test(executeReport, reportName)

    u = d.getWCUnitTest('Verify entire multiqueries are being sent to the listview')
    u.setup(insertReport, {
        'name': reportName,
        'sql_query': "SET @one=1; SET @two=2; SET @three='asd'; SELECT @one, @two, @three, 'Static'"
    }, reason='Insert a report that uses multiquery and sets some variables we can check')
    u.verifyElements([
        wcElement('xpath', "//span[@class='LVTitle' and text()='{0} Query Results']".format(reportName)),
        wcElement('xpath', "//td[text()='1']"),
        wcElement('xpath', "//td[text()='2']"),
        wcElement('xpath', "//td[text()='asd']"),
        wcElement('xpath', "//td[text()='Static']"),
    ], reason='Look for the selected variable values as part of the final output')
    u.test(executeReport, reportName)
