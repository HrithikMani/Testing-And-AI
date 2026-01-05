"""
    @owner: sgrider
"""
from wcunittest import wcElement, wcJSCode, wcDBRecord

# The following verified javascript tests ensure that a login has occurred
validLoginJS = [
    wcJSCode('user_id', lambda x: x > 0 if isinstance(x, int) else False),
    wcJSCode('username', lambda x: len(x) if isinstance(x, str) else False),
]
invalidLoginJS = [
    wcJSCode('username', ''),
    wcJSCode('user_id', 0),
]

def cryptSetup(wcunit, data):
    d = wcunit.getDriver()
    dropLogins(d, data)
    d.miedb.dbExec('UPDATE users SET password=%s, password_salt=%s,'\
        'pwd_expire=DATE_ADD(CURDATE(), INTERVAL 10 YEAR) WHERE username=%s',
        'XYVeVFl1l2FBk', '', 'selenium')
    d.navigate()

def normalizeDB(wcunit, data):
    d = wcunit.getDriver()
    # Do the demo date so we don't get any extra login messages other than normal ones
    d.miedb.dbExec("UPDATE system_settings SET value='' WHERE module='WebChart' AND "\
                   "section='Demo' AND item='Demo Date'")
    # Set up the new login screen
    d.miedb.dbExec("UPDATE system_settings SET value='1' WHERE module='System' AND "\
                   "section='Login' AND item='New login style'")
    # Make sure the password won't expire
    d.miedb.dbExec("UPDATE users SET pwd_expire=DATE_ADD(CURDATE(), INTERVAL 500 YEAR) "\
                   "WHERE username='%s'" %d.getUserData('selenium_username'))
    # Set System setting to show password reset options
    d.miedb.dbExec("UPDATE system_settings SET value='1' WHERE module='webchart' AND "\
                   "section='login' AND item='show password reset'")
    # Log out
    dropLogins(d, data)
    d.navigate()

def dropLogins(d, data):
    d.miedb.dbExec('TRUNCATE logins')

def clickElement(wcunit, text):
    wcunit.getDriver().clickElement(text=text)

