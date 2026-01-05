"""
    Unit Test for chart purge module

    THIS TEST IS NOT READY FOR RUNNING YET
    @owner: sgrider
"""
from wcunittest import wcElement, wcDBRecord

def createChart(unit, data):
    sql = "REPLACE INTO patients (%s) VALUES (%s)" %(','.join(data.keys()),
        ','.join(['%s'] * len(data)))
    d = unit.getDriver()
    res = d.miedb.dbExec(sql, *data.values())
    return str(res.lastrowid)

def setPermission(unit, value):
    d = unit.getDriver()
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
        "WHERE module_name='Control' AND category_name='Purge Charts' "\
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
        "username=%s)", value, d.getUserData('selenium_username'))

def deleteChart(unit, chart_id):
    unit.getDriver().miedb.dbExec('DELETE FROM patients WHERE pat_id=%s', unit.getSetupData()[0])

def purgeCharts(unit, data):
    unit.getDriver().navigate('?f=ajaxpost&s=purge_chart&chart_id=' + unit.getSetupData()[0])

def main(d, _):
    # Purge charts is an ajaxpost and that makes it hard to validate the output of the xml
    # without resorting to using wccurl. So instead I'm just going to hit the urls and then
    # check that it either worked or didn't using the preseence of the expected db records
    with d.getWCUnitTest('No permission') as u:
        u.setup(createChart, {
            'last_name': 'McPurgerson',
            'first_name': 'Purgy',
            'email': 'purgy@mieweb.com'
        }, reason='Make a new chart')
        u.setup(setPermission, 0, reason='Turn off permission')
        u.teardown(deleteChart, reason='Delete the new chart')
        # Need to fix this so that queries can access setupdata or userdata
        u.verifyDB(wcDBRecord("FROM patients WHERE first_name='Purgy'",
            {'first_name': 'Purgy'}), reason='Ensure the chart is still there')
        u.test(purgeCharts, reason='Try to purge the chart')
