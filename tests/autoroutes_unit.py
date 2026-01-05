"""
@owners: pepperson
"""
from wcunittest import wcElement, wcDBRecord

# Verify No Access
# Verify Auto Route Editor page
# Verify Add Auto Route page
# Verify Edit Auto Route page
# Verify Delete Auto Route page
# Warning: Please fill in all fields
# Warning: Unable to find DataSend Auto Route
# Verify Recipient Type changes to Recipient and Method
# Verify Method changes to Method Details
# Verify Recipient auto route preference
# Add an Auto Route
# Edit an Auto Route
# Delete an Auto Route
# Add AR with Custom Pending Status - User Setting Define DataSend Status ON
# Edit AR with Custom Pending Status - User Setting Define DataSend Status ON
# Add AR with Custom Pending Status - User Setting Define DataSend Status OFF but Custom Pending Status should still be available
# Edit AR with Custom Pending Status - User Setting Define DataSend Status OFF but Custom Pending Status should still be available
# Remove Custom Pending Status - User Setting Define DataSend Status ON
# Auto Route Execution - Family Physician Auto Route
# Auto Route Execution - All Contacts Auto Route
# Auto Route Execution - Self Auto Route
# Auto Route Execution - User and Encounter User Auto Routes
# Auto Route Execution - Re-send the Auto Routes
# Auto Route Execution - Click to Error the Auto Routes
# Auto Route Execution - Acknowledge the Auto Routes
# Auto Route Execution - Deactivate the Auto Routes
# Auto Route Execution - Cancel the Auto Routes





def clickElement(d, text):
	d.clickElement(text=text)

def clickSave(d, data):
	d.clickElement(value='Save')

def grantAutoRouteAccess(d, data):
	d.miedb.dbExec("UPDATE security_exception SET security_value='1' WHERE user_id='8' AND category_name='Send Patient Data'")

def removeAutoRouteAccess(d, data):
	d.miedb.dbExec("INSERT INTO security_exception (user_id, module_name, category_name, security_value) VALUES ('8', 'E-Chart', 'Send Patient Data', '0')")

def grantCustomPendingAccess(d, data):
	d.miedb.dbExec("INSERT INTO security_exception (user_id, module_name, category_name, security_value) VALUES ('8', 'E-Chart', 'Define DataSend Status', '1')")

def removeCustomPendingAccess(d, data):
	d.miedb.dbExec("UPDATE security_exception SET security_value='0' WHERE user_id='8' AND category_name='Define DataSend Status'")

def enterUser(d, idx):
	d.enterFormData('Anderson, Fred', id='user_ac_txt', blur=False)
	acchoice = d.waitFor(d, lambda d: d.getElement(id='user_ac_span_choices_%d' %idx), expected_return=True, timeout=30)
	if not acchoice:
		d.reportCommandStatus('Timeout', '', False, '', 'Autocomplete choices not displayed')
	else:
		# d.clickElement(id='user_ac_span_choices_%d' %idx)
		d.runJS(f"user_ac.SetSelection({idx}); \
		jxacExtremeLog('user_ac', 'mouseup received, focusing input'); \
		user_ac.rowClicking=true; \
		user_ac.f.focus(); \
		user_ac.f.select(); \
		user_ac.rowClicking=false; \
		user_ac.RemoveBox(); \
		user_ac.clicked=true; \
		user_ac.ClickHandler();")

def setUsrFax(d, data):
	d.enterFormData('Anderson, Fred', id='user_ac_txt', blur=False)
	d.miedb.dbExec("UPDATE users SET fax_number='2604596271' WHERE last_name='Anderson' AND first_name='Frederick'")

def setPrefRoute(d, data):
	d.enterFormData('Anderson, Fred', id='user_ac_txt', blur=False)
	d.miedb.dbExec("UPDATE users SET preferred_route='26' WHERE last_name='Anderson' AND first_name='Frederick'")

def addCustomStatusY(d, data):
	d.enterFormData('Y', id="custom_pending")

def editCustomStatus(d, data):
	d.enterFormData('X', id="custom_pending")

def insertCustomRouteY(d, data):
	d.miedb.dbExec("INSERT INTO datasend_auto_route (trigger_type, description, custom_join, where_clause, user_id, recipient_name, recipient_id, method, method_detail, send_criteria, no_auto_resend, custom_pending) VALUES ('5', 'CustomRoute', 'LEFT JOIN patient_mrns pm ON p.pat_id=pm.pat_id', '0 AND d.doc_type IN', '8', 'Sample, John', '9', '2', '(260) 459-6271', '2', '0', 'Y')")

def removeCustomRouteY(d, data):
	d.miedb.dbExec("DELETE FROM datasend_auto_route WHERE description='CustomRoute'")

def cleanDB(d, data):
	d.miedb.dbExec("DELETE FROM security_exception_revisions")
	d.miedb.dbExec("DELETE FROM documents where pat_id='18'")
	d.miedb.dbExec("DELETE FROM users WHERE last_name='Hart'")
	d.miedb.dbExec("DELETE FROM user_patients WHERE pat_id='18' AND entered_date='2007-02-02 09:15:00'")
	d.miedb.dbExec("DELETE FROM encounter_users")
	d.miedb.dbExec("DELETE FROM datasend_auto_route")
	d.miedb.dbExec("TRUNCATE datasend_auto_route")

def removeDocs(d, data):
	d.miedb.dbExec("DELETE FROM documents WHERE pat_id='18'")

def addAutoRoute(d, data):
	d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add')
	d.enterFormData('On Document Add', id="trigger_type")
	d.enterFormData('TestRoute', id="description")
	d.enterFormData('LEFT JOIN patient_mrns pm ON p.pat_id=pm.pat_id AND pm.wc_partition="Employer Organization"', id="custom_join")
	d.enterFormData('0 AND d.doc_type IN ("7600A") AND pm.mrnumber IS NOT NULL AND d.storage_type!=1', id="where_clause")
	d.enterFormData('Family Physician', id="recipient_type")
	d.enterFormData('Final Signed Only', id="send_criteria")
	d.enterFormData('1', xpath='//td[@class="value"][contains(.,"No")]/input[@type="radio"][@value="1"]')

def openAutoRoute(d, idx):
	d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&tabmodule=admin&tabselect=Auto+Routes')
	d.clickElement(xpath='//td[contains(.,"TestRoute") or contains(.,"RouteTest")]/following-sibling::td/a[contains(.,"Edit")]')

def editAutoRoute(d, idx):
	d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&tabmodule=admin&tabselect=Auto+Routes')
	d.clickElement(xpath='//td[contains(.,"TestRoute")]/following-sibling::td/a[contains(.,"Edit")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.enterFormData('On Encounter Add', id="trigger_type")
	d.enterFormData('RouteTest', id="description")
	d.enterFormData('LEFT JOIN patient_mrns pm ON p.pat_id=pm.pat_id AND pm.wc_partition="Provider Organization"', id="custom_join")
	d.enterFormData('0 AND d.doc_type IN ("7600B") AND pm.mrnumber IS NOT NULL AND d.storage_type!=1', id="where_clause")
	d.enterFormData('User', id="recipient_type")
	d.enterFormData('Sample, John', id='user_ac_txt', blur=False)
	acchoice = d.waitFor(d, lambda d: d.getElement(id='user_ac_span_choices_%d' %idx), expected_return=True, timeout=30)
	if not acchoice:
		d.reportCommandStatus('Timeout', '', False, '', 'Autocomplete choices not displayed')
	else:
		d.clickElement(id='user_ac_span_choices_%d' %idx)
	d.enterFormData('Fax', id="method")
	d.enterFormData('(260) 459-6271', id="method_detail_Fax_input")
	d.enterFormData('Default Setting', id="route_option_Fax_input")
	d.enterFormData(True, id="fax_wo_headers")
	d.enterFormData('0', xpath='//td[@class="value"][contains(.,"Yes")]/input[@type="radio"][@value="0"]')

def deleteAutoRoute(d, data):
	d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&tabmodule=admin&tabselect=Auto+Routes')
	d.clickElement(xpath='//td[contains(.,"TestRoute") or contains(.,"RouteTest")]/following-sibling::td/a[contains(.,"Delete")]')
	d.clickElement(value='Confirm')

def executionConfig(d, data):
	d.miedb.dbExec("INSERT INTO security_exception_revisions (user_id, module_name, category_name, security_value, admin_user_id, create_datetime, revision_datetime, active) VALUES ('8', 'E-Chart', 'Send Patient Data', '1', '8', '2007-02-02 09:15:00', '2007-02-02 09:15:00', '0')")
	d.miedb.dbExec("INSERT INTO security_exception_revisions (user_id, module_name, category_name, security_value, admin_user_id, create_datetime, revision_datetime, active) VALUES ('8', 'E-Chart', 'Send By AutoRoute', '2', '8', '2007-02-02 09:15:00', '2007-02-02 09:15:00', '0')")
	d.miedb.dbExec("INSERT INTO datasend_auto_route (trigger_type, description, custom_join, where_clause, user_id, recipient_type, recipient_name, recipient_id, method, method_detail, send_criteria, no_auto_resend, custom_pending, route_option) VALUES ('0', 'Testing a User Route', '', '1', '8', '0', 'Selenium, Selenium ( Fort Wayne, IN United States 46804)', '0', '2', '(260) 459-6271', '0', '0', '', '')")
	d.miedb.dbExec("INSERT INTO datasend_auto_route (trigger_type, description, custom_join, where_clause, user_id, recipient_type, recipient_name, recipient_id, method, method_detail, send_criteria, no_auto_resend, custom_pending, route_option) VALUES ('0', 'Testing a Physician Route', '', 'd.doc_type=\\'WCDOCNOT\\'', '8', '1', '', '0', '0', '', '0', '0', '', '')")
	d.miedb.dbExec("INSERT INTO datasend_auto_route (trigger_type, description, custom_join, where_clause, user_id, recipient_type, recipient_id, method, send_criteria, no_auto_resend, custom_pending, route_option) VALUES ('0', 'Testing an Encounter User Route', '', '1', '8', '5', '0', '0', '0', '0', '', '')")
	d.miedb.dbExec("INSERT INTO datasend_auto_route (trigger_type, description, custom_join, where_clause, user_id, recipient_type, recipient_name, recipient_id, method, method_detail, send_criteria, no_auto_resend, custom_pending, route_option) VALUES ('0', 'Testing a Patient Contact Route', '', 'd.doc_type=\\'BILLINGQ\\'', '8', '7', '', '0', '0', '', '0', '0', '', '')")
	d.miedb.dbExec("INSERT INTO datasend_auto_route (trigger_type, description, custom_join, where_clause, user_id, recipient_type, recipient_name, recipient_id, method, method_detail, send_criteria, no_auto_resend, custom_pending, route_option) VALUES ('0', 'Testing a Specific Patient Contact Route', '', 'd.doc_type=\\'ADVDIRECT\\'', '8', '7', '', '501', '0', '', '0', '0', '', '')")
	d.miedb.dbExec("UPDATE users SET preferred_route='2' WHERE last_name='Sample' AND user_id='9'")
	d.miedb.dbExec("UPDATE users SET preferred_route='2' WHERE last_name='Butler' AND user_id='16'")
	d.miedb.dbExec("UPDATE users SET preferred_route='2' WHERE username='reception' AND user_id='21'")
	d.miedb.dbExec("INSERT INTO users (username, status, realm, last_name, first_name, fax_number, user_role_id, security_role_id, preferred_route) VALUES ('whart', '2', 'MIE', 'Hart', 'William', '2604596271', '0', '0', '2')")
	d.miedb.dbExec("INSERT INTO user_patients (id, id_type, pat_id, role_id, security_role_id, rank, entered_date) SELECT user_id, 'user', '18', '501', '0', '0', '2007-02-02 09:15:00' FROM users WHERE last_name='Hart'")
	d.miedb.dbExec("INSERT INTO user_patients (id, id_type, pat_id, role_id, security_role_id, rank, entered_date) SELECT user_id, 'user', '18', '38', '0', '0', '2007-02-02 09:15:00' FROM users WHERE username='reception'")
	d.miedb.dbExec("INSERT INTO encounter_users (id, id_type, enc_id, role_id, rank, entered_date) SELECT user_id, 'user', '11', '9', '0', '2007-02-02 09:15:00' FROM users WHERE last_name='Butler'")

def checkDocProp(d, data):
	d.navigate('?f=chart&s=pat&t=Documents&v=list&pat_id=18')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//div//td[@class="lv__wc_Doc_20ID_cell"]/a')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//a[contains(.,"Properties")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def prepResendRoutes(d, data):
    d.miedb.dbExec("UPDATE datasend_route SET status='C', sent_datetime=NOW(), progress='Complete' WHERE recipient_name='Butler, Internist'")

def clickResend(d, data):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//a[contains(.,"Resend")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def clickAcknowledge(d, data):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//a[contains(.,"Acknowledge")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def clickError(d, data):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//a[contains(.,"Error")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def clickDeactivate(d, data):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//a[contains(.,"Deactivate")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)

def clickCancel(d, data):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.clickElement(xpath='//a[contains(.,"Cancel")]')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)



