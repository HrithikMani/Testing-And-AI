def main (d, WCURL):
    """
    Adds a task 'F/U Appointment' and assigns it to
    'self' (selenium) and verifies that it shows up
    in the task listview.
    """
    d.navigate(WCURL.CHART_HART_WILLIAM)

    note = 'Added Task via Selenium'

    d.clickElement(text='Add Task')
    d.clickElement(text='F/U Appointment')
    d.enterFormData(note,id='notes',clear=True)
    d.enterFormData(True,id='assign_to0')
    d.clickElement(value='Add Task')

    d.navigate(WCURL.TASK_SEARCH)
    d.enterFormData('F/U Appointment',id='task_template')
    #d.clickElement(id='entry_start_dateTODAY')
    #d.clickElement(id='entry_end_dateTODAY')
    d.clickElement(value='Submit')

    d.verifyElementPresent(True,xpath="//div[@id='lv_task_search_span']//td[text()='%s']" %note)

    # Change regard_type patient to pat_id as if it had been created from a scriptlet
    query = "UPDATE tasks SET regard_type='pat_id' ORDER BY task_id DESC LIMIT 1"
    if not d.miedb.dbExec(query):
        d.addErrorMessage(d.miedb.dbError())
        d.reportCommandStatus('dbExec', query, False, '', d.miedb.dbError())
        return

    d.navigate(WCURL.TASK_SEARCH)
    d.enterFormData('F/U Appointment',id='task_template')
    d.clickElement(value='Submit')
    d.verifyElementPresent(xpath='//div[contains(@class, "dynItem") and contains(.,"Hart, William S.")]')

    d.mouseOver(xpath='//div[contains(@class, "dynItem") and contains(.,"Hart, William S.")]')
    d.verifyElementPresent(xpath='//div[@class="dynItem" and contains(.,"Hart, William S.")]/span/a[contains(@class,"fa-user")]', present=True)

    # Looking for bad URL's breaking regrading
    d.navigate(WCURL.TASK_SEARCH +'&type=patient&search_submit=Submit&pat_id=22')
    d.verifyElementPresent(xpath='//div[contains(@class, "dynItem") and contains(.,"Doe, John L.")]')

    d.navigate(WCURL.TASK_SEARCH +'&type=document&search_submit=Submit')
    d.verifyElementPresent(xpath='//div[contains(@class, "dynItem") and contains(.,"Lab Results:")]//span[contains(@class, "datetime")]//span[contains(., "04-08-2010")]')

    d.navigate(WCURL.TASK_SEARCH +'&type=document&search_submit=Submit&doc_id=309')
    d.verifyElementPresent(xpath='//div[contains(@class, "dynItem") and contains(.,"Lab Results:")]//span[contains(@class, "datetime")]//span[contains(., "04-08-2010")]')
