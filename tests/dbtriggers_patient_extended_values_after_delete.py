#
#Test for wc_patient_extended_values_after_delete.sql
#
from dbtest import SelectTest


def main  (d, WCURL):
    """
    Test the triggers that run when data in the table patient_extended_values is affected.

    Each of the triggers is tested with and without the disable flag to ensure that they all run when
    they are intended to, and that they don't run when they are not meant to.
    """

    d.setScreenShotOnError(False)

    #obtain max observation code
    try:
        dbres = d.miedb.dbQuery("SELECT MAX(obs_code) from observation_codes")
        row = dbres.getRow(0)
        if 'MAX(obs_code)' in row and row['MAX(obs_code)']:
            obs_code = int(row['MAX(obs_code)'])
        else:
            d.addErrorMessage('Unable to determine max observation code')
            return
        
    except Exception as e:
        d.addErrorMessage('dbQuery failed: ' + d.miedb.dbError())
        return

    try:
        #insert values that can be deleted
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=1, ext_id=12, value='foo'")
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=2, ext_id=11, value='foo'")

        #delete with disable flag off (default bahavior)
        d.miedb.dbExec("DELETE FROM patient_extended_values WHERE ext_id=11 AND pat_id=2")

        #delete with disable flag on (should not change observations table)
        d.miedb.dbExec("SET @DISABLE_PATIENT_EXTENDED_AFTER_DELETE_TRIGGER=1;DELETE FROM patient_extended_values WHERE ext_id=12 AND pat_id=1")

    except Exception as e:
        d.addErrorMessage('dbExec failed: ' + d.miedbError())
        return
   


    test_dict = {'select': [("obs.pat_id",
                            ['1', '2', '2']),
                            ("ev.ext_id",
                            ['NULL', 'NULL', 'NULL']),
                            ("obs.obs_name",
                            ['pev.pat_misc', 'pev.pat_diet', 'pev.pat_diet']),
                            ("obs.obs_result",
                            ['foo', 'DELETED', 'foo']),
                            ("obs.obs_code",
                            [str(obs_code+1), str(obs_code+2), str(obs_code+2)])],
                 'expr': 'FROM patient_extended_values ev RIGHT JOIN observations obs ON ev.pat_id=obs.pat_id WHERE obs.pat_id>=0 AND obs.pat_id<6 ORDER BY obs.pat_id ASC',
                 'count': 3 }


    try:
        query_test = SelectTest(d, test_dict)
    except ValueError as e:
        d.addErrorMessage('Error creating test object: %s' % e)
        return

    try:
        query_test.run_query()

        if query_test.count_error():
            d.startSection('Incorrect number of rows returned')
            d.reportCommandStatus('count_error', 'Given: %d' % query_test.expected_count(), False, 'Returned: %d' % query_test.count(), '')
            d.endSection()

        for field, rows in query_test.status():
            d.startSection('Column: ' + field)
            for row in rows:
                d.reportCommandStatus('status', row['given_value'], row['passed'], row['return_value'], '')
            d.endSection()
    except Exception as e:
        d.addErrorMessage('Error running Query: %s' % e)
        d.addErrorMessage(query_test.__dict__)
        d.addErrorMessage(query_test.query_string)
        return

    try:
        d.miedb.dbExec("DELETE FROM patient_extended_values WHERE pat_id>=0 AND pat_id <6")
        d.miedb.dbExec("DELETE FROM observations WHERE obs_code>%d OR (pat_id>=0 AND pat_id <6)" % (obs_code))
        d.miedb.dbExec("DELETE FROM observation_codes WHERE obs_code>%d" % (obs_code))
        d.miedb.dbExec("DELETE FROM translate WHERE trans_to>%d AND trans_from IN ('pev.pat_diet','pev.pat_misc')" % (obs_code))
        d.miedb.dbExec("ALTER TABLE observation_codes AUTO_INCREMENT=1")
    except:
        d.addErrorMessage('dbExec failed: ' + d.miedb.dbError())