# xpath bases:
MAIN ='//div[@id="wc_body_container"]/div[@id="wc_body"]/div[@id="wc_main"]'
MAIN_FRM='//div[@id="wc_body_container"]/div[@id="wc_body"]/div[@id="wc_main"]/form[@method="POST"]'
LV_TITLE='/table/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"]'
LV_HEADER='/table[@class="lv_root"][@id="lv_root_DataSend_20Auto_20Routes"]/tbody/tr/td/fieldset/div[@id="lv_da_route_span"]/table[@class="newui zebra"]/thead'
LV_BODY='/table[@class="lv_root"][@id="lv_root_DataSend_20Auto_20Routes"]/tbody/tr/td/fieldset/div[@id="lv_da_route_span"]/table[@class="newui zebra"]/tbody'
LV_FOOTER='/table[@class="lv_root"][@id="lv_root_DataSend_20Auto_20Routes"]/tbody/tr/td/fieldset/div[@id="lv_da_route_span"]/table[@class="newui zebra"]/tfoot'
AR_ADD_TABLE='/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Add DataSend Auto Route")]/parent::legend/following-sibling::table/tbody/tr'
AR_EDIT_TABLE='/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Edit DataSend Auto Route")]/parent::legend/following-sibling::table/tbody/tr'
DELETE_TABLE='/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Confirm Delete")]/parent::legend/following-sibling::table/tbody/tr'

SHOW_LINK='/table/tbody/tr/td/fieldset/legend/font/span[@id="lv_da_route_show_link"][@class="LVTitle"]'
HIDE_LINK='/table/tbody/tr/td/fieldset/legend/font/span[@id="lv_da_route_hide_link"][@class="LVTitle"]'

RECIPIENT_ROLE_CELL='/td[@class="value"]/span[@id="DAR_recipient_role"]'
RECIPIENT_ROLE_OPT='/select[@id="recipient_role"]/option'

METHOD_CELL='/td[@class="value"]/span[@id="DAR_recipient_method_input"]'
METHOD_OPT='/select[@id="method"]/option'

DETAIL_CELL='/td[@class="value"]/span[@id="DAR_recipient_detail_input"]'

PRINT_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailPrint_label"]'
PRINT_ROUTEOPTION_LABEL='/table/tbody/tr/td/span[@id="route_optionPrint_label"]'
PRINT_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionPrint"]'
PRINT_ROUTEOPTION_INPUT='/select[@id="route_option_Print_input"]'
PRINT_METHOD='/table/tbody/tr/td/span[@id="method_detailPrint"]'
PRINT_METHOD_INPUT='/select[@id="method_detail_Print_input"]'

FAX_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailFax_label"]'
FAX_ROUTEOPTION_LABEL='/table/tbody/tr/td/span[@id="route_optionFax_label"]'
FAX_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionFax"]'
FAX_ROUTEOPTION_INPUT='/select[@id="route_option_Fax_input"]'
FAX_METHOD='/table/tbody/tr/td/span[@id="method_detailFax"]'
FAX_METHOD_INPUT='/select[@id="method_detail_Fax_input"]'

HL7_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailHL7 Send_label"]'
HL7_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionHL7"]'
HL7_ROUTEOPTION_INPUT='/select[@id="route_option_HL7 Send_input"]'
HL7_METHOD='/table/tbody/tr/td/span[@id="method_detailHL7 Send"]'
HL7_METHOD_INPUT='/select[@id="method_detail_HL7 Send_input"]'

TEXTEXPORT_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailText Export_label"]'
TEXTEXPORT_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionText Export"]'
TEXTEXPORT_ROUTEOPTION_INPUT='/select[@id="route_option_Text Export_input"]'
TEXTEXPORT_METHOD='/table/tbody/tr/td/span[@id="method_detailText Export"]'
TEXTEXPORT_METHOD_INPUT='/select[@id="method_detail_Text Export_input"]'

DICTAPHONE_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailDictaphone HL7_label"]'
DICTAPHONE_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionDictaphone HL7"]'
DICTAPHONE_ROUTEOPTION_INPUT='/select[@id="route_option_Dictaphone HL7_input"]'
DICTAPHONE_METHOD='/table/tbody/tr/td/span[@id="method_detailDictaphone HL7"]'
DICTAPHONE_METHOD_INPUT='/select[@id="method_detail_Dictaphone HL7_input"]'

ORDERRESULTS_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailORDER RESULTS HL7_label"]'
ORDERRESULTS_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionORDER RESULTS HL7"]'
ORDERRESULTS_ROUTEOPTION_INPUT='/select[@id="route_option_ORDER RESULTS HL7_input"]'
ORDERRESULTS_METHOD='/table/tbody/tr/td/span[@id="method_detailORDER RESULTS HL7"]'
ORDERRESULTS_METHOD_INPUT='/select[@id="method_detail_ORDER RESULTS HL7_input"]'

PHS_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailPublic Health Surveillance_label"]'
PHS_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionPublic Health Surveillance"]'
PHS_ROUTEOPTION_INPUT='/select[@id="route_option_Public Health Surveillance_input"]'
PHS_METHOD='/table/tbody/tr/td/span[@id="method_detailPublic Health Surveillance"]'
PHS_METHOD_INPUT='/select[@id="method_detail_Public Health Surveillance_input"]'

OSHA_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailOSHA_label"]'
OSHA_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionOSHA"]'
OSHA_ROUTEOPTION_INPUT='/select[@id="route_option_OSHA_input"]'
OSHA_METHOD='/table/tbody/tr/td/span[@id="method_detailOSHA"]'
OSHA_METHOD_INPUT='/select[@id="method_detail_OSHA_input"]'

WORKCOMP_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailWork Comp_label"]'
WORKCOMP_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionWork Comp"]'
WORKCOMP_ROUTEOPTION_INPUT='/select[@id="route_option_Work Comp_input"]'
WORKCOMP_METHOD='/table/tbody/tr/td/span[@id="method_detailWork Comp"]'
WORKCOMP_METHOD_INPUT='/select[@id="method_detail_Work Comp_input"]'

INCIDENT_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailIncident_label"]'
INCIDENT_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionIncident"]'
INCIDENT_ROUTEOPTION_INPUT='/select[@id="route_option_Incident_input"]'
INCIDENT_METHOD='/table/tbody/tr/td/span[@id="method_detailIncident"]'
INCIDENT_METHOD_INPUT='/select[@id="method_detail_Incident_input"]'

XDSREG_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailXDS Registry_label"]'
XDSREG_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionXDS Registry"]'
XDSREG_ROUTEOPTION_INPUT='/select[@id="route_option_XDS Registry_input"]'
XDSREG_METHOD='/table/tbody/tr/td/span[@id="method_detailXDS Registry"]'
XDSREG_METHOD_INPUT='/select[@id="method_detail_XDS Registry_input"]'

W2TFTP_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailWord2TIFF FTP_label"]'
W2TFTP_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionWord2TIFF FTP"]'
W2TFTP_ROUTEOPTION_INPUT='/select[@id="route_option_Word2TIFF FTP_input"]'
W2TFTP_METHOD='/table/tbody/tr/td/span[@id="method_detailWord2TIFF FTP"]'
W2TFTP_METHOD_INPUT='/select[@id="method_detail_Word2TIFF FTP_input"]'

IFQ_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailRemote IFQ Batch_label"]'
IFQ_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionRemote IFQ Batch"]'
IFQ_ROUTEOPTION_INPUT='/select[@id="route_option_Remote IFQ Batch_input"]'
IFQ_METHOD='/table/tbody/tr/td/span[@id="method_detailRemote IFQ Batch"]'
IFQ_METHOD_INPUT='/select[@id="method_detail_Remote IFQ Batch_input"]'

SCRIPTEDEXPORT_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailScripted Export_label"]'
SCRIPTEDEXPORT_ROUTEOPTION_LABEL='/table/tbody/tr/td/span[@id="route_optionScripted Export_label"]'
SCRIPTEDEXPORT_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionScripted Export"]'
SCRIPTEDEXPORT_ROUTEOPTION_INPUT='/select[@id="route_option_Scripted Export_input"]'
SCRIPTEDEXPORT_METHOD='/table/tbody/tr/td/span[@id="method_detailScripted Export"]'
SCRIPTEDEXPORT_METHOD_INPUT='/select[@id="method_detail_Scripted Export_input"]'

MDM_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailMDM Reports HL7_label"]'
MDM_ROUTEOPTION_LABEL='/table/tbody/tr/td/span[@id="route_optionMDM Reports HL7_label"]'
MDM_ROUTEOPTION_LABEL='/table/tbody/tr/td/span[@id="route_optionMDM Reports HL7_label"]'
MDM_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionMDM Reports HL7"]'
MDM_ROUTEOPTION_INPUT='/select[@id="route_option_MDM Reports HL7_input"]'
MDM_METHOD='/table/tbody/tr/td/span[@id="method_detailMDM Reports HL7"]'
MDM_METHOD_INPUT='/select[@id="method_detail_MDM Reports HL7_input"]'

IMMUNEXP_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailImmunization Export_label"]'
IMMUNEXP_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionImmunization Export"]'
IMMUNEXP_ROUTEOPTION_INPUT='/select[@id="route_option_Immunization Export_input"]'
IMMUNEXP_METHOD='/table/tbody/tr/td/span[@id="method_detailImmunization Export"]'
IMMUNEXP_METHOD_INPUT='/select[@id="method_detail_Immunization Export_input"]'

KAREO_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailKareo Billing_label"]'
KAREO_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionKareo Billing"]'
KAREO_ROUTEOPTION_INPUT='/select[@id="route_option_Kareo Billing_input"]'
KAREO_METHOD='/table/tbody/tr/td/span[@id="method_detailKareo Billing"]'
KAREO_METHOD_INPUT='/select[@id="method_detail_Kareo Billing_input"]'

ProffClaim_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detail837 Professional Claims_label"]'
ProffClaim_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_option837 Professional Claims"]'
ProffClaim_ROUTEOPTION_INPUT='/select[@id="route_option_837 Professional Claims_input"]'
ProffClaim_METHOD='/table/tbody/tr/td/span[@id="method_detail837 Professional Claims"]'
ProffClaim_METHOD_INPUT='/select[@id="method_detail_837 Professional Claims_input"]'

SYNDROMIC_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailSyndromic Surveillance_label"]'
SYNDROMIC_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionSyndromic Surveillance"]'
SYNDROMIC_ROUTEOPTION_INPUT='/select[@id="route_option_Syndromic Surveillance_input"]'
SYNDROMIC_METHOD='/table/tbody/tr/td/span[@id="method_detailSyndromic Surveillance"]'
SYNDROMIC_METHOD_INPUT='/select[@id="method_detail_Syndromic Surveillance_input"]'

DIRECTEMAIL_METHOD_LABEL='/table/tbody/tr/td/span[@id="method_detailDirect Email_label"]'
DIRECTEMAIL_ROUTEOPTION='/table/tbody/tr/td/span[@id="route_optionDirect Email"]'
DIRECTEMAIL_ROUTEOPTION_INPUT='/select[@id="route_option_Direct Email_input"]'
DIRECTEMAIL_METHOD='/table/tbody/tr/td/span[@id="method_detailDirect Email"]'
DIRECTEMAIL_METHOD_INPUT='/select[@id="method_detail_Direct Email_input"]'

SEND_ON_CRITERIA='/td[@class="value"]/span[@id="DAR_recipient_criteria_input"]'
TRIGGERTYPE_OPT='/td[@class="value"]/select[@id="trigger_type"]/option'
RECIPIENTTYPE_OPT='/td[@class="value"]/select[@id="recipient_type"]/option'

RADIO='/td[@class="value"]/input[@type="radio"]'
DISPLAYED='[@style="display:inline;" or @style="display: inline" or @style="display:inline" or @style="display: inline;"]'
NOTDISPLAYED='[@style="display:none;" or @style="display: none" or @style="display:none" or @style="display: none;"]'
HIDDEN_INPUT='/input[@type="hidden" or @type="HIDDEN"]'
VISIBLE='[@style="visibility:visible;" or @style="visibility: visible" or @style="visibility:visible" or @style="visibility: visible;"]'
HIDDEN='[@style="visibility:hidden;" or @style="visibility: hidden" or @style="visibility:hidden" or @style="visibility: hidden;"]'



