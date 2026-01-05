def main(d, WCURL):
    """
    Verifies that the merge manager is functioning correctly
    by entering some search criteria and ensuring that a listview displays.
    """
    d.navigate(WCURL.MERGE_MANAGER)

    d.enterAutocomplete('to_pat_id_ac','Hart',0)
    d.enterAutocomplete('user_id_ac','Selen',0)
    d.enterMIEDate('start_date',1,1,2000)
    d.enterMIEDate('end_date',1,1,2016)
    d.enterFormData(True,id='show_details')
    d.enterFormData(True,id='show_query')
    d.clickElement(value='Search')

    d.verifyElementPresent(True,id='lv_Patient Merge Log_span_title')
