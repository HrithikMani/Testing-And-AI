"""
@owners: aris
"""
from wcunittest import wcElement, wcDBRecord
from selenium.webdriver.common.keys import Keys

# Missing last name, first name, birth date, EO warning
# Matching Chart alert(s)
# Register a patient/add a patient chart - (NO PART MR) MR# not initially assigned
# Please select a MR Number warning
# Duplicate chart created
# Register patient using PDQ
# Edit Demographics

# Verify required fields; last name, first name, birth date
# Verify phone number and formatting
# "Is deceased checkbox checks automatically when a death date is entered
# County, City, State is auto-filled when the zip code is entered
# State/Province dropdown changes when Country is selected
# Temporary Chart/Record
# Invalid Chart/Record

def inserteditFett(d, data):
	d.miedb.dbExec("INSERT INTO patients (first_name, first_name_phn, last_name, last_name_phn, attending_physician, referring_physician, family_physician, state, country, cellco_id, email, preferred_alert_method, ssn, spouse_birthdate, employer_state, employer_country, interface, birth_date, death_indicator, death_date, chart_online, active, is_patient, is_tmp, signature_date, create_date, edit_date, revised_by, username) VALUES ('Boba', 11, 'Fett', 13, 0, 0, 0, 'IN', 'US', 0, 'bfett@bettercorp.com', 0, 848484848, '0000-00-00 00:00:00', 'IN', 'US', 'Unknown', '1981-03-03 00:00:00', 0, '0000-00-00 00:00:00', 0, 1, 1, 0, '0000-00-00 00:00:00', '2007-02-02 09:15:00', '2007-02-02 09:15:00', 8, 'NULL')")
	d.miedb.dbExec("INSERT INTO patient_mrns (wc_partition, mrnumber, pat_id) VALUES ('MIE', 10052, (SELECT pat_id FROM patients WHERE last_name='Fett'))")
	d.miedb.dbExec("INSERT INTO patient_extended_values (pat_id, ext_id, value) VALUES ((SELECT pat_id FROM patients WHERE last_name='Fett'), 95, 0)")
	d.miedb.dbExec("INSERT INTO recent_patients (user_id, pat_id, lookup_date) VALUES (8, (SELECT pat_id FROM patients WHERE last_name='Fett'), '2007-02-02 09:15:00')")
	d.miedb.dbExec("INSERT INTO observations (request_id, obs_code, template_id, pat_id, observer_id, revision_number, user_id, observed_datetime, obs_order, obs_result, obs_name, obs_units, verified_datetime, restricted, create_datetime, modified_datetime, interface, test_comments, free_text, micro_result, interpretive_text, inpatient, observed_start_ts, observed_end_ts) VALUES (0, 2934, 'patient_extended', (SELECT pat_id FROM patients WHERE last_name='Fett'), 8, 0, 8, '2007-02-02 09:15:00', 0, 0, 'pev.excluded_from_quality_care', 'NULL', '0000-00-00 00:00:00', 0, '2007-02-02 09:15:00', '2007-02-02 09:15:00', 'WEBCHART', '', '', '', '', 0, '0000-00-00 00:00:00', '2007-02-02 09:15:00')")
	d.navigate('?f=chart')
	d.enterFormData('Fett', name='sstring')
	d.clickElement(xpath='//input[@type="submit"][@name="pat_search"]')
	if d.wcutils.waitFor(lambda d: d.getElement(xpath='//span[@class="wc_tab_title"][contains(.,"Admin")]'), expected=True, timeout=60, comments="Wait for the Admin charttab to be clickable"):
		d.clickElement(xpath='//span[@class="wc_tab_title"][contains(.,"Admin")]')
	else:
		d.reportCommandStatus('', 'inserteditFett()', False, '', 'The chart tab was not clickable within 60s')
	if d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[@id="wc_tabbar" and contains(@class, "menuOpen")]//ul/li/a[contains(.,"Demographics")]'), expected=True, timeout=60, comments="Wait for the Demographics subtab to be clickable"):
		d.clickElement(xpath='//div[@id="wc_tabbar" and contains(@class, "menuOpen")]//ul/li/a[contains(.,"Demographics")]')
	else:
		d.reportCommandStatus('', 'inserteditFett()', False, '', 'The sub tab was not clickable within 60s')
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')

