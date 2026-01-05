def main(d, WCURL):
    """
    Log into webchart with a user that does not have a salt.
    Ensure after logging in that they now have a salt and ensure
    that they may log out and back in correctly with the new salt.
    """
    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    username = 'selenium'
    password = 'selenium'
    salt = 'XY'
    hash = 'XYVeVFl1l2FBk'
    db = d.miedb
    db.dbExec("UPDATE users SET password=%s,"\
              "pwd_expire=DATE_ADD(CURDATE(), INTERVAL 10 YEAR) "\
              "WHERE username=%s", hash, username)
    d.enterFormData(username, id='login_user')
    d.enterFormData(password, id='login_passwd')
    d.clickElement(value='Log On')
    d.verifyElementPresent(False, value='Log On')

    res = db.dbQuery("SELECT password, password_salt FROM users "\
                     "WHERE username=%s", username)
    if not res:
        raise Exception("Failed to query users table", db.dbError())
    hash = res.getRow(0)['password']
    salt = res.getRow(0)['password_salt']
    d.reportCommandStatus('Password Upgrade', 'To SHA512', len(hash) == 128, '', hash)
    d.reportCommandStatus('Salt Generation', '', len(salt), '', salt)

    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    d.enterFormData(username, id='login_user')
    d.enterFormData(password, id='login_passwd')
    d.clickElement(value='Log On')
    d.verifyElementPresent(False, value='Log On')

    password = 'selenium1?' # We can't use username for password
    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    d.clickElement(text='Reset Password')
    d.enterFormData(username, id='login_user')
    d.clickElement(value='Submit')
    d.enterFormData('260-459-6270', id='preset_secret_answer')
    d.clickElement(value='Submit')
    d.enterFormData('46804', id='preset_zip_answer')
    d.clickElement(value='Submit')
    d.enterFormData(password, id='preset_np')
    d.enterFormData(password, id='preset_vp')
    d.clickElement(value='Submit')
    d.clickElement(value='Continue')
    res = db.dbQuery("SELECT password, password_salt FROM users "\
                     "WHERE username=%s", username)
    if not res:
        raise Exception("Failed to query users table", db.dbError())
    newp = res.getRow(0)['password']
    news = res.getRow(0)['password_salt']
    d.reportCommandStatus('New Salt', '', news != salt, '', news)

    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    d.enterFormData(username, id='login_user')
    d.enterFormData(password, id='login_passwd')
    d.clickElement(value='Log On')
    d.verifyElementPresent(False, value='Log On')
