# 
# Webchart Patient Demo Test
# Makes sure the try it link goes to demographics and tries out some of the sample patient stuff
#
def main (d, WCURL):
    d.navigate(WCURL.OMNISCOPE)
    d.clickElement(id="tryitlink")

    # These are the default Patient Portlets that are displayed at the time I wrote this test
    d.verifyElementPresent(xpath="//label[text()='Demographics']")
    d.verifyElementPresent(xpath="//label[text()='Patient Portal']")
    d.verifyElementPresent(xpath="//label[text()='Vitals']")
    d.verifyElementPresent(xpath="//label[text()='Medical Contacts']")
    d.verifyElementPresent(xpath="//label[text()='Insurance']")
    d.verifyElementPresent(xpath="//label[text()='PINNACLE']")
    d.verifyElementPresent(xpath="//label[text()='Patient Chart File Export']")
    d.verifyElementPresent(xpath="//label[text()='Warnings & Alerts']")
    d.verifyElementPresent(xpath="//label[text()='Labs']")
    d.verifyElementPresent(xpath="//label[text()='Documents']")
    d.verifyElementPresent(xpath="//label[text()='Xray/Radiology']")
    d.verifyElementPresent(xpath="//label[text()='Ultrasounds']")
    d.verifyElementPresent(xpath="//label[text()='Cardio']")
    d.verifyElementPresent(xpath="//label[text()='Quick Links']")
    d.verifyElementPresent(xpath="//label[text()='Allergies']")
    d.verifyElementPresent(xpath="//label[text()='Medications']")
    d.verifyElementPresent(xpath="//label[text()='Medical History']")
    d.verifyElementPresent(xpath="//label[text()='Family Medical History']")
    d.verifyElementPresent(xpath="//label[text()='Immunizations']")
    d.verifyElementPresent(xpath="//label[text()='Surgeries/Procedures']")
    d.verifyElementPresent(xpath="//label[text()='Social History']")
    d.verifyElementPresent(xpath="//label[text()='Preventive Care']")

    # test delete MRNs
    mrn = "943"
    d.clickElement(xpath="//label[text()='Demographics']/following-sibling::div/div/a[@title='Manage Information']")
    # add CCHIT MRN
    d.enterFormData(mrn,name="patient_mrnumber_CCHIT")
    # click submit clickElement
    d.clickElement(name="savepatient")
    # find edit again
    d.clickElement(xpath="//font[text()='Edit Demo']/parent::a")
    # delete CCHIT MRN 
    d.clickElement(id="CCHIT%s_delete" %mrn)
    d.closeAlert()
    # click submit clickElement
    d.clickElement(name="savepatient")

    # Test temp patient merging
    # Go to temp patient chart
    d.navigate(WCURL.ECHART + WCURL.PATIENT + WCURL.CHART_TEMP_HART_WILLIAM + 'v=demo');
    # Search for patient to merge to
    d.enterFormData(True,name="from_pats_id")
    d.clickElement(name="preview")
    # Merge temp to normal chart
    d.clickElement(xpath="//input[@name='merge_opts_26' and @value='2']")
    d.clickElement(name="submit_merge")
    # Verify 'Cannot Merge' message
    x = "//div[@id='wc_main']/h4/center[text()='Cannot Merge to a Temporary Patient Record!']"
    d.verifyElementPresent(xpath=x)
