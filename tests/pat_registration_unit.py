"""
@owners: nwallace aris 
"""
from wcunittest import wcElement, wcDBRecord

def skipUnit(d, data):
	d.reportCommandStatus('Unit Skipped', '', True, '', 'This unit is being skipped and will not be tested')

def navRegistration(d, data):
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		d.navigate('?f=layout&module=MASTER&name=CommonRegistrationPage&chart_type_value=Patient&relation_type_value=Employee&use_pat_id=-1&tabmodule=patsearch&tabmodule=patsearch&tabselect=Patient+Registration')
	elif systyp == 'WCNOW':
		d.navigate('?f=chart&s=pat&opp=add&tabmodule=patsearch&tabselect=Patient+Registration')

def clickAddorSearch(d, data):
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		d.clickElement(id='AddNew')
	elif systyp == 'WCNOW':
		d.clickElement(xpath='//input[@name="check_dup"][@value="Search"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def registerHart(d, data):
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		d.enterFormData('Hart', id='last_name')
		d.enterFormData('William', id='first_name', blur=True)
		d.enterFormData('30', id='birth_dateDAY', blur=True)
		d.enterFormData('11', id='birth_dateMONTH', blur=True)
		d.enterFormData('1954', id='birth_dateYEAR', blur=True)
	if systyp == 'WCNOW':
		d.enterFormData('Hart', id='patient_last_name')
		d.enterFormData('William', id='patient_first_name', blur=True)
		d.enterFormData('30', id='patient_birth_dateDAY', blur=True)
		d.enterFormData('11', id='patient_birth_dateMONTH', blur=True)
		d.enterFormData('1954', id='patient_birth_dateYEAR', blur=True)

def registerHartLNFN(d, data):
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		d.enterFormData('Hart', id='last_name')
		d.enterFormData('William', id='first_name', blur=True)
	if systyp == 'WCNOW':
		d.enterFormData('Hart', id='patient_last_name')
		d.enterFormData('William', id='patient_first_name', blur=True)
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)


