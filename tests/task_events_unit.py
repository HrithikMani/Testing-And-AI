"""
    Unit Test for task events
    @owners: dcornewell
    @filedeps: src/tasklistevent.c, jsbin/tle_editor.js, include/tasklistdb.h, src/tasklistdb.c
"""

def main (d, WCURL):
    """
    Tests task events    
    """
    d.startSection('Perform URL Event - send email on document add')
    d.navigate("?f=tlist&s=tl_events&opp=add")

    d.enterFormData('?f=ajaxpost&s=patemail&layout_name=Pat+Portal+Message+Notification',id='evt_perform_url')
    d.enterFormData('1',id='evt_priority')
    d.enterFormData('On Document Add',id='evt_type')
    d.enterFormData('d.doc_type=\'WCCHECKOUT\' AND d.storage_type=1',id='evt_where')

    d.clickElement(value='Save And Close')

    d.verifyElementPresent(True,xpath="//div[contains(@class,'folder') and contains(., 'Task List Event Added')]")

    d.navigate("?f=chart&s=doc&opp=add&pat_id=18&method=text&doc_type=WCCHECKOUT")
    d.enterFormData('testing a document triggering an email',id='file')
    d.clickElement(value='Add Document')
    d.verifyElementPresent(True,xpath="//span[contains(., 'has been uploaded successfully')]")

    # Check for the email document
    d.navigate("?f=chart&s=pat&t=Documents&v=list&pat_id=18&lv_lv_wc_order=%60Doc+ID%60&lv_lv_wc_dir=DESC&lv_lv_wc_dir2=ASC&lv_lv_wc_dir3=ASC")
    d.verifyElementPresent(True,xpath="//td[contains(., 'Reminder to Review Notifications')]")
    d.endSection()

    d.startSection('Add Task on document add')
    d.navigate("?f=tlist&s=tl_events&opp=add")

    d.enterFormData('Phone Note',id='evt_name')
    d.enterFormData('1',id='evt_priority')
    d.enterFormData('On Document Add',id='evt_type')
    d.enterFormData('d.doc_type=\'WCCHECKOUT\' AND d.storage_type=1',id='evt_where')

    d.clickElement(value='Save And Close')

    d.verifyElementPresent(True,xpath="//div[contains(., 'Task List Event Added')]")

    d.navigate("?f=chart&s=doc&opp=add&pat_id=18&method=text&doc_type=WCCHECKOUT")
    d.enterFormData('testing a document add to make a task',id='file')
    d.clickElement(value='Add Document')
    # Document added and has a task
    d.verifyElementPresent(True,xpath="//span[contains(., 'has been uploaded successfully')]")
    d.verifyElementPresent(True,xpath="//div[contains(., 'Tasks')]")
    d.endSection()

    d.startSection('Add Task on document add regarding patient')
    # Change type on fast task to patient
    d.navigate("?f=tlist&s=template&tabmodule=tasklist&tabselect=Fast+Tasks")
    d.clickElement(xpath="//td[contains(@class,'fast_20tasks_Name_cell') and contains(., 'Phone Note')]/following-sibling::td[contains(@class, 'fast_20tasks_Options_cell')]/a[contains(., 'Edit')]")
    d.enterFormData('Patient',id='type')
    d.clickElement(value='Save')

    d.navigate("?f=chart&s=doc&opp=add&pat_id=18&method=text&doc_type=WCCHECKOUT")
    d.enterFormData('testing a document add to make a task',id='file')
    d.clickElement(value='Add Document')
    # Document added and has a task
    d.verifyElementPresent(True,xpath="//span[contains(., 'has been uploaded successfully')]")
    d.verifyElementPresent(False,xpath="//div[contains(@class, 'document_tasks') and contains(., 'Hide/Show Tasks')]")
    # Check for the Task document. It will have a subject of Phone Note
    d.navigate("?f=chart&s=pat&t=Documents&v=list&pat_id=18&lv_lv_wc_order=%60Doc+ID%60&lv_lv_wc_dir=DESC&lv_lv_wc_dir2=ASC&lv_lv_wc_dir3=ASC")
    d.verifyElementPresent(True,xpath="//td[contains(@class, 'lv__wc_Subject_cell') and contains(., 'Phone Note')]")
    d.endSection()

    # d.startSection('Add Task on observation add regarding document')
    # d.navigate("?f=tlist&s=tl_events&opp=add")

    # d.enterFormData('Test Results for Review',id='evt_name')
    # d.enterFormData('1',id='evt_priority')
    # d.enterFormData('On Observation Add',id='evt_type')
    # d.enterFormData('WHERE 1',id='evt_where')

    # d.clickElement(value='Save And Close')

    # d.verifyElementPresent(True,xpath="//div[contains(., 'Task List Event Added')]")

    # d.clickElement(xpath='//a[@id="wc_homeicon" and @title="Home"]')
    # d.waitFor(d, lambda d: d.getElement(xpath='//ul//a[contains(., "Better Corp.")]'), expected_return=True)

    # d.miedb.execute("INSERT INTO documents SET pat_id=55, doc_type='PCONSENT', storage_type=1")
    # d.miedb.execute("INSERT INTO document_sign (status, doc_id) SELECT 1, doc_id FROM documents WHERE pat_id=55 AND doc_type='PCONSENT' AND storage_type=1")

    # d.clickElement(xpath='//ul//a[contains(., "Better Corp.")]')
    # d.navigate("?f=layout&pat_id=55&cobrand_patid=43&module=Patient+Portal&module=Patient+Portal&name=Create+Order&order_name=Travel%20Questionnaire&fromPage=Home")
    # d.enterFormData('Canada',id='obs_result_58_3')
    # d.clickElement(xpath="//span[contains(., 'NEXT')]")
    # d.wcutils.waitForToggle(lambda d: d.getElement(xpath="//*[contains(@class, 'portal_mask')]"), expected=False, timeout=10)
    # d.clickElement(xpath="//span[contains(., 'SUBMIT')]")

    # d.wcutils.waitForToggle(lambda d: d.getElement(xpath="//*[contains(@class, 'portal_mask')]"), expected=False, timeout=10)
    # d.clickElement(xpath="//span[@title='Menu']")
    # d.clickElement(xpath="//a[contains(., 'Return to') and contains(., 'Enterprise Health')]")

    # # find the document with tasks
    # d.navigate("?f=chart&s=pat&t=Admin+%28EO%2FPO%29%3AEncounters+%28EO%2FPO%29&v=encounter&pat_id=55")
    # d.wcutils.waitForAJAX(30)
    # d.waitFor(d, lambda d: d.runJS("return MIE.WC_DataVis.grids['Encounters'].isIdle()"), expected_return=True, timeout=30)

    # d.runJS('jQuery("a:contains(Properties)")[0].scrollIntoView()')

    # d.clickElement(xpath="//a[contains(., 'Properties')]")
    # d.clickElement(xpath="//a[contains(., 'Questionnaire-Travel')]")
    # if d.switchToPopup():
    #     d.verifyElementPresent(True,xpath="//div[contains(@class, 'document_tasks') and contains(., 'Hide/Show Tasks')]")
    #     d.closePopup()
    # d.endSection()

    d.startSection('Add Task on patient update')
    d.navigate("?f=tlist&s=tl_events&opp=add")

    d.enterFormData('Fax Records',id='evt_name')
    d.enterFormData('1',id='evt_priority')
    d.enterFormData('On Patient Edit',id='evt_type')
    d.enterFormData('1',id='evt_where')
    d.clickElement(value='Save And Close')

    d.verifyElementPresent(True,xpath="//div[contains(., 'Task List Event Added')]")

    d.navigate("?f=chart&s=pat&t=Edit+Demographics&v=dashboard&pat_id=18")
    d.enterFormData('Sr',id='DPI_suffix')
    d.clickElement(value='Save')
    d.navigate("?f=chart&s=pat&t=Documents&v=list&pat_id=18&lv_lv_wc_order=%60Doc+ID%60&lv_lv_wc_dir=DESC&lv_lv_wc_dir2=ASC&lv_lv_wc_dir3=ASC")
    d.verifyElementPresent(True,xpath="//td[contains(@class, 'lv__wc_Subject_cell') and contains(., 'Fax Records')]")

    d.endSection()
