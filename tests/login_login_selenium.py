def main(d, WCURL):
    """
    Logs into WebChart using the standard selenium/selenium
    username/password combination.
    Verifies the login process by making sure the Log On button
    is no longer present and that the page title has changed.
    """
    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    username = d.getUserData('username')
    password = d.getUserData('password')
    d.enterFormData(username,id='login_user')
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')

    if not d.verifyElementPresent(False,value='Log On'):
        d.addErrorMessage('The Log On button is still present on the page')
    d.verifyTitle('WebChart Testing System')
