from wcunittest import wcElement, wcDBRecord

def setUserLogins(d, data):
    d.miedb.dbExec("UPDATE users SET edit_date='2005-01-01', last_login='2005-01-01' WHERE username='butler'")
    d.miedb.dbExec("UPDATE users SET edit_date='1999-01-01', last_login='1999-01-01' WHERE username='nurse'")
    d.miedb.dbExec("UPDATE users SET edit_date='1999-01-01', last_login='1999-01-01' WHERE username='employee'")

# Test the disable inactive login feature
def main(d, WCURL):
    t = d.getWCUnitTest('Get users before disabling inactive')
    d.miedb.dbExec("UPDATE users SET edit_date='1999-01-01', last_login='1999-01-01' WHERE username='cronjobs'")
    t.verifyDB([
        wcDBRecord("FROM users WHERE username='cronjobs'", {
            'last_name': 'Cronjobs',
            'last_login': '1999-01-01 00:00:00',
            'status': 1
        }),
        wcDBRecord("FROM users WHERE username='butler'", {
            'first_name': 'Internist',
            'last_login': '0000-00-00 00:00:00',
            'status': 1
        }),
        wcDBRecord("FROM users WHERE username='nurse'", {
            'first_name': 'Nicole',
            'last_login': '0000-00-00 00:00:00',
            'status': 1
        })
    ], reason='Verify that the users havn\'t logged in recently')
    t.test()

    t = d.getWCUnitTest('Disable without days inactive system setting')
    t.setup(lambda d: d.wcutils.SetSystemSetting("System", "Security", "Days Inactive", "0", False), reason='Disable the days inactive system setting')
    t.setup(lambda d: d.navigate('?f=disableacc'))
    t.verifyElements([
        wcElement('xpath', '/html/body[contains(.,"Could not retrieve the (Security, Days Inactive) security setting.")]'),
        wcElement('xpath', '/html/body[contains(.,"Check that your \'Days Inactive\' setting is > 0")]')
    ], reason='Verify the "not configured" text is shown', timeout=5)
    t.test()

    t = d.getWCUnitTest('Disable with the system setting')
    t.setup(lambda d: d.wcutils.SetSystemSetting("System", "Security", "Days Inactive", "30", False), reason='Set the days inactive system setting to 30')
    t.setup(lambda d: d.navigate('?f=disableacc'))
    t.verifyElements([
        wcElement('xpath', '/html/body[contains(.,"All user accounts are active within 30 days")]')
    ], reason='Verify the correct text is displayed on the disable accounts screen', timeout=5)
    t.test()

    t = d.getWCUnitTest('Disable with new login dates')
    t.setup(lambda d: d.wcutils.SetSystemSetting("System", "Security", "Protected Security Roles", "Employees", False), reason='Protect employees security role from being disabled')
    t.setup(lambda d: d.wcutils.SetSystemSetting("System", "Security", "Protected Users", "nurse,selenium,dave", False), reason='Set the protected users setting')
    t.setup(setUserLogins)
    t.setup(lambda d: d.navigate('?f=disableacc'))
    t.verifyElements([
        wcElement('xpath', '/html/body[contains(.,"User found inactive (butler - 16) Internist Butler Dept: Physicians")]'),
        wcElement('xpath', '/html/body[contains(.,"User found inactive (cronjobs - 29)  Cronjobs Dept: MIE")]')
    ], reason='Verify the correct text is displayed on the disable accounts screen', timeout=5)
    t.test()

    t = d.getWCUnitTest('Disable for last time')
    t.setup(lambda d: d.navigate('?f=disableacc'))
    t.verifyElements([
        wcElement('xpath', '/html/body[contains(.,"All user accounts are active within 30 days")]')
    ], reason='Verify the correct text shows when there are no users to disable', timeout=5)
    t.test()

    t = d.getWCUnitTest('Users after disabling inactive')
    t.verifyDB([
        wcDBRecord("FROM users WHERE username='cronjobs'", {
            'last_name': 'Cronjobs',
            'last_login': '1999-01-01 00:00:00',
            'status': 0
        }),
        wcDBRecord("FROM users WHERE username='butler'", {
            'first_name': 'Internist',
            'last_login': '2005-01-01 00:00:00',
            'status': 0
        }),
        wcDBRecord("FROM users WHERE username='nurse'", {
            'first_name': 'Nicole',
            'last_login': '1999-01-01 00:00:00',
            'status': 1
        }),
        wcDBRecord("FROM users WHERE username='employee'", {
            'first_name': 'Frederick',
            'last_login': '1999-01-01 00:00:00',
            'status': 1
        })
    ], reason='Verify butler user was disabled and employee was not disabled')
    t.test()
