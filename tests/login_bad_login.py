def main(d, WCURL):
    """
    Verifies that WebChart will not allow a user
    with fake information to successfully login to
    WebChart. Ensures this by making sure the Log On
    button is still present and that the page title 
    has not changed.
    """
    # Make sure we start with a 0 login_failcount
    d.miedb.dbExec("UPDATE users SET login_failcount=0 WHERE username='selenium'")

    d.navigate(WCURL.LOGOUT)
    title = 'WebChart: WebChart Testing System Log On'
    if not d.verifyTitle(title):
        d.addErrorMessage('The page title did not match what was expected\
                           continue this test.')
        return

    username = 'something wrong'
    password = 'not even close'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with fake credentials \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    username = 'selenium'
    password = ''
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with blank password \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    username = 'selenium'
    password = 'SELENIUM'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with a capitalized password \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    password = 'seleniu'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with a truncated password \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    password = 'selenium123'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with extra characters on password \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    password = 'oh god I need access to my account!'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with a junk password \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    password = 'I think I just locked my account, help me'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with a junk password \
                               worked when it should not have')
            return
    else:
        d.addErrorMessage('The page title should not have changed, but it did')
        return

    msg = '*This account has been locked. Contact your administrator.'
    if not d.verifyAttribute('text',msg,id='login_message'):
        d.addErrorMessage('The account does not appear to be locked after 5 failed \
                          login attempts')
        return

    username = 'selenium'
    password = 'selenium'
    d.enterFormData(username,id='login_user',clear=True)
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    if d.verifyTitle(title):
        if not d.verifyElementPresent(True,value='Log On'):
            d.addErrorMessage('Attempted login with a locked account \
                               worked when it should not have')
        else:
            d.verifyAttribute('text', msg, id='login_message')
    else:
        d.addErrorMessage('The page title should not have changed, but it did')


    # Reset the login_failcount in the database
    d.miedb.dbExec("UPDATE users SET login_failcount=0 WHERE username='selenium'")
