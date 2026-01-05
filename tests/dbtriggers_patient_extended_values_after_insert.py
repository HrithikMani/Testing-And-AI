#
#Test for wc_patient_extended_values_after_insert.sql
#
from dbtest import SelectTest


def main  (d, WCURL):
    """
    Test the triggers that run when data in the table patient_extended_values is affected.

    Each of the triggers is tested with and without the disable flag to ensure that they all run when
    they are intended to, and that they don't run when they are not meant to.
    """
    
    d.setScreenShotOnError(False)

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
        #with disable flag on (should not modify observations table)
        d.miedb.dbExec("SET @DISABLE_PATIENT_EXTENDED_AFTER_INSERT_TRIGGER=1;INSERT INTO patient_extended_values SET pat_id=0, ext_id=38, value='foo'")


        #without disable flag (default behavior)
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=1, ext_id=25, value='foo'")
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=2, ext_id=27, value='foo'")
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=3, ext_id=29, value='foo'")


        #NULL values (should not change anything in either table)
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=4, ext_id=31, value=NULL")
        d.miedb.dbExec("INSERT INTO patient_extended_values SET pat_id=5, ext_id=NULL, value='foo'")
    except:
        d.addErrorMessage('dbExec failed: ' + d.miedb.dbError())
        return


    test_dict = {'select': [("ev.pat_id",
                            ['0', '1', '2', '3']),
                            ("ev.ext_id",
                            ['38', '25', '27', '29']),
                            ("obs.obs_name",
                            ['NULL', 'pev.caffeine_use', 'pev.living_will', 'pev.tobacco_use']),
                            ("obs.obs_result",
                            ['NULL', 'foo', 'foo', 'foo']),
                            ("obs.obs_code",
                            ['NULL', str(obs_code+1), str(obs_code+2), str(obs_code+3)])],
                 'expr': 'FROM patient_extended_values ev LEFT JOIN observations obs ON ev.pat_id=obs.pat_id WHERE ev.pat_id>=0 AND ev.pat_id<6 ORDER BY ev.pat_id ASC', 
                 'count': 4 }


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
        d.addErrorMessage('Error running query: %s' % e)
        d.addErrorMessage(query_test.__dict__)
        d.addErrorMessage(query_test.query_string)
        return

    try:
        d.miedb.dbExec("DELETE FROM patient_extended_values WHERE pat_id>=0 AND pat_id <6")
        d.miedb.dbExec("DELETE FROM observations WHERE obs_code>%d OR (pat_id>=0 AND pat_id <6)" % (obs_code))
        d.miedb.dbExec("DELETE FROM observation_codes WHERE obs_code>%d" % (obs_code))
        d.miedb.dbExec("DELETE FROM translate WHERE trans_to>%d AND trans_from IN ('pev.caffeine_use','pev.living_will','pev.tobacco_use')" % (obs_code))
        d.miedb.dbExec("ALTER TABLE observation_codes AUTO_INCREMENT=1")
    except:
        d.addErrorMessage('dbExec failed: ' + d.miedb.dbError())