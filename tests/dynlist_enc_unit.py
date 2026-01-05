"""
@owners: 
"""

from wcunittest import wcElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


ehSections = [
	'Smart Plan',
	'Case',
	'Past Medical History',
	'Past procedures',
	'Presenting medications',
	'Allergies / Intolerances',
	'Immunizations / Injections',
	'Tests & procedures',
	'Symptoms / Diagnosis',
	'Medication orders',
	'Visit orders',
	'Restrictions',
	'Accommodations',
	'CC',
	'Recommendations',
	'Goals',
	'Financials'
]

wcSections = [
	'Smart Plan',
	'Case',
	'Past Medical History',
	'Past procedures',
	'Presenting medications',
	'Allergies / Intolerances',
	'Immunizations / Injections',
	'Tests & procedures',
	'Symptoms / Diagnosis',
	'Medication orders',
	'Visit orders',
	'Restrictions',
	'Accommodations',
	'CC',
	'Recommendations',
	'Goals',
	'Financials'
]

def scroll(d, data):
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]'))


def addEncounter(d, pat_id):
	d.navigate('?f=chart&s=pat&pat_id=18')
	d.clickElement(text='Add Visit')
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "mask")]'), expected_return=False)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[contains(., "WebChart is currently working")]'), expected_return=False, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"]'), expected_return=True, timeout=30)

def allQL(d, section):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	if not d.getElement(xpath='//div[@id="wc_encnav_buttons"]/a[@title="Show/Hide Quick Lists"]'):
		d.reportCommandStatus('All Quick Lists toggle button', 'Show\/Hide Quick Lists button not present', False, '', '')
	else:
		d.clickElement(xpath='//div[@id="wc_encnav_buttons"]/a[@title="Show/Hide Quick Lists"]')

def openQL(d, section):
#	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "mask")]'), expected_return=False)
	d.wcutils.waitForMask(timeout=60)
	if d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@class, "forceQL") and not(@style="display: none;") or @style="display: block;"]'.format(section)), expected_return=True):
		d.reportCommandStatus('quicklist', '{0} quicklist open by default'.format(section), True, '', '')
	elif d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][@style="display: none;" or not(@style="display") and not(@style="display: block;")]'.format(section)), expected_return=True):
		d.clickElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div/a[@class="ql_toggle"]'.format(section))
		if not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][@style="display: block;" and not(@style="display: none;")]'.format(section)), expected_return=True):
			d.reportCommandStatus('quicklist', '{0} quicklist was not opened'.format(section), True, '', '')
		d.reportCommandStatus('quicklist', '{0} quicklist initial click'.format(section), True, '', '')
	else:
		d.reportCommandStatus('quicklist', '{0} quicklist already open'.format(section), True, '', '')

def closeQL(d, section):
#	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "mask")]'), expected_return=False, timeout=30)
	d.wcutils.waitForMask(timeout=60)
	if d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "display: block") or not(contains(@style, "display: none"))]'.format(section)):
#		d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "mask")]'), expected_return=False, timeout=30)
		d.wcutils.waitForMask(timeout=60)
		d.clickElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div/a[@class="ql_toggle"]'.format(section))
		d.reportCommandStatus('quicklist', '{0} quicklist closed'.format(section), True, '', '')

def commonElements(d, section):
	d.startSection('Dynamic item elements')
	d.startSection('Set Library icon/button')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div/a[@class="setLibrary"]'.format(section), present=True)
	d.endSection()
	d.startSection('Dynamic item container')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]'.format(section), present=True)
	d.endSection()
	d.endSection()

def quicklistToggle(d, section):
	d.startSection('Quicklist Toggle')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div/a[@class="ql_toggle"]'.format(section), present=True)
	d.endSection()

def quicklistExpCol(d, section):
	d.startSection('Quicklist expand/collapse toggle')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]/span[contains(@class, "ql-mode-toggle")]'.format(section), present=True)
	d.endSection()

