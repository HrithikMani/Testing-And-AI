"""
@owners: dhaneline
"""
from wcunittest import wcElement, wcDBRecord

# Verify obs code page
# Verify add obs code
# Verify edit obs code
# Verify delete obs code
# Verify custom range
# Verify view
# Verify merge
# Add an obs code
# Search an obs code
# Edit an obs code
# Delete an obs code
# Merge an obs code

def clickElement(d, text):
	d.clickElement(text=text)

def searchObs(d, data):
	d.navigate('?f=admin&subfunc=obscodes_manager&obscodes_search=Go&select_criteria=c&select_text=kessel&select_by=o.obs_name&select_interface=')

def deleteObs(d, data):
	d.clickElement(xpath='//td[contains(.,"Kessel")]/following-sibling::td[@class="obscodes_Options_cell"]/a[contains(.,"Delete")]')
	d.clickElement(xpath='//input[@type="SUBMIT"][@name="obs_submit"][@value="Delete"]')

def editObs(d, data):
	d.clickElement(xpath='//td[contains(.,"Kessel")]/following-sibling::td[@class="obscodes_Options_cell"]/a[contains(.,"Edit")]')
	d.enterFormData('kesselrun', id='obs_name', clear=True)
	d.enterFormData('0-12, >12', id='obs_range')
	d.clickElement(xpath='//input[@name="obs_submit"][@value="Save"]')


