"""
@owners: dcornewell
"""
from wcunittest import wcElement, wcDBRecord

# Verify cannot merge temp to non temp
# Verify cannot merge when patient is logged in
# Verify can merge otherwise

def addMergeTestCharts(unit, pat):
    d = unit.getDriver()
    ret = {
        'patients': None,
        'patient_partitions': None,
        'patient_mrns': None
    }
    sql = "REPLACE INTO patients (%s) VALUES (%s)" %(','.join(pat.keys()),
        ','.join(['%s'] * len(pat)))
    res = d.miedb.dbExec(sql, *pat.values())
    ret['patients']={'pat_id': res.lastrowid}
    d.miedb.dbExec("REPLACE INTO patient_partitions (wc_partition, name, active) VALUES "\
        "('UnitTest', 'UnitTest', 1)")
    ret['patient_partitions']={'id': res.lastrowid}
    d.miedb.dbExec("REPLACE INTO patient_mrns (wc_partition, mrnumber, pat_id) VALUES "\
        "('UnitTest', %s, %s)",
        pat['first_name'][-1], ret['patients']['pat_id'])
    ret['patient_mrns']={'id': res.lastrowid}
    return ret

def updateMergeTestChartsLoggedin(unit, udata):
    data = unit.getSetupData()
    d = unit.getDriver()
    to_pat_id=data[0]['patients']['pat_id']
    from_pat_id=data[1]['patients']['pat_id']
    d.miedb.dbExec("INSERT INTO logins (session_id,user_id,login_dt) "\
                               "SELECT UUID(),id,NOW() FROM user_patients WHERE role_id=501 AND id_type='user' AND pat_id={id}".format(**{
        'id': from_pat_id
    }))

def navigateMergeTestCharts(unit, udata):
    data = unit.getSetupData()
    d = unit.getDriver()
    to_pat_id=data[0]['patients']['pat_id']
    from_pat_id=data[1]['patients']['pat_id']
    d.navigate("?f=chart&s=pat&opp=merge&merge_opts_{from_pat_id}=1&pat_id={to_pat_id}&from_pats_id={from_pat_id}&submit_merge=".format(**{
        'from_pat_id': from_pat_id,
        'to_pat_id': to_pat_id
    }))

def dbDeletes(unit, udata):
    data = unit.getSetupData()
    for d in range(0,1):
        unit.getDriver().miedb.dbExec("DELETE FROM {table} WHERE {column}={id}".format(**{
            'table': 'patients',
            'column': 'pat_id',
            'id': data[d]['patients']['pat_id']
        }))
        unit.getDriver().miedb.dbExec("DELETE FROM {table} WHERE {column}={id}".format(**{
            'table': 'patient_partitions',
            'column': 'id',
            'id': data[d]['patient_partitions']['id']
        }))
        unit.getDriver().miedb.dbExec("DELETE FROM {table} WHERE {column}={id}".format(**{
            'table': 'patient_mrns',
            'column': 'id',
            'id': data[d]['patient_mrns']['id']
        }))

def main(d, WCURL):
    with d.getWCUnitTest('Verify cannot merge temp to non temp', timeout=30) as u:
        u.setup(addMergeTestCharts, {
            'last_name': 'MergeMe',
            'first_name': 'Tester1',
            'is_tmp': 1
        }, reason='Insert a patient to merge to')
        u.setup(addMergeTestCharts, {
            'last_name': 'MergeMe',
            'first_name': 'Tester1',
            'is_tmp': 0
        }, reason='Insert a patient to merge from')
        u.setup(navigateMergeTestCharts, reason='Navigate directly merging them where we should get an error')
        u.verifyElements([
            wcElement('xpath', '//span[@class="alert"][contains(.,"Cannot Merge to a Temporary")]'),
        ], reason='Confirm the message that we cannot merge')
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test()

    with d.getWCUnitTest('Verify cannot merge chart when patient is logged in', timeout=30) as u:
        u.setup(addMergeTestCharts, {
            'last_name': 'MergeMe',
            'first_name': 'Tester1',
            'is_tmp': 0
        }, reason='Insert a patient to merge to')
        u.setup(addMergeTestCharts, {
            'last_name': 'MergeMe',
            'first_name': 'Tester1',
            'is_tmp': 0
        }, reason='Insert a patient to merge from')
        u.setup(updateMergeTestChartsLoggedin, {}, reason='Make from chart logged in')
        u.setup(navigateMergeTestCharts, reason='Navigate directly merging them where we should get an error')
        u.verifyElements([
            wcElement('xpath', '//span[@class="alert"][contains(.,"is currently logged in")]'),
        ], reason='Confirm the message that we cannot merge')
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test()

    with d.getWCUnitTest('Verify can merge chart when thing are ok', timeout=30) as u:
        u.setup(addMergeTestCharts, {
            'last_name': 'MergeMe',
            'first_name': 'Tester1',
            'is_tmp': 0
        }, reason='Insert a patient to merge to')
        u.setup(addMergeTestCharts, {
            'last_name': 'MergeMe',
            'first_name': 'Tester1',
            'is_tmp': 0
        }, reason='Insert a patient to merge from')
        u.setup(navigateMergeTestCharts, reason='Navigate directly merging them where we should get an error')
        u.verifyElements([
            wcElement('xpath', '//span[@class="information"][contains(.,"Merge results for")]'),
        ], reason='Confirm the message that we can merge')
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test()