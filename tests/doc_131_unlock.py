def main (d, WCURL):
    doc_id = '131'

    if not d.miedb.dbExec("DELETE FROM record_locks WHERE module_id=%s AND lock_datetime='2013-07-13 10:10:10'" %doc_id):
        raise Exception(d.miedb.dbError())