def loginSelenium(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData(data.get('username', d.getUserData('selenium_username')), id='login_user')
    d.enterFormData(data.get('password', d.getUserData('selenium_password')), id='login_passwd')
    d.clickElement(name='login_submit')

def loginNurse(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData('nurse', id='login_user')
    d.enterFormData('selenium', id='login_passwd')
    d.clickElement(name='login_submit')

def loginExpiredSelenium(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData(data.get('username', d.getUserData('selenium_username')), id='login_user')
    d.enterFormData(data.get('password', d.getUserData('selenium_password')), id='login_passwd')
    d.pause(2)
    d.clickElement(name='login_submit')
    d.pause(2)

def loginInvalid(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData('invalidusername', id='login_user')
    d.enterFormData('invalidpassword', id='login_passwd')
    d.clickElement(name='login_submit')

def forgotUsername(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.clickElement(xpath="//a[contains(@href, 'f=login&s=ulookup')]")

def forgotPassword(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData(data.get('username', d.getUserData('selenium_username')), id='login_user')
    d.clickElement(xpath="//a[contains(@href, 'f=login&s=preset')]")

def invalidLookup(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.clickElement(xpath="//a[contains(@href, 'f=login&s=ulookup')]")
    d.enterFormData('something wrong', id='user_email')
    d.clickElement(value='Submit')

def validLookup(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.clickElement(xpath="//a[contains(@href, 'f=login&s=ulookup')]")
    d.enterFormData('selenium@mieweb.com', id='user_email')
    d.clickElement(value='Submit')

def invalidReset(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData('idontexist', name='login_user')
    d.clickElement(xpath="//a[contains(@href, 'f=login&s=preset')]")
    d.clickElement(value='Submit')

def validReset(wcunit, data):
    d = wcunit.getDriver()
    d.clickElement(xpath="//span[contains(., 'Standard Login')]")
    d.enterFormData(d.getUserData('selenium_username'), name='login_user')
    d.clickElement(xpath="//input[@value='Next']")
    d.clickElement(xpath="//a[contains(@href, 'f=login&s=preset')]")
    d.enterFormData(d.getUserData('selenium_username'), name='login_user')
    d.clickElement(value='Submit')
    d.enterFormData('260-459-6270', id='preset_secret_answer')
    d.clickElement(value='Submit')
    d.enterFormData('selenium@mieweb.com', id='preset_answer')
    d.clickElement(value='Submit')

    # Prompts to send a pin. Close it. we'll insert one ourselves
    d.clickElement(xpath="//button[contains(@class, 'xclose')]")

    # Insert the pin code
    d.miedb.dbExec("INSERT INTO login_trusts_translations SET domain='WCPINCODE',trans_type=1,trans_from=8,trans_to='U2FsdGVkX188KPlVPLSQ5GOg4wpi0IdyPhMSYWU++s8='")
    d.miedb.dbExec("INSERT INTO login_trusts_translations SET domain='WCPINCODE',trans_type=2,trans_from=8,trans_to=DATE_ADD(NOW(), INTERVAL 15 MINUTE)")

    # enter info to reset password
    d.enterFormData('63030', id='preset_pc')
    d.enterFormData('selenium@123', id='preset_np')
    d.enterFormData('selenium@123', id='preset_vp')

    d.clickElement(value='Submit')

def capturePassword(wcunit, udata):
    res = wcunit.getDriver().miedb.dbQuery('SELECT password, password_salt FROM users WHERE username=%s', 'selenium')
    udata.update(res.getRes()[0])

def restorePassword(wcunit, udata):
    wcunit.getDriver().miedb.dbExec('UPDATE users SET password=%s, password_salt=%s WHERE username=%s',
        udata['password'], udata['password_salt'], 'selenium')

def main(d, WCURL):
    """
    Verify the login pages via the UnitTest extension
    """
    d.startSection('New Login Form')
    with d.getWCUnitTest('New Login Form') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('xpath', "//span[contains(., 'Standard Login')]"),
            wcElement('id', 'login_user'),
            wcElement('id', 'login_passwd'),
        ], reason='Verify standard elements')

    with d.getWCUnitTest('New Login Form - Login') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', exists=False),
            wcElement('name', 'login_passwd', exists=False),
        ], reason='Ensure the input elements are gone', timeout=20)
        wcunit.verifyJS(validLoginJS)
        wcunit.test(loginSelenium, {}, reason='Login as selenium')

    d.endSection()
    d.startSection('Login Form')

    with d.getWCUnitTest('Default Login Page') as wcunit:
        wcunit.setup(normalizeDB)
        redirect = wcElement('name', '', type='hidden')
        loginElements = [
            wcElement('xpath', "//span[contains(., 'Standard Login')]"),
            wcElement('id', 'login_user'),
            wcElement('id', 'login_passwd'),
        ]
        wcunit.verifyElements(loginElements, reason='Ensures all expected elements are present')

    with d.getWCUnitTest('Login With Valid Credentials') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', exists=False),
            wcElement('name', 'login_passwd', exists=False),
            wcElement('xpath', '//label[@for="login_passwd"]', exists=False)
        ], reason='Ensure the input elements are gone', timeout=20)
        wcunit.verifyJS(validLoginJS)
        wcunit.test(loginSelenium, {}, reason='Login as selenium')

    with d.getWCUnitTest('Login with Invalid Credentials') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements(loginElements)
        wcunit.verifyElements(wcElement('xpath', '//span[contains(text(), "Incorrect log in.")]', exists=True),
            reason='Look for the error message')
        wcunit.verifyJS(invalidLoginJS)
        wcunit.test(loginInvalid)

    with d.getWCUnitTest('Verify Expired Passwords Do Not Allow Logins') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.setup(lambda u: u.getDriver().miedb.dbExec('UPDATE users SET pwd_expire=DATE_SUB(CURDATE(), INTERVAL 10 YEAR) WHERE username=%s', 'selenium'), reason='Ensure the password is expired')
        wcunit.verifyElements(wcElement('xpath', '//strong[text()="Your current password has expired and needs to be reset."]', exists=True),
             reason='Look for the password expired message',
             timeout=20)
        wcunit.test(loginExpiredSelenium, {}, reason='Attempt to log in with expired selenium credentials')

    with d.getWCUnitTest('Forgot Username Screen') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'user_email', maxlength=128, size=42, type='text'),
            wcElement('value', 'Submit'),
			wcElement('xpath', '//h1[text()="username lookup"]')
        ], reason='Ensure the expected elements are present')
        wcunit.test(forgotUsername, {}, reason='Attempt to recover username')

    with d.getWCUnitTest('Reset Password Screen') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', maxlength=255, size=15, type='text'),
            wcElement('value', 'Submit'),
            wcElement('xpath', '//h1[text()="password reset"]')
        ], reason='Ensure the expected elements are present')
        wcunit.test(forgotPassword, {}, reason='Attempt to reset password')

    with d.getWCUnitTest('Invalid Username Lookup') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('xpath', '//*[text()[contains(., "An e-mail containing your username has been sent to the address below.")]]'),
        ], reason='Look for the error message')
        wcunit.test(invalidLookup, reason='Try to lookup the username for an unknown user')

    with d.getWCUnitTest('Valid Username Lookup') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('xpath', '//*[text()[contains(., "Please follow the directions contained in the e-mail to continue")]]'),
        ], reason='Look for the message about the sent email')
        wcunit.test(validLookup)

