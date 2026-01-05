"""
    @owners: sgrider
    @filedeps: src/getdoc.c
    Unit Tests for the saved template functionality used in Document Search,
    Custom Reports and other places
"""
from wcunittest import wcElement, wcDBRecord, wcJSCode

dbTemplate = """
<save save_type="multiselect" title="Document Type"
    save_text="Abd Aorta UltraSound Study" save_value="ABDAORTAUS" 
    save_inputsrc="sdoc_type_multi_select"></save>
<save save_type="multiselect" title="Document Type"
    save_text="Cardic Risk Assessment-Peds" save_value="CARDPEDS"
    save_inputsrc="sdoc_type_multi_select"></save>
<save save_type="multiselect" title="Storage Type" save_text="AVI Video"
    save_value="20" save_inputsrc="docstg_type_multi_select"></save>
<save save_type="multiselect" title="Storage Type" save_text="BMP"
    save_value="25" save_inputsrc="docstg_type_multi_select"></save>
<save save_type="multiselect" title="Storage Type" save_text="X12"
    save_value="26" save_inputsrc="docstg_type_multi_select"></save>
<save save_type="multiselect" title="Storage Type" save_text="XML"
    save_value="27" save_inputsrc="docstg_type_multi_select"></save>
<save save_type="multiselect" title="Location" save_text="Office"
    save_value="OFFICE" save_inputsrc="location_multi_select"></save>
<save save_type="date" title="Created Start Date" save_text="01-01-2001 12:00am"
    save_inputsrc="enterstartdate" value="2001-01-01 00:00:00"></save>
<save save_type="date" title="Created End Date" save_text="12-31-2001 11:59pm"
    save_inputsrc="enterenddate" value="2001-12-31 23:59:00"></save>
<save save_type="date" title="Revision Start Date"
    save_text="01-01-2002 12:00am" save_inputsrc="revisionstartdate"
    value="2002-01-01 00:00:00"></save>
<save save_type="date" title="Revision End Date"
    save_text="12-31-2002 11:59pm" save_inputsrc="revisionenddate"
    value="2002-12-31 23:59:00"></save>
<save save_type="date" title="Service Start Date" save_text="01-01-2003 12:00am"
    save_inputsrc="servicestartdate" value="2003-01-01 00:00:00"></save>
<save save_type="date" title="Service End Date" save_text="12-31-2003 11:59pm"
    save_inputsrc="serviceenddate" value="2003-12-31 23:59:00"></save>
<save save_type="value" title="Subject" save_text="Selenium Subject"
    save_inputsrc="subject" value="Selenium Subject"></save>
<save save_type="checkbox" title="Optional Columns" save_text="subject" 
    save_inputsrc="cols" value="subject"></save>
    """

def deleteAll(d):
    d.miedb.dbExec("DELETE FROM saved_templates WHERE template_name='Document Search'")

def visitPage(d):
    d.navigate('?f=chart&s=search&search_method=doc')

def insertTemplate(d, xml):
    d.miedb.dbExec("REPLACE INTO saved_templates (template_name, save_name, user_id, template_xml) VALUES "\
        "('Document Search', 'Selenium Template', (SELECT user_id FROM users WHERE username=%s), %s)",
        d.getUserData('selenium_username'), xml)

def saveTemplate(d, template_name):
    d.clickElement(text='Save Filter Template')
    d.enterFormData(template_name, id='save_name_text')
    d.clickElement(value='Save')

def fillOutData(d):
    d.enterFormData('test_subject', id='subject')
    d.clickElement(id='docstg_type_dropdownarrow')
# 124147 - Adding scrollIntoView() to bring multiselect options into view so they are clickable for now. Look into updating enterFormData() in MIEDriver.
    d.runJS('arguments[0].scrollIntoView({block: "center"})', d.getElement(xpath="//input[attribute::id='docstg_type' and attribute::value='15']"))
    d.enterFormData(True, xpath="//input[attribute::id='docstg_type' and attribute::value='15']", clear=False, blur=False)
    d.runJS('arguments[0].scrollIntoView({block: "center"})', d.getElement(xpath="//input[attribute::id='docstg_type' and attribute::value='22']"))
    d.enterFormData(True, xpath="//input[attribute::id='docstg_type' and attribute::value='22']", clear=False, blur=False)
    d.enterFormData('01', id='enterstartdateMONTH')
    d.enterFormData('03', id='enterstartdateDAY')
    d.enterFormData('1981', id='enterstartdateYEAR')
    d.enterFormData('5p', id='enterstartdateTIME')
    d.enterFormData(True, id='unprinted')

