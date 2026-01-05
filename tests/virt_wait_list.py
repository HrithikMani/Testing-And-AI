"""
    Unit Test for virtual waiting room 
    @owners: dcornewell
    @filedeps: src/login.c, src/wclogdb.c
"""

def main (d, WCURL):
    """
    Tests getting sent to virtual waiting room 
    """
    d.startSection('Gets to login using portal URL when under active limit')
    d.navigate("?f=logout")
    d.navigate("?f=layout&module=Patient+Portal")
    d.verifyElementPresent(True,xpath="//input[@name='login_user']")
    d.endSection()

    d.startSection('Configure limited active logins low and add some logins')
    d.miedb.dbExec("INSERT INTO logins SET session_id='TEST1',user_id=500,login_dt=(SELECT value FROM system_settings WHERE item='Demo Date')")
    d.miedb.dbExec("INSERT INTO logins SET session_id='TEST2',user_id=500,login_dt=(SELECT value FROM system_settings WHERE item='Demo Date')")
    d.wcutils.SetSystemSetting("System","Login","Portal Max Active Logins","2",False)
    d.endSection()

    d.startSection('User is forwarded to virtual waiting list when too many active users')
    d.navigate("?f=logout")
    d.navigate("?f=layout&module=Patient+Portal")
    d.verifyElementPresent(True,xpath="//title[contains(., 'Queue')]")
    d.screenshot('Queued Site')

    d.wcutils.SetSystemSetting("System","Login","Portal Max Active Logins","500",False)
    d.endSection()
