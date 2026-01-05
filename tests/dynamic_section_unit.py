"""
@owners: sgrider gjones
    Unit Test for verifying basic functionality of dynamic sections.
    This unit test operates on a unique visit type which only has a single section
    present: Encounter info
    This is to help debugging various dynamic section failures inside of more 
    complex workflows without all the extra complexity of other sections, user interaction
    and untracked API calls.
"""

from wcunittest import wcElement

VISIT = 'DYNUNIT'
SECTION = 'Encounter'
LAYOUT = """
<WCFORM>
<WCSCRIPTVARS>
<INPUT TYPE="hidden" NAME="encplaceholder"><!-- We use this to sign and close encounter -->
<INPUT TYPE="hidden" NAME="relencplaceholder"><!-- We use this to release the encounter -->
<WCSCRIPT SRC="incident.js">
<WCSCRIPT SRC="tepr_ros.js">
<WCSCRIPT SRC="wcspell.js">
<WCSCRIPT SRC="observe.js">
<WCSCRIPT SRC="rxsig.js">
<WCSCRIPT SRC="wcgraph.js">
<WCINCLUDE MODULE="EXAM" NAME="IncludedCSSScript">
<WCFORMVARS>
<WCENCITEM TYPE="exam">
    <WCENCITEM NAME="Encounter Info" TITLE="{0}" BEFORE_POST_CB="CheckRequiredFields" AFTER_POST_CB="updateHeaders" />
</WCENCITEM>
<WCINCLUDE MODULE="WCENCSECTION" NAME="BottomLinks">
<WCINCLUDE MODULE="WCENCSECTION" NAME="Buttons">
</WCFORM>
""".format(SECTION)

def addEncounter(d, pat_id):
    d.navigate('?f=chart&s=pat&pat_id={0}&v=encounter&encopp=quick_add&visit_type={1}'.format(
        pat_id, VISIT))


def clickSectionAndWait(d, section):
    clickSection(d, section)
    ele = d.getElement(xpath="//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='{0}']/parent::div".format(section))
    d.reportCommandStatus('wait for toggling to start', section,
        d.waitFor(ele, lambda ele: 'wc-enc-dynamic-section-flipping' in ele.get_attribute('class').split(),
            timeout=30),
        '', '')
    d.reportCommandStatus('wait for toggling to stop', section,
        d.waitFor(ele, lambda ele: 'wc-enc-dynamic-section-flipping' not in ele.get_attribute('class').split(),
            timeout=30),
        '', '')

def clickSection(d, section):
    d.reportCommandStatus('Wait for Mask', section, d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'masked')]"), expected_return=False, timeout=30), '', '')
    d.clickElement(xpath="//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='{0}']".format(section))

def clickNextButton(d, section):
    d.clickElement(xpath="//*[self::h2 or self::h3][contains(@class, 'exam_tab')]/parent::div[contains(@class, 'edit_mode')]//button[contains(@class, 'next') and @type='button']")
    d.reportCommandStatus('Wait for section to close', section, d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]"), expected_return=False, timeout=30), '', '')

def clickNextIcon(d, section):
    d.clickElement(xpath="//div[@class='heading_buttons']/a[@class='next']")
    d.reportCommandStatus('Wait for section to close', section, d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]"), expected_return=False, timeout=30), '', '')

def clickCancelIcon(d, section):
    d.clickElement(xpath="//div[@class='heading_buttons']/a[@class='cancel']")
    d.reportCommandStatus('Wait for section to close', section, d.waitFor(d, lambda d: d.getElement(xpath="//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]"), expected_return=False, timeout=30), '', '')

def clickHideIcon(d, section):
    d.clickElement(xpath="//div[@class='heading_buttons']/a[@title='Hide section']")

