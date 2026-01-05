def main(d, WCURL):
    """
    Verifies that the username lookup process is
    working correctly by entering the user email address
    into the forgot username field.
    Can't actually check that the email is sent, but makes sure
    the process doesn't fail on the client side.
    """
    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    d.clickElement(text='Forgot Username')

    d.verifyTitle('WebChart: WebChart Testing System User Lookup')

    d.enterFormData('private_hudson@gameoverman.com', id='user_email')
    d.clickElement(value='Submit')

    msg = 'The email address you entered was not found in our records.'
    d.verifyAttribute('text', msg, xpath="//h2")

    email = '{0}@mieweb.com'.format(d.getUserData('developer'))
    d.enterFormData(email, id='user_email')
    d.clickElement(value='Submit')

    msg = "An e-mail containing your username has been sent to {0}.\n"\
          "Please follow the directions contained in the e-mail to continue.".format(email)
    d.verifyAttribute('text', msg, xpath="//h2")

