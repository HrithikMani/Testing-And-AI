"""
    Encounter Stub Document Unit Test
    @owners: gjones
"""

def main (d, WCURL):
    """
        Create and view a stub encounter document
    """
    pat_id = 18
    doc_date = '2001-01-01'

    
    # Make sure stub ext_id exists
    ext_name = "archive_stub"
    ext_id = None
    res = d.miedb.dbQuery("SELECT ext_id FROM encounter_extended_index WHERE name=%s", ext_name)
    if res:
        row = res.getRow(0)
        if row:
            ext_id = row['ext_id']
        else:
            ret = d.miedb.dbExec("INSERT INTO encounter_extended_index SET name=%s", ext_name)
            ext_id = ret.lastrowid
    else:
        d.reportCommandStatus("Query failure", "", False, "", "Unable to query for encounter_extended_index")
        return

    # Make encounter
    ret = d.miedb.dbExec("INSERT INTO encounters SET pat_id=%s, visit_type='VISIT', serv_date=%s, comment='Stub', chief_complaint='Stub Test', closed=1", pat_id, doc_date)
    encounter_id = ret.lastrowid

    # Make encounter extended
    d.miedb.dbExec("INSERT INTO encounter_extended_values SET enc_id=%s, ext_id=%s, value='1'", encounter_id, ext_id)

    # Make observation
    ret = d.miedb.dbExec("INSERT INTO observations SET pat_id=%s, obs_name='PlanNarrative'," +
        " obs_code=(SELECT obs_code FROM observation_codes WHERE obs_name='PlanNarrative' LIMIT 1), obs_result='Do the thing'," +
        " observed_datetime=%s, template_id='', test_comments='', free_text='', micro_result='', interpretive_text=''",
        pat_id, doc_date)
    obs_id = ret.lastrowid

    # Make encounter link
    d.miedb.dbExec("INSERT INTO encounters_link SET encounter_id=%s, module=3, linked_id=%s", encounter_id, obs_id)

    # Make document
    ret = d.miedb.dbExec("INSERT INTO documents SET pat_id=%s, storage_type=4, doc_type='VISIT', origin_date=%s, enter_date=%s, revision_date=%s, service_date=%s",
        pat_id, doc_date, doc_date, doc_date, doc_date)
    doc_id = ret.lastrowid

    # Make encounter-document
    d.miedb.dbExec("INSERT INTO encounter_documents SET doc_id=%s, encounter_id=%s, layout_name='View Visit'", doc_id, encounter_id)

    d.navigate(WCURL.DOCUMENT + "doc_id=" + str(doc_id))
    d.verifyElementPresent(xpath="//*[contains(text(), 'Stub Test')]")
    d.verifyElementPresent(xpath="//*[contains(text(), 'Do the thing')]")
