def main (d, WCURL):
    doc_id = '131'

    if not d.miedb.dbExec("INSERT INTO record_locks SET module_type='document', module_id=%s, user_id=26, lock_datetime='2013-07-13 10:10:10'" %doc_id):
        raise Exception(d.miedb.dbError())