def main(d, WCURL):
    d.setUserData('skip_logging_functions', True)
    d.startSection('Setup the visit type with the single section layout')
    d.miedb.dbExec("INSERT INTO layout (active, module, name, layout_html) VALUES (1, 'encounters', %s, %s)",
                   VISIT, LAYOUT)
    d.miedb.dbExec("INSERT INTO encounter_exams (visit_type, layout_name, exam_name) VALUES (%s, %s, %s)",
                   VISIT, VISIT, VISIT)
    d.endSection()

    u = d.getWCUnitTest('Verify Single Dynamic Section')
    u.setup(addEncounter, 18)
    u.verifyElements([
        wcElement('xpath', "//div[@class='wc-enc-dynamic-exam']"),
        wcElement('xpath', "//div[@class='wc-enc-dynamic-group-content']"),
        wcElement('xpath', "//div[contains(@class, 'wc-enc-dynamic-section') and "\
            "contains(@class, 'show_summary') and contains(@class, 'no_toggle')]"),
        wcElement('xpath', "//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='Encounter']"),
        wcElement('xpath', "//div[@class='heading_buttons']"),
        wcElement('xpath', "//div[@class='heading_buttons']/a[@class='sectionEdit' and @title='Edit']"),
        wcElement('xpath', "//div[@class='wc-enc-dynamic-section-content']"),
    ], reason='Check for dynamic section structure')
    u.test()

    u = d.getWCUnitTest('Verify Opening Section')
    u.setup(addEncounter, 18)
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]"),
    ], reason='Ensure section is open/editable')
    u.verifyElements([
        wcElement('xpath', "//*[self::h2 or self::h3][contains(@class, 'exam_tab')]/parent::div[contains(@class, 'edit_mode')]//button[contains(@class, 'next') and @type='button']")
    ], reason='Ensure the Next button is present')
    u.verifyElements([
        wcElement('xpath', "//div[@class='heading_buttons']/a[@class='next' and @title='Next']"),
        wcElement('xpath', "//div[@class='heading_buttons']/a[@class='cancel' and @title='Cancel']"),
        wcElement('xpath', "//div[@class='heading_buttons']/a[@class='wc-enc-dynamic-section-x' and @title='Hide section']"),
    ], reason='Ensure control icons are present')
    u.test(clickSectionAndWait, SECTION)

    u = d.getWCUnitTest('Verify Closing Section')
    u.setup(addEncounter, 18)
    u.setup(clickSectionAndWait, SECTION, reason='Open the section')
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]", exists=False),
    ], reason='Ensure section is closed/non-editable')
    u.verifyElements([
        wcElement('xpath', "//*[self::h2 or self::h3][contains(@class, 'exam_tab')]/parent::div[contains(@class, 'edit_mode')]//button[contains(@class, 'next') and @type='button']", exists=False)
    ], reason='Ensure the Next button is not present')
    u.test(clickSectionAndWait, SECTION)

    u = d.getWCUnitTest('Verify UI Indicates "Busy" Status When Opening')
    u.setup(addEncounter, 18)
    u.setup(lambda d: d.runJS("window.jsHTTP = null; miehttp.post = miehttp.get = miefunction.noop"),
        reason='Intentionally break the ajax utility so the section will fail to load and remain in the busy state')
    u.setup(lambda d: d.runJS("encdynamic.invalidateCache()"), reason='Clear the cache')
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'wc-enc-dynamic-section-flipping')]"),
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]", exists=False),
    ], reason='Ensure section is not editable and is still in the busy state')
    u.test(clickSection, SECTION)

    u = d.getWCUnitTest('Verify UI Indicates "Busy" Status When Closing')
    u.setup(addEncounter, 18)
    u.setup(clickSectionAndWait, SECTION, reason='First open the section properly')
    u.setup(lambda d: d.runJS("window.jsHTTP = null; miehttp.post = miehttp.get = miefunction.noop"),
        reason='Intentionally break the ajax utility so the section will fail to close and remain in the busy state')
    u.setup(lambda d: d.runJS("encdynamic.invalidateCache()"), reason='Clear the cache')
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'wc-enc-dynamic-section-flipping')]"),
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]", exists=True),
    ], reason='Ensure section is still editable and is still in the busy state')
    u.test(clickSection, SECTION)

    u = d.getWCUnitTest('Verify Next Button')
    u.setup(addEncounter, 18)
    u.setup(clickSectionAndWait, SECTION, reason='Open the section')
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]", exists=False),
    ], reason='Ensure section is closed/non-editable')
    u.test(clickNextButton)

    u = d.getWCUnitTest('Verify Control Button For Next')
    u.setup(addEncounter, 18)
    u.setup(clickSectionAndWait, SECTION, reason='Open the section')
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]", exists=False),
    ], reason='Ensure section is closed/non-editable')
    u.test(clickNextIcon)

    u = d.getWCUnitTest('Verify Control Button For Cancel')
    u.setup(addEncounter, 18)
    u.setup(clickSectionAndWait, SECTION, reason='Open the section')
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'edit_mode') and contains(@class, 'wc-enc-dynamic-section')]", exists=False),
    ], reason='Ensure section is closed/non-editable')
    u.verifyElements([
        wcElement('xpath', "//*[self::h2 or self::h3][contains(@class, 'exam_tab')]/parent::div[contains(@class, 'edit_mode')]//button[contains(@class, 'next') and @type='button']", exists=False)
    ], reason='Ensure the Next button is not present')
    u.test(clickCancelIcon)

    u = d.getWCUnitTest('Verify Control Button For Hide')
    u.setup(addEncounter, 18)
    u.verifyElements([
        wcElement('xpath', "//div[contains(@class, 'wc-enc-dynamic-section') and "\
            "contains(@class, 'show_summary') and contains(@class, 'no_toggle')]", exists=False),
        wcElement('xpath', "//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='{0}']".format(SECTION),
            text=SECTION.upper(), exists=False),
        wcElement('xpath', "//div[@class='heading_buttons']", exists=False),
        wcElement('xpath', "//div[@class='wc-enc-dynamic-section-content']", exists=False),
    ], reason='Verify structure is gone')
    u.test(clickHideIcon)

 
