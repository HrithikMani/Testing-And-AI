"""
    Conditions Unit Test
    Ensures that all available conditions related areas are rendered as expected
    @owners:
"""

from wcunittest import wcElement

def addEncounter(d, data):
    d.navigate('?f=chart&s=pat&t=Patient+Summary&v=dashboard&pat_id=18')
    d.clickElement(text='Add Visit')

def goToSection(d, data):
    d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_encnav"]//a[text()="Plan"]'), expected_return=True, timeout=120)
    d.mouseOver(xpath='//div[@id="wc_encnav"]//a[text()="Plan"]')
    d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_encnav"]//a[text()="Plan"]/following-sibling::ul//li[contains(., "Clinical education")]'), expected_return=True, timeout=120)
    d.clickElement(xpath='//div[@id="wc_encnav"]//a[text()="Plan"]/following-sibling::ul//li[contains(., "Clinical education")]')


def openClinicalEducation(d, data):
    d.startSection('Wait for Masking')
    if d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'masked')]"), expected_return=True, timeout=1):
        d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'masked')]"), expected_return=False, timeout=60)
    else:
        if d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'masked')]"), expected_return=True, timeout=1):
            d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'masked')]"), expected_return=False, timeout=60)
        else:
            d.reportCommandStatus('Waited for', 'Unmask', True, '', 'Mask not present')
    d.endSection()
    d.startSection('Verify section is present')
    if d.waitFor(d, lambda d: d.getElement(xpath='//h3[@class="exam_tab" and contains(., "Clinical education")]'), expected_return=True, timeout=60):
        d.reportCommandStatus('Waited for', 'Section Opened', True, '', 'section is present')
    else:
        d.reportCommandStatus('Waited for', 'Section Opened', False, '', 'section not found')
    d.endSection()
    d.clickElement(xpath='//h3[@class="exam_tab" and contains(., "Clinical education")]')
    d.startSection('Wait for section to open')
    if d.waitFor(d, lambda d: d.getElement(xpath="//h3[text()='Clinical education']/parent::div[contains(@class, 'edit_mode')]"), expected_return=True, timeout=60):
        d.reportCommandStatus('Waited for', 'Section Open', True, '', 'section opened')
    else:
        d.reportCommandStatus('openClinicalEducation', '', False, '', 'section failed to open')
    d.endSection()

def setHWUrl(d, data):
    d.miedb.dbExec("REPLACE INTO system_settings SET module='Webchart', section='Google', item='Search URL', value='https://clinicianIx.healthwise.net/miewebchart/Launch?hw.key=AECHY7SHQJ47ZLMIYLUEMADCM77TGNXIRPQFFY6SXTVTWWHQ72QQCH3QTIZPCCDHTHQFDX5ADWFFTC'")

def main(d, WCURL):
    u = d.getWCUnitTest('Validate ICD-10 Healthwise Links')
    u.setup(setHWUrl)
    u.setup(addEncounter)
    u.setup(goToSection)
    u.setup(openClinicalEducation)
    u.verifyElements([
        wcElement('xpath', '//a[contains(@href,"https://clinicianIx.healthwise.net/miewebchart/Launch")]')], reason='Look for first Healthwise Link')
    u.test()


