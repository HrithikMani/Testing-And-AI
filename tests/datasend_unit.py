"""
@owners: pepperson
"""
from wcunittest import wcElement, wcDBRecord

def clearRoutes(d, data):
	d.miedb.dbExec('TRUNCATE datasend_route')

def routeDoc(d, idx):
	d.navigate('?f=chart&s=print&doc_id=488&print_send_method=4')
	d.waitFor(d, lambda d: d.getElement(id='user_ac_txt'), expected_return=True, timeout=30)
	d.enterFormData('Selenium', id="user_ac_txt", blur=False)
	acchoice = d.waitFor(d, lambda d: d.getElement(id='user_ac_span_choices_%d' %idx), expected_return=True, timeout=30)
	if not acchoice:
		d.reportCommandStatus('Timeout', '', False, '', 'Autocomplete choices not displayed')
	else:
		d.clickElement(id='user_ac_span_choices_%d' %idx)

def addRoute(d, data):
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')

def printMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Print")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Print"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()=" Fort Wayne IN 46804"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def faxMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Fax")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Fax"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def hl7NMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "HL7 Send")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_HL7 Send_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="HL7 Send"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def hl7MEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "HL7 Send")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_HL7 Send_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="HL7 Send"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def hl7CDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "HL7 Send")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_HL7 Send_input"]/option[contains(., "CDC")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="HL7 Send"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def txtExpMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Text Export")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Text Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def dictaphoneNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Dictaphone HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Dictaphone HL7_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Dictaphone HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def dictaphoneMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Dictaphone HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Dictaphone HL7_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Dictaphone HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def dictaphoneCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Dictaphone HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Dictaphone HL7_input"]/option[contains(., "CDC")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Dictaphone HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def nmcMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "NMC - Cannot send (per physician)")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC - Cannot send (per physician)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def nmcMedAccMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "NMC - MedAccess")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC - MedAccess"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffSSMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "SS Eligibility")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="SS_ELIG"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffPOSTMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "NMC_POST")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_POST"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffPUBMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "MIEPub Server API")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MIEPUB_API"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffDMONMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "MIE Daemon Monitor")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="DMON"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffCOMMMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "MIE Commerce")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MIECOMMERCE"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def word2TiffCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Word2TIFF FTP")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Word2TIFF FTP_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Word2TIFF FTP"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def orderNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "ORDER RESULTS HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_ORDER RESULTS HL7_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="ORDER RESULTS HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def orderMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "ORDER RESULTS HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_ORDER RESULTS HL7_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="ORDER RESULTS HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def orderCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "ORDER RESULTS HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_ORDER RESULTS HL7_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="ORDER RESULTS HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def oshaNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "OSHA")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_OSHA_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="OSHA"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def oshaMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "OSHA")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_OSHA_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="OSHA"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def oshaCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "OSHA")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_OSHA_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="OSHA"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def wrkcompNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Work Comp")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Work Comp_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Work Comp"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def wrkcompMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Work Comp")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Work Comp_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Work Comp"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def wrkcompCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Work Comp")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Work Comp_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Work Comp"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def incidentSSMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Incident")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Incident_input"]/option[contains(., "SS Eligibility")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Incident"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="SS_ELIG"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def incidentPUBMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Incident")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Incident_input"]/option[contains(., "MIEPub Server API")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Incident"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MIEPUB_API"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def incidentDMONMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Incident")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Incident_input"]/option[contains(., "MIE Daemon Monitor")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Incident"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="DMON"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def incidentCOMMMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Incident")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Incident_input"]/option[contains(., "MIE Commerce")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Incident"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MIECOMMERCE"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def wcPostMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Webchart Post")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Webchart Post"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def esignMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Esign Request")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Esign Request"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def remIFQMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Remote IFQ Batch")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Remote IFQ Batch"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_POST"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def scrptExpSSMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Scripted Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Scripted Export_input"]/option[contains(., "SS Eligibility")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Scripted Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="SS_ELIG"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def scrptExpPUBMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Scripted Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Scripted Export_input"]/option[contains(., "MIEPub Server API")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Scripted Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MIEPUB_API"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def scrptExpDMONMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Scripted Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Scripted Export_input"]/option[contains(., "MIE Daemon Monitor")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Scripted Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="DMON"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def scrptExpCOMMMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Scripted Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Scripted Export_input"]/option[contains(., "MIE Commerce")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Scripted Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MIECOMMERCE"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def mdmNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "MDM Reports HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_MDM Reports HL7_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MDM Reports HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def mdmMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "MDM Reports HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_MDM Reports HL7_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MDM Reports HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def mdmCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "MDM Reports HL7")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_MDM Reports HL7_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MDM Reports HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def immunNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Immunization Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Immunization Export_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Immunization Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def immunMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Immunization Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Immunization Export_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Immunization Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def immunCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Immunization Export")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Immunization Export_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Immunization Export"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def kareoNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Kareo Billing")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Kareo Billing_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Kareo Billing"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def kareoMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Kareo Billing")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Kareo Billing_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Kareo Billing"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def kareoCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Kareo Billing")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Kareo Billing_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Kareo Billing"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def directMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Direct Email")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Direct Email"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def synSurvNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Syndromic Surveillance")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Syndromic Surveillance_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Syndromic Surveillance"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def synSurvMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Syndromic Surveillance")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Syndromic Surveillance_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Syndromic Surveillance"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def synSurvCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "Syndromic Surveillance")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_Syndromic Surveillance_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Syndromic Surveillance"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def profClaimNMCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "837 Professional Claims")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_837 Professional Claims_input"]/option[contains(., "NMC_HL7")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="837 Professional Claims"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="NMC_HL7"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def profClaimMEDMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "837 Professional Claims")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_837 Professional Claims_input"]/option[contains(., "Medisys")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="837 Professional Claims"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="MEDISYS"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def profClaimCDCMethod(d, data):
	d.clickElement(xpath='//select[@id="le_datasendroute_method_value"]/option[contains(., "837 Professional Claims")]')
	d.clickElement(xpath='//select[@id="le_datasendroute_method_detail_value_837 Professional Claims_input"]/option[contains(., "CDC Reporting")]')
	d.clickElement(xpath='//input[@id="le_datasendroute_button"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="Selenium, Selenium ( Fort Wayne, IN United States 46804)"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="837 Professional Claims"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="CDC"]')
	d.verifyElementPresent(xpath='//td[@id="le_datasendroute_display"]//font[text()="All Revisions"]')
	d.clickElement(xpath='//input[@value="Update & Close"]')