def quicklistAllExpColl(d, section):
	d.startSection('Quicklist group expand all quicklists')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//div[contains(@class, "ql-group-controls")]/span[@title="Expand all" and contains(@class, "expand-all")]'.format(section), present=True)
	d.endSection()
	d.startSection('Quicklist group collapse all quicklists')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//div[contains(@class, "ql-group-controls")]/span[@title="Collapse all" and contains(@class, "collapse-all")]'.format(section), present=True)
	d.endSection()

def quicklistSearch(d, section):
	d.startSection('Quicklist Search')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]/div[contains(@class, "ql-group-search-container")]//input[@class="default-search" and @type="search"]'.format(section), present=True)
	d.endSection()

def quicklistShowHide(d, section):
	d.startSection('Quicklist show/hide toggle')
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//*[@class="dynTitle"]/span[@class="dynQL-controls"]/span[@title="Toggle Show/Hide"]'.format(section), present=True)
	d.endSection()

def quicklistAddButton(d, section):
	d.startSection('Quicklist Add button')
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]'))
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item")  or contains(., "Add New Presenting Problem")]'.format(section)), expected_return=True, timeout=10)
	d.mouseOver(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item")  or contains(., "Add New Presenting Problem")]'.format(section))
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//div[@class="ql-list"]//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]/span[@class="dynOps"]//button[@title="Add" or "Prescribe"]'.format(section)), expected_return=True, timeout=3)
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//div[@class="ql-list"]//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]/span[@class="dynOps"]//button[@title="Add" or "Prescribe"]'.format(section), present=True)
	d.endSection()

def quicklistAddFinancialsButton(d, section):
	d.startSection('Quicklist Add button')
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//li[@class="dynItem other-sc-trigger"][contains(., "Charge")]'))
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//li[@class="dynItem other-sc-trigger"][contains(., "Charge")]'.format(section)), expected_return=True, timeout=10)
	d.mouseOver(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//li[@class="dynItem other-sc-trigger"][contains(., "Charge")]'.format(section))
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//div[@class="ql-list"]//li[@class="dynItem other-sc-trigger"][contains(., "Charge")]/span[@class="dynOps"]//button[@title="Add"]'.format(section)), expected_return=True, timeout=3)
	d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")]//div[@class="ql-list"]//li[@class="dynItem other-sc-trigger"][contains(., "Charge")]/span[@class="dynOps"]//button[@title="Add"]'.format(section), present=True)
	d.endSection()

def addDynItem(d, section):
	oldtimeout = d.timeout
	d.setTimeout(10)
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete prior to adding'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "mask")]'), expected_return=False)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "block") or contains(@class, "forceQL")]//div[@class="ql-header"][contains(.,"Tests & Procedures") or contains(., "Visit Orders") or contains(., "Carboned Copied User") or contains(., "Quick List") or contains(.,"New Presenting Problem") or contains(.,"New PMH Item") or contains(.,"Make New Assessment")]/following-sibling::div//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]'.format(section)), expected_return=True, timeout=10)
	d.mouseOver(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "block") or contains(@class, "forceQL")]//div[@class="ql-header"][contains(.,"Tests & Procedures") or contains(., "Visit Orders") or contains(., "Carboned Copied User") or contains(., "Quick List") or contains(.,"New Presenting Problem") or contains(.,"New PMH Item") or contains(.,"Make New Assessment")]/following-sibling::div//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]'.format(section))
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "block") or contains(@class, "forceQL")]//div[@class="ql-header"][contains(.,"Tests & Procedures") or contains(., "Visit Orders") or contains(., "Carboned Copied User") or contains(., "Quick List") or contains(.,"New Presenting Problem") or contains(.,"New PMH Item") or contains(.,"Make New Assessment")]/following-sibling::div//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]/span/button[contains(@title, "Add") or contains(@title, "Prescribe")]'.format(section)), expected_return=True, timeout=3)
	d.clickElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "block") or contains(@class, "forceQL")]//div[@class="ql-header"][contains(.,"Tests & Procedures") or contains(., "Visit Orders") or contains(., "Carboned Copied User") or contains(., "Quick List") or contains(.,"New Presenting Problem") or contains(.,"New PMH Item") or contains(.,"Make New Assessment")]/following-sibling::div//li[@class="dynItem"][contains(., "Other") or contains(., "Add New Assessment Item") or contains(., "Add New Presenting Problem")]/span/button[contains(@title, "Add") or contains(@title, "Prescribe")]'.format(section))
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.wcutils.waitForEle(xpath='//input[contains(@class, "autocomplete")]', timeout=60)
	d.enterFormData('a', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
	if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
		d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
	else:
		d.enterFormData('ab', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
		if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
			d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
		else:
			d.enterFormData('20', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
			if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
				d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
			else:
				d.enterFormData('com', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
				if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
					d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
				else:
					d.enterFormData('pre', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
					if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
						d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
					else:
						d.enterFormData('obes', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
						if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
							d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
						else:
							d.enterFormData('obes', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
							if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
								d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
							else:
								d.enterFormData('botu', xpath='//input[contains(@class, "autocomplete")]', clear=True, blur=False)
								if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=20):
									d.clickElement(xpath='//div[@class="defaultacdiv"]//div')
								else:
									d.reportCommandStatus('Autocomplete failed', '', False, '', 'None of the test-defined entries worked for this autocomplete')
	if not d.getElement(xpath='//div[@class="defaultacdiv" and not(contains(@style, "visibility: visible"))]//div') and d.getElement(xpath='//input[contains(@class, "autocomplete")]/parent::span/preceding-sibling::input[contains(@name, "description") and string-length(@value)!=0]'):
		if d.getElement(xpath='//div[@class="defaultacdiv" and contains(@style, "visibility: visible")]//div'):
			d.reportCommandStatus('', '', False, '', 'Autocomplete options are still present')
		if not d.getElement(xpath='//input[contains(@class, "autocomplete")]/parent::span/preceding-sibling::input[contains(@name, "description") and string-length(@value)!=0]'):
			d.reportCommandStatus('', '', False, '', 'Autocomplete input has no value')
	if section == "Medication orders":
		medExtras(d, section)
	if d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[contains(@class, "wc_win")]//button[@type="button" and contains(., "Save") and not(contains(., "Save "))]'), expected=True, timeout=60):
		d.clickElement(xpath='//div[contains(@class, "wc_win")]//button[@type="button" and contains(., "Save") and not(contains(., "Save "))]')
	else:
		if d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[contains(@class, "wc_win")]//button[@type="button" and contains(., "Save") and not(contains(., "Save "))]'), expected=True, timeout=60, comments='Wait an additional 60s for the Save button'):
			d.clickElement(xpath='//div[contains(@class, "wc_win")]//button[@type="button" and contains(., "Save") and not(contains(., "Save "))]')
		else:
			d.reportCommandStatus('', '', False, '', 'Unable to locate Save button after 2m')
	if section == "Tests & procedures":
		tpwait(d, section)
	if not d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[@class="wc_win"]'), expected=False, timeout=60):
		d.reportCommandStatus('', '', False, '', 'An miewin popup is still open')
	d.setTimeout(oldtimeout)

def medExtras(d, section):
	miewin = d.getElement(xpath='//div[@class="wc_win"]//div[contains(@class, "wc_win_body")]')
	ele = d.getElement(xpath='//div[contains(@class, "wc_win")]//label[contains(., "None")]/preceding-sibling::input[@type="radio"]')
	d.enterFormData('1 po bid', xpath='//label[contains(., "Practitioner Sig")]/following-sibling::*//input[@name="sig"]', clear=True, blur=False)
	d.enterFormData('30', xpath='//label[contains(., "Duration")]/following-sibling::*//input[@name="duration"]', clear=True, blur=False)
	d.enterFormData('30', xpath='//label[contains(., "Total Quantity")]/following-sibling::*//input[@name="total_quantity"]', clear=True, blur=False)
	d.enterFormData('Capsule', xpath='//label[contains(., "Total Quantity")]/following-sibling::*//select[@name="qty_uom"]', clear=True, blur=False)
	d.enterFormData('0', xpath='//label[contains(., "Refills")]/following-sibling::*//input[@name="refills"]', clear=True, blur=False)
	d.enterFormData('Sample, John M.', xpath='//label[contains(., "Prescriber")]/following-sibling::*//select')
	if ele:
		d.runJS('arguments[0].scrollIntoView(true)', ele)
		d.clickElement(xpath='//label[contains(., "None")]/preceding-sibling::input[@type="radio"]')
	else:
		d.reportCommandStatus('Prescribe Medication miewin', 'Element not found', False, ele, 'Failed to click the None transmission radio')
	d.clickElement(xpath='//legend[contains(., "Transmission")]/following-sibling::div//label[contains(.,"None")]')


def tpwait(d, section):
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and not(contains(@class, "edit_mode"))]/*[@class="exam_tab" and contains(., "Tests & procedures")]/following-sibling::div/div[contains(@class, "dynContent")]/div[contains(@class, "dynQL") and contains(@style, "display: none;")]'), expected_return=True, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab" and contains(., "Tests & procedures")]/parent::div[contains(@class, "wc-enc-dynamic-section")]/following-sibling::div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab" and contains(., "Abdomen")]'), expected_return=True, timeout=30)
	if not d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[@class="wc_win"]'), expected=False, timeout=60):
		d.reportCommandStatus('', '', False, '', 'An miewin popup is still open')

def editDIButton(d, section):
	d.startSection('Dynamic item Edit/Correct Medication button')
	d.wcutils.waitForAJAX(timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section)), expected_return=True)
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]'.format(section)))
	d.mouseOver(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section))
	if d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[@title="Edit" or @title="Correct Medication" or @title="Change Therapy"]'.format(section)), expected_return=True):
		d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[@title="Edit" or @title="Correct Medication" or @title="Change Therapy"]'.format(section), present=True)
	elif not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[@title="Edit" or @title="Correct Medication" or @title="Change Therapy"]'.format(section)), expected_return=True):
		d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section)), expected_return=True)
		d.mouseOver(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section))
		d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[@title="Edit" or @title="Correct Medication" or @title="Change Therapy"]'.format(section)), expected_return=True)
		d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[@title="Edit" or @title="Correct Medication" or @title="Change Therapy"]'.format(section), present=True)
	else:
		d.reportCommandStatus('DynOps', 'element not found after 2 attempts', False, '', '')
	d.endSection()

def delDIButton(d, section):
	d.startSection('Dynamic item Delete/Remove button')
	d.wcutils.waitForAJAX(timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section)), expected_return=True)
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]'.format(section)))
	d.mouseOver(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section))
	if d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[contains(@title, "Delete") or contains(@title, "Remove")]'.format(section)), expected_return=True):
		d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[contains(@title, "Delete") or contains(@title, "Remove")]'.format(section), present=True)
	elif not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[contains(@title, "Delete") or contains(@title, "Remove")]'.format(section)), expected_return=True):
		d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section)), expected_return=True)
		d.mouseOver(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section))
		d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[contains(@title, "Delete") or contains(@title, "Remove")]'.format(section)), expected_return=True)
		d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul//li[@class="dynItem"]//span[@class="dynOps"]//button[contains(@title, "Delete") or contains(@title, "Remove")]'.format(section), present=True)
	else:
		d.reportCommandStatus('DynOps', 'element not found after 2 attempts', False, '', '')
	d.endSection()

def moveDIButton(d, section):
	d.startSection('Dynamic item Move button')
	d.wcutils.waitForAJAX(timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section)), expected_return=True)
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]'.format(section)))
	d.mouseOver(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section))
	if d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]//span[@class="dynOps"]/span[@title="Move"]'.format(section)), expected_return=True):
		d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]//span[@class="dynOps"]/span[@title="Move"]'.format(section), present=True)
	elif not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]//span[@class="dynOps"]/span[@title="Move"]'.format(section)), expected_return=True):
		d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section)), expected_return=True)
		d.mouseOver(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]'.format(section))
		d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]//span[@class="dynOps"]/span[@title="Move"]'.format(section)), expected_return=True)
		d.verifyElementPresent(xpath='//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div[@class="wc-enc-dynamic-section-content"]//div[contains(@class, "dynContent")]//ul/li[@class="dynItem"]//span[@class="dynOps"]/span[@title="Move"]'.format(section), present=True)
	else:
		d.reportCommandStatus('DynOps', 'element not found after 2 attempts', False, '', '')
	d.endSection()

def goToSection(d, section):
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//*[@class="exam_tab"][contains(., "{0}")]'.format(section)))


def main(d, WCURL):
	systype = d.getUserData('systemType')
	section = []
	exclude = []
	ehExclude = []
	wcExclude = []
	if systype == 'EH':
		sections = ehSections
	elif systype == 'WCNOW':
		sections = wcSections

	t = d.getWCUnitTest('Add a Visit Encounter')
	t.test(addEncounter)

	d.startSection('Quicklists')

	d.startSection('Open all Quicklists button')
	t = d.getWCUnitTest('Open all quicklists')
	t.setup(allQL)
	t.verifyElements([
		wcElement('xpath', '//*[@class="exam_tab"]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "display: block") or not(contains(@style, "display: none"))]'),
	], reason='Verify that the quicklist containers are open and not hidden')
	t.test()
	d.endSection()

	d.startSection('Close all Quicklists button')
	t = d.getWCUnitTest('Open all quicklists')
	t.setup(allQL)
	t.verifyElements([
		wcElement('xpath', '//*[@class="exam_tab"]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "display: none;")]'),
		wcElement('xpath', '//*[@class="exam_tab"]/following-sibling::div//div[contains(@class, "dynQL")][not (contains(@style, "display: block"))]'),
	], reason='Verify that the quicklist containers are closed')
	t.test()
	d.endSection()

	d.startSection('Open all Quicklist Containers from their respective quicklist container show/hide toggle')
	ehExclude = []
	wcExclude = ['Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Open the {0} quicklists'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		ele = []
		ele.append(wcElement('xpath', '//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "display: block") or not(contains(@style, "display: none"))]'.format(s)))
		t.verifyElements(ele, reason='Verify that the {0} quicklist container is open and not hidden'.format(s))
		ele.append(wcElement('xpath', '//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][not (contains(@style, "display: none"))]'.format(s)))
		t.verifyElements(ele, reason='Verify that the {0} quicklist container is open and not hidden'.format(s))
		t.test()
	d.endSection()

	d.startSection('Close all Quicklist Containers from their respective quicklist container show/hide toggle')
	ehExclude = []
	wcExclude = ['Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Close the {0} quicklist'.format(s))
		t.setup(closeQL, s)
		ele = []
		ele.append(wcElement('xpath', '//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][not (contains(@style, "display: block;"))]'.format(s)))
		t.verifyElements(ele, reason='Verify that the {0} quicklist container is closed and not hidden'.format(s))
		ele.append(wcElement('xpath', '//*[@class="exam_tab"][contains(., "{0}")]/following-sibling::div//div[contains(@class, "dynQL")][contains(@style, "display: none")]'.format(s)))
		t.verifyElements(ele, reason='Verify that the {0} quicklist container is closed and not hidden'.format(s))
		t.test()
	d.endSection()

	d.startSection('Quicklist Toggles')
	ehExclude = []
	wcExclude = ['Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(quicklistToggle, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Quicklist Expand/Collapse')
	ehExclude = []
	wcExclude = ['Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(quicklistExpCol, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Quicklist Expand All / Collapse All')
	ehExclude = ['CC', 'Financials']
	wcExclude = ['CC', 'Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(quicklistAllExpColl, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Quicklist Search')
	ehExclude = ['CC', 'Financials']
	wcExclude = ['CC', 'Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(quicklistSearch, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Quicklist Show/Hide')
	ehExclude = []
	wcExclude = ['Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(quicklistShowHide, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Quicklist Add Button')
	ehExclude = ['Smart Plan', 'Case', 'Recommendations', 'Financials']
	wcExclude = ['Smart Plan', 'Case', 'Recommendations', 'Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(quicklistAddButton, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('TODO-Quicklist Add to Exam Button')
	ehExclude = []
	wcExclude = ['Smart Plan', 'Case', 'Recommendations', 'Accommodations', 'Financials']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	d.endSection()
	d.endSection()

	d.startSection('Dynamic Items')
	d.startSection('Add a test dynItem to each section')
	ehExclude = ['Smart Plan', 'Case', 'Recommendations', 'Financials', 'Tests & procedures']
	wcExclude = ['Smart Plan', 'Case', 'Recommendations', 'Accommodations', 'Financials', 'Tests & procedures']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Add a dynamic item to {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(addDynItem, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Dyn Item Edit buttons')
	ehExclude = ['Case', 'Medication orders', 'Recommendations', 'Financials']
	wcExclude = ['Case', 'Medication orders', 'Recommendations', 'Financials', 'Accommodations']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(editDIButton, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Dyn Item Delete buttons')
	ehExclude = ['Case', 'Recommendations', 'Financials']
	wcExclude = ['Case', 'Recommendations', 'Financials', 'Accommodations']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(delDIButton, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()

	d.startSection('Dyn Item Move buttons')
	ehExclude = ['Case', 'Recommendations', 'Financials', 'Tests & procedures', 'CC']
	wcExclude = ['Case', 'Recommendations', 'Financials', 'Tests & procedures', 'CC', 'Accommodations']
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	sec = [x for x in sections if x not in exclude]
	for s in sec:
		t = d.getWCUnitTest('Verify element(s) are present in {0}'.format(s))
		t.setup(goToSection, s)
		t.setup(openQL, s)
		t.setup(moveDIButton, s)
		t.setup(closeQL, s)
		t.test()
	d.endSection()
	d.endSection()

	d.startSection('TODO-Dyn Item Drug Info buttons')
	ehExclude = []
	wcExclude = []
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	d.endSection()

	d.startSection('TODO-Add to Exam button')
	ehExclude = []
	wcExclude = []
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	d.endSection()

	d.startSection('TODO-Excluded/Unique functionality sections')
	ehExclude = []
	wcExclude = []
	systype = d.getUserData('systemType')
	if systype == 'EH':
		exclude = ehExclude
	elif systype == 'WCNOW':
		exclude = wcExclude

	d.startSection('Add an item from the Tests & procedures dynamic section quicklist')
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	t = d.getWCUnitTest('Add an item from Tests & procedures')
	t.setup(goToSection, 'Tests & procedures')
	t.setup(openQL, 'Tests & procedures')
	t.setup(addDynItem, 'Tests & procedures')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "wc-enc-dynamic-section") and not(contains(@class, "edit_mode"))]/*[@class="exam_tab" and contains(., "Tests & procedures")]')
	], reason="Verify when an order is added from the Tests & Procedures quicklist, Tests & procedures section remains closed")
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "wc-enc-dynamic-section") and not(contains(@class, "edit_mode"))]/*[@class="exam_tab" and contains(., "Tests & procedures")]/following-sibling::div/div[contains(@class, "dynContent")]/div[contains(@class, "dynQL")][contains(@style, "display: none") or not(contains(style, "display: block"))]')
	], reason="Verify when an order is added from the Tests & Procedures quicklist, Tests & procedures section quicklist is closed")
	t.verifyElements([
		wcElement('xpath', '//*[@class="exam_tab" and contains(., "Tests & procedures")]/parent::div[contains(@class, "wc-enc-dynamic-section")]/following-sibling::div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab" and contains(., "Abdomen")]')
	], reason="Verify when an order is added from the Tests & Procedures quicklist, it adds a new section")
	t.test()
	d.endSection()

	d.startSection('Test the Financials section quicklist')
	d.startSection('Excluded Sections')
	d.reportCommandStatus('Excluded sections:', '{0}'.format(exclude), True, '', '')
	d.endSection()
	if systype == 'EH':
		d.startSection('Financials Quicklist')
		t = d.getWCUnitTest('Verify element(s) are present in Financials')
		t.setup(openQL, 'Financials')
		t.setup(quicklistAddFinancialsButton, 'Financials')
		t.setup(closeQL, 'Financials')
		t.test()
		d.endSection()
	d.endSection()
	d.endSection()

