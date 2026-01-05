"""
@owners: pepperson
"""
from wcunittest import wcElement, wcDBRecord

def main (d, WCURL):
    """
    Verifies that the Document Add/Edit screen is working properly.
    """

    u = d.getWCUnitTest('Verify the Hide Operation of the Doc Types List')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.verifyElements([
        wcElement('xpath', '//table[@class="dlg_root" and contains(., "All Types")]//tr[@name="show_hide_doc_type_tr" and contains(@style, "display: none")]//div[contains(.,"Displaying")]')
    ], reason='Should be hidden to begin with')
    u.test()

    u = d.getWCUnitTest('Verify the Show Operation of the Doc Types List')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.verifyElements([
        wcElement('xpath', '//table[@class="dlg_root" and contains(., "All Types")]//tr[@name="show_hide_doc_type_tr" and not (contains(@style, "display: none"))]//div[contains(.,"Displaying")]')
    ], reason='Should be displaying after clicking Show')
    u.test()

    u = d.getWCUnitTest('Verify the Show Operation of the Doc Types List')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.setup(lambda d: d.clickElement(id='hide_doc_types'), reason='Click the Hide link')
    u.verifyElements([
        wcElement('xpath', '//table[@class="dlg_root" and contains(., "All Types")]//tr[@name="show_hide_doc_type_tr" and contains(@style, "display: none")]//div[contains(.,"Displaying")]')
    ], reason='Should be hidden again')
    u.test()

    u = d.getWCUnitTest('Verify the Document Add Form')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.verifyElements([
        wcElement('xpath', "//td/select[@name='selected_origin_id']"),
        wcElement('xpath', "//td/select[@id='doc_type']"),
        wcElement('xpath', "//td//input[@id='service_dateDAY']"),
        wcElement('xpath', "//td/select[@id='service_location']"),
        wcElement('xpath', "//td//input[@id='subject']"),
        wcElement('xpath', "//td/span[@id='encounter_ac_span']"),
        wcElement('xpath', "//td/span[@id='LinkOrders_span']"),
        wcElement('xpath', "//td/span[@id='doc_inc_id_ac_span']"),
        wcElement('xpath', "//td/span[contains(.,'Add')]"),
        wcElement('xpath', "//td//textarea[@id='file']")
    ], reason='')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')

    # Authored By possibilities
    u = d.getWCUnitTest('Remove Author Documents')
    u.setup(lambda d: d.wcutils.SetPermission('E-Chart','Author Documents',0))
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.verifyElements([
        wcElement('xpath', "//td/select[@name='selected_origin_id']", exists=False),
    ], reason='')
    u.teardown(lambda d: d.wcutils.SetPermission('E-Chart','Author Documents',0), reason='DB cleanup')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')

    u = d.getWCUnitTest('Remove Document Transcription')
    u.setup(lambda d: d.wcutils.SetPermission('E-Chart','Document Transcription',0))
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.verifyElements([
        wcElement('xpath', "//td/select[@name='selected_origin_id']", exists=False),
    ], reason='')
    u.teardown(lambda d: d.wcutils.SetPermission('E-Chart','Document Transcription',1), reason='DB cleanup')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')
    
    # Document Type - Chart Type filters
    u = d.getWCUnitTest('Default Patient Chart Type')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.setup(lambda d: d.miedb.dbExec("UPDATE document_types SET text_add=1 WHERE description in ('Asset Calibration Request','Email Consent','EOB Document')"),reason='Ensure document types pass the input filter')
    u.verifyElements([
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Asset Calibration Request']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Email Consent']"),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Alert Comment']"),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'EOB Document']", exists=False),
    ], reason='')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')

    u = d.getWCUnitTest('No Chart Types')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.setup(lambda d: d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=18"), reason='Create Baseline')
    u.verifyElements([
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Asset Calibration Request']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Email Consent']"),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Alert Comment']"),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'EOB Document']", exists=False),
    ], reason='')
    u.teardown(lambda d: d.miedb.dbExec("INSERT INTO pat_chart_types SET pat_id=18,chart_type_id=0"), reason='DB Cleanup')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')
    
    u = d.getWCUnitTest('Single Chart Type')
    u.setup(lambda d: d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=18"), reason='Create Baseline')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO pat_chart_types SET pat_id=18,chart_type_id=2"), reason='Add EOB Doc Type')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.verifyElements([
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Asset Calibration Request']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Email Consent']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Alert Comment']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'EOB Document']",exists=False), # reason='Only a single Doc Type option, there is no need for a dropdown.'
        wcElement('xpath', "//td[contains(text(),'EOB Document')]"), # reason='Pick up the text display of the available Document Type')
    ], reason='')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=18"), reason='DB Cleanup')
    u.teardown(lambda d: d.miedb.dbExec("INSERT INTO pat_chart_types SET pat_id=18,chart_type_id=0"), reason='DB Cleanup')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')
    
    u = d.getWCUnitTest('Multiple Chart Types')
    u.setup(lambda d: d.navigate(WCURL.DOCUMENT_HART_WILLIAM + '&opp=add'))
    u.setup(lambda d: d.clickElement(id='show_doc_types'), reason='Click the Show link')
    u.setup(lambda d: d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=18"), reason='Create Baseline')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO pat_chart_types SET pat_id=18,chart_type_id=2"), reason='Add EOB Doc Type')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO pat_chart_types SET pat_id=18,chart_type_id=3"), reason='Add Alert Doc Type')
    u.verifyElements([
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Asset Calibration Request']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Email Consent']", exists=False),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'Alert Comment']"),
        wcElement('xpath', "//td/select[@id='doc_type']/option[. = 'EOB Document']"),
    ], reason='')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=18"), reason='Create Baseline')
    u.teardown(lambda d: d.miedb.dbExec("INSERT INTO pat_chart_types SET pat_id=18,chart_type_id=0"), reason='DB Cleanup')
    u.teardown(lambda d: d.miedb.dbExec("UPDATE document_types SET text_add=0 WHERE description in ('sset Calibration Request','Email Consent','EOB Document')"),reason='DB cleanup')
    u.test(lambda d: d.clickElement(xpath="//td//tbody//a[contains(.,'Text')]"), reason='View Document Add screen')

    u = d.getWCUnitTest('PDF Editing')
    u.setup(lambda d: d.navigate('?f=chart&s=doc&doc_id=298'))
    u.setup(lambda d: d.clickElement(xpath="//div[@class='doc_opp_links']//li/a[contains(.,'Edit')]"))
    u.setup(lambda d: d.switchToPopup())
    u.verifyElements([
        wcElement('xpath', "//table[@class='dlg_root']/tbody//td/input[@type='button' and @value='Click To Edit File']", exists=False)
    ], reason='Button should not exist in non-IE browsers')
    u.test()

    u = d.getWCUnitTest('Sketch Adding')
    u.setup(lambda d: d.navigate('?t=Documents&v=list&f=chart&s=doc&opp=add&pat_id=40&method=sketch&doc_type=SKETCHBODY'))
    u.verifyElements([
        wcElement('xpath', "//div[@class='lc-drawing with-gui']", exists=True)
    ], reason='Make sure literally canvas loaded')
    u.test()