def searchFett(d, data):
	d.navigate('?f=chart')
	d.enterFormData('Fett', xpath='//input[@name="sstring"]')
	d.clickElement(xpath='//input[@name="pat_search"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def registerFett(d, idx):
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		d.navigate('?f=layout&module=MASTER&name=CommonRegistrationPage&chart_type_value=Patient&relation_type_value=Employee&use_pat_id=-1&tabmodule=patsearch&tabmodule=patsearch&tabselect=Patient+Registration')
		d.waitFor(d, lambda d: d.getElement(xpath='//legend[@class="dlgtitle"]/span[contains(., "Enter Information")]'))
		d.enterFormData('Fett', id='last_name')
		d.enterFormData('Boba', id='first_name')
		d.enterFormData('03', id='birth_dateMONTH')
		d.enterFormData('03', id='birth_dateDAY')
		d.enterFormData('1981', id='birth_dateYEAR')
		d.enterFormData('bfett@bettercorp.com', id='email')
		d.enterFormData('Better Corp', id='eo_pat_id_patac_input', blur=False)
		acchoice = d.waitFor(d, lambda d: d.getElement(id='eo_pat_id_patac_span_choices_%d' %idx), timeout=60)
		if not acchoice:
			d.reportCommandStatus('Timeout', '', False, '', 'Autocomplete choices not displayed')
		else:
			d.clickElement(id='eo_pat_id_patac_span_choices_%d' %idx)
		d.wcutils.waitForAJAX(timeout=90, quiet=20)
		d.clickElement(id='AddNew')
		d.waitFor(d, lambda d: d.getElement(xpath='//h2[@class="exam_tab"][contains(., "Demographic Information")]'))
	elif systyp == 'WCNOW':
		d.navigate('?f=chart&s=pat&opp=add&tabmodule=patsearch&tabselect=Patient+Registration')
		d.waitFor(d, lambda d: d.getElement(xpath='//legend[@class="dlgtitle"]/span[contains(., "Enter Information")]'))
		d.enterFormData('Fett', id='patient_last_name')
		d.enterFormData('Boba', id='patient_first_name')
		d.enterFormData('03', id='patient_birth_dateMONTH')
		d.enterFormData('03', id='patient_birth_dateDAY')
		d.enterFormData('1981', id='patient_birth_dateYEAR')
		d.clickElement(xpath='//input[@name="check_dup"][@value="Search"]')
		d.waitFor(d, lambda d: d.getElement(xpath='//legend[@class="dlgtitle"]/span[contains(., "Demographic Information")]'))
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def dupMsg(d, data):
	dup = d.waitFor(d, lambda d: d.getElement(xpath='//span[contains(.,"DUPLICATE")]'), timeout=120)
	if not dup:
		d.wcutils.waitForAJAX(timeout=90, quiet=20)
		d.reportCommandStatus('dupMsg', '', False, '', 'Inline alert not present')

def clickSave(d, data):
	sb = d.waitFor(d, lambda d: d.getElement(xpath='//input[@value="Save"]'), timeout=60)
	if not sb:
		d.reportCommandStatus('clickSave', '', False, '', 'Save button not present')
	else:
		d.clickElement(xpath='//input[@value="Save"]')

def reqPartMR(d, data):
	d.miedb.dbExec("UPDATE patient_partitions SET echart_opts='O' WHERE wc_partition='MIE'")
	d.miedb.dbExec("UPDATE patient_partitions SET echart_opts='R' WHERE wc_partition='MR'")

def enterMR(d, data):
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		d.clickElement(xpath="//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='Employee Numbers']")
	mrchkd = d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MR" and @type="hidden" and not(@unchecked)]'), timeout=60)
	mrtxt = d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MR" and @type="text" and not(@type="hidden")]'), timeout=60)
	if mrchkd:
		d.reportCommandStatus('enterMR', '', True, '', 'MR to be assigned is checked')
	elif mrtxt:
		d.enterFormData('98989898989', xpath='//input[@name="EDITMR_mrnumber_MR" and not(@type="hidden")]')
	else:
		d.reportCommandStatus('enterMR', '', False, '', 'MR input not found')
	if systyp == 'EH':
		d.clickElement(xpath='//*[contains(@class, "exam_tab") and contains(text(), "Employee Numbers")]/parent::div//button[contains(@class, "save") and @type="button" or contains(., "save")]')
	elif systyp == 'WCNOW':
		d.clickElement(xpath='//input[@value="Save"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def enterDupMRPat(d, idx):
	systyp = d.getUserData('systemType')
	d.navigate('?f=chart&s=pat&opp=add&tabmodule=patsearch&tabselect=Patient+Registration')
	d.waitFor(d, lambda d: d.getElement(xpath='//legend[@class="dlgtitle"]/span[contains(., "Enter Information")]'))
	d.enterFormData('Mereel', id='patient_last_name')
	d.enterFormData('Jaster', id='patient_first_name')
	d.enterFormData('05', id='patient_birth_dateMONTH')
	d.enterFormData('05', id='patient_birth_dateDAY')
	d.enterFormData('1975', id='patient_birth_dateYEAR')
	d.clickElement(xpath='//input[@name="check_dup"][@value="Search"]')
	if systyp == 'EH':
		d.waitFor(d, lambda d: d.getElement(xpath='//h2[@class="exam_tab"][contains(., "Employee Numbers")]'))
	elif systyp == 'WCNOW':
		d.waitFor(d, lambda d: d.getElement(xpath='//legend[@class="dlgtitle"]/span[contains(., "Demographic Information")]'))
	mrchkd = d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MR" and @type="hidden" and not(@unchecked)]'), timeout=60)
	mrtxt = d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MR" and @type="text" and not(@type="hidden")]'), timeout=60)
	if mrchkd:
		d.reportCommandStatus('enterMR', '', True, '', 'MR to be assigned is checked')
	elif mrtxt:
		d.enterFormData('98989898989', xpath='//input[@name="EDITMR_mrnumber_MR" and not(@type="hidden")]')
	else:
		d.reportCommandStatus('enterMR', '', False, '', 'MR input not found')
	d.wcutils.waitFor(lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MR"]/following-sibling::span[@style="color: red;" and contains(.,"In Use")]'), timeout=90)
	if systyp == 'EH':
		d.clickElement(xpath='//*[contains(@class, "exam_tab") and contains(text(), "Employee Numbers")]/parent::div//button[contains(@class, "save") and @type="button" or contains(., "save")]')
	elif systyp == 'WCNOW':
		d.clickElement(xpath='//input[@value="Save"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def mieMR2(d, data):
	systyp = d.getUserData('systemType')
	mrfld = d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MIE"]'), timeout=60)
	mrtxt = d.waitFor(d, lambda d: d.getElement(xpath='//input[@name="EDITMR_mrnumber_MIE"][@type="text"]'), timeout=60)
	mrchkbx = d.waitFor(d, lambda d: d.getElement(xpath='//input[@id="EDITMR_mrnumber_MIE_use"][@type="checkbox"]'), timeout=60)
	if not mrfld:
		d.reportCommandStatus('mieMR2', '', False, '', 'Page not loaded')
	if mrchkbx:
		d.enterFormData(True, id="EDITMR_mrnumber_MIE_use")
	elif mrtxt:
		d.enterFormData('12121212121', xpath='//input[@name="EDITMR_mrnumber_MIE"]')
	if systyp == 'EH':
		d.clickElement(xpath='//*[contains(@class, "exam_tab") and contains(text(), "Employee Numbers")]/parent::div//button[contains(@class, "save") and @type="button" or contains(., "save")]')
	elif systyp == 'WCNOW':
		d.clickElement(xpath='//input[@value="Save"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def continueLink(d, data):
	d.waitFor(d, lambda d: d.getElement(xpath='//a//strong[contains(.,"To continue adding the Patient")]'), timeout=60)
	d.clickElement(xpath='//a//strong[contains(.,"To continue adding the Patient")]')

def clearDB(d, data):
	d.miedb.dbExec("DELETE FROM patient_mrns WHERE pat_id NOT IN(SELECT pat_id FROM patients WHERE last_name='Better Corp.')")
	d.miedb.dbExec("DELETE FROM patient_mrns WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM pat_pat_relflat WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM pat_pat_relations WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM charts WHERE chart_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM recent_patients WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM observations WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM patient_extended_values WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("DELETE FROM patients WHERE last_name='Fett'")
	d.miedb.dbExec("DELETE FROM recent_patients WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett')")
	d.miedb.dbExec("UPDATE patient_partitions SET mr_sequence=mr_sequence - 1 WHERE wc_partition='MIE'")
	d.miedb.dbExec("UPDATE patient_partitions SET mr_sequence=mr_sequence - 1 WHERE wc_partition='MR'")

def clearDB2(d, data):
	d.miedb.dbExec("DELETE FROM patient_mrns WHERE pat_id NOT IN(SELECT pat_id FROM patients WHERE last_name='Better Corp.')")
	d.miedb.dbExec("DELETE FROM patient_mrns WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM patient_mrns WHERE pat_id=(SELECT pat_id FROM patients WHERE last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM pat_pat_relflat WHERE pat_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM pat_pat_relflat WHERE pat_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM pat_pat_relations WHERE pat_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM pat_pat_relations WHERE pat_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM pat_chart_types WHERE pat_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM charts WHERE chart_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("DELETE FROM charts WHERE chart_id=(SELECT pat_id FROM patients Where last_name='Fett' LIMIT 1)")
	d.miedb.dbExec("UPDATE patient_partitions SET mr_sequence=mr_sequence - 1 WHERE wc_partition='MIE'")
	d.miedb.dbExec("UPDATE patient_partitions SET mr_sequence=mr_sequence - 1 WHERE wc_partition='MIE'")
	d.miedb.dbExec("UPDATE patient_partitions SET mr_sequence=mr_sequence - 1 WHERE wc_partition='MR'")
	d.miedb.dbExec("UPDATE patient_partitions SET mr_sequence=mr_sequence - 1 WHERE wc_partition='MR'")
	d.miedb.dbExec("DELETE FROM patients WHERE last_name='Fett'")

def changeTempEH(d, data):
	d.wcutils.waitForAJAX(timeout=90, quiet=20)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(., "mask")]'), expected_return=False, timeout=90)
	d.clickElement(xpath="//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='Demographic Information']")
	if not d.waitFor(d, lambda d: d.getElement(xpath='//h2[@class="exam_tab"][contains(., "Demographic Information")]')):
		d.reportCommandStatus('', '', False, '', 'Test is not on the Edit Demographics page')
	else:
		d.clickElement(xpath="//*[self::h2 or self::h3][contains(@class, 'exam_tab') and text()='Demographic Information']")
		tmpch = d.waitFor(d, lambda d: d.getElement(xpath='//input[@id="DPI_is_tmp_1"]'), timeout=60)
		if not tmpch:
			d.reportCommandStatus('Timeout', '', False, '', 'Temporary Chart checkbox not present')
		else:
			d.clickElement(xpath='//input[@id="DPI_is_tmp_1" and @type="radio"]')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)

def changeTempWC(d, data):
	d.wcutils.waitForAJAX(timeout=90, quiet=20)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(., "mask")]'), expected_return=False, timeout=90)
	tmpch = d.waitFor(d, lambda d: d.getElement(xpath='//input[@id="DPCB_is_tmp"]'), timeout=60)
	if not d.waitFor(d, lambda d: d.getElement(xpath='//legend[@class="dlgtitle"]/span[contains(., "Demographic Information")]')):
		d.reportCommandStatus('', '', False, '', 'Test is not on the Edit Demographics page')
	if not tmpch:
		d.reportCommandStatus('Timeout', '', False, '', 'Temporary Chart checkbox not present')
	else:
		d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//input[contains(@id, "_is_tmp")]'))
		d.enterFormData(True, id='DPCB_is_tmp')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=90, comments='Wait for ajax and layoutInsert operations to complete'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))
	d.wcutils.waitForAJAX(timeout=90, quiet=20)


def main(d, WCURL):
	t = d.getWCUnitTest('Missing last name, first name, birth date, EO warning')
	t.setup(navRegistration)
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.verifyElements([
			wcElement('xpath', '//strong[contains(., "Enter required fields and/or address issues")]')
		])
	else:
		t.verifyElements([
			wcElement('xpath', '//input[@id="DPI_first_name"]')
		])
	t.test(clickAddorSearch)

	t = d.getWCUnitTest('Matching Chart alert(s)')
	t.setup(navRegistration)
	t.setup(registerHartLNFN)
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.verifyElements([
			wcElement('xpath', '//tr[@id="existing_charts"][@style=""]/td[@class="alert"][contains(.,"Matching Charts")]'),
			wcElement('xpath', '//tr[@id="other_charts"][@style=""]/td[@class="field"][contains(.,"All Matching Charts")]'),
			wcElement('xpath', '//tr[@id="existing_charts"]/td/p[@id="existing_charts_message"]/div/a[contains(.,"Hart, William S. (TEST-10019)")]'),
			wcElement('xpath', '//tr[@id="existing_charts"]/td/p[@id="existing_charts_message"]/div/a[contains(.,"Hart, William (HOSPITAL-495653)")]'),
			wcElement('xpath', '//tr[@id="other_charts"]/td/p[@id="other_charts_message"]/div/a[contains(.,"Hart, William S. (TEST-10019)")]'),
			wcElement('xpath', '//tr[@id="other_charts"]/td/p[@id="other_charts_message"]/div/a[contains(.,"Hart, William (HOSPITAL-495653)")]'),
		])
	else:
		t.setup(clickAddorSearch)
		t.verifyElements([
			wcElement('xpath', '//div[@id="wc_body_container"]//table//font/strong[contains(.,"The Following Patient(s) Matched some/all of the criteria.")]'),
			wcElement('xpath', '//div[@id="wc_body_container"]//table//font/strong[contains(.,"To edit the Patient, click on the MR number.")]'),
			wcElement('xpath', '//div[@id="wc_body_container"]//table//a/font/strong[contains(.,"To continue adding the Patient (Hart, William), click here")]'),
			wcElement('xpath', '//table[@id="lv_root_Matching_20Patients"]//span[@id="lv_ecpatients_span_title"][contains(.,"Matching Patients")]'),
			wcElement('xpath', '//div[@id="lv_ecpatients_span"]//td[@class="ecpatients_Last_cell"][contains(.,"Hart, William")]'),
		])
	t.test()

	t = d.getWCUnitTest('Register a Duplicate chart')
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.setup(registerFett, 0)
		t.setup(registerFett, 0)
		t.verifyElements([
			wcElement('xpath', '//div[@id="wc_pat_bar"]//span[contains(.,"DUPLICATE")]'),
		], reason='Verify that we get the DUPLICATE alert after registering the patient twice and not linking the chart')
	else:
		t.setup(registerFett, 0)
		t.setup(enterMR)
		t.setup(registerFett, 0)
		t.setup(continueLink)
		t.setup(mieMR2)
		t.verifyElements([
			wcElement('xpath', '//div[@id="wc_pat_bar"]//span[contains(.,"DUPLICATE")]'),
		], reason='Verify that we get the DUPLICATE alert after registering the patient twice and not linking the chart')
	t.teardown(clearDB2)
	t.test(dupMsg)

	t = d.getWCUnitTest('Attempt to register a patient chart without MR')
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.setup(registerFett, 0)
		t.setup(searchFett)
		t.verifyElements([
			wcElement('xpath', '//a[contains(.,"No Part-MR!")]', exists=False),
		], reason='Make sure that the patient chart was created and shown in E-Chart\'s patient search and does not have a "No Part-MR"')
		t.verifyDB(wcDBRecord("FROM patients WHERE last_name='Fett'", {'first_name': 'Boba'}))
	else:
		t.setup(reqPartMR)
		t.setup(registerFett, 0)
		t.setup(clickSave)
		t.verifyElements([
			wcElement('xpath', '//div[@class="wc_win"]//div[contains(.,"Please select a MR Number")]')
		], reason='Make sure user is prompted with the alert that an MR# must be entered')
	t.teardown(clearDB)
	t.test()

	t = d.getWCUnitTest('Register a patient chart with an MR Number')
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.setup(registerFett, 0)
		t.verifyElements([
			wcElement('xpath', '//*[contains(.,"No Part-MR")]', exists=False),
			wcElement('xpath', '//span[@id="wc_pat_bar_mrns"][contains(.,"TEST-")]'),
		], reason='Verify the chosen MR Number was assigned and the patient was not assigned a No Part-MR', timeout=5)
		t.verifyElements([
			wcElement('xpath', '//td/a[contains(.,"Fett")]/ancestor::div//div[@class="obnoxious_warning"][contains(.,"INACTIVE RECORD")]', exists=False),
			wcElement('xpath', '//td/a[contains(.,"Fett")]/ancestor::div//div[@class="obnoxious_warning"]', exists=False),
		], reason='Verify the patient\'s chart is not flagged as Inactive or Temporary')
	else:
		t.setup(reqPartMR)
		t.setup(registerFett, 0)
		t.setup(enterMR)
		t.verifyElements([
			wcElement('xpath', '//*[contains(.,"No Part-MR")]', exists=False),
			wcElement('xpath', '//span[@id="wc_pat_bar_mrns"][contains(.,"MR-")]'),
		], reason='Verify the chosen MR Number was assigned and the patient was not assigned a No Part-MR')
		t.verifyElements([
			wcElement('xpath', '//td/a[contains(.,"Fett")]/ancestor::div//div[@class="obnoxious_warning"][contains(.,"INACTIVE RECORD")]', exists=False),
			wcElement('xpath', '//td/a[contains(.,"Fett")]/ancestor::div//div[@class="obnoxious_warning"]', exists=False),
		], reason='Verify the patient\'s chart is not flagged as Inactive or Temporary')
	t.teardown(clearDB2)
	t.test()

	t = d.getWCUnitTest('Attempt to Register with a Duplicate MR#')
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.setup(skipUnit)
	else:
		t.setup(reqPartMR)
		t.setup(registerFett, 0)
		t.setup(enterMR)
		t.setup(enterDupMRPat, 0)
		t.verifyElements([
			wcElement('xpath', '//div[@class="wc_win_title"][contains(.,"Warning")]'),
			wcElement('xpath', '//div[contains(@class,"wc_win_body")][contains(.,"Partition: MR (Medical Record Number) and Record #: 98989898989 already exist")]'),
		], reason='Verify that we get the alert that the MR# is already in use')
	t.teardown(clearDB2)
	t.test()

	t = d.getWCUnitTest('Register a Temporary chart')
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.setup(registerFett, 0)
		t.setup(changeTempEH)
		t.teardown(clearDB)
		t.test(enterMR)
	else:
		t.setup(registerFett, 0)
		t.setup(changeTempWC)
		t.verifyElements([
			wcElement('xpath', '//div[@class="obnoxious_warning"][contains(.,"TEMPORARY RECORD")]'),
		], reason='Verify that we get the TEMPORARY RECORD alert on the page')
		t.teardown(clearDB)
		t.test(enterMR)
		
