# 
# Webchart Login UnitTest
#
def main (driver, WCURL):
    """
    Verifies that login process works using
    user/pass selenium/selenium
    """
    d = driver

    # Make sure we're logged out to begin with
    d.navigate(WCURL.LOGOUT)

    d.verifyAttribute('href','*f=login&s=ulookup',text='Forgot Username')
    d.verifyAttribute('href','*f=login&s=preset',text='Reset Password')

    d.enterFormData('nosuchuser',id='login_user')
    d.enterFormData('nosuchpassword',id='login_passwd')
    d.clickElement(value='Log On')

    # That should NOT have logged us in, make sure the username field is still on the screen!
    d.verifyElementPresent(id='login_user')

    d.enterFormData('selenium',id='login_user')
    d.enterFormData('selenium',id='login_passwd')
    d.clickElement(value='Log On')

    # Now we should be logged in, make sure the username field is gone
    d.verifyElementPresent(False,id='login_user')
    d.verifyTitle('(Selenium Testing System) - User: (Selenium, Selenium)')