def main(d, WCURL):
# Verify No Access
	t = d.getWCUnitTest('Verify No Access to Auto Route Editor')
	t.setup(removeAutoRouteAccess)
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&tabmodule=admin&tabselect=Auto+Routes'), reason='Navigate directly to Auto Route Editor page warning that the user does not have access')
	t.verifyElements([
		wcElement('xpath', MAIN + '/div[@class="center bold"][contains(.,"Your current permission of")][contains(.,"No")][contains(.,"E-Chart")][contains(.,"Send Patient Data")][contains(.,") security setting does not allow access to Edit Document Auto Routes.")]'),
		wcElement('xpath', MAIN + '/div[@class="center bold"][contains(.,"A permission level of")][contains(.,"Yes")][contains(.,"is required.")]'),
		wcElement('xpath', MAIN + '/div[@class="center bold"][contains(.,"Please see your administrator with any questions.")]'),
	], reason='Confirm the warning message for no access to Auto Route Editor')
	t.test()


# Verify Auto Route Editor page
	t = d.getWCUnitTest('Verify the Auto Route Editor Page')
	t.setup(grantAutoRouteAccess)
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&tabmodule=admin&tabselect=Auto+Routes'), reason='Navigate directly to Auto Route Editor')
	t.verifyElements([
		wcElement('xpath', MAIN + '/div[@class="nobr"]/a[@class="folder"][contains(.,"Add A Route")]'),
		wcElement('xpath', MAIN + '/script[contains(.,"showSpan")]'),
	], reason='Verify the quick link and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN + SHOW_LINK + '[contains(.,"DataSend Auto Routes")]'),
		wcElement('xpath', MAIN + SHOW_LINK + NOTDISPLAYED + '/font/span[contains(.,"Show")]'),
		wcElement('xpath', MAIN + LV_TITLE + '/font/span[contains(.,"Hide")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Trigger_20Type_header"]/a[@class="link"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Description_header"]/a[@class="link"][contains(.,"Description")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Where_20Clause_header"]/a[@class="link"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Recipient_header"]/a[@class="link"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Method_header"]/a[@class="link"][contains(.,"Method")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Detail_header"]/a[@class="link"][contains(.,"Detail")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]/a[@class="link"][contains(.,"Options")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Send_20On_header"]/a[@class="link"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"][contains(.,"Options")]'),
		wcElement('xpath', MAIN + LV_BODY),
		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify the DataSend Auto Routes listview elements are present')
	t.test()


# Verify Add Auto Route page
	t = d.getWCUnitTest('Verify the Add Auto Route Page')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add'), reason='Navigate directly to Add Auto Route Page')
	t.verifyElements([
		wcElement('xpath', MAIN + '/script[contains(@src,"ecdocroute")]'),
		wcElement('xpath', MAIN_FRM),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="f"][@value="chart"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="s"][@value="dar_editor"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="t"][@value="Auto Routes"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="opp"][@value="add"]'),
		wcElement('xpath', MAIN_FRM + '/script[contains(.,"docRoute_methods")]'),
	], reason='Verify the hidden form inputs and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + '/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Add DataSend Auto Route")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/select[@id="trigger_type"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="0"][contains(.,"On Document Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="1"][contains(.,"On Dictation Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="5"][contains(.,"On Encounter Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="12"][contains(.,"On Encounter Update")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="2"][contains(.,"On Patient Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="3"][contains(.,"Process Patient On DICOM Transfer Complete")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="4"][contains(.,"Process Encounter on DICOM Transfer Complete")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="14"][contains(.,"Process Documents on DICOM Transfer Complete")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="6"][contains(.,"On Patient Merge")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="7"][contains(.,"On Patient Admit/vist Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="8"][contains(.,"On Appointments Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="9"][contains(.,"On Procedures for Billing Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="10"][contains(.,"On Order Add")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="11"][contains(.,"Send demographic update on encounter close")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="13"][contains(.,"On Incident Update")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="15"][contains(.,"On Document Update")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + TRIGGERTYPE_OPT + '[@value="16"][contains(.,"On Patient Update")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/select[@id="trigger_type"]/following-sibling::script[contains(.,"DAR_triggerTypeChangeHandler")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Route Description")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/input[@type="text"][@id="description"]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Custom Join")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/textarea[@id="custom_join"]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/textarea[@id="where_clause"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "globalize")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "jqx-all")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "incident")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "enclinks")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "wcencsearch")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "pat_clinical_restrict")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(@src, "clause_builder")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(., "build_warn_me")][contains(., "clause_builder")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@class="link"][contains(.,"Help Me")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Recipient Type")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/select[@id="recipient_type"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="0"][contains(.,"User")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="1"][contains(.,"Family Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="2"][contains(.,"Attending Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="3"][contains(.,"Referring Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="4"][contains(.,"Performing Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="5"][contains(.,"Encounter Physicians")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="6"][contains(.,"Ordering Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="7"][contains(.,"Patient Contact")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="8"][contains(.,"Lab Request Refer To Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/script[contains(.,"DAR_recipTypeChangeHandler")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/input[@id="recipient_id"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + DISPLAYED + '/span[@id="user_ac_span"]/input[@id="user_ac_txt"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + DISPLAYED + '/span[@id="user_ac_span"]/script[contains(.,"jsXMLAutoComplete")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + DISPLAYED + '/input[@id="recipient_name"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + DISPLAYED + '/script[contains(.,"recip_clear")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + '/select[@id="recipient_role"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value=""][@selected=""][contains(.,"All Patient Contact Roles")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="262"][contains(.,"Acupuncturist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="303"][contains(.,"Addiction Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="157"][contains(.,"Addiction Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="38"][contains(.,"Administrative Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="162"][contains(.,"Adolescent Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="139"][contains(.,"Allergy & Immunology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="163"][contains(.,"Ambulatory Care")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="101"][contains(.,"Anesthesiologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="304"][contains(.,"Anesthesiology Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="305"][contains(.,"Art Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="999"][contains(.,"Asset Custodian")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="998"][contains(.,"Asset Owner")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="335"][contains(.,"Athletic Trainer")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="2"][contains(.,"Attending Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="260"][contains(.,"Audiologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="36"][contains(.,"Backup Supervisor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="308"][contains(.,"Behavioral Analyst")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="164"][contains(.,"Behavioral Health")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="165"][contains(.,"Blood Banking")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="9"][contains(.,"Carboned Copied User")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="102"][contains(.,"Cardiology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="156"][contains(.,"Cardiovascular Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="271"][contains(.,"Case Management")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="39"][contains(.,"Case Manager")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="103"][contains(.,"Chiropractor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="309"][contains(.,"Christian Science Practitioner/Nurse")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="167"][contains(.,"Clinic Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="270"][contains(.,"Clinical Neurophysiology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="269"][contains(.,"Clinical Neuropsychologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="166"][contains(.,"Clinical Nurse Specialist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="150"][contains(.,"Colorectal Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="168"][contains(.,"Community Health")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="10"][contains(.,"Consulting Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="250"][contains(.,"Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="311"][contains(.,"Critical Care Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="306"][contains(.,"Dance Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="307"][contains(.,"Dental Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="268"][contains(.,"Dental Hygienist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="132"][contains(.,"Dentist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="312"][contains(.,"Denturist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="104"][contains(.,"Dermatology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="173"][contains(.,"Development and Rehabilitative Services")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="313"][contains(.,"Developmental Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="169"][contains(.,"Diagnostic Services")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="170"][contains(.,"Dietician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="450"][contains(.,"DIRECT Email")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="292"][contains(.,"Emergency Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="105"][contains(.,"Emergency Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="50"][contains(.,"Employer Company")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="106"][contains(.,"Endocrinology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="133"][contains(.,"Endodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="146"][contains(.,"ER Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="171"][contains(.,"Eye & Vision Care")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="295"][contains(.,"Eye Bank")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="4"][contains(.,"Family Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="172"][contains(.,"Family Planning")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="107"][contains(.,"Family Practitioner")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="263"][contains(.,"Family Therapist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="108"][contains(.,"Gastroenterology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="109"][contains(.,"General Practice")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="314"][contains(.,"Genetic Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="255"][contains(.,"Geneticist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="110"][contains(.,"Geriatric Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="176"][contains(.,"Gynecology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="177"][contains(.,"Healthcare Provider")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="400"][contains(.,"Healthcare Provider Location")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="111"][contains(.,"Hematology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="175"][contains(.,"Hematology & Oncology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="315"][contains(.,"Hepatology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="296"][contains(.,"Home Health Aid")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="316"][contains(.,"Homeopath")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="256"][contains(.,"Hospice and Palliative Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="174"][contains(.,"Hospice Worker")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="7"][contains(.,"Hospital for pregnancy delivery")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="178"][contains(.,"Hospitalist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="112"][contains(.,"Immunology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="182"][contains(.,"Infectious Disease")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="147"][contains(.,"Intensivist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="113"][contains(.,"Internal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="297"][contains(.,"Interpreter")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="317"][contains(.,"Kinesiotherapist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="185"][contains(.,"Legal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="0"][contains(.,"Limited Access User")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="5"][contains(.,"Local Pharmacy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="318"][contains(.,"Lodging Facility")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="6"][contains(.,"Mail-In Pharmacy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="181"][contains(.,"Managed Care Organization")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="194"][contains(.,"Massage Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="187"][contains(.,"Maternal & Fetal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="319"][contains(.,"Mechanotherapist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="100"][contains(.,"Medical Care Team")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="254"][contains(.,"Medical Examiner")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="114"][contains(.,"Medical Genetics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="179"][contains(.,"Mental Health")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="180"][contains(.,"Midwife")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="321"][contains(.,"Military Medical Technician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="320"][contains(.,"Military Provider")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="322"][contains(.,"Music Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="323"][contains(.,"Naprapath")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="278"][contains(.,"Naturopath")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="115"][contains(.,"Nephrology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="116"][contains(.,"Neurologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="324"][contains(.,"Neuromuscular Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="325"][contains(.,"Neuromusculoskeletal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="144"][contains(.,"Neuropsychiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="273"][contains(.,"Neuropsychologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="140"][contains(.,"Neurosurgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="60"][contains(.,"NMC - Auto Rights")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="70"][contains(.,"NMC Administrator")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="41"][contains(.,"NMC Cobrand - Registration")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="40"][contains(.,"NMC Cobrand - Visitor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="11"][contains(.,"NMC Provider")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="71"][contains(.,"NMC Read Only")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="298"][contains(.,"Non-Pharmacy Dispensing Site")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="265"][contains(.,"Nuclear Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="159"][contains(.,"Nurse")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="184"][contains(.,"Nurse Anesthetist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="153"][contains(.,"Nurse Practitioner")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="183"][contains(.,"Nursing Service Providers")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="326"][contains(.,"Nutritionist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="117"][contains(.,"OB/GYN")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="186"][contains(.,"Occupational Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="143"][contains(.,"Occupational Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="258"][contains(.,"Occupational Therapy Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="118"][contains(.,"Oncology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="119"][contains(.,"Ophthalmology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="145"][contains(.,"Optician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="121"][contains(.,"Optometry")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="158"][contains(.,"Oral & Maxillofacial Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="134"][contains(.,"Oral Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="12"][contains(.,"Ordering Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="13"][contains(.,"Organization Staff")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="135"][contains(.,"Orthodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="120"][contains(.,"Orthopaedic Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="299"][contains(.,"Orthotics & Prosthetics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="148"][contains(.,"Osteopathic Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="293"][contains(.,"Other Service Providers")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="122"][contains(.,"Otolaryngology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="154"][contains(.,"Pain Management")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="123"][contains(.,"Pathologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="136"][contains(.,"Pediatric Dentist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="124"][contains(.,"Pediatrics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="137"][contains(.,"Periodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="275"][contains(.,"Pharmacist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="310"][contains(.,"Pharmacology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="300"][contains(.,"Pharmacy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="302"][contains(.,"Phlebology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="161"][contains(.,"Physiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="125"][contains(.,"Physical Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="149"][contains(.,"Physical Therapy Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="160"][contains(.,"Physician Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="126"][contains(.,"Physician: Other")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="127"][contains(.,"Plastic/Reconstructive Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="141"][contains(.,"Podiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="327"][contains(.,"Podiatry Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="333"][contains(.,"Poetry Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="1"][contains(.,"Portal User")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="201"][contains(.,"Preferred hospital for emergency visits")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="200"][contains(.,"Preferred hospital for planned procedures")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="8"][contains(.,"Preferred Lab")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="267"][contains(.,"Preventative Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="290"][contains(.,"Primary Care Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="138"][contains(.,"Prosthodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="128"][contains(.,"Psychiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="257"][contains(.,"Psychiatry & Neurology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="272"][contains(.,"Psychoanalyst")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="193"][contains(.,"Psychologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="195"][contains(.,"Psychoterapist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="151"][contains(.,"Pulmonary")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="266"][contains(.,"Radiologic Technologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="129"][contains(.,"Radiology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="328"][contains(.,"Recreation Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="3"][contains(.,"Referring Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="334"][contains(.,"Reflexologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="329"][contains(.,"Rehabilitation Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="330"][contains(.,"Rehabilitation Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="331"][contains(.,"Rehabilitation Practitioner")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="15"][contains(.,"Resident Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="188"][contains(.,"Residential Care")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="259"][contains(.,"Respiratory Therapist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="142"][contains(.,"Rheumatology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="501"][contains(.,"Self")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="502"][contains(.,"Self - Duplicate")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="277"][contains(.,"Sleep Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="192"][contains(.,"Social Worker")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="276"][contains(.,"Specialist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="294"][contains(.,"Specialist/Technologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="261"][contains(.,"Speech/Language Pathologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="189"][contains(.,"Sports Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="37"][contains(.,"Supervisor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="301"][contains(.,"Supplier")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="190"][contains(.,"Support Services")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="130"][contains(.,"Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="252"][contains(.,"Technician/Technologist")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="152"][contains(.,"Thoracic Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="274"][contains(.,"Thoracic Surgery")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="191"][contains(.,"Toxicology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="332"][contains(.,"Transplant Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="291"][contains(.,"Urgent Care Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="131"][contains(.,"Urology")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="155"][contains(.,"Vascular Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="253"][contains(.,"Veterinarian")]'),


		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Method")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + '/input[@id="method_desc"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + '/select[@id="method"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value=""][@selected=""][contains(.,"")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="1"][contains(.,"Print")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="2"][contains(.,"Fax")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="4"][contains(.,"HL7 Send")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="6"][contains(.,"Text Export")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="9"][contains(.,"Dictaphone HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="12"][contains(.,"Word2TIFF FTP")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="13"][contains(.,"ORDER RESULTS HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="14"][contains(.,"OSHA")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="15"][contains(.,"Work Comp")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="25"][contains(.,"Incident")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="16"][contains(.,"Webchart Post")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="18"][contains(.,"Esign Request")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="20"][contains(.,"Remote IFQ Batch")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="21"][contains(.,"Scripted Export")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="22"][contains(.,"MDM Reports HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="23"][contains(.,"Immunization Export")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="24"][contains(.,"Kareo Billing")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="26"][contains(.,"Direct Email")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="27"][contains(.,"Syndromic Surveillance")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="28"][contains(.,"837 Professional Claims")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + '/script[contains(.,"method_clear")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + '/script[contains(.,"le_arShowInput")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Method Detail")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + '/input[@id="route_option"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + '/input[@id="method_detail"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + '/script[contains(.,"method_detail_clear")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + '/script[contains(.,"armethdetail_setHidden")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Mail to:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_METHOD + NOTDISPLAYED + '/input[@type="text"][@id="method_detail_Print_input"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Printer:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="ar_tray_span_holder"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/script[contains(.,"arshowTrayinput")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="printer_value"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="tray_value"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + PRINT_ROUTEOPTION_INPUT),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + PRINT_ROUTEOPTION_INPUT + '/option[contains(.,"Default Setting")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + PRINT_ROUTEOPTION_INPUT + '/option[contains(.,"My Computer")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/span[@id="My Computer_tray_span"]' + NOTDISPLAYED + '/select[@id="My Computer_tray_input"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/span[@id="My Computer_tray_span"]' + NOTDISPLAYED + '[contains(.,"Paper")][contains(.,"Tray")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/input[@type="checkbox"][@id="print_wo_headers"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '[contains(.,"Print without document Header")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Fax Number:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_METHOD + NOTDISPLAYED + '/input[@id="method_detail_Fax_input"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Coversheet:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="printer_value"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="tray_value"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT + '/option[contains(.,"Default Setting")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT + '/option[@value="SKIPFCS"][contains(.,"No Coversheet")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT + '/option[@value="FAX"][contains(.,"FAX")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + '[contains(.,"Fax without document Header")]/input[@type="checkbox"][@id="fax_wo_headers"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + '[contains(.,"Fax without document Header")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"CCR:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + HL7_METHOD_INPUT),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + HL7_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + HL7_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + '/script[contains(.,"armethdetail_setRouteOptionCCRAsHTML")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + '/input[@type="checkbox"][@id="ccr_as_html"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + '[contains(.,"Send As HTML")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + TEXTEXPORT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"output:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + TEXTEXPORT_METHOD + NOTDISPLAYED + TEXTEXPORT_METHOD_INPUT),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + TEXTEXPORT_METHOD + NOTDISPLAYED + TEXTEXPORT_METHOD_INPUT + '/option[contains(.,"No Destinations Available")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DICTAPHONE_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DICTAPHONE_METHOD + NOTDISPLAYED + DICTAPHONE_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DICTAPHONE_METHOD + NOTDISPLAYED + DICTAPHONE_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + ORDERRESULTS_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + ORDERRESULTS_METHOD + NOTDISPLAYED + ORDERRESULTS_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + ORDERRESULTS_METHOD + NOTDISPLAYED + ORDERRESULTS_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PHS_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PHS_METHOD + NOTDISPLAYED + PHS_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PHS_METHOD + NOTDISPLAYED + PHS_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + OSHA_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + OSHA_METHOD + NOTDISPLAYED + OSHA_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + OSHA_METHOD + NOTDISPLAYED + OSHA_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + WORKCOMP_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + WORKCOMP_METHOD + NOTDISPLAYED + WORKCOMP_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + WORKCOMP_METHOD + NOTDISPLAYED + WORKCOMP_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + INCIDENT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="SS_ELIG"][contains(.,"SS Eligibility")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="MIEPUB_API"][contains(.,"MIEPub Server API")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="DMON"][contains(.,"Daemon Monitor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="MIECOMMERCE"][contains(.,"MIE Commerce")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + XDSREG_METHOD_INPUT + '/option[contains(.,"No Destinations Available")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + '/script[contains(.,"armethdetail_setRouteOptionXDRRoute")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + '[contains(.,"XDR Route")]/input[@type="checkbox"][@id="xdr_route"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + '[contains(.,"XDR Route")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="SS_ELIG"][contains(.,"SS Eligibility")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="NMC_POST"][contains(.,"NMC_POST")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="MIEPUB_API"][contains(.,"MIEPub Server API")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="DMON"][contains(.,"Daemon Monitor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="MIECOMMERCE"][contains(.,"MIE Commerce")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + IFQ_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Remote WebChart")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + IFQ_METHOD + NOTDISPLAYED + IFQ_METHOD_INPUT + '/option[@value="NMC_POST"][contains(.,"NMC_POST")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Script RTS:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="SS_ELIG"][contains(.,"SS Eligibility")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="MIEPUB_API"][contains(.,"MIEPub Server API")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="DMON"][contains(.,"Daemon Monitor")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="MIECOMMERCE"][contains(.,"MIE Commerce")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Script Name:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_ROUTEOPTION + NOTDISPLAYED + '/input[@type="text"][@id="route_optionScripted Export_input"]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + MDM_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + MDM_METHOD + NOTDISPLAYED + MDM_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + MDM_METHOD + NOTDISPLAYED + MDM_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + MDM_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Send as TIFF image:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + MDM_ROUTEOPTION + NOTDISPLAYED + '/input[@type="checkbox"][@id="route_optionMDM Reports HL7_input"]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + IMMUNEXP_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + IMMUNEXP_METHOD + NOTDISPLAYED + IMMUNEXP_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + IMMUNEXP_METHOD + NOTDISPLAYED + IMMUNEXP_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + KAREO_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + KAREO_METHOD + NOTDISPLAYED + KAREO_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + KAREO_METHOD + NOTDISPLAYED + KAREO_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + ProffClaim_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + ProffClaim_METHOD + NOTDISPLAYED + ProffClaim_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + ProffClaim_METHOD + NOTDISPLAYED + ProffClaim_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SYNDROMIC_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SYNDROMIC_METHOD + NOTDISPLAYED + SYNDROMIC_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + SYNDROMIC_METHOD + NOTDISPLAYED + SYNDROMIC_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Direct Address:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/input[@type="email"][@id="method_detail_Direct Email_input"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/script[contains(.,"armethdetail_setRouteOptionDirectRoute")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/span[@id="route_optionDirect Email_label"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/span[@id="route_optionDirect Email"]' + HIDDEN_INPUT + '[contains(@value, "from:")][@id="route_option_Direct Email_input"]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + SEND_ON_CRITERIA + HIDDEN_INPUT + '[@id="send_criteria_desc"][@value="All Revisions"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]/option[@value="0"][contains(.,"All Revisions")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]/option[@value="1"][contains(.,"Preliminary Signed")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]/option[@value="2"][contains(.,"Final Signed Only")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + SEND_ON_CRITERIA + '/script[contains(.,"s_crit_clear")]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Automatically Resend on Item Revision")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]' + HIDDEN_INPUT + '[@value="Yes"][@id="no_auto_resend_desc"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RADIO + '[@value="1"][@id="no_auto_resend_1"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RADIO + '[@value="1"][@id="no_auto_resend_1"]/parent::td[contains(.,"No")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RADIO + '[@value="0"][@id="no_auto_resend_0"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RADIO + '[@value="0"][@id="no_auto_resend_0"]/parent::td[contains(.,"Yes")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@class="fa wc_help"]'),

		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="foot"]/input[@type="submit"][@value="Save"][@name="ar_save"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="foot"]/input[@type="reset"][@value="Reset"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="foot"]/input[@type="submit"][@value="Cancel"][@name="ar_cancel"]'),
	], reason='Verify all Add Auto Route elements are present')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Use a Custom Pending Status")]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/select[@id="custom_pending"]', exists=False),
	], reason='Verify that the Custom Pending Status option is not available by default')
	t.verifyElements([
		wcElement('xpath', MAIN + '/div[@class="nobr"]/a[@class="folder"][contains(.,"Add A Route")]'),
		wcElement('xpath', MAIN + '/script[contains(.,"showSpan")]'),
	], reason='Verify the quick link and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN + LV_TITLE + NOTDISPLAYED + '[@id="lv_da_route_show_link"]/font/span[contains(.,"Show")]'),
		wcElement('xpath', MAIN + LV_TITLE + '[@id="lv_da_route_hide_link"]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', MAIN + LV_TITLE + '[@id="lv_da_route_span_title"][contains(.,"DataSend Auto Routes")]'),

		wcElement('xpath', MAIN + '/table[@class="lv_root"][@id="lv_root_DataSend_20Auto_20Routes"]/tbody/tr/td/fieldset/div[@id="lv_da_route_span"]/table[@class="newui zebra"]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Trigger_20Type_header"]/a[@class="link"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Description_header"]/a[@class="link"][contains(.,"Description")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Where_20Clause_header"]/a[@class="link"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Recipient_header"]/a[@class="link"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Method_header"]/a[@class="link"][contains(.,"Method")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Detail_header"]/a[@class="link"][contains(.,"Detail")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]/a[@class="link"][contains(.,"Options")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Send_20On_header"]/a[@class="link"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]'),

		wcElement('xpath', MAIN + LV_BODY),

		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify the DataSend Auto Routes listview elements are present')
	t.teardown(cleanDB)
	t.test()


# Verify Edit Auto Route page
	t = d.getWCUnitTest('Verify the Edit Auto Route Page')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=selenium&custom_join=selenium&where_clause=selenium&recipient_type=1&recipient_id=0&user_ac_txt=&recipient_name=&recipient_role=&method_desc=&method=&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0&ar_save=Save'), reason='Add an Auto Route to edit')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=edit&ar_id=1'), reason='Navigate directly to Edit Auto Route Page')
	t.verifyElements([
		wcElement('xpath', MAIN + '/script[contains(@src,"ecdocroute")]'),
		wcElement('xpath', MAIN_FRM),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="f"][@value="chart"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="s"][@value="dar_editor"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="t"][@value="Auto Routes"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="opp"][@value="edit"]'),
		wcElement('xpath', MAIN_FRM + '/script[contains(.,"docRoute_methods")]'),
	], reason='Verify the hidden form inputs and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + '/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Edit DataSend Auto Route")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="trigger_type"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="0"][contains(.,"On Document Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="1"][contains(.,"On Dictation Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="5"][contains(.,"On Encounter Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="12"][contains(.,"On Encounter Update")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="2"][contains(.,"On Patient Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="3"][contains(.,"Process Patient On DICOM Transfer Complete")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="4"][contains(.,"Process Encounter on DICOM Transfer Complete")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="14"][contains(.,"Process Documents on DICOM Transfer Complete")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="6"][contains(.,"On Patient Merge")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="7"][contains(.,"On Patient Admit/vist Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="8"][contains(.,"On Appointments Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="9"][contains(.,"On Procedures for Billing Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="10"][contains(.,"On Order Add")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="11"][contains(.,"Send demographic update on encounter close")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="13"][contains(.,"On Incident Update")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="15"][contains(.,"On Document Update")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + TRIGGERTYPE_OPT + '[@value="16"][contains(.,"On Patient Update")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="trigger_type"]/following-sibling::script[contains(.,"DAR_triggerTypeChangeHandler")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Route Description")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@type="text"][@id="description"]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Custom Join")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/textarea[@id="custom_join"]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/textarea[@id="where_clause"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "globalize")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "jqx-all")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "incident")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "enclinks")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "wcencsearch")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "pat_clinical_restrict")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(@src, "clause_builder")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(., "build_warn_me")][contains(., "clause_builder")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/span[@class="link"][contains(.,"Help Me")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Recipient Type")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="recipient_type"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="0"][contains(.,"User")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="1"][contains(.,"Family Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="2"][contains(.,"Attending Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="3"][contains(.,"Referring Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="4"][contains(.,"Performing Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="5"][contains(.,"Encounter Physicians")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="6"][contains(.,"Ordering Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="7"][contains(.,"Patient Contact")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENTTYPE_OPT + '[@value="8"][contains(.,"Lab Request Refer To Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/script[contains(.,"DAR_recipTypeChangeHandler")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@id="recipient_id"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + NOTDISPLAYED + '/span[@id="user_ac_span"]/input[@id="user_ac_txt"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + NOTDISPLAYED + '/span[@id="user_ac_span"]/script[contains(.,"jsXMLAutoComplete")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + NOTDISPLAYED + '/input[@id="recipient_name"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + NOTDISPLAYED + '/script[contains(.,"recip_clear")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + '/select[@id="recipient_role"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value=""][@selected=""][contains(.,"All Patient Contact Roles")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="262"][contains(.,"Acupuncturist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="303"][contains(.,"Addiction Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="157"][contains(.,"Addiction Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="38"][contains(.,"Administrative Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="162"][contains(.,"Adolescent Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="139"][contains(.,"Allergy & Immunology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="163"][contains(.,"Ambulatory Care")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="101"][contains(.,"Anesthesiologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="304"][contains(.,"Anesthesiology Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="305"][contains(.,"Art Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="999"][contains(.,"Asset Custodian")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="998"][contains(.,"Asset Owner")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="335"][contains(.,"Athletic Trainer")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="2"][contains(.,"Attending Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="260"][contains(.,"Audiologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="36"][contains(.,"Backup Supervisor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="308"][contains(.,"Behavioral Analyst")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="164"][contains(.,"Behavioral Health")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="165"][contains(.,"Blood Banking")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="9"][contains(.,"Carboned Copied User")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="102"][contains(.,"Cardiology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="156"][contains(.,"Cardiovascular Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="271"][contains(.,"Case Management")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="39"][contains(.,"Case Manager")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="103"][contains(.,"Chiropractor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="309"][contains(.,"Christian Science Practitioner/Nurse")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="167"][contains(.,"Clinic Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="270"][contains(.,"Clinical Neurophysiology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="269"][contains(.,"Clinical Neuropsychologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="166"][contains(.,"Clinical Nurse Specialist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="150"][contains(.,"Colorectal Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="168"][contains(.,"Community Health")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="10"][contains(.,"Consulting Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="250"][contains(.,"Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="311"][contains(.,"Critical Care Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="306"][contains(.,"Dance Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="307"][contains(.,"Dental Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="268"][contains(.,"Dental Hygienist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="132"][contains(.,"Dentist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="312"][contains(.,"Denturist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="104"][contains(.,"Dermatology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="173"][contains(.,"Development and Rehabilitative Services")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="313"][contains(.,"Developmental Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="169"][contains(.,"Diagnostic Services")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="170"][contains(.,"Dietician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="450"][contains(.,"DIRECT Email")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="292"][contains(.,"Emergency Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="105"][contains(.,"Emergency Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="50"][contains(.,"Employer Company")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="106"][contains(.,"Endocrinology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="133"][contains(.,"Endodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="146"][contains(.,"ER Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="171"][contains(.,"Eye & Vision Care")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="295"][contains(.,"Eye Bank")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="4"][contains(.,"Family Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="172"][contains(.,"Family Planning")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="107"][contains(.,"Family Practitioner")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="263"][contains(.,"Family Therapist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="108"][contains(.,"Gastroenterology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="109"][contains(.,"General Practice")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="314"][contains(.,"Genetic Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="255"][contains(.,"Geneticist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="110"][contains(.,"Geriatric Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="176"][contains(.,"Gynecology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="177"][contains(.,"Healthcare Provider")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="400"][contains(.,"Healthcare Provider Location")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="111"][contains(.,"Hematology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="175"][contains(.,"Hematology & Oncology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="315"][contains(.,"Hepatology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="296"][contains(.,"Home Health Aid")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="316"][contains(.,"Homeopath")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="256"][contains(.,"Hospice and Palliative Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="174"][contains(.,"Hospice Worker")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="7"][contains(.,"Hospital for pregnancy delivery")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="178"][contains(.,"Hospitalist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="112"][contains(.,"Immunology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="182"][contains(.,"Infectious Disease")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="147"][contains(.,"Intensivist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="113"][contains(.,"Internal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="297"][contains(.,"Interpreter")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="317"][contains(.,"Kinesiotherapist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="185"][contains(.,"Legal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="0"][contains(.,"Limited Access User")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="5"][contains(.,"Local Pharmacy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="318"][contains(.,"Lodging Facility")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="6"][contains(.,"Mail-In Pharmacy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="181"][contains(.,"Managed Care Organization")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="194"][contains(.,"Massage Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="187"][contains(.,"Maternal & Fetal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="319"][contains(.,"Mechanotherapist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="100"][contains(.,"Medical Care Team")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="254"][contains(.,"Medical Examiner")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="114"][contains(.,"Medical Genetics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="179"][contains(.,"Mental Health")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="180"][contains(.,"Midwife")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="321"][contains(.,"Military Medical Technician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="320"][contains(.,"Military Provider")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="322"][contains(.,"Music Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="323"][contains(.,"Naprapath")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="278"][contains(.,"Naturopath")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="115"][contains(.,"Nephrology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="116"][contains(.,"Neurologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="324"][contains(.,"Neuromuscular Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="325"][contains(.,"Neuromusculoskeletal Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="144"][contains(.,"Neuropsychiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="273"][contains(.,"Neuropsychologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="140"][contains(.,"Neurosurgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="60"][contains(.,"NMC - Auto Rights")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="70"][contains(.,"NMC Administrator")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="41"][contains(.,"NMC Cobrand - Registration")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="40"][contains(.,"NMC Cobrand - Visitor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="11"][contains(.,"NMC Provider")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="71"][contains(.,"NMC Read Only")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="298"][contains(.,"Non-Pharmacy Dispensing Site")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="265"][contains(.,"Nuclear Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="159"][contains(.,"Nurse")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="184"][contains(.,"Nurse Anesthetist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="153"][contains(.,"Nurse Practitioner")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="183"][contains(.,"Nursing Service Providers")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="326"][contains(.,"Nutritionist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="117"][contains(.,"OB/GYN")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="186"][contains(.,"Occupational Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="143"][contains(.,"Occupational Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="258"][contains(.,"Occupational Therapy Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="118"][contains(.,"Oncology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="119"][contains(.,"Ophthalmology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="145"][contains(.,"Optician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="121"][contains(.,"Optometry")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="158"][contains(.,"Oral & Maxillofacial Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="134"][contains(.,"Oral Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="12"][contains(.,"Ordering Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="13"][contains(.,"Organization Staff")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="135"][contains(.,"Orthodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="120"][contains(.,"Orthopaedic Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="299"][contains(.,"Orthotics & Prosthetics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="148"][contains(.,"Osteopathic Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="293"][contains(.,"Other Service Providers")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="122"][contains(.,"Otolaryngology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="154"][contains(.,"Pain Management")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="123"][contains(.,"Pathologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="136"][contains(.,"Pediatric Dentist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="124"][contains(.,"Pediatrics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="137"][contains(.,"Periodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="275"][contains(.,"Pharmacist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="310"][contains(.,"Pharmacology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="300"][contains(.,"Pharmacy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="302"][contains(.,"Phlebology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="161"][contains(.,"Physiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="125"][contains(.,"Physical Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="149"][contains(.,"Physical Therapy Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="160"][contains(.,"Physician Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="126"][contains(.,"Physician: Other")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="127"][contains(.,"Plastic/Reconstructive Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="141"][contains(.,"Podiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="327"][contains(.,"Podiatry Assistant")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="333"][contains(.,"Poetry Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="1"][contains(.,"Portal User")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="201"][contains(.,"Preferred hospital for emergency visits")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="200"][contains(.,"Preferred hospital for planned procedures")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="8"][contains(.,"Preferred Lab")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="267"][contains(.,"Preventative Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="290"][contains(.,"Primary Care Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="138"][contains(.,"Prosthodontics")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="128"][contains(.,"Psychiatrist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="257"][contains(.,"Psychiatry & Neurology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="272"][contains(.,"Psychoanalyst")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="193"][contains(.,"Psychologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="195"][contains(.,"Psychoterapist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="151"][contains(.,"Pulmonary")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="266"][contains(.,"Radiologic Technologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="129"][contains(.,"Radiology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="328"][contains(.,"Recreation Therapy")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="3"][contains(.,"Referring Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="334"][contains(.,"Reflexologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="329"][contains(.,"Rehabilitation Counselor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="330"][contains(.,"Rehabilitation Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="331"][contains(.,"Rehabilitation Practitioner")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="15"][contains(.,"Resident Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="188"][contains(.,"Residential Care")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="259"][contains(.,"Respiratory Therapist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="142"][contains(.,"Rheumatology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="501"][contains(.,"Self")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="502"][contains(.,"Self - Duplicate")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="277"][contains(.,"Sleep Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="192"][contains(.,"Social Worker")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="276"][contains(.,"Specialist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="294"][contains(.,"Specialist/Technologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="261"][contains(.,"Speech/Language Pathologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="189"][contains(.,"Sports Medicine")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="37"][contains(.,"Supervisor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="301"][contains(.,"Supplier")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="190"][contains(.,"Support Services")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="130"][contains(.,"Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="252"][contains(.,"Technician/Technologist")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="152"][contains(.,"Thoracic Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="274"][contains(.,"Thoracic Surgery")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="191"][contains(.,"Toxicology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="332"][contains(.,"Transplant Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="291"][contains(.,"Urgent Care Physician")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="131"][contains(.,"Urology")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="155"][contains(.,"Vascular Surgeon")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RECIPIENT_ROLE_CELL + NOTDISPLAYED + RECIPIENT_ROLE_OPT + '[@value="253"][contains(.,"Veterinarian")]'),


		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Method")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + '/input[@id="method_desc"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + '/select[@id="method"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value=""][contains(.,"")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="1"][contains(.,"Print")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="2"][contains(.,"Fax")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="4"][contains(.,"HL7 Send")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="6"][contains(.,"Text Export")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="9"][contains(.,"Dictaphone HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="12"][contains(.,"Word2TIFF FTP")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="13"][contains(.,"ORDER RESULTS HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="14"][contains(.,"OSHA")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="15"][contains(.,"Work Comp")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="25"][contains(.,"Incident")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="16"][contains(.,"Webchart Post")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="18"][contains(.,"Esign Request")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="20"][contains(.,"Remote IFQ Batch")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="21"][contains(.,"Scripted Export")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="22"][contains(.,"MDM Reports HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="23"][contains(.,"Immunization Export")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="24"][contains(.,"Kareo Billing")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="26"][contains(.,"Direct Email")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="27"][contains(.,"Syndromic Surveillance")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + METHOD_OPT + '[@value="28"][contains(.,"837 Professional Claims")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + '/script[contains(.,"method_clear")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + METHOD_CELL + HIDDEN + '/script[contains(.,"le_arShowInput")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Method Detail")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + '/input[@id="route_option"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + '/input[@id="method_detail"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + '/script[contains(.,"method_detail_clear")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + '/script[contains(.,"armethdetail_setHidden")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Mail to:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_METHOD + NOTDISPLAYED + '/input[@type="text"][@id="method_detail_Print_input"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Printer:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="ar_tray_span_holder"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/script[contains(.,"arshowTrayinput")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="printer_value"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="tray_value"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + PRINT_ROUTEOPTION_INPUT),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + PRINT_ROUTEOPTION_INPUT + '/option[contains(.,"Default Setting")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + PRINT_ROUTEOPTION_INPUT + '/option[contains(.,"My Computer")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/span[@id="My Computer_tray_span"]' + NOTDISPLAYED + '/select[@id="My Computer_tray_input"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/span[@id="My Computer_tray_span"]' + NOTDISPLAYED + '[contains(.,"Paper")][contains(.,"Tray")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '/input[@type="checkbox"][@id="print_wo_headers"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION + NOTDISPLAYED + '[contains(.,"Print without document Header")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Fax Number:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_METHOD + NOTDISPLAYED + '/input[@id="method_detail_Fax_input"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Coversheet:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="printer_value"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + HIDDEN_INPUT + '[@id="tray_value"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT + '/option[contains(.,"Default Setting")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT + '/option[@value="SKIPFCS"][contains(.,"No Coversheet")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + FAX_ROUTEOPTION_INPUT + '/option[@value="FAX"][contains(.,"FAX")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + '[contains(.,"Fax without document Header")]/input[@type="checkbox"][@id="fax_wo_headers"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + FAX_ROUTEOPTION + NOTDISPLAYED + '[contains(.,"Fax without document Header")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"CCR:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + HL7_METHOD_INPUT),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + HL7_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + HL7_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + '/script[contains(.,"armethdetail_setRouteOptionCCRAsHTML")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + '/input[@type="checkbox"][@id="ccr_as_html"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + HL7_METHOD + NOTDISPLAYED + '[contains(.,"Send As HTML")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + TEXTEXPORT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"output:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + TEXTEXPORT_METHOD + NOTDISPLAYED + TEXTEXPORT_METHOD_INPUT),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + TEXTEXPORT_METHOD + NOTDISPLAYED + TEXTEXPORT_METHOD_INPUT + '/option[contains(.,"No Destinations Available")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DICTAPHONE_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DICTAPHONE_METHOD + NOTDISPLAYED + DICTAPHONE_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DICTAPHONE_METHOD + NOTDISPLAYED + DICTAPHONE_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + ORDERRESULTS_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + ORDERRESULTS_METHOD + NOTDISPLAYED + ORDERRESULTS_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + ORDERRESULTS_METHOD + NOTDISPLAYED + ORDERRESULTS_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PHS_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PHS_METHOD + NOTDISPLAYED + PHS_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + PHS_METHOD + NOTDISPLAYED + PHS_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + OSHA_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + OSHA_METHOD + NOTDISPLAYED + OSHA_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + OSHA_METHOD + NOTDISPLAYED + OSHA_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + WORKCOMP_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + WORKCOMP_METHOD + NOTDISPLAYED + WORKCOMP_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + WORKCOMP_METHOD + NOTDISPLAYED + WORKCOMP_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + INCIDENT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="SS_ELIG"][contains(.,"SS Eligibility")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="MIEPUB_API"][contains(.,"MIEPub Server API")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="DMON"][contains(.,"Daemon Monitor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + INCIDENT_METHOD + NOTDISPLAYED + INCIDENT_METHOD_INPUT + '/option[@value="MIECOMMERCE"][contains(.,"MIE Commerce")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + XDSREG_METHOD_INPUT + '/option[contains(.,"No Destinations Available")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + '/script[contains(.,"armethdetail_setRouteOptionXDRRoute")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + '[contains(.,"XDR Route")]/input[@type="checkbox"][@id="xdr_route"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + XDSREG_METHOD + NOTDISPLAYED + '[contains(.,"XDR Route")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="SS_ELIG"][contains(.,"SS Eligibility")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="NMC_POST"][contains(.,"NMC_POST")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="MIEPUB_API"][contains(.,"MIEPub Server API")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="DMON"][contains(.,"Daemon Monitor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="MIECOMMERCE"][contains(.,"MIE Commerce")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + W2TFTP_METHOD + NOTDISPLAYED + W2TFTP_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + IFQ_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Remote WebChart")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + IFQ_METHOD + NOTDISPLAYED + IFQ_METHOD_INPUT + '/option[@value="NMC_POST"][contains(.,"NMC_POST")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Script RTS:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="SS_ELIG"][contains(.,"SS Eligibility")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="MIEPUB_API"][contains(.,"MIEPub Server API")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="DMON"][contains(.,"Daemon Monitor")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_METHOD + NOTDISPLAYED + SCRIPTEDEXPORT_METHOD_INPUT + '/option[@value="MIECOMMERCE"][contains(.,"MIE Commerce")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Script Name:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SCRIPTEDEXPORT_ROUTEOPTION + NOTDISPLAYED + '/input[@type="text"][@id="route_optionScripted Export_input"]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + MDM_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + MDM_METHOD + NOTDISPLAYED + MDM_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + MDM_METHOD + NOTDISPLAYED + MDM_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + MDM_ROUTEOPTION_LABEL + NOTDISPLAYED + '[contains(.,"Send as TIFF image:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + MDM_ROUTEOPTION + NOTDISPLAYED + '/input[@type="checkbox"][@id="route_optionMDM Reports HL7_input"]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + IMMUNEXP_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + IMMUNEXP_METHOD + NOTDISPLAYED + IMMUNEXP_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + IMMUNEXP_METHOD + NOTDISPLAYED + IMMUNEXP_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + KAREO_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + KAREO_METHOD + NOTDISPLAYED + KAREO_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + KAREO_METHOD + NOTDISPLAYED + KAREO_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + ProffClaim_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + ProffClaim_METHOD + NOTDISPLAYED + ProffClaim_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + ProffClaim_METHOD + NOTDISPLAYED + ProffClaim_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SYNDROMIC_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Interface:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SYNDROMIC_METHOD + NOTDISPLAYED + SYNDROMIC_METHOD_INPUT + '/option[@value="NMC_HL7"][contains(.,"NMC_HL7")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + SYNDROMIC_METHOD + NOTDISPLAYED + SYNDROMIC_METHOD_INPUT + '/option[@value="CDC"][contains(.,"CDC Reporting")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD_LABEL + NOTDISPLAYED + '[contains(.,"Direct Address:")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/input[@type="email"][@id="method_detail_Direct Email_input"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/script[contains(.,"armethdetail_setRouteOptionDirectRoute")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/span[@id="route_optionDirect Email_label"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + DETAIL_CELL + DIRECTEMAIL_METHOD + NOTDISPLAYED + '/span[@id="route_optionDirect Email"]' + HIDDEN_INPUT + '[contains(@value, "from:")][@id="route_option_Direct Email_input"]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + SEND_ON_CRITERIA + HIDDEN_INPUT + '[@id="send_criteria_desc"][@value="All Revisions"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]/option[@value="0"][contains(.,"All Revisions")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]/option[@value="1"][contains(.,"Preliminary Signed")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + SEND_ON_CRITERIA + '/select[@id="send_criteria"]/option[@value="2"][contains(.,"Final Signed Only")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + SEND_ON_CRITERIA + '/script[contains(.,"s_crit_clear")]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="field"][contains(.,"Automatically Resend on Item Revision")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]' + HIDDEN_INPUT + '[@value="Yes"][@id="no_auto_resend_desc"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RADIO + '[@value="1"][@id="no_auto_resend_1"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RADIO + '[@value="1"][@id="no_auto_resend_1"]/parent::td[contains(.,"No")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RADIO + '[@value="0"][@id="no_auto_resend_0"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + RADIO + '[@value="0"][@id="no_auto_resend_0"]/parent::td[contains(.,"Yes")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/span[@class="fa wc_help"]'),

		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="foot"]/input[@type="submit"][@value="Save"][@name="ar_save"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="foot"]/input[@type="reset"][@value="Reset"]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="foot"]/input[@type="submit"][@value="Cancel"][@name="ar_cancel"]'),
	], reason='Verify all Edit Auto Route elements are present')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="field"][contains(.,"Use a Custom Pending Status")]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/select[@id="custom_pending"]', exists=False),
	], reason='Verify that the Custom Pending Status option is not available by default')
	t.verifyElements([
		wcElement('xpath', MAIN + '/div[@class="nobr"]/a[@class="folder"][contains(.,"Add A Route")]'),
		wcElement('xpath', MAIN + '/script[contains(.,"showSpan")]'),
	], reason='Verify the quick link and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN + LV_TITLE + NOTDISPLAYED + '[@id="lv_da_route_show_link"]/font/span[contains(.,"Show")]'),
		wcElement('xpath', MAIN + LV_TITLE + '[@id="lv_da_route_hide_link"]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', MAIN + LV_TITLE + '[@id="lv_da_route_span_title"][contains(.,"DataSend Auto Routes")]'),

		wcElement('xpath', MAIN + '/table[@class="lv_root"][@id="lv_root_DataSend_20Auto_20Routes"]/tbody/tr/td/fieldset/div[@id="lv_da_route_span"]/table[@class="newui zebra"]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Trigger_20Type_header"]/a[@class="link"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Description_header"]/a[@class="link"][contains(.,"Description")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Where_20Clause_header"]/a[@class="link"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Recipient_header"]/a[@class="link"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Method_header"]/a[@class="link"][contains(.,"Method")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Detail_header"]/a[@class="link"][contains(.,"Detail")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]/a[@class="link"][contains(.,"Options")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Send_20On_header"]/a[@class="link"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]'),

		wcElement('xpath', MAIN + LV_BODY),

		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify the DataSend Auto Routes listview elements are present')
	t.test()


# Verify Delete Auto Route page
	t = d.getWCUnitTest('Verify the Delete Auto Route Page')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=delete&ar_id=1'), reason='Navigate directly to Delete Auto Route Page')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="f"][@value="chart"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="s"][@value="dar_editor"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="t"][@value="Auto Routes"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="opp"][@value="delete"]'),
		wcElement('xpath', MAIN_FRM + HIDDEN_INPUT + '[@name="ar_id"][@value="1"]'),
	], reason='Verify the hidden form inputs and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + '/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Confirm Delete")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="field"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="value"][contains(.,"On Document Add")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="field"][contains(.,"Custom Join")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="value"][contains(.,"selenium")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="field"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="value"][contains(.,"selenium")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="field"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="value"][contains(.,"")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="field"][contains(.,"Method")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="value"][contains(.,"Unknown:")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="field"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="value"][contains(.,"All Revisions")]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="foot"]/input[@type="submit"][@value="Confirm"]'),
		wcElement('xpath', MAIN_FRM + DELETE_TABLE + '/td[@class="foot"]/input[@type="submit"][@value="Cancel"]'),
	], reason='Verify all Delete Auto Route elements are present')
	t.verifyElements([
		wcElement('xpath', MAIN + '/div[@class="nobr"]/a[@class="folder"][contains(.,"Add A Route")]'),
		wcElement('xpath', MAIN + '/script[contains(.,"showSpan")]'),
	], reason='Verify the quick link and scripts are present')
	t.verifyElements([
		wcElement('xpath', MAIN + LV_TITLE + NOTDISPLAYED + '[@id="lv_da_route_show_link"]/font/span[contains(.,"Show")]'),
		wcElement('xpath', MAIN + LV_TITLE + '[@id="lv_da_route_hide_link"]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', MAIN + LV_TITLE + '[@id="lv_da_route_span_title"][contains(.,"DataSend Auto Routes")]'),

		wcElement('xpath', MAIN + '/table[@class="lv_root"][@id="lv_root_DataSend_20Auto_20Routes"]/tbody/tr/td/fieldset/div[@id="lv_da_route_span"]/table[@class="newui zebra"]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Trigger_20Type_header"]/a[@class="link"][contains(.,"Trigger Type")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Description_header"]/a[@class="link"][contains(.,"Description")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Where_20Clause_header"]/a[@class="link"][contains(.,"Where Clause")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Recipient_header"]/a[@class="link"][contains(.,"Recipient")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Method_header"]/a[@class="link"][contains(.,"Method")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Detail_header"]/a[@class="link"][contains(.,"Detail")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]/a[@class="link"][contains(.,"Options")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Send_20On_header"]/a[@class="link"][contains(.,"Send On")]'),
		wcElement('xpath', MAIN + LV_HEADER + '/tr/th[@class="da__route_Options_header"]'),

		wcElement('xpath', MAIN + LV_BODY),

		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify the DataSend Auto Routes listview elements are present')
	t.test()


# Warning: Please fill in all fields
	t = d.getWCUnitTest('Verify Warning: Please fill in all fields')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=&custom_join=&where_clause=&recipient_type=0&recipient_id=&user_ac_txt=&recipient_name=&recipient_role=&method_desc=&method=&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0&ar_save=Save'), reason='Navigate directly to the Add Auto Route Page with the warning')
	t.verifyElements([
		wcElement('xpath', MAIN + '/center/strong[contains(.,"Please Fill In All Fields")]'),
	], reason='Verify we get the warning to fill in all fields when no fields are completed')
	t.test()


# Warning: Unable to find DataSend Auto Route
	t = d.getWCUnitTest('Verify Warning: Unable to find DataSend Auto Route')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=edit&ar_id=99999'), reason='Navigate directly to the Add Auto Route Page with the warning')
	t.verifyElements([
		wcElement('xpath', MAIN + '/center/strong[contains(.,"Unable to Find DataSend Auto Route (99999)")]'),
	], reason='Verify we get the warning for a non-existent Auto Route')
	t.test()


# Verify Recipient Type changes to Recipient and Method
	t = d.getWCUnitTest('Verify Recipient Type changes to Recipient and Method')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=selenium&custom_join=test&where_clause=test&recipient_type=1&recipient_id=0&user_ac_txt=&recipient_name=&recipient_role=&method_desc=&method=&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0'), reason='Navigate directly to the Add Auto Route Page with Recipient Type selected which makes the Recipient and Method inputs available')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="1"][contains(.,"User")][@selected=""]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + RECIPIENTTYPE_OPT + '[@value="1"][contains(.,"Family Physician")][@selected=""]'),
	], reason='Verify Family Physician is selected and User is not selected')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + '/td[@class="value"]/span[@id="DAR_recipient_input"]' + NOTDISPLAYED + '/span[@id="user_ac_span"]/input[@id="user_ac_txt"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + HIDDEN),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + '/table/tbody/tr/td/span[@style="display: inline;" or @style="display:inline"]', exists=False),
	], reason='Verify that the Recipient, Method, and Method Details inputs are hidden')
	t.test()


# Verify Method changes to Method Details
	t = d.getWCUnitTest('Verify Method changes to Method Details')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=selenium&custom_join=test&where_clause=test&recipient_type=0&recipient_id=0&user_ac_txt=&recipient_name=&recipient_role=&method_desc=Print&method=1&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0'), reason='Navigate directly to the Add Auto Route Page with the Method selected which makes Method Details inputs available')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value=""][@selected=""][contains(.,"")]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + METHOD_CELL + VISIBLE + METHOD_OPT + '[@value="1"][@selected=""][contains(.,"Print")]'),
	], reason='Verify that Print is selected and not the default empty selection')
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_METHOD_LABEL + DISPLAYED + '[contains(.,"Mail to:")]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_METHOD + DISPLAYED + '/input[@type="text"][@id="method_detail_Print_input"]'),
		wcElement('xpath', MAIN_FRM + AR_ADD_TABLE + DETAIL_CELL + PRINT_ROUTEOPTION_LABEL + DISPLAYED),
	], reason='Verify that the Method Details inputs are NO LONGER hidden')
	t.test()


# Verify Recipient auto route preference
	t = d.getWCUnitTest('Recipient Auto Route Preference - No Preferred Route set for recipient. Recipient has address and NO fax number.')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=selenium&custom_join=selenium&where_clause=selenium&recipient_type=0&recipient_id=0&user_ac_txt=&recipient_name=&recipient_role=&method_desc=&method=&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0'), reason='Navigate to the Add Auto Route page')
	t.verifyElements([
		wcElement('xpath', '//input[@id="user_ac_txt"][@class="autocomplete selected"]'),
		wcElement('xpath', '//span[@id="method_detailPrint_label"]' + DISPLAYED + '[contains(.,"Mail to:")]'),
		wcElement('xpath', '//span[@id="method_detailPrint"]' + DISPLAYED),
		wcElement('xpath', '//span[@id="route_optionPrint_label"]' + DISPLAYED + '[contains(.,"Printer:")]'),
		wcElement('xpath', '//span[@id="route_optionPrint"]' + DISPLAYED + PRINT_ROUTEOPTION_INPUT),
		wcElement('xpath', '//span[@id="route_optionPrint"]' + DISPLAYED + '/input[@type="checkbox"][@id="print_wo_headers"]'),
	], reason="Verify the Method Details inputs are made available for PRINTING by default because the user has no fax number and no Preferred Route set in demographics")
	t.test(enterUser, 0)

 
	t = d.getWCUnitTest('Recipient Auto Route Preference - No Preferred Route set for recipient. Recipient has address and fax number.')
	t.setup(setUsrFax)
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=selenium&custom_join=selenium&where_clause=selenium&recipient_type=0&recipient_id=0&user_ac_txt=&recipient_name=&recipient_role=&method_desc=&method=&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0'), reason='Navigate to the Add Auto Route page')
	t.verifyElements([
		wcElement('xpath', '//input[@id="user_ac_txt"][@class="autocomplete selected"]'),
		wcElement('xpath', '//span[@id="method_detailFax_label"]' + DISPLAYED + '[contains(.,"Fax Number:")]'),
		wcElement('xpath', '//span[@id="method_detailFax"]' + DISPLAYED),
		wcElement('xpath', '//span[@id="route_optionFax_label"]' + DISPLAYED + '[contains(.,"Coversheet:")]'),
		wcElement('xpath', '//span[@id="route_optionFax"]' + DISPLAYED + FAX_ROUTEOPTION_INPUT),
		wcElement('xpath', '//span[@id="route_optionFax"]' + DISPLAYED + '/input[@type="checkbox"][@id="fax_wo_headers"]'),
	], reason="Verify the Method Details inputs are made available for FAXING over printing because the user now has a fax number but still has no Preferred Route set in demographics")
	t.test(enterUser, 0)

	t = d.getWCUnitTest('Recipient Auto Route Preference - Preferred Route set for recipient and has address and fax number')
	t.setup(setPrefRoute)
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor&t=Auto+Routes&opp=add&trigger_type=0&description=selenium&custom_join=selenium&where_clause=selenium&recipient_type=0&recipient_id=0&user_ac_txt=&recipient_name=&recipient_role=&method_desc=&method=&route_option=&method_detail=&method_detail_Print_input=&ar_tray_span_holder=&printer_value=printer%3A&tray_value=tray%3A&route_option_Print_input=&method_detail_Fax_input=&printer_value=coversheet%3A&tray_value=tray%3A&route_option_Fax_input=&method_detail_HL7+Send_input=NMC_HL7&method_detail_Text+Export_input=&method_detail_Dictaphone+HL7_input=NMC_HL7&method_detail_ORDER+RESULTS+HL7_input=NMC_HL7&method_detail_Public+Health+Surveillance_input=NMC_HL7&method_detail_OSHA_input=NMC_HL7&method_detail_Work+Comp_input=NMC_HL7&method_detail_Incident_input=SS_ELIG&method_detail_XDS+Registry_input=&method_detail_Word2TIFF+FTP_input=SS_ELIG&method_detail_Remote+IFQ+Batch_input=NMC_POST&method_detail_Scripted+Export_input=SS_ELIG&route_optionScripted+Export_input=&method_detail_MDM+Reports+HL7_input=NMC_HL7&method_detail_Immunization+Export_input=NMC_HL7&method_detail_Kareo+Billing_input=NMC_HL7&method_detail_837+Professional+Claims_input=NMC_HL7&method_detail_Syndromic+Surveillance_input=NMC_HL7&method_detail_Direct+Email_input=&route_option_Direct+Email_input=from%3Aselenium%40mieweb.com&send_criteria_desc=All+Revisions&send_criteria=0&no_auto_resend_desc=Yes&no_auto_resend=0'), reason='Navigate to the Add Auto Route page')
	t.verifyElements([
		wcElement('xpath', '//input[@id="user_ac_txt"][@class="autocomplete selected"]'),
		wcElement('xpath', '//span[@id="method_detailDirect Email_label"]' + DISPLAYED + '[contains(.,"Direct Address:")]'),
		wcElement('xpath', '//span[@id="method_detailDirect Email"]' + DISPLAYED),
	], reason="Verify the Method Details inputs are made available for DIRECT EMAIL over faxing or printing because the user now has a Preferred Route set in demographics")
	t.teardown(cleanDB)
	t.test(enterUser, 0)

 
# Add an Auto Route
	t = d.getWCUnitTest('Add an Auto Route')
	t.setup(addAutoRoute)
	t.setup(clickSave)
	t.verifyElements([
		wcElement('xpath', MAIN + '/center[contains(.,"Auto Route Added")]'),
	], reason='Verify the Success message')
	t.verifyElements([
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Trigger_20Type_cell"][contains(.,"On Document Add")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Description_cell"][contains(.,"TestRoute")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Where_20Clause_cell"]/span[contains(.,"0 AND d.doc_type IN")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Where_20Clause_cell"]/span[contains(.,"Custom Join: LEFT JOIN patient_mrns")][contains(.,"Where Clause: 0 AND d.doc_type IN")][contains(.,"7600A")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Recipient_cell"][contains(.,"Family Physician")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Method_cell"][contains(.,"")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Detail_cell"][contains(.,"")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"][contains(.,"")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Send_20On_cell"][contains(.,"Final Signed Only")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"]/a[contains(.,"Edit")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"]/a[contains(.,"Delete")]'),
		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify that the auto route is listed in the listview and reflected in the footer')
	t.test()


# Edit an Auto Route
	t = d.getWCUnitTest('Edit an Auto Route')
	t.setup(editAutoRoute, 0)
	t.setup(clickSave)
	t.verifyElements([
		wcElement('xpath', MAIN + '/center[contains(.,"Auto Route Edited")]'),
	], reason='Verify the Success message')
	t.verifyElements([
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Trigger_20Type_cell"][contains(.,"On Encounter Add")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Description_cell"][contains(.,"RouteTest")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Where_20Clause_cell"]/span[contains(.,"0 AND d.doc_type IN")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Where_20Clause_cell"]/span[contains(.,"Custom Join: LEFT JOIN patient_mrns")][contains(.,"Where Clause: 0 AND d.doc_type IN")][contains(.,"7600B")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Recipient_cell"]/a[@class="link"][contains(@onclick,"var Popup=WC_Popup")][contains(.,"Sample, John M.")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Method_cell"][contains(.,"Fax")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Detail_cell"][contains(.,"(260) 459-6271")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"][contains(.,"")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Send_20On_cell"][contains(.,"Final Signed Only")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"]/a[contains(.,"Edit")]'),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"]/a[contains(.,"Delete")]'),
		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify that the auto route is listed with changes in the listview and reflected in the footer')
	t.test()

# Delete an Auto Route
	t = d.getWCUnitTest('Delete an Auto Route')
	t.setup(deleteAutoRoute)
	t.verifyElements([
		wcElement('xpath', MAIN + '/center[contains(.,"Auto Route Deleted")]'),
	], reason='Verify the Success message')
	t.verifyElements([
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Trigger_20Type_cell"][contains(.,"On Encounter Add")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Description_cell"][contains(.,"TestRoute1") or contains(.,"RouteTest")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Where_20Clause_cell"]/span[contains(.,"0 AND d.doc_type IN")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Where_20Clause_cell"]/span[contains(.,"Custom Join: LEFT JOIN patient_mrns")][contains(.,"Where Clause: 0 AND d.doc_type IN")][contains(.,"7600B")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Recipient_cell"]/a[@class="link"][contains(@onclick,"var Popup=WC_Popup")][contains(.,"Sample, John M.")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Method_cell"][contains(.,"Fax")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Detail_cell"][contains(.,"(260) 459-6271")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"][contains(.,"")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Send_20On_cell"][contains(.,"All Revisions")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"]/a[contains(.,"Edit")]', exists=False),
		wcElement('xpath', MAIN + LV_BODY + '/tr[1]/td[@class="da__route_Options_cell"]/a[contains(.,"Delete")]', exists=False),
		wcElement('xpath', MAIN + LV_FOOTER + '/tr/td[contains(.,"Displaying") or contains(.,"Results")]'),
	], reason='Verify that the auto route is listed with changes in the listview and reflected in the footer')
	t.teardown(cleanDB)
	t.test()



# Add AR with Custom Pending Status - User Setting Define DataSend Status ON
	t = d.getWCUnitTest('Custom Pending Status - Add an Auto Route with Define DataSend Status setting ENABLED')
	t.setup(grantCustomPendingAccess)
	t.setup(addAutoRoute)
	t.setup(addCustomStatusY)
	t.setup(clickSave)
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"][@value="Y"]'),
	], reason='Confirm that the Custom Pending Status field contains what was entered')
	t.test(openAutoRoute)
# Edit AR with Custom Pending Status - User Setting Define DataSend Status ON
	t = d.getWCUnitTest('Custom Pending Status - Edit an Auto Route with Define DataSend Status setting ENABLED')
	t.setup(editAutoRoute, 0)
	t.setup(editCustomStatus)
	t.setup(clickSave)
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"][@value="X"]'),
	], reason='Confirm that the Custom Pending Status field contains what was edited')
	t.test(openAutoRoute)
# Add AR with Custom Pending Status - User Setting Define DataSend Status OFF but Custom Pending Status should still be available
	t = d.getWCUnitTest('Custom Pending Status - Add an Auto Route with Define DataSend Status setting DISABLED but with custom pending status still available')
	t.setup(insertCustomRouteY)
	t.setup(removeCustomPendingAccess)
	t.setup(addAutoRoute)
	t.setup(addCustomStatusY)
	t.setup(clickSave)
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[@value="Y"][contains(.,"Y")][@selected=""]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[@value="X"][contains(.,"X")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[contains(.,"None (System Standard)")]'),
	], reason='Confirm that with the Define DataSend Status setting disabled the textfield is replaced by a dropdown with a "None" option and a Custom Pending Status')
	t.test(openAutoRoute)
# Edit AR with Custom Pending Status - User Setting Define DataSend Status OFF but Custom Pending Status should still be available
	t = d.getWCUnitTest('Custom Pending Status - Edit an Auto Route with Define DataSend Status setting DISABLED but with custom pending status still available')
	t.setup(editAutoRoute, 0)
	t.setup(editCustomStatus)
	t.setup(clickSave)
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[@value="Y"][contains(.,"Y")]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[@value="X"][contains(.,"X")][@selected=""]'),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[contains(.,"None (System Standard)")]'),
	], reason='Confirm that the Auto Route can be changed to another existing Custom Pending Status from a dropdown')
	t.teardown(cleanDB)
	t.test(openAutoRoute)

# Remove Custom Pending Status - User Setting Define DataSend Status ON
	t = d.getWCUnitTest('Custom Pending Status - Remove Custom Pending Status from a Auto Route with Define DataSend Status setting DISABLED but with custom pending status still available until removed from the route')
	t.setup(insertCustomRouteY)
	t.setup(addAutoRoute)
	t.setup(addCustomStatusY)
	t.setup(clickSave)
	t.setup(editAutoRoute, 0)
	t.setup(lambda d: d.enterFormData('None (System Standard)', id='custom_pending'))
	t.setup(clickSave)
	t.setup(removeCustomRouteY)
	t.verifyElements([
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/input[@type="text"][@id="custom_pending"]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[@value="Y"][contains(.,"Y")]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[@value="X"][contains(.,"X")][@selected=""]', exists=False),
		wcElement('xpath', MAIN_FRM + AR_EDIT_TABLE + '/td[@class="value"]/select[@id="custom_pending"]/option[contains(.,"None (System Standard)")]', exists=False),
	], reason='Change the Custom Pending Status to "None" which removes any Custom Pending Status if it does not exist within any other Auto Route')
	t.teardown(cleanDB)
	t.test(openAutoRoute)

# Auto Route Execution - Family Physician Auto Route
	t = d.getWCUnitTest('Auto Route Execution - Family Physician Auto Route')
	t.setup(executionConfig, reason ='Insert/Update all routes and settings necessary to auto route documents')
	t.setup(lambda d: d.navigate('?chart&opp=add&t=Documents&v=list&f=chart&s=doc&pat_id=18&method=text&allow_disabled=1&user_search=Selenium%2C+Selenium&origin_id=8&doc_type=WCDOCNOT&service_dateMONTH=02&service_dateDAY=02&service_dateYEAR=2007&service_location=OFFICE&subject=&encounter_id=&encounter_ac_hidden=&encounter_ac_txt=&LinkOrders_hidden=&LinkOrders_txt=&inc_id=&doc_inc_id_ac_hidden=&doc_inc_id_ac_txt=&ccuserlist=&file=I+saw+this+patient+today&edit_start=2007-02-02+09%3A15%3A00&submit_document=Add+Document'), reason='Add a "Doctor Note" document')
	t.setup(checkDocProp, reason='Navigate to the properties page for the document to confirm auto routing')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Selenium")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for Selenium as a Fax and is set to a Pending status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Sample, John")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for John Sample as a Fax and is set to a Pending status')
	t.teardown(removeDocs)
	t.test(checkDocProp)

# Auto Route Execution - All Contacts Auto Route
	t = d.getWCUnitTest('Auto Route Execution - All Contacts Auto Route')
	t.setup(lambda d: d.navigate('?chart&opp=add&f=chart&s=doc&pat_id=18&method=text&allow_disabled=1&user_search=Selenium%2C+Selenium&origin_id=8&doc_type=BILLINGQ&service_dateMONTH=02&service_dateDAY=02&service_dateYEAR=2007&service_location=OFFICE&subject=&encounter_id=&encounter_ac_hidden=&encounter_ac_txt=&LinkOrders_hidden=&LinkOrders_txt=&inc_id=&doc_inc_id_ac_hidden=&doc_inc_id_ac_txt=&ccuserlist=&file=Why+am+I+being+billed+for+this&edit_start=2007-02-02+09%3A15%3A00&submit_document=Add+Document'), reason='Add a "Billing Question" document')
	t.setup(checkDocProp, reason='Navigate to the properties page for the document to confirm auto routing')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Selenium")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for Selenium as a Fax and is set to a Pending status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Thomas, Alice")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for Alice Thomas as a Fax and is set to a Pending status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Hart, William")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for William Hart as a Fax and is set to a Pending status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Sample, John")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for John Sample as a Fax and is set to a Pending status')
	t.teardown(removeDocs)
	t.test(checkDocProp)

# Auto Route Execution - Self Auto Route
	t = d.getWCUnitTest('Auto Route Execution - Self Auto Route')
	t.setup(lambda d: d.navigate('?chart&opp=add&f=chart&s=doc&pat_id=18&method=text&allow_disabled=1&user_search=Selenium%2C+Selenium&origin_id=8&doc_type=ADVDIRECT&service_dateMONTH=02&service_dateDAY=02&service_dateYEAR=2007&service_location=OFFICE&subject=&encounter_id=&encounter_ac_hidden=&encounter_ac_txt=&LinkOrders_hidden=&LinkOrders_txt=&inc_id=&doc_inc_id_ac_hidden=&doc_inc_id_ac_txt=&ccuserlist=&file=DNR&edit_start=2007-02-02+09%3A15%3A00&submit_document=Add+Document'), reason='Add a "Advanced Directives" document')
	t.setup(checkDocProp, reason='Navigate to the properties page for the document to confirm auto routing')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Selenium")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for Selenium as a Fax and is set to a Pending status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Hart, William")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for William Hart as a Fax and is set to a Pending status')
	t.teardown(removeDocs)
	t.test(checkDocProp)

# Auto Route Execution - User and Encounter User Auto Routes
	# DO NOT CHANGE THE ORDER - THIS MUST BE THE LAST EXECUTION UNIT PRIOR TO THE RESEND UNIT
	t = d.getWCUnitTest('Auto Route Execution - User and Encounter User Auto Routes')
	t.setup(lambda d: d.navigate('?f=chart&opp=add&f=chart&s=doc&pat_id=18&method=text&allow_disabled=1&user_search=Selenium%2C+Selenium&origin_id=8&doc_type=NNOTE&service_dateMONTH=02&service_dateDAY=02&service_dateYEAR=2007&service_location=OFFICE&subject=&encounter_id=11&encounter_ac_hidden=11+02-25-2010+%28Office+Visit-Initial%29+Hart%2C+William+S.&encounter_ac_txt=11+02-25-2010+%28Office+Visit-Initial%29+Hart%2C+William+S.&LinkOrders_hidden=&LinkOrders_txt=&inc_id=&doc_inc_id_ac_hidden=&doc_inc_id_ac_txt=&ccuserlist=&file=I+am+a+Nursing+Note&edit_start=2007-02-02+09%3A15%3A00&submit_document=Add+Document'), reason='Add a "Phone Note" document')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Selenium")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for Selenium as a Fax and is set to a Pending status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Butler, Internist")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm "Current Routes" contains a route created for Internist Butler as a Fax and is set to a Pending status')
	t.test(checkDocProp)

# Auto Route Execution - Re-send the Auto Routes
	t = d.getWCUnitTest('Re-send the Auto Route')
	t.setup(prepResendRoutes)
	t.setup(checkDocProp)
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr/td[@class="doc__curr__routes_Recipient_cell"][contains(.,"Butler, Internist")]/following-sibling::td[@class="doc__curr__routes_Method_cell"][contains(.,"Fax")]/following-sibling::td[@class="doc__curr__routes_Status_cell"][contains(.,"Pending")]'), reason='Confirm the route has been set back to Pending status')
	t.test(clickResend)

# Auto Route Execution - Click to Error the Auto Routes
	t = d.getWCUnitTest('Click to Error the Auto Route')
	t.setup(checkDocProp)
	t.verifyElements([
		wcElement('xpath', '//div[@id="wc_main"]/center[contains(.,"Route ")][contains(.," has been errored")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Status_cell"][contains(.,"Error")]'),
	], reason='Confirm the route has been set to an Error status')
	t.verifyElements([
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Acknowledge the error on this Document Route and move the item to the completed list in the Queue")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Force a resend of this Document Route")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Documents with active Routes will be automatically resent after each Edit. A deactivated Route will not receive updates to the Document unless manually reactivated.")]'),
	], reason='Confirm that the Options links are or are not present')
	t.test(clickError)

# Auto Route Execution - Acknowledge the Auto Routes
	t = d.getWCUnitTest('Acknowledge the Auto Route')
	t.setup(checkDocProp)
	t.verifyElements([
		wcElement('xpath', '//div[@id="wc_main"]/center[contains(.,"Route ")][contains(.," has been acknowledged")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Status_cell"][contains(.,"Acknowledged")]'),
	], reason='Confirm the route has been set to an Error status')
	t.verifyElements([
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Acknowledge the error on this Document Route and move the item to the completed list in the Queue")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Force a resend of this Document Route")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]'),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Documents with active Routes will be automatically resent after each Edit. A deactivated Route will not receive updates to the Document unless manually reactivated.")]'),
	], reason='Confirm that the Options links are or are not present')
	t.test(clickAcknowledge)

# Auto Route Execution - Deactivate the Auto Routes
	t = d.getWCUnitTest('Deactivate the Auto Route')
	t.setup(checkDocProp)
	t.verifyElements(wcElement('xpath', '//div[@id="wc_main"]/center[contains(.,"Route ")][contains(.," has been deactivated")]'), reason='Confirm the route has been set to an Error status')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr[2]', exists=False), reason='Confirm that there is only one route remaining in Current Routes')
	t.verifyElements([
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Acknowledge the error on this Document Route and move the item to the completed list in the Queue")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Force a resend of this Document Route")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Documents with active Routes will be automatically resent after each Edit. A deactivated Route will not receive updates to the Document unless manually reactivated.")]', exists=False),
	], reason='Confirm that the Options links are or are not present')
	t.test(clickDeactivate)

# Auto Route Execution - Cancel the Auto Routes
	t = d.getWCUnitTest('Cancel the Auto Route')
	t.setup(checkDocProp)
	t.verifyElements(wcElement('xpath', '//div[@id="wc_main"]/center[contains(.,"Route ")][contains(.," has been canceled")]'), reason='Confirm the route has been canceled')
	t.verifyElements(wcElement('xpath', MAIN + '/table[@class="lv_root"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_doc_curr_routes_span_title"][contains(.,"Current Routes for Document")]/ancestor::legend/following-sibling::div[@id="lv_doc_curr_routes_span"]/table[@class="newui zebra"]/tbody/tr', exists=False), reason='Confirm that there are NO routes remaining in Current Routes')
	t.verifyElements([
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Acknowledge")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Acknowledge the error on this Document Route and move the item to the completed list in the Queue")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Resend")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Force a resend of this Document Route")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]', exists=False),
		wcElement('xpath', '//td[@class="doc__curr__routes_Options_cell"]/a[contains(.,"Deactivate")]/following-sibling::span[@class="fa wc_help"][contains(@onmouseover,"Documents with active Routes will be automatically resent after each Edit. A deactivated Route will not receive updates to the Document unless manually reactivated.")]', exists=False),
	], reason='Confirm that the Options links are or are not present')
	t.test(clickCancel)