def checkDocProp(d, data):
	d.navigate('?f=chart&s=doc&doc_id=488&opp=properties')

def main(d, WCURL):
	t = d.getWCUnitTest ('Alert')
	t.setup(routeDoc, 0)
	t.verifyElements([
		wcElement('xpath', '//div[@class="wc_win"]//div[contains(@class, "wc_win_body")]/div[contains(.,"The field \'Method\' is required.")]'),
	], reason='Verify we get an alert when no method is selected.')
	t.test(addRoute)

	d.startSection('DataSend Methods')

	t = d.getWCUnitTest ('Print Method')
	t.setup(clearRoutes)
	t.setup(routeDoc, 0)
	t.setup(printMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Print")]'),
	], reason='Verify the Print method DataSend route was created and is shown in the UI')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 1,
					 'method_detail': ' Fort Wayne IN 46804',
					 'status': 'W',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Print method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Fax Method')
	t.setup(routeDoc, 0)
	t.setup(faxMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Fax")]'),
	], reason='Fax DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 2,
					 'method_detail': '',
					 'status': 'W',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Fax method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.startSection('HL7 Send Methods')

	t = d.getWCUnitTest ('HL7 Send Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(hl7NMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"HL7 Send")]'),
	], reason='HL7 Send DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 4,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the HL7 Send method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('HL7 Send Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(hl7MEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"HL7 Send")]'),
	], reason='HL7 Send DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 4,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the HL7 Send method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('HL7 Send Method - CDC Method Detail')
	t.setup(routeDoc, 0)
	t.setup(hl7CDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"HL7 Send")]'),
	], reason='HL7 Send DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 4,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the HL7 Send method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()

	t = d.getWCUnitTest ('Text Export Method')
	t.setup(routeDoc, 0)
	t.setup(txtExpMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Text Export")]'),
	], reason='Text Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 6,
					 'method_detail': '',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Text Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.startSection('Dictaphone HL7 Send Methods')

	t = d.getWCUnitTest ('Dictaphone HL7 Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(dictaphoneNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Dictaphone HL7")]'),
	], reason='Dictaphone HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 9,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Dictaphone HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Dictaphone HL7 Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(dictaphoneMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Dictaphone HL7")]'),
	], reason='Dictaphone HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 9,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Dictaphone HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Dictaphone HL7 Method - CDC Method Detail')
	t.setup(routeDoc, 0)
	t.setup(dictaphoneCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Dictaphone HL7")]'),
	], reason='Dictaphone HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 9,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Dictaphone HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()

	t = d.getWCUnitTest ('NMC - Cannot send (per physician) Method')
	t.setup(routeDoc, 0)
	t.setup(nmcMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"NMC - Cannot send (per physician)")]'),
	], reason='NMC - Cannot send (per physician) DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 11,
					 'method_detail': '',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the NMC - Cannot send (per physician) method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('NMC - MedAccess Method')
	t.setup(routeDoc, 0)
	t.setup(nmcMedAccMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"NMC - MedAccess")]'),
	], reason='NMC - MedAccess DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 10,
					 'method_detail': '',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the NMC - MedAccess method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.startSection('Word2TIFF FTP Methods')

	t = d.getWCUnitTest ('Word2TIFF FTP Method - SS Eligibility Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffSSMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'SS_ELIG',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - NMC_POST Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffPOSTMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'NMC_POST',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - MIEPub Server API Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffPUBMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'MIEPUB_API',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - MIE Daemon Monitor Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffDMONMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'DMON',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - MIE Commerce Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffCOMMMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'MIECOMMERCE',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Word2TIFF FTP Method - CDC Method Detail')
	t.setup(routeDoc, 0)
	t.setup(word2TiffCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Word2TIFF FTP")]'),
	], reason='Word2TIFF FTP DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 12,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Word2TIFF FTP method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('ORDER RESULTS HL7 Methods')

	t = d.getWCUnitTest ('ORDER RESULTS HL7 Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(orderNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"ORDER RESULTS HL7")]'),
	], reason='ORDER RESULTS HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 13,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the ORDER RESULTS HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('ORDER RESULTS HL7 Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(orderMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"ORDER RESULTS HL7")]'),
	], reason='ORDER RESULTS HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 13,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the ORDER RESULTS HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('ORDER RESULTS HL7 Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(orderCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"ORDER RESULTS HL7")]'),
	], reason='ORDER RESULTS HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 13,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the ORDER RESULTS HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('OSHA Methods')

	t = d.getWCUnitTest ('OSHA Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(oshaNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"OSHA")]'),
	], reason='OSHA DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 14,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the OSHA method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('OSHA Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(oshaMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"OSHA")]'),
	], reason='OSHA DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 14,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the OSHA method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('OSHA Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(oshaCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"OSHA")]'),
	], reason='OSHA DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 14,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the OSHA method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('Work Comp Methods')

	t = d.getWCUnitTest ('Work Comp Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(wrkcompNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Work Comp")]'),
	], reason='Work Comp DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 15,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Work Comp method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Work Comp Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(wrkcompMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Work Comp")]'),
	], reason='Work Comp DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 15,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Work Comp method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Work Comp Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(wrkcompCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Work Comp")]'),
	], reason='Work Comp DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 15,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Work Comp method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('Incident Methods')

	t = d.getWCUnitTest ('Incident Method - SS Eligibility Method Detail')
	t.setup(routeDoc, 0)
	t.setup(incidentSSMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Incident")]'),
	], reason='Incident DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 25,
					 'method_detail': 'SS_ELIG',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Incident method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Incident Method - MIEPub Server API Method Detail')
	t.setup(routeDoc, 0)
	t.setup(incidentPUBMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Incident")]'),
	], reason='Incident DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 25,
					 'method_detail': 'MIEPUB_API',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Incident method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Incident Method - MIE Daemon Monitor Method Detail')
	t.setup(routeDoc, 0)
	t.setup(incidentDMONMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Incident")]'),
	], reason='Incident DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 25,
					 'method_detail': 'DMON',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Incident method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Incident Method - MIE Commerce Method Detail')
	t.setup(routeDoc, 0)
	t.setup(incidentCOMMMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Incident")]'),
	], reason='Incident DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 25,
					 'method_detail': 'MIECOMMERCE',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Incident method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()

	t = d.getWCUnitTest ('Webchart Post Method')
	t.setup(routeDoc, 0)
	t.setup(wcPostMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Webchart Post")]'),
	], reason='Webchart Post DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 16,
					 'method_detail': '',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Webchart Post method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Esign Request Method')
	t.setup(routeDoc, 0)
	t.setup(esignMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Esign Request")]'),
	], reason='Esign Request DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 18,
					 'method_detail': '',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Esign Request method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Remote IFQ Batch Method')
	t.setup(routeDoc, 0)
	t.setup(remIFQMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Remote IFQ Batch")]'),
	], reason='Remote IFQ Batch DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 20,
					 'method_detail': 'NMC_POST',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Remote IFQ Batch method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.startSection('Scripted Export Methods')

	t = d.getWCUnitTest ('Scripted Export Method - SS Eligibility Method Detail')
	t.setup(routeDoc, 0)
	t.setup(scrptExpSSMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Scripted Export")]'),
	], reason='Scripted Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 21,
					 'method_detail': 'SS_ELIG',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Scripted Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Scripted Export Method - MIEPub Server API Method Detail')
	t.setup(routeDoc, 0)
	t.setup(scrptExpPUBMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Scripted Export")]'),
	], reason='Scripted Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 21,
					 'method_detail': 'MIEPUB_API',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Scripted Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Scripted Export Method - MIE Daemon Monitor Method Detail')
	t.setup(routeDoc, 0)
	t.setup(scrptExpDMONMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Scripted Export")]'),
	], reason='Scripted Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 21,
					 'method_detail': 'DMON',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Scripted Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Scripted Export Method - MIE Commerce Method Detail')
	t.setup(routeDoc, 0)
	t.setup(scrptExpCOMMMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Scripted Export")]'),
	], reason='Scripted Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 21,
					 'method_detail': 'MIECOMMERCE',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Scripted Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('MDM Reports HL7 Methods')

	t = d.getWCUnitTest ('MDM Reports HL7 Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(mdmNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"MDM Reports HL7")]'),
	], reason='MDM Reports HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 22,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the MDM Reports HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('MDM Reports HL7 Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(mdmMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"MDM Reports HL7")]'),
	], reason='MDM Reports HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 22,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the MDM Reports HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('MDM Reports HL7 Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(mdmCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"MDM Reports HL7")]'),
	], reason='MDM Reports HL7 DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 22,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the MDM Reports HL7 method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('Immunization Export Methods')

	t = d.getWCUnitTest ('Immunization Export Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(immunNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Immunization Export")]'),
	], reason='Immunization Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 23,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Immunization Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Immunization Export Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(immunMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Immunization Export")]'),
	], reason='Immunization Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 23,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Immunization Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Immunization Export Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(immunCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Immunization Export")]'),
	], reason='Immunization Export DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 23,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Immunization Export method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('Kareo Billing Methods')

	t = d.getWCUnitTest ('Kareo Billing Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(kareoNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Kareo Billing")]'),
	], reason='Kareo Billing DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 24,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Kareo Billing method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Kareo Billing Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(kareoMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Kareo Billing")]'),
	], reason='Kareo Billing DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 24,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Kareo Billing method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Kareo Billing Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(kareoCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Kareo Billing")]'),
	], reason='Kareo Billing DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 24,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Kareo Billing method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()

	t = d.getWCUnitTest ('Direct Email Method')
	t.setup(routeDoc, 0)
	t.setup(directMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Direct Email")]'),
	], reason='Direct Email DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 26,
					 'method_detail': 'selenium@mieweb.com',
					 'status': 'P',
					 'active': 1,
					 'route_option': 'from:selenium@mieweb.com',
				}),
	], reason='Verify the Direct Email method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.startSection('Syndromic Surveillance Methods')

	t = d.getWCUnitTest ('Syndromic Surveillance Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(synSurvNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Syndromic Surveillance")]'),
	], reason='Syndromic Surveillance DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 27,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Syndromic Surveillance method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Syndromic Surveillance Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(synSurvMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Syndromic Surveillance")]'),
	], reason='Syndromic Surveillance DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 27,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Syndromic Surveillance method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('Syndromic Surveillance Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(synSurvCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"Syndromic Surveillance")]'),
	], reason='Syndromic Surveillance DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 27,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the Syndromic Surveillance method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.startSection('837 Professional Claims Methods')

	t = d.getWCUnitTest ('837 Professional Claims Method - NMC_HL7 Method Detail')
	t.setup(routeDoc, 0)
	t.setup(profClaimNMCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"837 Professional Claims")]'),
	], reason='837 Professional Claims DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 28,
					 'method_detail': 'NMC_HL7',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the 837 Professional Claims method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('837 Professional Claims Method - Medisys Method Detail')
	t.setup(routeDoc, 0)
	t.setup(profClaimMEDMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"837 Professional Claims")]'),
	], reason='837 Professional Claims DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 28,
					 'method_detail': 'MEDISYS',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the 837 Professional Claims method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	t = d.getWCUnitTest ('837 Professional Claims Method - CDC Reporting Method Detail')
	t.setup(routeDoc, 0)
	t.setup(profClaimCDCMethod)
	t.verifyElements([
		wcElement('xpath', '//legend[contains(.,"Current Routes for Document")]/following-sibling::div//span[contains(.,"837 Professional Claims")]'),
	], reason='837 Professional Claims DataSend')
	t.verifyDB([
		  wcDBRecord("FROM datasend_route", {
					 'item_type': 'doc',
					 'item_id': 488,
					 'method': 28,
					 'method_detail': 'CDC',
					 'status': 'P',
					 'active': 1,
					 'route_option': '',
				}),
	], reason='Verify the 837 Professional Claims method DataSend route exists in the db')
	t.teardown(clearRoutes)
	t.test(checkDocProp)

	d.endSection()
	d.endSection()
