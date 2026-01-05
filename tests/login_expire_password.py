def main (d, WCURL):
    """
    Tests the password expiring functionality by forcefully
    expiring a users password using a custom layout.
    The user's password is then reset to its original value
    """
    d.navigate(WCURL.LOGOUT, report=False)
    d.navigate()
    username = 'selenium'
    password = 'selenium1?'
    d.enterFormData(username,id='login_user')
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')

    d.navigate(WCURL.LAYOUT+'module=testtaglayouts&name=wcuserexppw',auto_screenshot=False);
    d.navigate(WCURL.LOGOUT)

    d.enterFormData(username,id='login_user')
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')

    # That should have brought up the changed password elements
    d.verifyElementPresent(id="login_new_vpasswd")

    d.verifyElementPresent(True, xpath="//*[text()='Your current password "\
    "has expired and needs to be reset.']")

    d.enterFormData(password,id='login_new_passwd')
    d.enterFormData(password,id='login_new_vpasswd')
    d.clickElement(value='Log On')

    d.verifyElementPresent(False,id='login_user')
    d.verifyTitle('WebChart Testing System')
