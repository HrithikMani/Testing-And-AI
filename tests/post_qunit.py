def main(d, _):
    d.wcutils.insertWCTSession(d.getUserData('selenium_username'))
    d.navigate('?f=layout&wclmodule=UnitTest&wclname=qunit')
    d.waitFor(d, lambda d: d.runJS("return (QUnitResults && QUnitResults.complete === true)"))
    res = d.runJS("return QUnitResults")
    if not res or not res['complete']:
        d.reportCommandStatus('QUnit Results Incomplete', res, False, '', '')
        d.screenshot('QUnit Incomplete')
    else:
        if res['details']['failed'] > 0 and res['details']['failed'] != res['todo']:
            d.reportCommandStatus('QUnit Test Failures', '{0} Failure(s)'.format(
                res['details']['failed'] - res['todo']), False, '',
                ','.join(['{0}:{1}'.format(f['module'], f['name']) for f in res['failures']]))
            d.screenshot('QUnit Failed')
        else:
            d.reportCommandStatus('QUnit Success', '{0} Tests Passed in {1}ms'.format(
                res['details']['passed'], res['details']['runtime']), True, '', '')
 
