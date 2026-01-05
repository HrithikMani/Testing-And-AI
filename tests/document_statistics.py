"""
@owners: ccartwright
"""
from wcunittest import wcDBRecord

def main(d, WCURL):
    t = d.getWCUnitTest('Add Document')
    t.setup(lambda d: d.miedb.dbExec("INSERT INTO documents (user_id, pat_id, doc_type, interface, origin_id, storage_type, service_location, origin_date, enter_date, revision_date, service_date) VALUES (8, 2, 'FRED', 'FLINTSTONE', 1, 1, 'OFFICE', '2007-02-02 09:15:00', '2007-02-02 09:15:00', '2007-02-02 09:15:00', '2007-02-02 09:15:00'); INSERT INTO documents_txt (doc_id, subject, txt_value) VALUES (last_insert_id(), 'bogus document trigger test document', 'Nothing to see here: mind your business.')"))
    t.setup(lambda d: d.miedb.dbExec("	INSERT INTO documents (user_id, pat_id, doc_type, interface, origin_id, storage_type, service_location, origin_date, enter_date, revision_date, service_date) VALUES (8, 2, 'WILMA', 'FLINTSTONE', 1, 1, 'OFFICE', '2007-02-02 09:15:00', '2007-02-02 09:15:00', '2007-02-02 09:15:00', '2007-02-02 09:15:00'); INSERT INTO documents_txt (doc_id, subject, txt_value) VALUES (last_insert_id(), 'bogus document trigger test document #2', 'Nothing to see here: mind your business.')"))
    t.verifyDB([
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='FRED' AND storage_type=1",
            { 'num_docs': 1 }),
        wcDBRecord( "FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='WILMA' AND storage_type=1",
            { 'num_docs': 1 }),
          ], reason = 'Ensure that two rows get inserted into document_statistics.')
    t.test()

    t = d.getWCUnitTest('UPDATE Document')
    t.setup(lambda d: d.miedb.dbExec("UPDATE documents SET doc_type='BARNEY' WHERE doc_type='FRED' AND interface='FLINTSTONE' AND storage_type=1"))
    t.verifyDB([
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='FRED' AND storage_type=1",
                { 'num_docs': 0 }),
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='BARNEY' AND storage_type=1",
                { 'num_docs': 1 }),
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='WILMA' AND storage_type=1",
                { 'num_docs': 1 }),
          ], reason = 'Ensure that the counts document_statistics are properly updated.')
    t.test()

    t = d.getWCUnitTest('Make an irrelevant change')
    t.setup(lambda d: d.miedb.dbExec("UPDATE documents SET user_id=2 WHERE doc_type='BARNEY' AND interface='FLINTSTONE' AND storage_type=1"))
    t.verifyDB([
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='FRED' AND storage_type=1",
                { 'num_docs': 0 }),
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='BARNEY' AND storage_type=1",
                { 'num_docs': 1 }),
        wcDBRecord("FROM document_statistics WHERE interface='FLINTSTONE' AND doc_type='WILMA' AND storage_type=1",
                { 'num_docs': 1 }),
          ], reason = 'Ensure that the counts document_statistics in document_statistics don\'t change when they shouldn\'t .')
    t.test()

