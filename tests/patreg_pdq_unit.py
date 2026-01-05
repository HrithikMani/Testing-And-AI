"""
@owners: pepperson
"""
from wcunittest import wcElement, wcDBRecord

def searchHeartSuccess(d, data):
	d.miedb.dbExec("UPDATE patient_partitions SET echart_opts='O' WHERE wc_partition='MR'")
	d.navigate('?f=chart&s=pat&s=search&search_method=detail&tabmodule=patsearch')
	d.enterFormData('Heart', id='last_name')
	d.enterFormData('William', id='first_name')
	d.clickElement(xpath='//input[@type="submit"][@name="pat_searchPDQ"]')
	d.waitFor(d, lambda d: d.getElement(xpath='//td[@class="pdq__results_Last_cell"]'), expected_return=True, timeout=60)

def searchHeartFailed(d, data):
	d.navigate('?f=chart&s=pat&s=search&search_method=detail&tabmodule=patsearch')
	d.enterFormData('Heart', id='last_name')
	d.enterFormData('William', id='first_name')
	d.clickElement(xpath='//input[@type="submit"][@name="pat_searchPDQ"]')
	d.waitFor(d, lambda d: d.getElement(xpath='//*[contains(.,"PDQ Query Failed")]'), expected_return=True, timeout=60)