def editFett(d, data):
	d.navigate('?f=chart')
	d.enterFormData('Fett', name='sstring')
	d.clickElement(xpath='//input[@type="submit"][@name="pat_search"]')
	if d.wcutils.waitFor(lambda d: d.getElement(xpath='//span[@class="wc_tab_title"][contains(.,"Admin")]'), expected=True, timeout=60, comments="Wait for the Admin charttab to be clickable"):
		d.clickElement(xpath='//span[@class="wc_tab_title"][contains(.,"Admin")]')
	else:
		d.reportCommandStatus('', 'editFett()', False, '', 'The chart tab was not clickable within 60s')
	if d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[@id="wc_tabbar" and contains(@class, "menuOpen")]//ul/li/a[contains(.,"Demographics")]'), expected=True, timeout=60, comments="Wait for the Demographics subtab to be clickable"):
		d.clickElement(xpath='//div[@id="wc_tabbar" and contains(@class, "menuOpen")]//ul/li/a[contains(.,"Demographics")]')
	else:
		d.reportCommandStatus('', 'editFett()', False, '', 'The sub tab was not clickable within 60s')
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')

def clickElement(d, text):
	d.clickElement(text=text)

def clickSave(d, data):
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Save button not present')
	else:
		d.clickElement(xpath='//input[@value="Save"]')

def otherDemo(d, data):
# rm?	d.wcutils.waitForMask(expected=False, timeout=120)
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	if d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(.,"Other Data")]'), expected_return=True, timeout=120):
		d.clickElement(xpath='//*[@class="exam_tab"][contains(.,"Other Data")]')
		if not d.waitFor(d, lambda d: d.getElement(xpath='//td[contains(.,"Birth Sex")]/following-sibling::td//input'), expected_return=True, timeout=120):
			d.reportCommandStatus('Timeout', '', False, '', 'Other Demographics - birth sex input not found')
	else:
		d.reportCommandStatus('Timeout', '', False, '', 'Other Demographics section not found')

def enterDemo(d, idx):
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')
	else:
		if not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "Demographic Information")]/following-sibling::div//input[@id="DPI_middle_name"]'), expected_return=True, timeout=20):
			d.reportCommandStatus('Dynamic Section', '', False, '', 'Demographic Information section input not found')
		else:
			d.enterFormData('A', id='DPI_middle_name')
			d.enterFormData('United States', id='DPI_country')
			d.enterFormData('46804', id='DPI_zip_code', blur=False)
			d.wcutils.waitForAJAX(timeout=60, quiet=30)
			if d.wcutils.waitForEle(xpath='//*[contains(@onblur, "autoFill")]', expected=True, timeout=60):
				d.enterFormData(Keys.TAB, id="DPI_zip_code", clear=False)
			else:
				d.reportCommandStatus('enterDemo', '', False, 'ele not present', 'The autofill was not found')
			d.enterFormData('6302 Constitution Drive', id='DPI_address1')
			d.wcutils.waitFor(
				lambda d: d.getElement(id='DPI_county').get_attribute('value') == 'Allen',
				comments='Wait for zip to autofill', timeout=60)
			d.verifyAttribute('value', 'Allen', id='DPI_county')
			d.verifyAttribute('value', 'Fort Wayne', id='DPI_city')
			d.verifyAttribute('value', 'IN', id='DPI_state')
			d.enterFormData('2604596270', id='DPI_home_phone')
			d.enterFormData('2604596271', id='DPI_fax_number')
			d.enterFormData('bfett@better.com', id='DPI_email')
			d.enterFormData('848484848', id='DPI_ssn')
			d.enterFormData('Male', id='DPI_sex')

def changeDemo(d, idx):
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')
	else:
		if not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "Demographic Information")]/following-sibling::div//input[@id="DPI_middle_name"]'), expected_return=True, timeout=20):
			d.reportCommandStatus('Dynamic Section', '', False, '', 'Demographic Information section input not found')
		else:
			d.enterFormData('B', id='DPI_middle_name')
			d.enterFormData('United States', id='DPI_country')
			d.enterFormData('46001', id='DPI_zip_code', blur=False)
			d.wcutils.waitForAJAX(timeout=60, quiet=30)
			if d.wcutils.waitForEle(xpath='//*[contains(@onblur, "autoFill")]', expected=True, timeout=60):
				d.enterFormData(Keys.TAB, id="DPI_zip_code", clear=False)
			else:
				d.reportCommandStatus('changeDemo', '', False, 'ele not present', 'The autofill was not found')
			d.enterFormData('50082 Coliseum Blvd', id='DPI_address1')
			d.enterFormData('Apt 3', id='DPI_address2')
			d.enterFormData('Downstairs', id='DPI_address3')
			d.wcutils.waitFor(
				lambda d: d.getElement(id='DPI_county').get_attribute('value') == 'Madison',
				comments='Wait for zip to autofill', timeout=60)
			d.verifyAttribute('value', 'Madison', id='DPI_county')
			d.verifyAttribute('value', 'Alexandria', id='DPI_city')
			d.verifyAttribute('value', 'IN', id='DPI_state')
			d.enterFormData('2604596272', id='DPI_home_phone')
			d.enterFormData('2604596273', id='DPI_fax_number')
			d.enterFormData('bbfett@better.com', id='DPI_email')
			d.enterFormData('484848484', id='DPI_ssn')
			d.enterFormData('Unknown', id='DPI_sex')

