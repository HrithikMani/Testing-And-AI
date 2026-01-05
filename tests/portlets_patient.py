def main (d, WCURL):
    """
    Verifies patient portlets. Makes sure that the default portlets are
    visible and checks to make sure all of the expeteced portlets are
    available when clicking the 'Select Modules' link.
    If you add or remove portlets or change the default visibility of 
    patient portlets, this test will know about it.
    """
    d.navigate(WCURL.CHART_HART_WILLIAM)

    d.startSection('Verify the default portlets are showing on the Summary page')
    labels = ["Demographics", "Contacts", "Appointments", "Titer Results", "TB Skin Test", "TB Screening Questionnaires",
              "Due List", "Work Status", "Labs", "Fit Test Results", "Documents", "Quick Links",
              "Allergies", "Medications", "Medical History", "Vitals"]
    for i, v in enumerate(labels, 1):
        d.verifyAttribute("text",v,xpath="(//div[@class='portlet'])[%d]/div[@class='portlet-header']/label" %i)
    d.verifyElementPresent(False,xpath="(//div[@class='portlet'])[%d]/div[@class='portlet-header']/label" %(i + 1))
    d.endSection()

    d.startSection('Click the \'Select Portlets\' link and verify that all of the expected portlets are there')
    d.clickElement(xpath="//div[@class='links_right']/a[@title='Select Portlets']")
    win = d.getElement(xpath="//div[@class='wc_win_title' and text()='Available Portlets']")
    if win:
        values = ["Allergies", "Appointments", "Cardio", "Contacts", "Contacts - View Only", "CT Scans", "Deal Quick Links", "Demographics", "Documents", "Due List",
                  "Encounter Quick Links", "Family Medical History", "FHIR Launch", "Fit Test Results", "Flu Program Panel", "Gynecology History", "Health Surveillance Quick Links",
                  "Injections", "Insurance", "Labs", "Manual Merge", "Medical Contacts", "Medical History", "Medical Summary", "Medications", "MRI Scans",
                  "OB Alerts", "Open Encounters", "Order Quick Links", "Other Tests", "Panel Membership", "Past Medical History", "Pathology",
                  "Patient Chart File Export", "Patient Portal", "PDMP", "PET Scans", "PINNACLE", "Portal", "Preferred Pharmacy", "Pregnancy History",
                  "Preventive Care", "Problem List", "Procedures", "Quality Reporting", "Quick Links", "Radiology", "Referral", "Services", "Social History",
                  "TB Screening Questionnaires", "TB Skin Test", "Titer Results", "Today's Due List", "Topaz Forms", "Ultrasounds",
                  "Unreconciled Summaries", "Vitals", "Warnings & Alerts", "Work Status"]
        for i, v in enumerate(values, 1):
            d.verifyAttribute("value",v,xpath="(//input[@name='layout_name'])[%d]" %i)
        d.verifyElementPresent(False,xpath="(//input[@name='layout_name'])[%d]" %(i + 1))

        d.clickElement(xpath="//div[@class='wc_win_title' and text()='Available Portlets']/parent::div//button[@class='xclose']")
    else:
        d.reportCommandStatus("Available Portlets window could not be found", "", False, "", "")
        return
    d.endSection()

    d.startSection('Add and Remove Portlet')
    d.startSection('Turn on manual merge portlet and make sure it appears on the page')
    d.clickElement(xpath="//div[@class='links_right']/a[@title='Select Portlets']")
    win = d.getElement(xpath="//div[@class='wc_win_title' and text()='Available Portlets']")
    if win:
        d.enterFormData(True,xpath="//input[@name='layout_name' and @value='Manual Merge']")
        d.clickElement(value="Save")
    else:
        d.reportCommandStatus("Available Portlets window could not be found", "", False, "", "")
        return
    d.waitFor(d, lambda d: d.getElement(xpath="//div[@class='portlet-header']/label[text()='Manual Merge']"), expected_return=True, timeout=30)
    d.endSection()

    d.startSection('Turn off manual merge and make sure it goes away again')
    d.clickElement(xpath="//div[@class='links_right']/a[@title='Select Portlets']")
    win = d.getElement(xpath="//div[@class='wc_win_title' and text()='Available Portlets']")
    if win:
        d.enterFormData(False,xpath="//input[@name='layout_name' and @value='Manual Merge']")
        d.clickElement(value="Save")
    else:
        d.reportCommandStatus("Available Portlets window could not be found", "", False, "", "")
        return

    d.waitFor(d, lambda d: d.getElement(xpath="//div[@class='portlet-header']/label[text()='Manual Merge']"), expected_return=False, timeout=30)
    d.endSection()
    d.endSection()

    d.startSection('Verify "Save As Default For" allows Security Role A to update the portlets in Security Role B')

    d.startSection('Login as "Dave" (SuperUser)')
    d.wcutils.insertWCTSession('dave')
    d.endSection()

    d.startSection('Update default portlets for SystemOwner and apply to users')
    d.navigate(WCURL.CHART_HART_WILLIAM)
    d.clickElement(xpath="//div[@class='links_right']/a[@title='Select Portlets']")
    d.clickElement(xpath="//select[@id='saveAsDefaultFor']")
    d.clickElement(xpath="//option[@value='1']")
    d.clickElement(xpath="//input[@name='apply_to_users']")
    d.clickElement(xpath="//input[@value='PDMP']")
    d.clickElement(value="Save")
    d.clickElement(value="Yes")
    d.wcutils.waitForAJAX(timeout=60, quiet=5)
    d.endSection()

    d.startSection('Login as "Selenium" (SystemOwner)')
    d.wcutils.insertWCTSession('selenium')
    d.endSection()

    d.startSection('Verify the portlets "Dave" (SuperUser) selected are present in "Selenium" (SystemOwner)')
    d.navigate(WCURL.CHART_HART_WILLIAM)
    d.verifyElementPresent(True,xpath='//div[@class="portlet-header"]//label[text()="PDMP"]')
    d.endSection()

    d.endSection()
