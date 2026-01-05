def main(d, WCURL):
    """
    Verifies that the reset password process is
    working correctly by entering the selenium username
    into the password reset field.
    Can't actually check that the email is sent, but makes sure
    the process doesn't fail on the client side.
    """
    d.navigate(WCURL.LOGOUT,report=False)
    d.navigate()
    d.clickElement(text='Reset Password')
    
    title = 'WebChart: WebChart Testing System Password Reset'
    if not d.verifyTitle(title):
        d.addErrorMessage('Either the link took us to the wrong \
                          page or the password reset page title changed')
    else:
        d.enterFormData('Murphy',id='login_user')
        d.clickElement(value='Submit')
        d.enterFormData('McManus',id='preset_secret_answer')
        d.clickElement(value='Submit')
        d.enterFormData('46804',id='preset_zip_answer')
        d.clickElement(value='Submit')

        msg = 'Your password cannot be reset.\nThere may be a problem with the '
        msg += 'username you entered, or you have answered one or more of the questions incorrectly.'
        d.verifyAttribute('text',msg,xpath="//h2")

        d.clickElement(text="click here to try again")
        if not d.verifyTitle(title):
            d.addErrorMessage('Either the link took us to the wrong \
                              page or the password reset page title changed')
        else:
            d.enterFormData('selenium',id='login_user')
            d.clickElement(value='Submit')
            d.enterFormData('260-459-6270',id='preset_secret_answer')
            d.clickElement(value='Submit')
            d.enterFormData('46804',id='preset_zip_answer')
            d.clickElement(value='Submit')

            d.enterFormData('selenium1?',id='preset_np')
            d.enterFormData('selenium1?',id='preset_vp')
            d.setUserData('password','selenium1?')

            # Do this so we don't really send an email
            d.miedb.dbExec("UPDATE users SET email='' WHERE username='selenium'")

            d.clickElement(value='Submit')
            d.verifyAttribute('text','You have successfully updated your password.',xpath="//h2")
            d.clickElement(value='Continue')

            title = 'WebChart: WebChart Testing System Log On'
            if not d.verifyTitle(title):
                d.addErrorMessage('Either the link has taken us to the wrong page \
                                  or the login page title has changed')