def blankRequired(d, data):
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')
	else:
		d.enterFormData('', id='DPI_last_name')
	d.enterFormData('', id='DPD_birth_dateMONTH')
	d.enterFormData('', id='DPD_birth_dateDAY')
	d.enterFormData('', id='DPD_birth_dateYEAR')
	d.enterFormData('', id='DPD_birth_dateTIME')

def selectDeath(d, data):
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, 'Manual Search link not found', 'Page may not have finished loading')
	else:
		if not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "Demographic Information")]/following-sibling::div//select[@id="DPI_death_indicator"]'), expected_return=True, timeout=20):
			d.reportCommandStatus('Dynamic Section', '', False, '', 'Demographic Information section "Death indicator" input not found')
		else:
			d.enterFormData('Yes', id='DPI_death_indicator')

def enterDeath(d, data):
	if not d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Manual Search")]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, 'Manual Search link not found', 'Page may not have finished loading')
	else:
		if not d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"][contains(., "Demographic Information")]/following-sibling::div//select[@id="DPI_death_indicator"]'), expected_return=True, timeout=20):
			d.reportCommandStatus('Dynamic Section', '', False, '', 'Demographic Information section "Death indicator" input not found')
		else:
			d.enterFormData('Yes', id='DPI_death_indicator')
			d.enterFormData('01', id='DPD_death_dateMONTH')
			d.enterFormData('01', id='DPD_death_dateDAY')
			d.enterFormData('2018', id='DPD_death_dateYEAR')

def excludeQC(d, data):
	if not d.waitFor(d, lambda d: d.getElement(xpath='//input[contains(@id, "DPI_excluded_from_quality_care") and @type="radio"]'), expected_return=True, timeout=120):
		d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')
	else:
		d.enterFormData('1', xpath='//input[contains(@id, "DPI_excluded_from_quality_care") and @type="radio"]')

def enterMIEMR(d, data):
   if not d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MIE"]'), expected_return=True, timeout=20):
      d.reportCommandStatus('Timeout', '', False, '', 'Page not loaded')
   if d.waitFor(d, lambda d: d.getElement(xpath='//input[@id="EDITMR_mrnumber_MIE_use"][@type="checkbox"]'), expected_return=True, timeout=20):
      d.enterFormData(True, id="EDITMR_mrnumber_MIE_use")
   elif d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MIE"][@type="text"]'), expected_return=True, timeout=20):
      d.enterFormData('98989898989', xpath='//input[@name="EDITMR_mrnumber_MIE"]')

