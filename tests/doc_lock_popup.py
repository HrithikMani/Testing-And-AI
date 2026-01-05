def main (d, WCURL):
    """
    Verifies the functionality of the close button in the document edit lock 
    """
    doc_id = '131'

    if not d.miedb.dbExec("INSERT INTO record_locks SET module_type='document', module_id=%s, user_id=26, lock_datetime='2013-07-13 10:10:10'" %doc_id):
        raise Exception(d.miedb.dbError())
    
    d.navigate(WCURL.ECHART)
    d.clickElement(xpath='//input[@name="by" and @value="d"]')
    d.enterFormData(doc_id, name='sstring')
    d.clickElement(value='Search')

    d.clickElement(id='edit_doc%s' %doc_id)
    d.switchToPopup()
    d.screenshot()

    d.clickElement(id='close_lock')
    d.closePopup()

    if not d.miedb.dbExec("DELETE FROM record_locks WHERE module_id=%s AND lock_datetime='2013-07-13 10:10:10'" %doc_id):
        raise Exception(d.miedb.dbError())