def main(d, WCURL):
	t = d.getWCUnitTest('Verify the Observation Code Manager Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Display Flowsheets")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Flowsheets System Report")]'),
	], reason='Make sure the quick links in the upper right corner of the page are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]//fieldset/legend[@class="dlgtitle"]/span[contains(.,"Search")]'),
		wcElement('xpath', '//td[@class="field"]/span[@class="bold"][contains(.,"Criteria")]'),
		wcElement('xpath', '//td[@class="field"]/span[@class="bold"][contains(.,"Search")]'),
		wcElement('xpath', '//td[@class="field"]/span[@class="bold"][contains(.,"By")]'),
		wcElement('xpath', '//td[@class="field"]/span[@class="bold"][contains(.,"Interface")]'),
		wcElement('xpath', '//td[@class="folder"]/select[@id="select_criteria"]'),
		wcElement('xpath', '//td[@class="value"]/input[@id="select_text"]'),
		wcElement('xpath', '//td[@class="folder"]/select[@id="select_by"]'),
		wcElement('xpath', '//td[@class="folder"]/select[@id="select_interface"]'),
		wcElement('xpath', '//td[@class="folder"]/input[@id="obscodes_search"]'),
	], reason='Make sure the Search elements are all present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="lv_root"][@id="lv_root_Observation_20Codes"]//fieldset/legend/font/span[@id="lv_obscodes_show_link"][@class="LVTitle"]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Obs_20Code_header"]/a[@class="link"][contains(.,"Obs Code")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Obs_20Name_header"]/a[@class="link"][contains(.,"Obs Name")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Interface_header"]/a[@class="link"][contains(.,"Interface")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_HL7_20Code_header"][contains(.,"HL7 Code")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_LOINC_20Code_header"]/a[@class="link"][contains(.,"LOINC Code")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Template_20ID_header"]/a[@class="link"][contains(.,"Template ID")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Units_header"]/a[@class="link"][contains(.,"Units")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Target_20Type_header"]/a[@class="link"][contains(.,"Target Type")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Target_header"]/a[@class="link"][contains(.,"Target")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Obs_20Range_header"]/a[@class="link"][contains(.,"Obs Range")]'),
		wcElement('xpath', '//thead/tr/th[@class="obscodes_Options_header"][contains(.,"Options")]'),
		wcElement('xpath', '//table[@class="lv_root"][@id="lv_root_Observation_20Codes"]//fieldset/div[@id="lv_obscodes_span"]/table[@class="newui zebra"][@data-tttype="sticky"][@border="1"]/tbody/tr/td'),
		wcElement('xpath', '//table[@class="lv_root"][@id="lv_root_Observation_20Codes"]//fieldset/div[@id="lv_obscodes_span"]/table[@class="newui zebra"][@data-tttype="sticky"][@border="1"]/tfoot/tr/td[contains(.,"Displaying")]/a[@class="link"][contains(.,"Next")]/following-sibling::a[contains(.,"Show All")]'),
	], reason='Make sure the Observation listview table and all elements are present')
	t.test()

	t = d.getWCUnitTest('Verify Add Observation Code Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager&opp=add'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Display Flowsheets")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Flowsheets System Report")]'),
	], reason='Make sure the quick links in the upper right corner of the page are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/legend/span[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[contains(.,"Observation Name")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="text"][@id="obs_name"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Result Type")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//select[@id="obs_type"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="DECIMAL"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="TEXT"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="DATETIME"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="LIST"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="CWE"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td[contains(.,"Result Type Group")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/script[contains(.,"updateObsGroup")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Sexual Orientation")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Gender Identity")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Birth Sex")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Race (Hierarchical Code)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Ethnicity (Hierarchical Code)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Race (Unique ID)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Ethnicity (Unique ID)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"LOINC Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="loinc_num"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Template ID")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="template_id"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/span[@id="template_id_ac_span"]/input[@id="template_id_input"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/script[contains(.,"template_id_ac.SetFixedValues")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Display Units")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"per unit system")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Display Units")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/span[@class="bold"][contains(.,"English:")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/input[@id="locale_unit_input_English"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/span[@class="bold"][contains(.,"Metric:")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/input[@id="locale_unit_input_Metric"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Default Add Unit")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Default Add Unit")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/span[@id="obs_units_ac_span"]/input[@id="obs_units_txt"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Observation Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Observation Range")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="obs_range"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Target")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Target")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]/option[@value="abrange"][contains(.,"Abnormal Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]/option[@value="range"][contains(.,"Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]/option[@value="target"][contains(.,"Target")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Conditional")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//textarea[@id="conditional"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Calculation")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/textarea[@id="calculation"]'),
	], reason='Make sure the Add Observation labels and inputs are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_fieldlist"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_addfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_delfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_undelfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_editfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/div[@id="le_obs_codes_translations_RecordList_maincontainer"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/div[@id="le_obs_codes_translations_RecordList_maincontainer"]/table/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"HL7 Translations")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/div[@id="le_obs_codes_translations_RecordList_maincontainer"]/table/tbody/tr/td/fieldset/table/tbody/tr/td[@id="le_obs_codes_translations_display"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_fieldlist"][contains(@value, "SUBSTRING")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_addfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_delfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_undelfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_editfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//div[@id="le_obs_codes_translations_RecordList_maincontainer"]/table//legend[@class="dlgtitle"]/span[contains(.,"HL7 Translations")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//tr/td[@id="le_obs_codes_translations_display"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//tr/td[@class="value"]/span[@id="le_obs_codes_translations_RecordList_inputspan"]//table[@class="dlg_root"]//table//td[@class="value"]//table[@class="dlg_root"]//table//td[@class="HeaderCell"]/label[contains(.,"Interface Name")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_translations_trans_from_inp_head_td"]/label[@for="le_obs_codes_translations_trans_from_value"][contains(.,"HL7 Code")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="HeaderCell"]/center/span[@id="obs_codes_translations_RecordList_addedit_title"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_inp_td"]/span[@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value_input_span"]/input[@type="text"][@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value"][@title="Interface Name"][@onblur="if(this.value.length>0) add_Record(obs_codes_translations_RecordList,true);"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_inp_td"]/span[@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value_input_span"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"SUBSTRING")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_trans_from_inp_td"]/span[@id="le_obs_codes_translations_trans_from_value_input_span"]/input[@type="text"][@id="le_obs_codes_translations_trans_from_value"][@title="HL7 Code"][@onblur="if(this.value.length>0) add_Record(obs_codes_translations_RecordList,true);"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_trans_from_inp_td"]/span[@id="le_obs_codes_translations_trans_from_value_input_span"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"trans_from")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_add_span"]/span/input[@type="button"][@id="le_obs_codes_translations_button"][@value="Add"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_add_span"]/span/input[@type="button"][@id="le_obs_codes_translations_button"][@value="Clear"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"obs_codes_translations_RecordList_add_span")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_edit_span"]/span/input[@type="button"][@value="OK"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_edit_span"]/span/input[@type="button"][@value="Cancel"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"obs_codes_translations_RecordList_edit_span")]'),
	], reason='Make sure the HL7 Translations elements are present in the listview')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_obs_result_inp_head_td"]/label[@for="le_obs_codes_codes_list_obs_result_value"][contains(., "Value")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_obs_result_desc_inp_head_td"]/label[@for="le_obs_codes_codes_list_obs_result_desc_value"][contains(., "Display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_concept_id_inp_head_td"]/label[@for="le_obs_codes_codes_list_concept_id_value"][contains(., "Concept ID")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_sort_order_inp_head_td"]/label[@for="le_obs_codes_codes_list_sort_order_value"][contains(., "Sort Order")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"]/center/span[@id="obs_codes_codes_list_RecordList_addedit_title"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_id_value"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_id_display"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_id_value")][contains(., "le_obs_codes_codes_list_id_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_obs_code_value"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_obs_code_display"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_obs_code_value")][contains(., "le_obs_codes_codes_list_obs_code_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_obs_result_inp_td"]/span[@id="le_obs_codes_codes_list_obs_result_value_input_span"]/input[@id="le_obs_codes_codes_list_obs_result_value"][@title="Value"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_obs_result_value")][contains(., "le_obs_codes_codes_list_obs_result_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_obs_result_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_obs_result_desc_inp_td"]/span[@id="le_obs_codes_codes_list_obs_result_desc_value_input_span"]/input[@id="le_obs_codes_codes_list_obs_result_desc_value"][@title="Display"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_obs_result_desc_value")][contains(., "le_obs_codes_codes_list_obs_result_desc_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_obs_result_desc_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_concept_id_inp_td"]/span[@id="le_obs_codes_codes_list_concept_id_value_input_span"]/input[@id="le_obs_codes_codes_list_concept_id_value"][@title="SNOMED Concept ID"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_concept_id_value")][contains(., "le_obs_codes_codes_list_concept_id_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_concept_id_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_sort_order_inp_td"]/span[@id="le_obs_codes_codes_list_sort_order_value_input_span"]/input[@id="le_obs_codes_codes_list_sort_order_value"][@title="Sort Order"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_sort_order_value")][contains(., "le_obs_codes_codes_list_sort_order_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_sort_order_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_add_span"]/span/input[@id="le_obs_codes_codes_list_button"][@type="button"][@value="Add"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_add_span"]/span/input[@id="le_obs_codes_codes_list_button"][@type="button"][@value="Clear"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_label_buttons")][contains(.,"obs_codes_codes_list_RecordList_add_span")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_edit_span"]/span/input[@type="button"][@value="OK"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_edit_span"]/span/input[@type="button"][@value="Cancel"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_label_buttons")][contains(.,"obs_codes_codes_list_RecordList_edit_span")]'),
		wcElement('xpath', '//div[contains(.,"Custom Discrete Values")]/following-sibling::script[contains(.,"var obs_codes_codes_list_RecordList")][contains(.,"le_obs_codes_codes_list_id_value")][contains(.,"le_obs_codes_codes_list_obs_code_value")][contains(.,"le_obs_codes_codes_list_obs_result_value")][contains(.,"le_obs_codes_codes_list_obs_result_desc_value")][contains(.,"le_obs_codes_codes_list_concept_id_value")][contains(.,"le_obs_codes_codes_list_sort_order_value")]'),
		wcElement('xpath', '//div[contains(.,"Custom Discrete Values")]/following-sibling::script[contains(.,"obs_codes_codes_list_onLEInit")]'),
		wcElement('xpath', '//div[contains(.,"Custom Discrete Values")]/following-sibling::script[contains(.,"document.getElementById")][contains(.,"le_obs_codes_codes_list_concept_id_inp_td")]'),
	], reason='Make sure the Custom Discrete Value elements are present in the listview')
	t.verifyElements([
		wcElement('xpath', '//div[@class="buttonbar"]/input[@type="submit"][@name="obs_submit"][@value="Save"]'),
		wcElement('xpath', '//div[@class="buttonbar"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]'),
	], reason='Make sure the Save and Cancel buttons are present')
	t.test()

	t = d.getWCUnitTest('Verify Edit Observation Code Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager&opp=edit&obs_old_code=1'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Display Flowsheets")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Flowsheets System Report")]'),
	], reason='Make sure the quick links in the upper right corner of the page are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/legend/span[contains(.,"Edit Observation Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[contains(.,"Observation Name")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="text"][@id="obs_name"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Result Type")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//select[@id="obs_type"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="DECIMAL"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="TEXT"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="DATETIME"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="LIST"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/select[@id="obs_type"]/option[@value="CWE"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td[contains(.,"Result Type Group")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/script[contains(.,"updateObsGroup")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Sexual Orientation")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Gender Identity")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Birth Sex")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Race (Hierarchical Code)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Ethnicity (Hierarchical Code)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Race (Unique ID)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//tr[@class="observation_group hidden"]/td/select[@id="obs_group"]/option[contains(.,"Ethnicity (Unique ID)")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"LOINC Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="loinc_num"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Template ID")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="template_id"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/span[@id="template_id_ac_span"]/input[@id="template_id_input"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/script[contains(.,"template_id_ac.SetFixedValues")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Display Units")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"per unit system")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Display Units")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/span[@class="bold"][contains(.,"English:")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/input[@id="locale_unit_input_English"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/span[@class="bold"][contains(.,"Metric:")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/input[@id="locale_unit_input_Metric"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Default Add Unit")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Default Add Unit")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/span[@id="obs_units_ac_span"]/input[@id="obs_units_txt"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Observation Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Observation Range")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="obs_range"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Target")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Target")]/span[@class="fa wc_help"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]/option[@value="abrange"][contains(.,"Abnormal Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]/option[@value="range"][contains(.,"Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@id="target"]/following-sibling::select[@id="target_type"]/option[@value="target"][contains(.,"Target")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Conditional")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//textarea[@id="conditional"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td[contains(.,"Calculation")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/textarea[@id="calculation"]'),
	], reason='Make sure the Edit Observation labels and inputs are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_fieldlist"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_addfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_delfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_undelfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_editfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/div[@id="le_obs_codes_translations_RecordList_maincontainer"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/div[@id="le_obs_codes_translations_RecordList_maincontainer"]/table/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"HL7 Translations")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/div[@id="le_obs_codes_translations_RecordList_maincontainer"]/table/tbody/tr/td/fieldset/table/tbody/tr/td[@id="le_obs_codes_translations_display"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_fieldlist"][contains(@value, "SUBSTRING")]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_addfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_delfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_undelfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//td/input[@type="hidden" or @type="HIDDEN"][@id="le_obs_codes_translations_RecordList_editfield"]'),
		wcElement('xpath', '//table[@class="dlg_root"]//div[@id="le_obs_codes_translations_RecordList_maincontainer"]/table//legend[@class="dlgtitle"]/span[contains(.,"HL7 Translations")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//tr/td[@id="le_obs_codes_translations_display"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//tr/td[@class="value"]/span[@id="le_obs_codes_translations_RecordList_inputspan"]//table[@class="dlg_root"]//table//td[@class="value"]//table[@class="dlg_root"]//table//td[@class="HeaderCell"]/label[contains(.,"Interface Name")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_translations_trans_from_inp_head_td"]/label[@for="le_obs_codes_translations_trans_from_value"][contains(.,"HL7 Code")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="HeaderCell"]/center/span[@id="obs_codes_translations_RecordList_addedit_title"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_inp_td"]/span[@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value_input_span"]/input[@type="text"][@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value"][@title="Interface Name"][@onblur="if(this.value.length>0) add_Record(obs_codes_translations_RecordList,true);"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_inp_td"]/span[@id="le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value_input_span"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"SUBSTRING")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_trans_from_inp_td"]/span[@id="le_obs_codes_translations_trans_from_value_input_span"]/input[@type="text"][@id="le_obs_codes_translations_trans_from_value"][@title="HL7 Code"][@onblur="if(this.value.length>0) add_Record(obs_codes_translations_RecordList,true);"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_translations_trans_from_inp_td"]/span[@id="le_obs_codes_translations_trans_from_value_input_span"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"trans_from")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_add_span"]/span/input[@type="button"][@id="le_obs_codes_translations_button"][@value="Add"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_add_span"]/span/input[@type="button"][@id="le_obs_codes_translations_button"][@value="Clear"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"obs_codes_translations_RecordList_add_span")]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_edit_span"]/span/input[@type="button"][@value="OK"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_translations_RecordList_edit_span"]/span/input[@type="button"][@value="Cancel"]'),
		wcElement('xpath', '//span[contains(.,"HL7 Translations")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"obs_codes_translations_RecordList_edit_span")]'),
	], reason='Make sure the HL7 Translations elements are present in the listview')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_obs_result_inp_head_td"]/label[@for="le_obs_codes_codes_list_obs_result_value"][contains(., "Value")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_obs_result_desc_inp_head_td"]/label[@for="le_obs_codes_codes_list_obs_result_desc_value"][contains(., "Display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_concept_id_inp_head_td"]/label[@for="le_obs_codes_codes_list_concept_id_value"][contains(., "Concept ID")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_codes_codes_list_sort_order_inp_head_td"]/label[@for="le_obs_codes_codes_list_sort_order_value"][contains(., "Sort Order")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="HeaderCell"]/center/span[@id="obs_codes_codes_list_RecordList_addedit_title"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_id_value"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_id_display"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_id_value")][contains(., "le_obs_codes_codes_list_id_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_obs_code_value"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_codes_codes_list_obs_code_display"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_obs_code_value")][contains(., "le_obs_codes_codes_list_obs_code_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_obs_result_inp_td"]/span[@id="le_obs_codes_codes_list_obs_result_value_input_span"]/input[@id="le_obs_codes_codes_list_obs_result_value"][@title="Value"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_obs_result_value")][contains(., "le_obs_codes_codes_list_obs_result_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_obs_result_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_obs_result_desc_inp_td"]/span[@id="le_obs_codes_codes_list_obs_result_desc_value_input_span"]/input[@id="le_obs_codes_codes_list_obs_result_desc_value"][@title="Display"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_obs_result_desc_value")][contains(., "le_obs_codes_codes_list_obs_result_desc_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_obs_result_desc_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_concept_id_inp_td"]/span[@id="le_obs_codes_codes_list_concept_id_value_input_span"]/input[@id="le_obs_codes_codes_list_concept_id_value"][@title="SNOMED Concept ID"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_concept_id_value")][contains(., "le_obs_codes_codes_list_concept_id_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_concept_id_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_codes_codes_list_sort_order_inp_td"]/span[@id="le_obs_codes_codes_list_sort_order_value_input_span"]/input[@id="le_obs_codes_codes_list_sort_order_value"][@title="Sort Order"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_codes_codes_list")][contains(., "le_obs_codes_codes_list_sort_order_value")][contains(., "le_obs_codes_codes_list_sort_order_display")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="le_obs_codes_codes_list_sort_order_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_add_span"]/span/input[@id="le_obs_codes_codes_list_button"][@type="button"][@value="Add"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_add_span"]/span/input[@id="le_obs_codes_codes_list_button"][@type="button"][@value="Clear"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_label_buttons")][contains(.,"obs_codes_codes_list_RecordList_add_span")]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_edit_span"]/span/input[@type="button"][@value="OK"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_codes_codes_list_RecordList_edit_span"]/span/input[@type="button"][@value="Cancel"]'),
		wcElement('xpath', '//span[contains(.,"Custom Discrete Values")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_label_buttons")][contains(.,"obs_codes_codes_list_RecordList_edit_span")]'),
		wcElement('xpath', '//div[contains(.,"Custom Discrete Values")]/following-sibling::script[contains(.,"var obs_codes_codes_list_RecordList")][contains(.,"le_obs_codes_codes_list_id_value")][contains(.,"le_obs_codes_codes_list_obs_code_value")][contains(.,"le_obs_codes_codes_list_obs_result_value")][contains(.,"le_obs_codes_codes_list_obs_result_desc_value")][contains(.,"le_obs_codes_codes_list_concept_id_value")][contains(.,"le_obs_codes_codes_list_sort_order_value")]'),
		wcElement('xpath', '//div[contains(.,"Custom Discrete Values")]/following-sibling::script[contains(.,"obs_codes_codes_list_onLEInit")]'),
		wcElement('xpath', '//div[contains(.,"Custom Discrete Values")]/following-sibling::script[contains(.,"document.getElementById")][contains(.,"le_obs_codes_codes_list_concept_id_inp_td")]'),
	], reason='Make sure the Custom Discrete Value elements are present in the listview')
	t.verifyElements([
		wcElement('xpath', '//div[@class="buttonbar"]/input[@type="submit"][@name="obs_submit"][@value="Save"]'),
		wcElement('xpath', '//div[@class="buttonbar"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]'),
	], reason='Make sure the Save and Cancel buttons are present')
	t.test()

	t = d.getWCUnitTest('Verify Delete Observation Code Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager&opp=delete&obs_old_code=1'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Display Flowsheets")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Flowsheets System Report")]'),
	], reason='Make sure the quick links in the upper right corner of the page are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/legend/span[contains(.,"Delete Observation Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Template ID")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target Type")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Interface")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Conditional")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Calculation")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target Type")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
	], reason='Make sure the Delete Observation fields are present')

	t.verifyElements([
		wcElement('xpath', '//div[@class="center"]/input[@type="SUBMIT"][@name="obs_submit"][@value="Delete"]'),
		wcElement('xpath', '//div[@class="center"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]'),
	], reason='Make sure the Save and Cancel buttons are present')
	t.test()

	t = d.getWCUnitTest('Verify Custom Range Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager&opp=custom_range&obs_old_code=1'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Display Flowsheets")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Flowsheets System Report")]'),
		wcElement('xpath', '//div[@class="links_right"]/following-sibling::div/a[contains(.,"Back to Observation Codes")]'),
	], reason='Make sure the quick links in the upper right corner of the page are present')
	t.verifyElements([
		wcElement('xpath', '//div[@class="center"][contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form[@action="webchart.cgi"][@method="POST"][@onsubmit="return miecgictrl.formSubmit(this);"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@value="obscodes_manager"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="custom_range"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="custom_range"][2]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="obs_old_code"][@value="1"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="le_obs_ranges_RecordList_fieldlist"][contains(@value,"o.range_id")]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="le_obs_ranges_RecordList_addfield"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="le_obs_ranges_RecordList_delfield"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="le_obs_ranges_RecordList_undelfield"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/input[@type="hidden" or @type="HIDDEN"][@name="le_obs_ranges_RecordList_editfield"][@size="100"]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/div[@id="le_obs_ranges_RecordList_maincontainer"][@style="position: relative"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Observation Custom Ranges")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table/tbody/tr/td[@id="le_obs_ranges_display"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table/tbody/tr/td[@class="value"]/span[@id="le_obs_ranges_RecordList_inputspan"]/table/tbody/tr/td/fieldset/table/tbody/tr/td//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="HeaderCell"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_ranges_o_criteria_code_inp_head_td"]/label[@for="le_obs_ranges_o_criteria_code_value"][contains(.,"Template Name")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_ranges_o_obs_range_inp_head_td"]/label[@for="le_obs_ranges_o_obs_range_value"][contains(.,"Range")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="HeaderCell"][@id="le_obs_ranges_o_units_inp_head_td"]/label[@for="le_obs_ranges_o_units_value"][contains(.,"Units")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="HeaderCell"]/center/span[@id="obs_ranges_RecordList_addedit_title"][contains(.,"Add")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_range_id_value"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_range_id_display"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_ranges")][contains(.,"o.range_id")][contains(.,"le_obs_ranges_o_range_id_value")][contains(.,"le_obs_ranges_o_range_id_display")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_obs_code_value"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_obs_code_display"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_make_default_js_functions")][contains(.,"obs_ranges")][contains(.,"o.obs_code")][contains(.,"le_obs_ranges_o_obs_code_value")][contains(.,"le_obs_ranges_o_obs_code_display")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_criteria_code_inp_td"]/span[@id="le_obs_ranges_o_criteria_code_value_input_span"]/script[contains(.,"le_obs_ranges_o_criteria_code_clear")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_criteria_code_inp_td"]/span[@id="le_obs_ranges_o_criteria_code_value_input_span"]/span[@id="le_obs_ranges_ac_span"]/input[@id="le_obs_ranges_o_criteria_code_value"][@class="autocomplete"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_criteria_code_inp_td"]/span[@id="le_obs_ranges_o_criteria_code_value_input_span"]/span[@id="le_obs_ranges_ac_span"]/script[contains(.,"le_obs_ranges_ac")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_criteria_code_inp_td"]/span[@id="le_obs_ranges_o_criteria_code_value_input_span"]/script[contains(.,"le_obs_ranges_o_criteria_code_set")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_obs_range_inp_td"]/span[@id="le_obs_ranges_o_obs_range_value_input_span"]/input[@id="le_obs_ranges_o_obs_range_value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_obs_range_inp_td"]/span[@id="le_obs_ranges_o_obs_range_value_input_span"]/script[contains(.,"obs_ranges")][contains(.,"o.obs_range")][contains(.,"le_obs_ranges_o_obs_range_value")][contains(.,"le_obs_ranges_o_obs_range_display")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_obs_range_inp_td"]/span[@id="le_obs_ranges_o_obs_range_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_units_inp_td"]/span[@id="le_obs_ranges_o_units_value_input_span"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_units_inp_td"]/span[@id="le_obs_ranges_o_units_value_input_span"]/input[@id="le_obs_ranges_o_units_value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_units_inp_td"]/span[@id="le_obs_ranges_o_units_value_input_span"]/script[contains(.,"obs_ranges")][contains(.,"o.units")][contains(.,"le_obs_ranges_o_units_value")][contains(.,"le_obs_ranges_o_units_display")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"][@id="le_obs_ranges_o_units_inp_td"]/span[@id="le_obs_ranges_o_units_value_display_span"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_user_id_value"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_user_id_display"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"obs_ranges")][contains(.,"o.user_id")][contains(.,"le_obs_ranges_o_user_id_value")][contains(.,"le_obs_ranges_o_user_id_display")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_enter_datetime_value"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/input[@id="le_obs_ranges_o_enter_datetime_display"][@type="hidden" or @type="HIDDEN"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"obs_ranges")][contains(.,"o.enter_datetime")][contains(.,"le_obs_ranges_o_enter_datetime_value")][contains(.,"le_obs_ranges_o_enter_datetime_display")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_ranges_RecordList_add_span"]/span/input[@id="le_obs_ranges_button"][@type="button"][@value="Add"]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_label_buttons")][contains(.,"obs_ranges_RecordList_add_span")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_ranges_RecordList_edit_span"]/span/input[@type="button"][@value="OK"][contains(@onclick,"miele_editOK")][contains(@onclick,"miele_editDone")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/span[@id="obs_ranges_RecordList_edit_span"]/span/input[@type="button"][@value="Cancel"][contains(@onclick,"miele_editDone")]'),
		wcElement('xpath', '//span[contains(.,"Observation Custom Ranges")]/parent::legend/following-sibling::table//td[@class="value"]/script[contains(.,"miele_label_buttons")][contains(.,"obs_ranges_RecordList_edit_span")]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/script[contains(.,"define_RecordField(obs_ranges_RecordList")][contains(.,"Range ID")][contains(.,"Observation Code")][contains(.,"Template Name")][contains(.,"Range")][contains(.,"Units")][contains(.,"User")][contains(.,"Create DateTime")]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/script[contains(.,"obs_ranges_onLEInit")][contains(.,"display_GenericRecordList(obs_ranges_RecordList)")]'),
		wcElement('xpath', '//div[contains(.,"Custom Ranges for INTRAVASCULAR SUPINE BP")]/following-sibling::form/div[@class="center"]/input[@type="SUBMIT"][@name="custom_range_submit"][@value="Submit"]'),
	], reason='Make sure all elements within the page are present')
	t.test()

	t = d.getWCUnitTest('Verify View Observation Code Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager&opp=view&obs_old_code=1'))
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="edit"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@value="obscodes_manager"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="view"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="obs_old_code"][@value="1"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="interface"][@value="WEBCHART"]'),
		wcElement('xpath', '//div[@id="wc_main"]/form[@action="webchart.cgi"][@method="POST"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"View Observation Code")]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"][contains(.,"INTRAVASCULAR SUPINE BP")]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Result Type")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr[@class="observation_group hidden"]/td[@class="field"][contains(.,"Result Type Group")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"LOINC Code")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Display Units")][contains(.,"per unit system")]/span[@class="fa wc_help"][contains(@onmouseover,"Specify appropriate units for displaying results in the corresponding unit systems.")][contains(@onmouseover,"The system will attempt to convert results into the given units when viewing them in the corresponding unit system.")][contains(@onmouseover,"If the system is unable to convert the result, it will be displayed exactly how it was entered.")]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="value"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]/span[@class="bold"][contains(.,"English")]/parent::td/following-sibling::td'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="value"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]/span[@class="bold"][contains(.,"Metric")]/parent::td/following-sibling::td'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Default Add Unit")]/span[@class="fa wc_help"][contains(@onmouseover,"Specify the unit to be used when adding new observations of this type")][contains(@onmouseover,"This unit will apply to the Observation Range value as well.")]/parent::td/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Range")]/span[@class="fa wc_help"][contains(@onmouseover,"Specify the appropriate range(or abnormal range) desired.")]/parent::td/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Target")]/span[@class="fa wc_help"][contains(@onmouseover,"Specify the target desired.  Use this if observation range is")]/parent::td/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="submit"][@name="obs_change"][@value="Modify"]'),
		wcElement('xpath', '//span[contains(.,"View Observation Code")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]'),
	], reason='Make sure all elements within the View Observation table are present')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/table[@class="lv_root"][@id="lv_root_HL7_20Translations"]/tbody/tr/td/fieldset/legend/font/span[@id="lv_obs_code_translations_show_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font[contains(.,"HL7 Translations")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//legend/font/span[@id="lv_obs_code_translations_show_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Show")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//legend/font/span[@id="lv_obs_code_translations_hide_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//div[@id="lv_obs_code_translations_span"]/table/thead/tr/th[@class="obs__code__translations_Interface_20Name_header"]/a[@class="link"][contains(.,"Interface Name")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//div[@id="lv_obs_code_translations_span"]/table/thead/tr/th[@class="obs__code__translations_HL7_20Code_header"]/a[@class="link"][contains(.,"HL7 Code")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//div[@id="lv_obs_code_translations_span"]/table/tbody/tr/td[@class="obs__code__translations_Interface_20Name_cell"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//div[@id="lv_obs_code_translations_span"]/table/tbody/tr/td[@class="obs__code__translations_HL7_20Code_cell"][contains(.,"INTRAVASCULAR SUPINE BP")]'),
		wcElement('xpath', '//table[@id="lv_root_HL7_20Translations"]/tbody//div[@id="lv_obs_code_translations_span"]/table/tfoot/tr/td[contains(.,"Displaying 1-")]'),
	], reason='Make sure the HL7 Translations elements are present in the listview')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/table[@class="lv_root"][@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody/tr/td/fieldset/legend/font/span[@id="lv_obs_code_obs_forms_show_link"][@class="LVTitle"][contains(.,"Flowsheets Containing This Code")]'),
		wcElement('xpath', '//table[@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody//legend/font/span[@id="lv_obs_code_obs_forms_show_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Show")]'),
		wcElement('xpath', '//table[@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody//legend/font/span[@id="lv_obs_code_obs_forms_hide_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', '//table[@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody//div[@id="lv_obs_code_obs_forms_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__obs__forms_Name_header"]/a[contains(.,"Name")]'),
		wcElement('xpath', '//table[@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody//div[@id="lv_obs_code_obs_forms_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__obs__forms_Observations_20Included_header"][contains(.,"Observations Included")]'),
		wcElement('xpath', '//table[@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody//div[@id="lv_obs_code_obs_forms_span"]/table[@class="newui zebra"]/tbody'),
		wcElement('xpath', '//table[@id="lv_root_Flowsheets_20Containing_20This_20Code"]/tbody//div[@id="lv_obs_code_obs_forms_span"]/table[@class="newui zebra"]/tfoot/tr/td[contains(.,"Results")]'),
	], reason='Make sure the elements are present in the Flowsheet Containing this Code listview')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td/table[@class="lv_root"][@id="lv_root_Custom_20Discrete_20Values"]/tbody/tr/td/fieldset/legend/font/span[@id="lv_obs_code_codes_list_show_link"][@class="LVTitle"][contains(.,"Custom Discrete Values")]'),
		wcElement('xpath', '//table[@id="lv_root_Custom_20Discrete_20Values"]/tbody//legend/font/span[@id="lv_obs_code_codes_list_show_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Show")]'),
		wcElement('xpath', '//table[@id="lv_root_Custom_20Discrete_20Values"]/tbody//legend/font/span[@id="lv_obs_code_codes_list_hide_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', '//table[@id="lv_root_Custom_20Discrete_20Values"]/tbody//div[@id="lv_obs_code_codes_list_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__codes__list_Value_header"]/a[@class="link"][contains(.,"Value")]'),
		wcElement('xpath', '//table[@id="lv_root_Custom_20Discrete_20Values"]/tbody//div[@id="lv_obs_code_codes_list_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__codes__list_Display_header"]/a[@class="link"][contains(.,"Display")]'),
		wcElement('xpath', '//table[@id="lv_root_Custom_20Discrete_20Values"]/tbody//div[@id="lv_obs_code_codes_list_span"]/table[@class="newui zebra"]/tbody'),
		wcElement('xpath', '//table[@id="lv_root_Custom_20Discrete_20Values"]/tbody//div[@id="lv_obs_code_codes_list_span"]/table[@class="newui zebra"]/tfoot/tr/td[contains(.,"Results")]'),
	], reason='Make sure the elements are present in the Custom Discrete Values listview')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//legend/font/span[@id="lv_obs_code_obs_ranges_show_link"][@class="LVTitle"][contains(.,"Observation Ranges")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//legend/font/span[@id="lv_obs_code_obs_ranges_show_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Show")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//legend/font/span[@id="lv_obs_code_obs_ranges_hide_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//div[@id="lv_obs_code_obs_ranges_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__obs__ranges_Range_header"]/a[@class="link"][contains(.,"Range")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//div[@id="lv_obs_code_obs_ranges_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__obs__ranges_Units_header"]/a[@class="link"][contains(.,"Units")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//div[@id="lv_obs_code_obs_ranges_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__obs__ranges_Criteria_20Code_header"]/a[@class="link"][contains(.,"Criteria Code")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//div[@id="lv_obs_code_obs_ranges_span"]/table[@class="newui zebra"]/tbody'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Observation_20Ranges"]/tbody//div[@id="lv_obs_code_obs_ranges_span"]/table[@class="newui zebra"]/tfoot/tr/td[contains(.,"Results")]'),
	], reason='Make sure the elements are present in the Observation Ranges listview')
	t.verifyElements([
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//legend/font/span[@id="lv_obs_code_patient_targets_show_link"][@class="LVTitle"][contains(.,"Patient Targets")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//legend/font/span[@id="lv_obs_code_patient_targets_show_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Show")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//legend/font/span[@id="lv_obs_code_patient_targets_hide_link"][@class="LVTitle"][contains(@onclick,"hideShowlistview")]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__patient__targets_Patient_header"]/a[@class="link"][contains(.,"Patient")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__patient__targets_Result_header"]/a[@class="link"][contains(.,"Result")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__patient__targets_Next_20Date_header"]/a[@class="link"][contains(.,"Next Date")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__patient__targets_Target_header"]/a[@class="link"][contains(.,"Target")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__patient__targets_Flag_header"]/a[@class="link"][contains(.,"Flag")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/thead/tr/th[@class="obs__code__patient__targets_Status_header"]/a[@class="link"][contains(.,"Status")]'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/tbody'),
		wcElement('xpath', '//table[@class="dlg_root"][2]//table[@class="lv_root"][@id="lv_root_Patient_20Targets"]/tbody//div[@id="lv_obs_code_patient_targets_span"]/table[@class="newui zebra"]/tfoot/tr/td[contains(.,"Results")]'),
	], reason='Make sure the elements are present in the Patient Targets listview')
	t.test()

	t = d.getWCUnitTest('Verify Merge Observation Code Page')
	t.setup(lambda d: d.navigate('?f=admin&s=obscodes_manager&opp=merge&obs_old_code=1'))
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="sopp"][@value="merge_info"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@value="obscodes_manager"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="merge"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form/input[@type="hidden" or @type="HIDDEN"][@name="obs_old_code"][@value="1"]'),
		wcElement('xpath', '//div[@id="wc_main"]/form[@action="webchart.cgi"][@method="POST"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Observation Code Merge")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="HeaderCell"][contains(.,"Source Details")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]/following-sibling::td[@class="value"][contains(.,"1")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"][contains(.,"INTRAVASCULAR SUPINE BP")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Target Type")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Target")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="HeaderCell"][contains(.,"Destination Details")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="field"][contains(.,"Enter Observation Code")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/parent::legend/following-sibling::table/tbody/tr/td[@class="value"]/input[@type="text"][@id="merge_obs_code_new"]'),
	], reason='Make sure the elements are present in the Observation Code Merge table')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="submit"][@name="obs_submit"][@value="Continue"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]'),
	], reason='Make sure the Observation Code Merge buttons are present')
	t.test()

	t = d.getWCUnitTest('Verify Merge Mismatch Page')
	t.setup(lambda d: d.navigate('?f=admin&subfunc=obscodes_manager&sopp=merge_info&f=admin&subfunc=obscodes_manager&opp=merge&obs_old_code=2&merge_obs_code_new=17&obs_submit=Continue'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Add Observation Code")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Display Flowsheets")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Flowsheets System Report")]'),
		wcElement('xpath', '//div[@class="links_right"]/a[contains(.,"Choose New Destination Code")]'),
	], reason='Make sure the quick links in the upper right corner of the page are present')
	t.verifyElements([
		wcElement('xpath', '//div[@class="center bold"][contains(.,"The Observation Units Do Not Match.")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"Source Template ID Assigned But Destination Template ID Is Different.")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"Source LOINC Assigned But Destination LOINC Is Different.")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"Unable To Merge.")]'),
	], reason='Verify the warnings at the top of the page are present')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="sopp"][@value="merge_confirm"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@value="obscodes_manager"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="merge"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="obs_old_code"][@value="2"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="merge_obs_code_new"][@value="17"]'),
		wcElement('xpath', '//form/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Observation Code Merge")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="HeaderCell"][contains(.,"Source Details")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]/following-sibling::td[@class="value"][contains(.,"2")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"][contains(.,"HEART RATE")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]/following-sibling::td[@class="value"][contains(.,"bpm")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]/following-sibling::td[@class="value"][contains(.,"8867-4")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"][contains(.,"VITAL SIGNS")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target Type")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="HeaderCell"][contains(.,"Destination Details")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]/following-sibling::td[@class="value"][contains(.,"17")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"][contains(.,"LVEF (Echo)")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]/following-sibling::td[@class="value"][contains(.,"%")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]/following-sibling::td[@class="value"][contains(.,"10230-1")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"][contains(.,"LAB RESULTS")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target Type")]/following-sibling::td[@class="value"][contains(.,"range")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]/following-sibling::td[@class="value"][contains(.,"> 55")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
	], reason='Verify the elements contained within the warning page table are present and correct')
	t.verifyElements([wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]')], reason='Verify the Cancel button is present')
	t.test()

	t = d.getWCUnitTest('Verify Merge Confirmation Page')
	t.setup(lambda d: d.navigate('?f=admin&subfunc=obscodes_manager&sopp=merge_info&f=admin&subfunc=obscodes_manager&opp=merge&obs_old_code=19&merge_obs_code_new=20&obs_submit=Continue'))
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="sopp"][@value="merge_confirm"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@value="obscodes_manager"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="opp"][@value="merge"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="obs_old_code"][@value="19"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::form[@method="POST"]/input[@type="hidden" or @type="HIDDEN"][@name="merge_obs_code_new"][@value="20"]'),
		wcElement('xpath', '//form/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Observation Code Merge")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="HeaderCell"][contains(.,"Source Details")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]/following-sibling::td[@class="value"][contains(.,"19")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"][contains(.,"LVEF (Nuclear)")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]/following-sibling::td[@class="value"][contains(.,"%")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"][contains(.,"LAB RESULTS")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target Type")]/following-sibling::td[@class="value"][contains(.,"range")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]/following-sibling::td[@class="value"][contains(.,"> 55")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="HeaderCell"][contains(.,"Destination Details")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Code")]/following-sibling::td[@class="value"][contains(.,"20")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Name")]/following-sibling::td[@class="value"][contains(.,"LVEF (Angio)")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Units")]/following-sibling::td[@class="value"][contains(.,"%")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"LOINC code")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Template ID")]/following-sibling::td[@class="value"][contains(.,"LAB RESULTS")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target Type")]/following-sibling::td[@class="value"][contains(.,"range")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Target")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation  Range")]/following-sibling::td[@class="value"][contains(.,"> 55")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Interface")]/following-sibling::td[@class="value"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Conditional")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Calculation")]/following-sibling::td[@class="value"][contains(.,"")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="field"][contains(.,"Observation Count")]/following-sibling::td[@class="value"]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="alert"][contains(.,"Verify")]'),
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::fieldset/table/tbody/tr/td[@class="value"][contains(.,"Check this box to acknowledge that all observations with code ")][contains(.,"This operation can NOT be undone!")]'),
	], reason='Verify the merge confirmation page elements are present and correct')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="SUBMIT"][@id="merge_submit"][@name="obs_submit"][@value="Merge"]'),
	wcElement('xpath', '//span[contains(.,"Observation Code Merge")]/ancestor::table[@class="dlg_root"]/following-sibling::div[@class="buttonbar"]/input[@type="submit"][@name="obs_cancel"][@value="Cancel"]'),
	], reason='Make sure the Observation Code Merge buttons are present')
	t.test()

	t = d.getWCUnitTest('Search an Observation Code')
	t.setup(lambda d: d.navigate('?f=admin&subfunc=obscodes_manager&select_criteria=b&select_text=heart&select_by=o.obs_name&select_interface=WEBCHART'))
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/preceding-sibling::span[@style="display:none"]/font[contains(.,"Show (")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/preceding-sibling::span[@style="padding-right:5px; "]/font[contains(.,"Hide (")]'),
	], reason='Verify that the results are not hidden and that the Hide/Show links are present')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Code_cell"]/a[contains(.,"2395")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Name_cell"]/a[contains(.,"Heart rate Encounter maximum")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Interface_cell"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_HL7_20Code_cell"][contains(.,"WEBCHART-Heart rate Encounter maximum")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_LOINC_20Code_cell"][contains(.,"55422-0")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Template_20ID_cell"][contains(.,"LAB RESULTS")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Units_cell"][contains(.,"/min")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Range_cell"][contains(.,"60-100")]'),
	], reason='Test search for an observation containing "heart" with criteria added and results limited')
	t.verifyElements([wcElement('xpath', '//tfoot/tr/td[contains(.,"Displaying 1-")]')], reason='Verify the listview footer contains the results count')
	t.test()

	t = d.getWCUnitTest('Add an Observation Code')
	t.setup(searchObs)
	t.setup(lambda d: d.navigate('?f=admin&subfunc=obscodes_manager&opp=add&obs_name=Kessel&obs_type=&obs_group=&loinc_num=&template_id=&template_id_input=&locale_unit_input_English=&locale_unit_input_Metric=&obs_units_txt=ns+-+nanosecond&obs_units=ns&obs_range=&target=&target_type=&conditional=&calculation=&le_obs_codes_translations_RecordList_fieldlist=SUBSTRING%28name%2C1%2CLOCATE%28%22-%22%2Cname%29-1%29+AS+orderfirst%12trans_from%14&le_obs_codes_translations_RecordList_addfield=&le_obs_codes_translations_RecordList_delfield=&le_obs_codes_translations_RecordList_undelfield=&le_obs_codes_translations_RecordList_editfield=&le_obs_codes_translations_SUBSTRING_name_1_LOCATE_____name__1__AS_orderfirst_value=&le_obs_codes_translations_trans_from_value=&le_obs_codes_codes_list_RecordList_fieldlist=id%12obs_code%12obs_result%12obs_result_desc%12concept_id%12sort_order%14&le_obs_codes_codes_list_RecordList_addfield=&le_obs_codes_codes_list_RecordList_delfield=&le_obs_codes_codes_list_RecordList_undelfield=&le_obs_codes_codes_list_RecordList_editfield=&obs_submit=Save'))
	t.verifyElements([
		wcElement('xpath', '//div[@class="center bold"][contains(.,"Successfully added new observation code.")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"No Translations Processed")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"No Discrete Values Processed")]'),
	], reason='Verify the confirmation message')
	t.test()

	t = d.getWCUnitTest('Verify Newly Added Observation Code Details in listview')
	t.setup(searchObs)
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Code_cell"]/a'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Name_cell"]/a[contains(.,"Kessel")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Interface_cell"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_HL7_20Code_cell"][contains(.,"WEBCHART-Kessel")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Units_cell"][contains(.,"ns")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Range_cell"][contains(.,"")]'),
	], reason='Make sure the observation was added')
	t.test()

	t = d.getWCUnitTest('Edit an Observation Code')
	t.setup(searchObs)
	t.setup(editObs)
	t.verifyElements([
		wcElement('xpath', '//div[@class="center bold"][contains(.,"Successfully updated observation code.")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"No Translations Processed")]'),
		wcElement('xpath', '//div[@class="center bold"][contains(.,"No Discrete Values Processed")]'),
	], reason='Verify the confirmation message')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Code_cell"]/a'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Name_cell"]/a[contains(.,"kesselrun")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Interface_cell"][contains(.,"WEBCHART")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_HL7_20Code_cell"][contains(.,"WEBCHART-Kessel,WEBCHART-kesselrun")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Units_cell"][contains(.,"ns")]'),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Range_cell"][contains(.,"0-12, >12")]'),
	], reason='Make sure the observation was edited')
	t.test()

	t = d.getWCUnitTest('Delete an Observation Code')
	t.setup(searchObs)
	t.setup(deleteObs)
	t.verifyElements([wcElement('xpath', '//div[@class="center bold"][contains(.,"Observation Code (")][contains(.,") was successfully deleted")]')], reason='Verify the confirmation message')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Name_cell"]/a[contains(.,"kesselrun")]', exists=False),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Interface_cell"][contains(.,"WEBCHART")]', exists=False),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_HL7_20Code_cell"][contains(.,"WEBCHART-Kessel,WEBCHART-kesselrun")]', exists=False),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Units_cell"][contains(.,"ns")]', exists=False),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Range_cell"][contains(.,"0-12, >12")]', exists=False),
	], reason='Make sure the observation was deleted')
	t.test()

	t = d.getWCUnitTest('Merge an Observation Code')
	t.setup(lambda d: d.navigate('?f=admin&subfunc=obscodes_manager&sopp=merge_confirm&f=admin&subfunc=obscodes_manager&f=admin&subfunc=obscodes_manager&opp=merge&obs_old_code=19&merge_obs_code_new=20&verify_merge_checkbox=on&obs_submit=Merge'))
	t.verifyElements([wcElement('xpath', '//div[@class="center"][contains(.,"SUCCESS merging observation code (19 ")]')], reason='Verify the confirmation message')
	t.verifyElements([
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_Obs_20Name_cell"]/a[contains(.,"19")]', exists=False),
		wcElement('xpath', '//span[contains(.,"Observation Codes")]/ancestor::fieldset/div//td[@class="obscodes_HL7_20Code_cell"][contains(.,"WEBCHART-LVEF (Angio),WEBCHART-LVEF (Nuclear)")]'),
	], reason='Make sure the observation was merged')
	t.test()
