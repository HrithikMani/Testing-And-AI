from wcunittest import wcElement

def main(d, WCURL):
    curl = d.getWCCurl(d._base_urls[-1]);
    curl.setHeaders({'Referer': 'https://pm.mieweb.com'})

    u = d.getWCUnitTest('Confirm JSON API requests get a referrer warning')
    u.setup(lambda d: d.navigate('/webchart.cgi/json/'), reason='JSON API')
    u.verifyElements([
        wcElement('xpath', "//h1[contains(., 'Looks like you navigated to ') and contains(., 'from an outside website')]", exists=True),
    ])
    u.test(reason='Ensure we get a referrer warning for JSON API')

    u = d.getWCUnitTest('Confirm f=chart request gets a referrer warning')
    curl.setHeaders({'Referer': 'https://pm.mieweb.com'})
    u.setup(lambda d: d.navigate('?f=chart'), reason='E-Chart is enough CGI vars to trigger warning')
    u.verifyElements([
        wcElement('xpath', "//h1[contains(., 'Looks like you navigated to ') and contains(., 'from an outside website')]", exists=True),
    ])
    u.test(reason='Ensure we get a referrer warning for E-Chart')

    u = d.getWCUnitTest('Confirm no login layout request gets a referrer warning when logged in')
    curl.setHeaders({'Referer': 'https://pm.mieweb.com'})
    u.setup(lambda d: d.navigate('?f=layoutnouser&name=RXDBmain'), reason='No login layout with a login session')
    u.verifyElements([
        wcElement('xpath', "//h1[contains(., 'Looks like you navigated to ') and contains(., 'from an outside website')]", exists=True),
    ])
    u.test(reason='Ensure we get a referrer warning for layoutnouser when logged in')

    # Make sure we're logged out for next tests
    d.navigate(WCURL.LOGOUT)

    u = d.getWCUnitTest('Confirm base url does not get a referrer warning')

    curl.setHeaders({'Referer': 'https://pm.mieweb.com'})
    u.setup(lambda d: d.navigate('?'), reason='User home page')
    u.verifyElements([
        wcElement('xpath', "//h1[contains(., 'Looks like you navigated to ') and contains(., 'from an outside website')]", exists=False),
    ])
    u.test(reason='Ensure we do not get a referrer warning for User home page')

    u = d.getWCUnitTest('Confirm covranded portal URL does not get a referrer warning')
    curl.setHeaders({'Referer': 'https://pm.mieweb.com'})
    u.setup(lambda d: d.navigate('?svar_cobrand_patid=41'), reason='Co-Branded portal')
    u.verifyElements([
        wcElement('xpath', "//h1[contains(., 'Looks like you navigated to ') and contains(., 'from an outside website')]", exists=False),
    ])
    u.test(reason='Ensure we do not get a referrer warning for Co-Branded portal')

    u = d.getWCUnitTest('Confirm no login layout does not get a referrer warning when not logged in')
    curl.setHeaders({'Referer': 'https://pm.mieweb.com'})
    u.setup(lambda d: d.navigate('?f=layoutnouser&name=RXDBmain'), reason='No login layout without a login session')
    u.verifyElements([
        wcElement('xpath', "//h1[contains(., 'Looks like you navigated to ') and contains(., 'from an outside website')]", exists=False),
    ], reason='Ensure we do not get a referrer warning')

    u.teardown(lambda d: d.wcutils.insertWCTSession('selenium'))
    u.test(reason='Ensure we do not get a referrer warning for layoutnouser when not logged in')
