def main(d, WCURL):
    """
    This test is not to be run in any Module, it is simply 
    a test to ensure that the wctest.py framework is behaving
    as expected
    """
    d.reportCommandStatus('Loaded miedb', '', hasattr(d,'miedb'), '', d.getUserData('dbConf'))
    d.reportCommandStatus('Loaded wcutils', '', hasattr(d,'wcutils'), '', d.wcutils)
    d.reportCommandStatus('Loaded webserver', '', hasattr(d, 'getWebServer'), '', d.getWebServer())
    d.reportCommandStatus('Loaded callstacks', '', hasattr(d, 'getCallStack'), '', d.getCallStack())
    d.reportCommandStatus('Loaded zeusServer', '', d.getUserData('zeusServer'), '', d.getUserData('zeusServer'))
    
    z = d.getUserData('zeusServer')
    ret = z.execCommand('hostname && whoami && pwd')
    d.reportCommandStatus('whoami on zeusServer', '', ret.returnCode() == 0, ret.stdout(), ret.stderr())
    z = d.getWebServer()
    ret = z.system('hostname && whoami && pwd')
    d.reportCommandStatus('whoami on webserver', '', ret.returnCode() == 0, ret.stdout(), ret.stderr())

    res = d.miedb.dbQuery("SELECT value FROM system_settings WHERE module='WebChart' AND section='Demo' AND item='Demo Date'")
    date = res.getRow(0)['value']
    expected = f'{d.getUserData("run_datetime")}'
    d.reportCommandStatus('Demo Date', expected, date == expected, '', date)

    d.navigate(WCURL.LOGOUT)
    d.navigate()

    d.screenshot('VALIDATION_LOGIN_PAGE')
    
    # Why exclude these 4 columns?
    # Because uuid and datetime obviously change
    # System_owner changes because it was initially installed by a developer
    # but then selenium took over and reinstalled it. Kind of expected
    # System_rc is no longer known because once we submit a test we no longer
    # have access to the git project from which it was built so we don't know
    # anything about the source version. I would like to keep this populated,
    # but I'm not sure it's that big of a deal.
    q = "SELECT name, value FROM system_info WHERE name NOT IN "\
        "('UUID', 'INSTALL_DATETIME', 'SYSTEM_OWNER', 'SYSTEM_RC')"
    res = d.miedb.dbQuery(q)
    before = res.getRes()
    d.wcutils.resetSystem(systemType='WCNOW', force=True)
    res = d.miedb.dbQuery(q)
    after = res.getRes()
    d.reportCommandStatus('Verify system_info',q,
                          before == after,
                          before if not before == after else '',
                          after if not before == after else '')