def changeActive(d, data):
	if not d.waitFor(d, lambda d: d.getElement(xpath='//input[contains(@name, "DPI_active") and @type="radio"]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Active Chart radio buttons not present')
	else:
		d.clickElement(xpath='//input[@id="DPI_active_0" and @type="radio"]')

def changeTemp(d, data):
	if not d.waitFor(d, lambda d: d.getElement(xpath='//input[contains(@id, "DPI_is_tmp") and @type="radio"]'), expected_return=True, timeout=20):
		d.reportCommandStatus('Timeout', '', False, '', 'Temporary Chart radio buttons not present')
	else:
		d.enterFormData('1', xpath='//input[contains(@id, "DPI_is_tmp") and @type="radio"]')

def openSection(d, section):
    if not d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and contains(@class, "edit_mode")]/*[@class="exam_tab" and contains(., "{0}")]'.format(section)), expected_return=True, timeout=20):
        d.clickElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab" and contains(., "{0}")]'.format(section))
        d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and contains(@class, "edit_mode") and not(contains(@class, "flipping"))]/*[@class="exam_tab" and contains(., "{0}")]'.format(section)), expected_return=True)
    elif d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and contains(@class, "edit_mode")]/*[@class="exam_tab" and contains(., "{0}")]'.format(section)), expected_return=True, timeout=20):
        d.reportCommandStatus('Demographics Dynamic Section', '', False, '', '{0} section is already open'.format(section))
    else:
        d.reportCommandStatus('Demographics Dynamic Section', '', False, '', '{0} cannot be opened'.format(section))

def closeSection(d, section):
    if d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and contains(@class, "edit_mode")]/*[@class="exam_tab" and contains(., "{0}")]'.format(section)), expected_return=True, timeout=20):
        d.clickElement(xpath='//div[contains(@class, "wc-enc-dynamic-section")]/*[@class="exam_tab" and contains(., "{0}")]'.format(section))
        d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and not(contains(@class, "edit_mode")) and not(contains(@class, "flipping"))]/*[@class="exam_tab" and contains(., "{0}")]'.format(section)), expected_return=True, timeout=20)
    elif d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc-enc-dynamic-section") and not(contains(@class, "edit_mode"))]/*[@class="exam_tab" and contains(., "{0}")]'.format(section)), expected_return=True, timeout=20):
        d.reportCommandStatus('Demographics Dynamic Section', '', False, '', '{0} section is already open'.format(section))
    else:
        d.reportCommandStatus('Demographics Dynamic Section', '', False, '', '{0} cannot be opened'.format(section))

def goToSummary(d, data):
	d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(@class, "wc_tab_title")][contains(.,"Summary")]'), expected_return=True, timeout=20)
	d.clickElement(xpath='//a[contains(@class, "wc_tab_title")][contains(.,"Summary")]')
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "portlet")]/div[contains(@class, "portlet-header")]'), expected_return=True, timeout=20)

def searchFett(d, data):
	d.navigate('?f=chart')
	d.enterFormData('Fett', name='sstring')
	d.clickElement(xpath='//input[@type="submit"][@name="pat_search"]')


	
# XPATH BASES:
LABEL='/parent::legend/following-sibling::table//td[@class="field"]'
DEMOALERT='/parent::legend/following-sibling::table//td[@class="alert"]'
INPUT='/parent::legend/following-sibling::table//td[@class="value"]'
QUICKADD='/div[@class="re_wrapper"]/div/div[contains(.,"Quick Add")]/following-sibling::div//'
CURRENTSEARCH='/div[@class="re_wrapper"]/div/div[contains(.,"Current + Search")]/following-sibling::div//'
DEMO_INFO='//span[contains(.,"Demographic Information")]'
PAT_CHART='//span[contains(.,"Patient Chart")]'
RELATIONSHIPS='//span[contains(.,"Relationships")]'
INS_SUM='//span[contains(.,"Insurance Summary")]'
MED_REC_NUM='//span[contains(.,"Medical Record Numbers")]'
EMP_INFO='//span[contains(.,"Employment Information")]'
MAR_INFO='//span[contains(.,"Marital/Contact Information")]'
PROVIDER_INFO='//span[contains(.,"Providers")]'


def main(d, WCURL):
	t = d.getWCUnitTest('Enter the patient\'s zip code')
	t.setup(inserteditFett)
	t.setup(openSection, "Demographic Information")
	t.setup(enterDemo, 0)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"Fort Wayne")]'),
	], reason='Verify entering a patient\'s demographics and zip code logic')
	t.test(goToSummary)

	t = d.getWCUnitTest('Edit the existing patient\'s demographics and zip code logic')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(enterDemo, 0)
	t.setup(changeDemo, 0)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"Alexandria")]'),
	], reason='Verify editing a patient\'s existing demographics information')
	t.test()

	t = d.getWCUnitTest('Submit without required fields; first and last name and birth date')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(blankRequired)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//input[@id="DPI_first_name"]'),
	], reason='Attempt to register a patient with blank required fields and verify that the page has not been navigated away from.')
	t.test()

	t = d.getWCUnitTest('Deceased patient - "Is Deceased" option only, no death date entered')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(selectDeath)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//div[@id="wc_patextended_bar"]//label[contains(.,"Patient is deceased.")]', exists=True),
		wcElement('xpath', '//span[contains(.,"Death Date")]/following-sibling::span[contains(.,"01-01-2018")]', exists=False),
	], reason='Verify the deceased checkbox functionality and resulting message', timeout=60)
	t.test()

	t = d.getWCUnitTest('Deceased patient - with the death date entered')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(enterDeath)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//div[@id="wc_patextended_bar"]//label[contains(.,"Death Date")]', exists=True),
		wcElement('xpath', '//span[contains(.,"Death Date")]/following-sibling::span[contains(.,"01-01-2018")]', exists=True),
	], reason='Verify the deceased checkbox functionality and resulting message', timeout=60)
	t.test()

	t = d.getWCUnitTest('Exclude patient from Quality Care Reporting')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(excludeQC)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//div[@class="bannerMsg" and contains(., "Excluded from Quality Care Reporting")]'),
	], reason='Verify the Exclude from Quality Care Reporting selection and message')
	t.test()

	t = d.getWCUnitTest('Other Data dynamic section elements')
	t.setup(editFett)
	t.setup(otherDemo)
	t.verifyElements([
		wcElement('xpath', '//caption[contains(.,"Demographic Data")]'),
		wcElement('xpath', '//span[contains(.,"Observed date/time")]/span/span[@class="dateinput"]/following-sibling::input[@id="observed_datetime_flowsheet_Demographic_20Data_284TIME"]'),
		wcElement('xpath', '//tbody[@data-obsname="Birth Sex"]/tr/td/div[@class="cell_content"][contains(.,"Birth Sex")]'),
		wcElement('xpath', '//tbody[@data-obsname="Birth Sex"]/tr/td[@class="results"]/div[@class="cell_content"]//input[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//tbody[@data-obsname="Birth Sex"]/tr/td[@class="results"]/div[@class="cell_content"]//button[@title="Clear"]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Gender Identity")]/parent::td/following-sibling::td//input[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Gender Identity")]/parent::td/following-sibling::td//span[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Sexual Orientation")]/parent::td/following-sibling::td//input[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Sexual Orientation")]/parent::td/following-sibling::td//span[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous First Name")]/parent::td/following-sibling::td//textarea[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous First Name")]/parent::td/following-sibling::td//textarea[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous First Name")]/parent::td/following-sibling::td//div[@class="macro-library-btn"]//a[@title="Macro Explorer"]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous First Name")]/parent::td/following-sibling::td//div[@class="macro-library-btn"]/following-sibling::input[@class="macros_filter"]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous First Name")]/parent::td/following-sibling::td//div[@class="macro-library-btn"]/following-sibling::span/input[@class="macros_global" and @type="checkbox"]/following-sibling::label[contains(., "Global Macros")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous Last Name")]/parent::td/following-sibling::td//textarea[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous Last Name")]/parent::td/following-sibling::td//textarea[contains(@id, "obs_result_")]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous Last Name")]/parent::td/following-sibling::td//div[@class="macro-library-btn"]//a[@title="Macro Explorer"]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous Last Name")]/parent::td/following-sibling::td//div[@class="macro-library-btn"]/following-sibling::input[@class="macros_filter"]'),
		wcElement('xpath', '//div[@class="cell_content"][contains(.,"Previous Last Name")]/parent::td/following-sibling::td//div[@class="macro-library-btn"]/following-sibling::span/input[@class="macros_global" and @type="checkbox"]/following-sibling::label[contains(., "Global Macros")]'),
		wcElement('xpath', '//button[contains(@class,"next")]'),
	], reason='Verify the elements are present within the "Other Data" dynamic section ***Functionality tested in the Okra workflow test')
	t.test()

	t = d.getWCUnitTest('Register a Temporary chart')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(changeTemp)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//div[@class="obnoxious_warning"][contains(.,"TEMPORARY RECORD")]'),
	], reason='Verify that we get the TEMPORARY RECORD alert on the page')
	t.test(goToSummary)

	t = d.getWCUnitTest('Register an Inactive chart and check the alert')
	t.setup(editFett)
	t.setup(openSection, "Demographic Information")
	t.setup(changeActive)
	t.setup(closeSection, "Demographic Information")
	t.verifyElements([
		wcElement('xpath', '//div[@class="obnoxious_warning"][contains(.,"INACTIVE RECORD")]'),
	], reason='Verify that we get the INACTIVE RECORD alert on the page')
	t.test(goToSummary)

	t = d.getWCUnitTest('Register an Inactive chart and make sure it is not searchable')
	t.verifyElements([
		wcElement('xpath', '//div[@id="lv_lv_recentpats_span"]//a[contains(.,"Fett")]', exists=False),
	], reason='Verify that the inactive chart is not found when searching from E-Chart')
	t.test(searchFett)