#    wcunit = d.getWCUnitTest('Invalid Password Reset')
#    wcunit.setup(normalizeDB)
#    wcunit.test(invalidReset)

    with d.getWCUnitTest('Valid Password Reset') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements(wcElement('xpath', '//*[text()[contains(., "You have successfully updated your password.")]]'), timeout=20)
        wcunit.test(validReset)

    with d.getWCUnitTest('Legacy Crypt Passwords Should Convert To SHA512 and Salted') as wcunit:
        wcunit.setup(cryptSetup, reason='Ensure the stored password is an old crypt-style password hash')
        res = []
        wcunit.verifyDB(wcDBRecord("FROM users WHERE username='selenium'", {
            'username': 'selenium',
            'password': lambda x: len(x) == 128,
            'password_salt': lambda x: len(x.split('|').pop()) == 128,
        }, res), reason='Ensures that the password hash is 128 characters and the salt is a pipe delimited 128 characters')
        wcunit.verifyJS(validLoginJS)
        wcunit.test(loginSelenium, {}, reason='Login using regular selenium credentials')

    with d.getWCUnitTest('Verify Upgraded Password is Functional') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', exists=False),
            wcElement('name', 'login_passwd', exists=False),
            wcElement('xpath', '//label[@for="login_passwd"]', exists=False)
        ], timeout=15)
        wcunit.verifyJS(validLoginJS)
        pwData = {}
        wcunit.teardown(capturePassword, pwData, reason='Get the hash for the default password')
        wcunit.test(loginSelenium, {})

    with d.getWCUnitTest('Verify that resetting a password generates a new hash/salt') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyDB(wcDBRecord("FROM users WHERE username='selenium'", {
            'username': 'selenium',
            'password': lambda x: x != res[0]['password'],
            'password_salt': lambda x: x != res[0]['password_salt'],
        }), reason='Ensures that the password hash and salt are not the same as the prior instances')
        wcunit.test(validReset, reason='Reset the password and ensure the hash/salt is brand new')

    with d.getWCUnitTest('Verify Reset Password is Functional') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', exists=False),
            wcElement('name', 'login_passwd', exists=False),
            wcElement('xpath', '//label[@for="login_passwd"]', exists=False)
        ], timeout=20)
        wcunit.verifyJS(validLoginJS)
        wcunit.teardown(restorePassword, pwData, reason='Restore default password data')
        wcunit.test(loginSelenium, {
            'password': 'selenium@123'
        })

    with d.getWCUnitTest('Acccess to nurse with security_role_id') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', exists=False),
            wcElement('name', 'login_passwd', exists=False),
            wcElement('xpath', '//label[@for="login_passwd"]', exists=False)
        ], timeout=20)
        wcunit.verifyJS(validLoginJS)
        wcunit.teardown(restorePassword, pwData, reason='Restore default password data')
        wcunit.test(loginNurse)

    with d.getWCUnitTest('No Acccess to security_role_id=0 nurse user') as wcunit:
        wcunit.setup(normalizeDB)
        wcunit.verifyElements([
            wcElement('name', 'login_user', exists=True),
            wcElement('name', 'login_passwd', exists=True),
            wcElement('xpath', '//label[@for="login_passwd"]', exists=True)
        ])
        wcunit.teardown(restorePassword, pwData, reason='Restore default password data')
        d.miedb.dbExec("UPDATE users SET security_role_id=0 WHERE username='nurse'")
        wcunit.test(loginNurse)

    d.endSection()