def searchHBHart(d, data):
	d.navigate('?f=layout&module=HealthBridge&name=HIE+Search&tabmodule=admin&tabselect=HIE+Search')
	d.enterFormData('William', id='first_name')
	d.enterFormData('Hart', id='last_name')
	d.enterFormData('11-30-1954', id='start_bdate')
	d.enterFormData('1111', id='ssn')
	d.clickElement(xpath='//input[@type="button"][@value="Search HIE"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete prior to adding'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def searchHBPicasso(d, data):
	d.navigate('?f=layout&module=HealthBridge&name=HIE+Search&tabmodule=admin&tabselect=HIE+Search')
	d.enterFormData('Pablo', id='first_name')
	d.enterFormData('Picasso', id='last_name')
	d.enterFormData('01-01-2001', id='start_bdate')
	d.enterFormData('1111', id='ssn')
	d.clickElement(xpath='//input[@type="button"][@value="Search HIE"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete prior to adding'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def setupPDQFail(d, data):
# Give the user access to 'Refer to Systems'
	d.navigate('?f=admin&t=security&opp=esecuser&user_id=8&realm=')
	d.enterFormData('1', xpath='//select[@name="Control_Refer to Systems Editor"]')
	d.enterFormData('rts', id="sec_role_comment")
	d.clickElement(value="Update Individual Security")
# Change partition restrictions so that we can look at the CCHIT partition
	d.navigate('?f=admin&s=partmanager&pm_srch_type=B&pm_srch_text=cchit&pm_srch_by=A&opp=edit&partition=CCHIT')
	d.enterFormData(True, id="part_restrict")
	d.enterFormData('Physicians', id="le_pm_allowed_realms_allowed_id_value")
	d.clickElement(id="le_pm_allowed_realms_button")
	d.clickElement(xpath="//input[@type='button'][@name='change_btn']")
# Set up Refer to Systems for PDQ
	d.navigate('?f=admin&subfunc=rts_editor&page=add')
	d.enterFormData('PDQ', id="system_id")
	d.enterFormData('PDQ Test', id="system_name")
	d.enterFormData('https://{0}/webchart/test_baseline_be_careful/pdqMultiServer.cgi'.format(d.getUserData("BE_CAREFUL_HOSTNAME")), id="system_address")
	d.enterFormData(True, xpath='//td[contains(.,"Is PDQ?")]/following-sibling::td/input[@type="checkbox"][@value="128"]')
	d.clickElement(xpath='//input[@name="subBtn"]')
# Enable PDQ in the system settings
	d.navigate('?f=admin&s=system_settings&select_criteria=b&select_text=enable+pdq&select_by=all&sys_search=Go&opp=edit&module=IHE&section=PDQ&item=Enable+PDQ')
	d.enterFormData('1', name='value')
	d.enterFormData('setup_error', name='reason')
	d.clickElement(xpath="//input[@type='submit'][@name='sysset_submit']")
	d.miedb.dbExec("UPDATE translate SET trans_to='CCHIT' WHERE trans_from='1.2.840.114398.1.13.1'")
	d.miedb.dbExec("UPDATE translate SET trans_to='CCME' WHERE trans_from='1.2.840.114398.1.66.1'")
	d.miedb.dbExec("UPDATE translate SET details='' WHERE trans_from='1.2.840.114398.1.13.1'")
	d.miedb.dbExec("UPDATE translate SET details='' WHERE trans_from='1.2.840.114398.1.66.1'")
	
def setupPDQ(d, idx):
# Give the user access to 'Refer to Systems'
	d.navigate('?f=admin&t=security&opp=esecuser&user_id=8&realm=')
	d.enterFormData('1', xpath='//select[@name="Control_Refer to Systems Editor"]')
	d.enterFormData('rts', id="sec_role_comment")
	d.clickElement(value="Update Individual Security")
# Change partition restrictions so that we can look at the CCHIT partition
	d.navigate('?f=admin&s=partmanager&pm_srch_type=B&pm_srch_text=cchit&pm_srch_by=A&opp=edit&partition=CCHIT')
	d.enterFormData(True, id="part_restrict")
	d.enterFormData('Physicians', id="le_pm_allowed_realms_allowed_id_value")
	d.clickElement(id="le_pm_allowed_realms_button")
	d.clickElement(xpath="//input[@type='button'][@name='change_btn']")
# Set up Refer to Systems for PDQ
	d.navigate('?f=admin&subfunc=rts_editor&page=add')
	d.enterFormData('PDQ', id="system_id")
	d.enterFormData('PDQ Test', id="system_name")
	d.enterFormData('https://{0}/webchart/test_baseline_be_careful/pdqMultiServer.cgi'.format(d.getUserData("BE_CAREFUL_HOSTNAME")), id="system_address")
	d.enterFormData(True, xpath='//td[contains(.,"Is PDQ?")]/following-sibling::td/input[@type="checkbox"][@value="128"]')
	d.clickElement(xpath='//input[@name="subBtn"]')
# Enable PDQ in the system settings
	d.navigate('?f=admin&s=system_settings&select_criteria=b&select_text=enable+pdq&select_by=all&sys_search=Go&opp=edit&module=IHE&section=PDQ&item=Enable+PDQ')
	d.enterFormData('1', name='value')
	d.enterFormData('setup_error', name='reason')
	d.clickElement(xpath="//input[@type='submit'][@name='sysset_submit']")
# Enable PDQ for the CCME partition in the system settings
	d.navigate('?f=admin&s=system_settings&opp=add')
	d.enterFormData('REG_PARTIT', id='settings_query', blur=False)
	acchoice = d.waitFor(d, lambda d: d.getElement(id='settings_ac_span_choices_%d' %idx), expected_return=True, timeout=60)
	if not acchoice:
		d.reportCommandStatus('Timeout', '', False, '', 'Autocomplete choices not displayed')
	else:
		d.clickElement(id='settings_ac_span_choices_%d' %idx)
	d.enterFormData('CCME', name='value')
	d.enterFormData('query_success', name='reason')
	d.clickElement(xpath="//input[@type='submit'][@name='sysset_submit']")
	d.miedb.dbExec("UPDATE translate SET trans_to='CCHIT' WHERE trans_from='1.2.840.114398.1.13.1'")
	d.miedb.dbExec("UPDATE translate SET trans_to='CCME' WHERE trans_from='1.2.840.114398.1.66.1'")
	d.miedb.dbExec("UPDATE translate SET details='' WHERE trans_from='1.2.840.114398.1.13.1'")
	d.miedb.dbExec("UPDATE translate SET details='' WHERE trans_from='1.2.840.114398.1.66.1'")

def setupHBPDQ(d, data):
	# Set up Refer to Systems for HBPDQ
	d.navigate('?f=admin&subfunc=rts_editor&page=add')
	d.enterFormData('HBPDQ', id="system_id")
	d.enterFormData('HB PDQ Test', id="system_name")
	d.enterFormData('https://{0}/webchart/test_baseline_be_careful/pdqMultiServer2.cgi'.format(d.getUserData("BE_CAREFUL_HOSTNAME")), id="system_address")
	d.enterFormData(True, xpath='//td[contains(.,"Is PDQ?")]/following-sibling::td/input[@type="checkbox"][@value="128"]')
	d.clickElement(xpath='//input[@name="subBtn"]')
	# Disable NMC Partition and create a fake
	d.navigate('?f=admin&subfunc=rts_editor&page=edit&system_id=NMC_POST')
	d.enterFormData('https://{0}/webchart/test_baseline_be_careful/nmcccrpost.cgi'.format(d.getUserData("BE_CAREFUL_HOSTNAME")), id="system_address", clear=True)# "We want queries to go to a system that returns a response that LOOKS like NMC, but isn't"
	d.clickElement(xpath='//input[@name="subBtn"][@value="Update"]')
	# Create HBRIDGE partition
	d.navigate('?f=admin&s=partmanager&opp=add')
	d.enterFormData('HBRIDGE', id='partition')
	d.enterFormData('HB', id='name')
	d.enterFormData('HealthBridge', id='description')
	d.enterFormData('80', id='mr_sequence')
	d.enterFormData('Allow Edit (Optional)', id='echart_opts')
	d.clickElement(xpath='//input[@type="button"][@name="save_btn"]')
	# Make CCME partition optional
	d.navigate('?f=admin&s=partmanager&opp=edit&partition=CCME')
	d.enterFormData('Allow Edit (Optional)', id='echart_opts')
	d.clickElement(xpath='//input[@type="button"][@name="change_btn"]')
	# Make a tab to access HIE Search
	d.navigate('?f=admin&t=menueditor&opp=add')
	d.enterFormData('admin', id='module')
	d.enterFormData('HIE Search', id='name')
	d.enterFormData('?f=layout&module=HealthBridge&name=HIE+Search', id='url')
	d.enterFormData(True, id='show_in_wc')
	d.clickElement(id='save')
	
def clickPDQQuery(d, data):
	d.clickElement(xpath='//input[@name="pat_searchPDQ"]')

def registerPDQHeart(d, data):
	rslts = d.waitFor(d, lambda d: d.getElement(xpath='//td[contains(.,"Heart, William")]/preceding-sibling::td[contains(@class, "pdq__results_MR")]/a'), expected_return=True, timeout=30)
	if not rslts:
		d.reportCommandStatus('Timeout', '', False, '', 'Results not present')
	else:
		d.clickElement(xpath='//td[contains(.,"Heart, William")]/preceding-sibling::td[contains(@class, "pdq__results_MR")]/a')

def clickSave(d, data):
	d.clickElement(xpath='//input[@value="Save"]')
	d.waitFor(d, lambda d: d.getElement(xpath='//span[@id="wc_pat_bar_mrns"][contains(.,"MR-")]/following-sibling::span[contains(.,"William, Heart")]'), expected_return=True, timeout=60)

def assignMR(d, data):
	d.enterFormData('98989898', xpath="//td[contains(.,'Manual Assigned Optional')]/following-sibling::td/input[@name='EDITMR_mrnumber_MR']")

def forceTranslation(d, data):
	d.navigate('?f=admin&s=system_settings&select_criteria=b&select_text=REG_PARTITION&select_by=all&sys_search=Go&opp=edit&module=IHE&section=PDQ&item=REG_PARTITION')
	d.enterFormData('0', name='value', clear=True)
	d.enterFormData('force translation', name='reason')
	d.clickElement(xpath="//input[@type='submit'][@name='sysset_submit']")
	d.navigate('?f=admin&subfunc=rts_editor&page=edit&system_id=PDQ')
	d.enterFormData('https://{0}/webchart/test_baseline_be_careful/pdqMultiServer2.cgi'.format(d.getUserData("BE_CAREFUL_HOSTNAME")), id="system_address", clear=True)
	d.clickElement(xpath='//input[@name="subBtn"][@value="Update"]')
# Create translations to CCME and CCHIT/TEST
	d.navigate('?f=admin&t=translate&search_namecat=ISO-partition&search_criteria=exact&search_text=1.2.840.114398.1.66.1&search_by=trans_from&trans_search=Search&opp=edit&name=ISO-partition&trans_from=1.2.840.114398.1.66.1')
	d.enterFormData('CCME', id='trans_to', clear=True)
	d.clickElement(xpath='//input[@name="addEditTrans"][@value="Edit"]')
	d.navigate('?f=admin&t=translate&search_namecat=ISO-partition&search_criteria=exact&search_text=1.2.840.114398.1.13.1&search_by=trans_from&trans_search=Search&opp=edit&name=ISO-partition&trans_from=1.2.840.114398.1.13.1')
	d.enterFormData('TEST', id='trans_to', clear=True)
	d.clickElement(xpath='//input[@name="addEditTrans"][@value="Edit"]')



def main(d, WCURL):
	t = d.getWCUnitTest('Verify Failed PDQ Search')
	d.wcErrorLog.ignore("*New partition system: (ISO) partition: (1.2.840.114398.1.13.1)*")
	d.wcErrorLog.ignore("*New partition system: (ISO) partition: (1.2.840.114398.1.66.1)*")
	t.setup(setupPDQFail)
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"PDQ Query Failed")]')
	], reason='Verify PDQ Query Failed message')
	t.test(searchHeartFailed)

	t = d.getWCUnitTest('Verify Successful PDQ Search')
	t.setup(setupPDQ, 0)
	t.verifyElements([
		wcElement('xpath', '//td[@class="pdq__results_Last_cell"][contains(.,"Heart, William")]')
	], reason='Verify PDQ Query Success')
	t.test(searchHeartSuccess)

	t = d.getWCUnitTest('Register William Heart from the PDQ Query results and reach Demographics entry page')
	t.setup(searchHeartSuccess)
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Demographic Information")]'),
		wcElement('xpath', '//td[contains(.,"Auto Assigned Optional")]/following-sibling::td/input[@name="EDITMR_mrnumber_MIE"]'),
		wcElement('xpath', '//td[contains(.,"Manual Assigned Optional")]/following-sibling::td/input[@name="EDITMR_mrnumber_MR"]')
	], reason='Verify we get the edit Demographics page to register William Heart and the option to Auto Assign an MR is present')
	t.test(registerPDQHeart)

	t = d.getWCUnitTest('Trigger the MR Number alert')
	t.setup(searchHeartSuccess)
	t.setup(registerPDQHeart)
	t.verifyElements([
		wcElement('xpath', '//div[@id="mieAlert"]/div[@class="wc_win"]//div[@class="wc_win_title"][contains(.,"Warning")]/parent::div/following-sibling::div//div[contains(.,"Please select a MR Number")]/div/input[@id="ok_btn"]')
	], reason='Verify we get the "Please select a MR Number" alert')
	t.test(clickSave)

	t = d.getWCUnitTest('Complete registration of William Heart with an MR')
	t.setup(searchHeartSuccess)
	t.setup(registerPDQHeart)
	t.setup(assignMR)
	t.verifyElements([
		wcElement('xpath', '//span[@id="wc_pat_bar_mrns"][contains(.,"MR-")]/following-sibling::span[contains(.,"William, Heart")]')
	], reason='Verify William Heart has an active chart with MR number')
	t.test(clickSave)

	t = d.getWCUnitTest('Create new translations and perform a PDQ search to verify the translations')
	t.setup(forceTranslation)
	t.verifyElements([
		wcElement('xpath', '//td[contains(@class,"pdq__results_")][contains(.,"Heart, William, R")]/preceding-sibling::td[contains(@class,"pdq__results_")]/a[contains(.,"ccMe")]'),
		wcElement('xpath', '//td[contains(@class,"pdq__results_")][contains(.,"Heart, William, R")]/preceding-sibling::td[contains(@class,"pdq__results_")]/a[contains(.,"TEST")]')
	], reason='Verify the ccMe and TEST partitions are present')
	t.test(searchHeartSuccess)

	t = d.getWCUnitTest('Health Bridge PDQ local search')
	t.setup(setupHBPDQ)
	t.verifyElements([
		wcElement('xpath', '//div[@id="search_results"]/fieldset/legend[contains(.,"Local Results")]'),
		wcElement('xpath', '//td[contains(.,"Hart")]/preceding-sibling::td/a/span[contains(.,"TEST-")]')
	], reason='')
	t.test(searchHBHart)

	t = d.getWCUnitTest('Health Bridge PDQ remote search')
	t.setup(searchHBPicasso)
	t.verifyElements([
		wcElement('xpath', '//div[@id="search_results"]/fieldset/legend[contains(.,"Remote Results")]'),
		wcElement('xpath', '//td[contains(.,"Heart")]/preceding-sibling::td/span/span[contains(.,"CCME-")]'),
		wcElement('xpath', '//td[contains(.,"Heart")]/preceding-sibling::td/span/span[contains(.,"TEST-")]')
	], reason='')
	t.test()