def main(d, WCURL):
    u = d.getWCUnitTest('Verify the No Templates Message', timeout=30)
    u.setup(deleteAll)
    u.setup(visitPage)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Saved Templates']"),
        wcElement('xpath', "//div[@class='wc_win']//td[text()='There are no [ Document Search ] templates defined for this system']"),
    ], reason='Look for the miewin and the message for No Templates')
    u.verifyElements([
        wcElement('text', 'Selenium Template', exists=False),
        wcElement('text', 'Delete', exists=False),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Personal Templates')]", exists=False),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Global Templates')]", exists=False),
    ], reason='Make sure we dont have these links because we havent inserted anything yet')
    u.test(lambda x: x.clickElement(text='Show Saved Filters'), reason='Click the Show Saved Filters link')

    u = d.getWCUnitTest('Verify the Save Window looks correct', timeout=30)
    u.setup(visitPage)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Save Template']"),
        wcElement('value', 'Check All'),
        wcElement('value', 'Un-Check All'),
        wcElement('value', 'Save'),
        wcElement('value', 'Cancel'),
        wcElement('id', 'save_name_text', maxlength=50, size=40),
        wcElement('id', 'template_add', type='checkbox', value=1),
    ], reason='These are the default expected items')
    u.test(lambda x: x.clickElement(text='Save Filter Template'), 'Click the Save Filter Template link')

    u = d.getWCUnitTest('Verify the Save Window Cancel button closes the miewindow', timeout=30)
    u.setup(visitPage)
    u.setup(lambda x: x.clickElement(text='Save Filter Template'))
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win' and text()='Save Template']", exists=False),
    ], reason='Ensure the window has closed')
    u.test(lambda x: x.clickElement(value='Cancel'))

    u = d.getWCUnitTest('Insert a DB template and ensure it shows up as a personal template', timeout=30)
    u.setup(insertTemplate, dbTemplate)
    u.setup(visitPage)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Saved Templates']"),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Personal Templates')]"),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Global Templates')]", exists=False),
        wcElement('text', 'Selenium Template'),
        wcElement('text', 'Delete'),
    ], reason='Ensure we get the links for the template we just inserted')
    u.test(lambda x: x.clickElement(text='Show Saved Filters'), reason='Click the Show Saved Filters link')

    u = d.getWCUnitTest('Apply the template and verify all inputs populated correctly', timeout=30)
    u.setup(visitPage)
    u.setup(lambda x: x.clickElement(text='Show Saved Filters'))
    u.setup(lambda x: x.clickElement(text='Selenium Template'))
    u.verifyElements([
        wcElement('xpath', "//input[@id='docstg_type' and @value='20']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='25']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='26']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='27']", checked=True),
    ], reason='Storage Types')
    u.verifyElements([
        wcElement('xpath', "//input[@id='slocation' and @value='OFFICE']", checked=True),
    ], reason='Location')
    u.verifyElements([
        wcElement('id', 'servicestartdateMONTH', value='01'),
        wcElement('id', 'servicestartdateDAY', value='01'),
        wcElement('id', 'servicestartdateYEAR', value='2003'),
        wcElement('id', 'servicestartdateTIME', value='00:00'),
        wcElement('id', 'serviceenddateMONTH', value='12'),
        wcElement('id', 'serviceenddateDAY', value='31'),
        wcElement('id', 'serviceenddateYEAR', value='2003'),
        wcElement('id', 'serviceenddateTIME', value='23:59'),
    ], reason='Service Dates')
    u.verifyElements([
        wcElement('id', 'enterstartdateMONTH', value='01'),
        wcElement('id', 'enterstartdateDAY', value='01'),
        wcElement('id', 'enterstartdateYEAR', value='2001'),
        wcElement('id', 'enterstartdateTIME', value='00:00'),
        wcElement('id', 'enterenddateMONTH', value='12'),
        wcElement('id', 'enterenddateDAY', value='31'),
        wcElement('id', 'enterenddateYEAR', value='2001'),
        wcElement('id', 'enterenddateTIME', value='23:59'),
    ], reason='Create Dates')
    u.verifyElements([
        wcElement('id', 'revisionstartdateMONTH', value='01'),
        wcElement('id', 'revisionstartdateDAY', value='01'),
        wcElement('id', 'revisionstartdateYEAR', value='2002'),
        wcElement('id', 'revisionstartdateTIME', value='00:00'),
        wcElement('id', 'revisionenddateMONTH', value='12'),
        wcElement('id', 'revisionenddateDAY', value='31'),
        wcElement('id', 'revisionenddateYEAR', value='2002'),
        wcElement('id', 'revisionenddateTIME', value='23:59'),
    ], reason='Revision Dates')
    u.verifyElements([
        wcElement('id', 'subject', value='Selenium Subject'),
    ], reason='Subject')
    u.verifyElements([
        wcElement('xpath', "//input[@id='cols' and @value='subject']", checked=True),
    ], reason='Optional Columns')
    u.test(lambda x: x.clickElement(value='Apply'), reason='Click the apply button')

    u = d.getWCUnitTest('Change the user on the template to verify that it becomes a global template', timeout=30)
    u.setup(lambda x: x.miedb.dbExec("UPDATE saved_templates SET user_id=1 WHERE template_name='Document Search' AND save_name='Selenium Template'"), reason='Alter the user_id to 1')
    u.setup(visitPage)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Saved Templates']"),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Personal Templates')]", exists=False),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Global Templates')]"),
        wcElement('text', 'Selenium Template'),
        wcElement('text', 'Delete'),
    ], reason='Personal should no longer exist and global should')
    u.test(lambda x: x.clickElement(text='Show Saved Filters'), reason='Click the Show Saved Filters link')

    u = d.getWCUnitTest('Apply the template again as the global and verify all inputs populated correctly', timeout=30)
    u.setup(visitPage)
    u.setup(lambda x: x.clickElement(text='Show Saved Filters'))
    u.setup(lambda x: x.clickElement(text='Selenium Template'))
    u.teardown(deleteAll)
    u.verifyElements([
        wcElement('xpath', "//input[@id='sdoc_type' and @value='ABDAORTAUS']", checked=True),
        wcElement('xpath', "//input[@id='sdoc_type' and @value='CARDPEDS']", checked=True),
    ], reason='Document Types')
    u.verifyElements([
        wcElement('xpath', "//input[@id='docstg_type' and @value='20']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='25']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='26']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='27']", checked=True),
    ], reason='Storage Types')
    u.verifyElements([
        wcElement('xpath', "//input[@id='slocation' and @value='OFFICE']", checked=True),
    ], reason='Location')
    u.verifyElements([
        wcElement('id', 'servicestartdateMONTH', value='01'),
        wcElement('id', 'servicestartdateDAY', value='01'),
        wcElement('id', 'servicestartdateYEAR', value='2003'),
        wcElement('id', 'servicestartdateTIME', value='00:00'),
        wcElement('id', 'serviceenddateMONTH', value='12'),
        wcElement('id', 'serviceenddateDAY', value='31'),
        wcElement('id', 'serviceenddateYEAR', value='2003'),
        wcElement('id', 'serviceenddateTIME', value='23:59'),
    ], reason='Service Dates')
    u.verifyElements([
        wcElement('id', 'enterstartdateMONTH', value='01'),
        wcElement('id', 'enterstartdateDAY', value='01'),
        wcElement('id', 'enterstartdateYEAR', value='2001'),
        wcElement('id', 'enterstartdateTIME', value='00:00'),
        wcElement('id', 'enterenddateMONTH', value='12'),
        wcElement('id', 'enterenddateDAY', value='31'),
        wcElement('id', 'enterenddateYEAR', value='2001'),
        wcElement('id', 'enterenddateTIME', value='23:59'),
    ], reason='Create Dates')
    u.verifyElements([
        wcElement('id', 'revisionstartdateMONTH', value='01'),
        wcElement('id', 'revisionstartdateDAY', value='01'),
        wcElement('id', 'revisionstartdateYEAR', value='2002'),
        wcElement('id', 'revisionstartdateTIME', value='00:00'),
        wcElement('id', 'revisionenddateMONTH', value='12'),
        wcElement('id', 'revisionenddateDAY', value='31'),
        wcElement('id', 'revisionenddateYEAR', value='2002'),
        wcElement('id', 'revisionenddateTIME', value='23:59'),
    ], reason='Revision Dates')
    u.verifyElements([
        wcElement('id', 'subject', value='Selenium Subject'),
    ], reason='Subject')
    u.verifyElements([
        wcElement('xpath', "//input[@id='cols' and @value='subject']", checked=True),
    ], reason='Optional Columns')
    u.test(lambda x: x.clickElement(value='Apply'), reason='Click the apply button')

    u = d.getWCUnitTest('Now lets fill out some data and ensure we can save it as a template', timeout=30)
    u.setup(visitPage)
    u.setup(fillOutData)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Save Template']", exists=False),
    ], reason='Look for the miewindow to close after ajaxsaving')
    u.test(saveTemplate, 'Selenium Manual')

    u = d.getWCUnitTest('Now make sure our new saved template shows up as a Personal Template', timeout=30)
    u.setup(visitPage)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Saved Templates']"),
        wcElement('xpath', "//div[@class='wc_win']//td[contains(text(), 'Personal Templates')]"),
        wcElement('text', 'Selenium Manual'),
    ])
    u.test(lambda x: x.clickElement(text='Show Saved Filters'), reason='Click the Show Saved Filters link')

    u = d.getWCUnitTest('Apply Selenium Manual and verify all the inputs populated correctly', timeout=30)
    u.setup(visitPage)
    u.setup(lambda x: x.clickElement(text='Show Saved Filters'))
    u.setup(lambda x: x.clickElement(text='Selenium Manual'))
    u.verifyElements([
        wcElement('xpath', "//input[@id='docstg_type' and @value='22']", checked=True),
        wcElement('xpath', "//input[@id='docstg_type' and @value='15']", checked=True),
    ], reason='Storage Types')
    u.verifyElements([
        wcElement('id', 'enterstartdateMONTH', value='01'),
        wcElement('id', 'enterstartdateDAY', value='03'),
        wcElement('id', 'enterstartdateYEAR', value='1981'),
        wcElement('id', 'enterstartdateTIME', value='17:00'),
    ], reason='Create Dates')
    u.verifyElements([
        wcElement('id', 'unprinted', checked=True),
    ], reason='View Unprinted Only')
    u.verifyElements([
        wcElement('id', 'subject', value='test_subject'),
    ], reason='Subject')
    u.test(lambda x: x.clickElement(value='Apply'), reason='Click the apply button')

    u = d.getWCUnitTest('Verify that we can delete our personal template', timeout=30)
    u.setup(visitPage)
    u.setup(lambda x: x.clickElement(text='Show Saved Filters'), reason='Click Show Saved Filters link')
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win_title' and text()='Confirm Delete Template']"),
        wcElement('value', 'Delete', type='button'),
        wcElement('value', 'Cancel', type='button'),
    ], reason='Verify that we got a confirmation window with the buttons')
    u.test(lambda x: x.clickElement(text='Delete'))

    u = d.getWCUnitTest('Verify that deleting our template does in fact delete it', timeout=30)
    u.setup(visitPage)
    u.setup(lambda x: x.clickElement(text='Show Saved Filters'), reason='Click Show Saved Filters link')
    u.setup(lambda x: x.clickElement(text='Delete'), reason='Click the delete link')
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc_win']//td[text()='There are no [ Document Search ] templates defined for this system']"),
    ], reason='We should be back to no templates in this system now')
    u.test(lambda x: x.clickElement(value='Delete'), reason='Click the delete button')
