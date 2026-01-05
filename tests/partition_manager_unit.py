"""
@owners: nwallace
"""
from wcunittest import wcElement, wcDBRecord

# Verify partition manager page
# Verify add partition
# Verify edit partition
# Verify delete partition
# Add a new partition
# Search a partition
# Edit a partition
# Delete a partition



def clickElement(d, text):
	d.clickElement(text=text)

def triggerRequired(d, data):
	d.enterFormData('Auto Increment', id='echart_opts')

def triggerAutoMerge(d, data):
	d.enterFormData('2', xpath='//td[@class="value"][contains(.," Active With Doc Queue")]/input[@type="radio"][@value="2"]')

# xpath bases:
WCMAIN='//div[@id="wc_body_container"]/div[@id="wc_body"]/div[@id="wc_main"]'
WCWIN_WARNING='//div[contains(@class, "wc_win_placement")][@id="mieAlert"]/div[@class="wc_win"]/button[@class="xclose"]/following-sibling::div[@class="wc_win_title"][contains(.,"Warning")]/following-sibling::div[contains(@class, "wc_win_body")]/div/div/input[@type="button"][@id="ok_btn"][@value="OK"]/parent::div/parent::'
HIDDEN_FORM_INPUTS='/form/input[@type="hidden" or @type="HIDDEN"]'
SEARCH_FIELDSET='//span[contains(.,"Search")]/parent::legend/following-sibling::table/tbody'
SEARCH_OPT_TYPE='/tr/td[@class="value"]/select[@id="pm_srch_type"]/option'
SEARCH_OPT_BY='/tr/td[@class="value"]/select[@id="pm_srch_by"]/option'
PARTMGR_FORM='//form[@name="part_manage_form"]'
PARTMGR_HEADERS='//table[@id="lv_root_Partition_20Manager"]//div[@id="lv_partmanager_span"]/table/thead/tr/th'
PARTMGR_LV='//table[@id="lv_root_Partition_20Manager"]//div[@id="lv_partmanager_span"]/table/tbody'
PARTADD_FIELDSET='//span[contains(.,"Partition Add")]/parent::legend/following-sibling::table/tbody'
PARTEDIT_FIELDSET='//span[contains(.,"Partition Edit")]/parent::legend/following-sibling::table/tbody'
PARTVIEW_OPTIONS='/tr/td[@class="value"]/select[@id="echart_opts"]/option'
RESTRICTIONS_MAIN='/tr/td/div[@id="pm_restrictions_div"][@style="display: inline;" or @style="display:inline"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]'
RESTRICTIONS_MAIN_HIDDEN='/tr/td/div[@id="pm_restrictions_div"][@style="display:none" or @style="display: none;"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]'
RESTRICTIONS_ALLOWEDUSRS='/div[@id="le_pm_allowed_users_RecordList_maincontainer"]/table/tbody/tr/td/fieldset[contains(.,"Allowed Users")]/table/tbody/tr/td'
RESTRICTIONS_ALLOWEDDEPT='/div[@id="le_pm_allowed_realms_RecordList_maincontainer"]/table/tbody/tr/td/fieldset[contains(.,"Allowed Departments")]/table/tbody/tr/td'
RESTRICTIONS_INPUTS='//div[@id="pm_restrictions_div"][@style="display:inline" or @style="display: inline;"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]/input[@type="hidden" or @type="HIDDEN"]'
RESTRICTIONS_INPUTS_HIDDEN='//div[@id="pm_restrictions_div"][@style="display:none" or @style="display: none;"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]/input[@type="hidden" or @type="HIDDEN"]'
USRS_LE_DISPLAY_HEADER='[@id="le_pm_allowed_users_display"]/table/tbody/tr/td[@class="HeaderCell"]'
USRS_LE_DISPLAY='[@id="le_pm_allowed_users_display"]/table/tbody/tr/td[@class="RowCell"]'
USRS_LE_INPUT='[@class="value"]/span[@id="le_pm_allowed_users_RecordList_inputspan"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]/span[@id="le_pm_allowed_users_RecordList_inputspan_inner"]/table/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]'
DEPT_LE_DISPLAY_HEADER='[@id="le_pm_allowed_realms_display"]/table/tbody/tr/td[@class="HeaderCell"]'
DEPT_LE_DISPLAY='[@id="le_pm_allowed_realms_display"]/table/tbody/tr/td[@class="RowCell"]'
DEPT_LE_INPUT='[@class="value"]/span[@id="le_pm_allowed_realms_RecordList_inputspan"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]/span[@id="le_pm_allowed_realms_RecordList_inputspan_inner"]/table/tbody/tr/td/fieldset/table/tbody/tr/td[@class="value"]'
MERGE_TYPES='/tr/td[@class="value"]/div[@id="merge_type_value_div"]'
MERGE_TYPES_HIDDEN='/tr/td[@class="value"]/div[@id="merge_type_value_div"][@style="display:none" or @style="display: none;"]'
MTYPE_CHARTONLY='[contains(.," Merge Chart only and ignore this partition")][contains(.,"s demographics")]/input[@type="radio"][@name="mtype"][@id="mtype_1"][@value="1"]'
MTYPE_CHRTDEMO='[contains(.," Merge Chart and Demographics and ignore this partition")][contains(.,"s duplicate MR Numbers")]/input[@type="radio"][@name="mtype"][@id="mtype_2"][@value="2"]'
MTYPE_PARTDOC='[contains(.," Merge this partition")][contains(.,"s documents, and keep all MR Numbers")]/input[@type="radio"][@name="mtype"][@id="mtype_3"][@value="3"]'
MTYPE_MRDOCONLY='[contains(.," Merge documents and MR Numbers Only")]/input[@type="radio"][@name="mtype"][@id="mtype_4"][@value="4"]'
REQUIRED='/tr[@id="pm_required"][@style!="display:none" or @style!="display: none;"]/td'
REQUIRED_HIDDEN='/tr[@id="pm_required"][@style="display:none" or @style="display: none;"]/td'
ADD_IDENTIFIER_OPTIONS='//span[contains(.,"Partition Add")]/parent::legend/following-sibling::table//td[@class="value"]/select[@id="part_identifier"]/option'
EDIT_IDENTIFIER_OPTIONS='//span[contains(.,"Partition Edit")]/parent::legend/following-sibling::table//td[@class="value"]/select[@id="part_identifier"]/option'

def main(d, WCURL):
	t = d.getWCUnitTest('Verify the Partition Manager Page')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&tabmodule=admin&tabselect=Partition+Mgr'), reason='Navigate to the Partition Manager page')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/form[@method="GET"][@name="search_form"]'),
		wcElement('xpath', '//form[@name="search_form"]/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', '//form[@name="search_form"]/input[@type="hidden" or @type="HIDDEN"][@name="s"][@value="partmanager"]'),
		wcElement('xpath', '//form[@name="search_form"]/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Search")]'),
		wcElement('xpath', SEARCH_FIELDSET + '/tr/td[@class="field"][contains(.,"Search Type")]'),
		wcElement('xpath', SEARCH_FIELDSET + '/tr/td[@class="field"][contains(.,"Search Text")]'),
		wcElement('xpath', SEARCH_FIELDSET + '/tr/td[@class="field"][contains(.,"Search By")]'),
		wcElement('xpath', SEARCH_FIELDSET + '/tr/td/input[@type="submit"][@id="go"][@value="Search"]'),
		wcElement('xpath', SEARCH_FIELDSET + '/tr/td/input[@type="submit"][@id="clear"][@value="Clear"]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_TYPE + '[@value="B"][contains(.,"Begins With")]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_TYPE + '[@value="C"][contains(.,"Contains")]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_TYPE + '[@value="E"][contains(.,"Exact")]'),
		wcElement('xpath', SEARCH_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="pm_srch_text"][@size="30"]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_BY + '[@value="A"][contains(.,"All")]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_BY + '[@value="P"][contains(.,"Partition")]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_BY + '[@value="N"][contains(.,"Name")]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_BY + '[@value="D"][contains(.,"Description")]'),
		wcElement('xpath', SEARCH_FIELDSET + SEARCH_OPT_BY + '[@value="G"][contains(.,"Global Identifier")]'),
	], reason='Verify all Search elements are present')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="textRight"]/a[contains(.,"Show Deactivated")]'),
		wcElement('xpath', WCMAIN + '/div[@class="textRight"]/a[contains(.,"Add Partition")]'),
	], reason='Verify the page links are present')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/table[@class="lv_root"][@id="lv_root_Partition_20Manager"]'),
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"]//font[contains(.,"Partition Manager")]'),
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_partmanager_show_link"]/font/span[contains(.,"Show")]'),
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]/tbody/tr/td/fieldset/legend/font/span[@class="LVTitle"][@id="lv_partmanager_hide_link"]/font/span[contains(.,"Hide")]'),
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]/tbody/tr/td/fieldset/div[@id="lv_partmanager_span"]/table[@class="newui zebra"][@data-tttype="sticky"]/thead/tr/th[@class="partmanager_Partition_header"]/a[@class="link"][contains(.,"Partition")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Global_20Identifier_header"]/a[@class="link"][contains(.,"Global Identifier")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Name_header"]/a[@class="link"][contains(.,"Name")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Description_header"]/a[@class="link"][contains(.,"Description")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_MR_20Sequence_header"]/a[@class="link"][contains(.,"MR Sequence")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_View_20Options_header"]/a[@class="link"][contains(.,"View Options")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Required_header"]/a[@class="link"][contains(.,"Required")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Active_20-_20Merge_20Type_header"]/a[@class="link"][contains(.,"Active - Merge Type")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Order_header"]/a[@class="link"][contains(.,"Order")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Restricted_header"]/a[@class="link"][contains(.,"Restricted")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Identifier_header"]/a[@class="link"][contains(.,"Identifier")]'),
		wcElement('xpath', PARTMGR_HEADERS + '[@class="partmanager_Options_header"][contains(.,"Options")]'),
	], reason='Verify all Title and Header elements are present')
	t.verifyElements([
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]/tbody/tr/td/fieldset/div[@id="lv_partmanager_span"]/table[@class="newui zebra"][@data-tttype="sticky"]/tbody/tr/td[@class="partmanager_Partition_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Global_20Identifier_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Name_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Description_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_MR_20Sequence_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_View_20Options_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Required_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Active_20-_20Merge_20Type_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Order_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Restricted_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Identifier_cell"]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Options_cell"]/a[contains(.,"Edit")]'),
		wcElement('xpath', PARTMGR_LV + '/tr/td[@class="partmanager_Options_cell"]/a[contains(.,"Delete")]'),
	], reason='Verify the Partition Manager listview body elements are present')
	t.verifyElements([
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]/tbody/tr/td/fieldset/div[@id="lv_partmanager_span"]/table[@class="newui zebra"][@data-tttype="sticky"]/tfoot/tr/td[contains(.,"Displaying")]'),
], reason='Verify the Footer elements are present')
	t.test()

	t = d.getWCUnitTest('Verify the Add Partition Page')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add'), reason='Navigate directly to the Add Partition page')

	t.verifyElements([
		wcElement('xpath', WCMAIN + '/form[@method="POST"][@id="part_manage_form"]'),
		wcElement('xpath', PARTMGR_FORM + '/input[@type="hidden" or @type="HIDDEN"][@id="opp"][@value="add"]'),
		wcElement('xpath', PARTMGR_FORM + '/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', PARTMGR_FORM + '/input[@type="hidden" or @type="HIDDEN"][@name="s"][@value="partmanager"]'),
		wcElement('xpath', PARTMGR_FORM + '/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Partition Add")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Partition")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="partition"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"WC GUID")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="wc_guid"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Name")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="name"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Description")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="description"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"MR Sequence")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="mr_sequence"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/script[contains(.,"showReq")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Partition View")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="V"][contains(.,"View Only")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="A"][contains(.,"Auto Increment")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="S"][contains(.,"Hidden From View But Searchable")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="X"][contains(.,"Hidden From View But Searchable (Auto Increment)")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="P"][contains(.,"Hidden From View But Searchable (Auto Increment Optional)")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="Y"][contains(.,"Hidden From View But Searchable (Randomly Generated)")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="H"][contains(.,"Hidden From View")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="O"][contains(.,"Allow Edit (Optional)")]'),
		wcElement('xpath', PARTADD_FIELDSET + PARTVIEW_OPTIONS + '[@value="R"][contains(.,"Allow Edit (Required)")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Active Types")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"][contains(.," Non Active")]/input[@type="radio"][@name="active"][@value="0"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"][contains(.," Active")]/input[@type="radio"][@name="active"][@value="1"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"][contains(.," Active With Doc Queue")]/input[@type="radio"][@name="active"][@value="2"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Part Order")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="part_order"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Allow Access to Restricted Users")]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="value"]/input[@type="checkbox"][@id="part_restrict"]'),
	], reason='Verify that all elements on the Partition Add page are present')
	t.verifyElements([
		wcElement('xpath', REQUIRED_HIDDEN + '/td[@class="field"][contains(.,"Required")]', exists=False),
		wcElement('xpath', REQUIRED_HIDDEN + '/td[@class="value"][contains(.,"Yes")]/input[@type="radio"][@id="part_required_1"][@value="1"]', exists=False),
		wcElement('xpath', REQUIRED_HIDDEN + '/td[@class="value"][contains(.,"No")]/input[@type="radio"][@id="part_required_0"][@value="0"]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"]/div[@id="merge_type_field_div"][@style="display:none" or @style="display: none;"][contains(.,"Auto Merge Type")]'),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge Chart only and ignore this partition")][contains(.,"s demographics")]/input[@type="radio"][@name="mtype"][@id="mtype_1"][@value="1"]'),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge Chart and Demographics and ignore this partition")][contains(.,"s duplicate MR Numbers")]/input[@type="radio"][@name="mtype"][@id="mtype_2"][@value="2"]'),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge this partition")][contains(.,"s documents, and keep all MR Numbers")]/input[@type="radio"][@name="mtype"][@id="mtype_3"][@value="3"]'),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge documents and MR Numbers Only")]/input[@type="radio"][@name="mtype"][@id="mtype_4"][@value="4"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_INPUTS_HIDDEN + '[@id="le_pm_allowed_users_RecordList_fieldlist"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_INPUTS_HIDDEN + '[@id="le_pm_allowed_users_RecordList_addfield"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_INPUTS_HIDDEN + '[@id="le_pm_allowed_users_RecordList_delfield"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_INPUTS_HIDDEN + '[@id="le_pm_allowed_users_RecordList_undelfield"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_INPUTS_HIDDEN + '[@id="le_pm_allowed_users_RecordList_editfield"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN_HIDDEN + RESTRICTIONS_ALLOWEDUSRS),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN_HIDDEN + RESTRICTIONS_ALLOWEDUSRS + '[@id="le_pm_allowed_users_display"]'),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY_HEADER + '/font[contains(., "User")]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY_HEADER + '/center/font[contains(., "Options")]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY + '/font[contains(.,*)]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY + '/center/font/table/tbody/tr/td/span/input[@type="button"]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY_HEADER + '/font[contains(., "Department")]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY_HEADER + '/center/font[contains(., "Options")]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY + '/font[contains(.,*)]', exists=False),
		wcElement('xpath', PARTADD_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY + '/center/font/table/tbody/tr/td/span/input[@type="button"]', exists=False),
	], reason='Verify the hidden Required, Auto Merge, and Restrictions sections are present and hidden by default')
	t.verifyElements([
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"][contains(.,"Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="AM"][contains(.,"American Express")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="AN"][contains(.,"Account Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="BR"][contains(.,"Birth Registry Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="DI"][contains(.,"Diner")][contains(.,"Club Card")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="DL"][contains(.,"Driver")][contains(.,"License Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="DN"][contains(.,"Doctor Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="DS"][contains(.,"Discover Card")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="EI"][contains(.,"Employee Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="EN"][contains(.,"Employer Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="FI"][contains(.,"Facility ID")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="GI"][contains(.,"Guarantor Internal Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="GN"][contains(.,"Guarantor External Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="LN"][contains(.,"License Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="LR"][contains(.,"Local Registry ID")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="MA"][contains(.,"Medicaid Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="MC"][contains(.,"Medicare Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="MR"][contains(.,"Medical Record Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="MS"][contains(.,"MasterCard")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="NE"][contains(.,"National Employer Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="NH"][contains(.,"National Health Plan Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="NPI"][contains(.,"National Provider Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="PI"][contains(.,"Patient Internal Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="PN"][contains(.,"Person Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="PRN"][contains(.,"Provider Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="PT"][contains(.,"Patient External Identifier")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="RR"][contains(.,"Railroad Retirement Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="RRI"][contains(.,"Regional Registry ID")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="SL"][contains(.,"State License")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="SR"][contains(.,"State Registry ID")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="SS"][contains(.,"Social Security Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="U"][contains(.,"Unspecified")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="UPIN"][contains(.,"Medicare/HCF")][contains(.,"Universal Physician Identification Numbers")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="VN"][contains(.,"Visit Number")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="VS"][contains(.,"VISA")]'),
		wcElement('xpath', ADD_IDENTIFIER_OPTIONS + '[@value="WC"][contains(.,"WIC Identifier")]'),
	], reason='Verify the Identifier dropdown and options elements are present')
	t.test()

	t = d.getWCUnitTest('Verify the hidden Required and Auto Merge sections are present and become available')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add'), reason='Navigate directly to the Add Partition page again; this time Required and AutoMerge options have been triggered')
	t.setup(triggerRequired)
	t.setup(triggerAutoMerge)
	t.verifyElements([
		wcElement('xpath', PARTADD_FIELDSET + REQUIRED + '[@class="field"][contains(.,"Required")]'),
		wcElement('xpath', PARTADD_FIELDSET + REQUIRED + '[@class="value"][contains(.,"Yes")]/input[@type="radio"][@id="part_required_1"][@value="1"]'),
		wcElement('xpath', PARTADD_FIELDSET + REQUIRED + '[@class="value"][contains(.,"No")]/input[@type="radio"][@id="part_required_0"][@value="0"]'),
		wcElement('xpath', PARTADD_FIELDSET + '/tr/td[@class="field"]/div[@id="merge_type_field_div"][@style!="display: none;"][contains(.,"Auto Merge Type")]'),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES + MTYPE_CHARTONLY),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES + MTYPE_CHRTDEMO),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES + MTYPE_PARTDOC),
		wcElement('xpath', PARTADD_FIELDSET + MERGE_TYPES + MTYPE_MRDOCONLY),
	], reason='Verify the hidden Required, Auto Merge, and Restrictions sections are present and now shown')
	t.test()

	t = d.getWCUnitTest('Verify the Edit Partition Page')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=edit&partition=ASSET'), reason='Navigate directly to the Edit Partition page for the ASSET partition')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/form[@method="POST"][@id="part_manage_form"]'),
		wcElement('xpath', PARTMGR_FORM + '/input[@type="hidden" or @type="HIDDEN"][@id="opp"][@value="edit"]'),
		wcElement('xpath', PARTMGR_FORM + '/input[@type="hidden" or @type="HIDDEN"][@name="f"][@value="admin"]'),
		wcElement('xpath', PARTMGR_FORM + '/input[@type="hidden" or @type="HIDDEN"][@name="s"][@value="partmanager"]'),
		wcElement('xpath', PARTMGR_FORM + '/table[@class="dlg_root"]/tbody/tr/td/fieldset/legend[@class="dlgtitle"]/span[contains(.,"Partition Edit")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Partition")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"][contains(.,"ASSET")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"WC GUID")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="wc_guid"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Name")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="name"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Description")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="description"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"MR Sequence")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="mr_sequence"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/script[contains(.,"showReq")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Partition View")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="V"][contains(.,"View Only")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="A"][contains(.,"Auto Increment")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="S"][contains(.,"Hidden From View But Searchable")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="X"][contains(.,"Hidden From View But Searchable (Auto Increment)")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="P"][contains(.,"Hidden From View But Searchable (Auto Increment Optional)")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="Y"][contains(.,"Hidden From View But Searchable (Randomly Generated)")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="H"][contains(.,"Hidden From View")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="O"][contains(.,"Allow Edit (Optional)")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + PARTVIEW_OPTIONS + '[@value="R"][contains(.,"Allow Edit (Required)")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Active Types")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"][contains(.," Non Active")]/input[@type="radio"][@name="active"][@value="0"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"][contains(.," Active")]/input[@type="radio"][@name="active"][@value="1"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"][contains(.," Active With Doc Queue")]/input[@type="radio"][@name="active"][@value="2"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Part Order")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"]/input[@type="text"][@id="part_order"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Allow Access to Restricted Users")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="value"]/input[@type="checkbox"][@id="part_restrict"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_INPUTS + '[@id="le_pm_allowed_users_RecordList_fieldlist"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_INPUTS + '[@id="le_pm_allowed_users_RecordList_addfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_INPUTS + '[@id="le_pm_allowed_users_RecordList_delfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_INPUTS + '[@id="le_pm_allowed_users_RecordList_undelfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_INPUTS + '[@id="le_pm_allowed_users_RecordList_editfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + '[@id="le_pm_allowed_users_display"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY_HEADER + '/font[contains(., "User")]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY_HEADER + '/center/font[contains(., "Options")]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY + '/font[contains(.,*)]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY + '/center/font/table/tbody/tr/td/span/input[@type="button"]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY_HEADER + '/font[contains(., "Department")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY_HEADER + '/center/font[contains(., "Options")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY + '/font[contains(., "System Owner")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY + '/center/font/table/tbody/tr/td/span/input[@type="button"]'),
	], reason='Verify that all elements on the Partition Edit page are present')
	t.verifyElements([
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"]/div[@id="merge_type_field_div"][contains(., "Auto Merge Type")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + REQUIRED + '[@class="value"][contains(.,"Yes")]/input[@type="radio"][@id="part_required_1"][@value="1"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + REQUIRED + '[@class="value"][contains(.,"No")]/input[@type="radio"][@id="part_required_0"][@value="0"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"]/div[@id="merge_type_field_div"][@style="display:none" or @style="display: none;"][contains(.,"Auto Merge Type")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge Chart only and ignore this partition")][contains(.,"s demographics")]/input[@type="radio"][@name="mtype"][@id="mtype_1"][@value="1"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge Chart and Demographics and ignore this partition")][contains(.,"s duplicate MR Numbers")]/input[@type="radio"][@name="mtype"][@id="mtype_2"][@value="2"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge this partition")][contains(.,"s documents, and keep all MR Numbers")]/input[@type="radio"][@name="mtype"][@id="mtype_3"][@value="3"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + MERGE_TYPES_HIDDEN + '[contains(.," Merge documents and MR Numbers Only")]/input[@type="radio"][@name="mtype"][@id="mtype_4"][@value="4"]'),
	], reason='Verify the hidden Auto Merge section elements are present and hidden by default')
	t.verifyElements([
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_users_RecordList_fieldlist"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_users_RecordList_addfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_users_RecordList_delfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_users_RecordList_undelfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_users_RecordList_editfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + '[@id="le_pm_allowed_users_display"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY_HEADER + '/font[contains(., "User")]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY_HEADER + '/center/font[contains(., "Options")]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY + '/font[contains(.,*)]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDUSRS + USRS_LE_DISPLAY + '/center/font/table/tbody/tr/td/span/input[@type="button"]', exists=False),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/div[@id="le_pm_allowed_users_RecordList_fillerspan"][@style="display:none" or @style="display: none;"]'),
	], reason='Verify the nested Allowed Users elements are present')
	t.verifyElements([
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_realms_RecordList_fieldlist"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_realms_RecordList_addfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_realms_RecordList_delfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_realms_RecordList_undelfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/input[@type="hidden" or @type="HIDDEN"][@id="le_pm_allowed_realms_RecordList_editfield"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + '[@id="le_pm_allowed_realms_display"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY_HEADER + '/font[contains(., "Department")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY_HEADER + '/center/font[contains(., "Options")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY + '/font[contains(.,"System Owner")]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + RESTRICTIONS_ALLOWEDDEPT + DEPT_LE_DISPLAY + '/center/font/table/tbody/tr/td/span/input[@type="button"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + RESTRICTIONS_MAIN + '/div[@id="le_pm_allowed_realms_RecordList_fillerspan"][@style="display:none" or @style="display: none;"]'),
	], reason='Verify the nested Allowed Departments elements are present')
	t.verifyElements([
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td[@class="field"][contains(.,"Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="AM"][contains(.,"American Express")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="AN"][contains(.,"Account Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="BR"][contains(.,"Birth Registry Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="DI"][contains(.,"Diner")][contains(.,"Club Card")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="DL"][contains(.,"Driver")][contains(.,"License Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="DN"][contains(.,"Doctor Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="DS"][contains(.,"Discover Card")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="EI"][contains(.,"Employee Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="EN"][contains(.,"Employer Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="FI"][contains(.,"Facility ID")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="GI"][contains(.,"Guarantor Internal Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="GN"][contains(.,"Guarantor External Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="LN"][contains(.,"License Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="LR"][contains(.,"Local Registry ID")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="MA"][contains(.,"Medicaid Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="MC"][contains(.,"Medicare Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="MR"][contains(.,"Medical Record Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="MS"][contains(.,"MasterCard")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="NE"][contains(.,"National Employer Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="NH"][contains(.,"National Health Plan Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="NPI"][contains(.,"National Provider Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="PI"][contains(.,"Patient Internal Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="PN"][contains(.,"Person Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="PRN"][contains(.,"Provider Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="PT"][contains(.,"Patient External Identifier")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="RR"][contains(.,"Railroad Retirement Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="RRI"][contains(.,"Regional Registry ID")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="SL"][contains(.,"State License")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="SR"][contains(.,"State Registry ID")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="SS"][contains(.,"Social Security Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="U"][contains(.,"Unspecified")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="UPIN"][contains(.,"Medicare/HCF")][contains(.,"Universal Physician Identification Numbers")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="VN"][contains(.,"Visit Number")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="VS"][contains(.,"VISA")]'),
		wcElement('xpath', EDIT_IDENTIFIER_OPTIONS + '[@value="WC"][contains(.,"WIC Identifier")]'),
	], reason='Verify the Identifier dropdown and options elements are present')
	t.verifyElements([
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td/input[@type="button"][@value="Change"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td/input[@type="reset"][@value="Reset"]'),
		wcElement('xpath', PARTEDIT_FIELDSET + '/tr/td/input[@type="button"][@value="Cancel"]'),
	], reason='Verify the Partition Edit buttons are present')
	t.test()

	t = d.getWCUnitTest('Verify the Delete Partition Page')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=delete&partition=ASSET'), reason='Navigate directly to the page to delete the ASSET partition')
	t.verifyElements([
		wcElement('xpath', WCMAIN + HIDDEN_FORM_INPUTS + '[@id="opp"][@value="delete"]'),
		wcElement('xpath', WCMAIN + HIDDEN_FORM_INPUTS + '[@id="partition"][@value="ASSET"]'),
		wcElement('xpath', WCMAIN + HIDDEN_FORM_INPUTS + '[@name="f"][@value="admin"]'),
		wcElement('xpath', WCMAIN + HIDDEN_FORM_INPUTS + '[@name="s"][@value="partmanager"]'),
	], reason='Verify hidden input elements on page are present')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/form/center/strong[contains(.,"WARNING")]'),
		wcElement('xpath', WCMAIN + '/form/center/strong[contains(.,"You are about to deactivate partition")]'),
		wcElement('xpath', WCMAIN + '/form/center/input[@type="SUBMIT"][@name="part_submit"][@value="Deactivate"]'),
		wcElement('xpath', WCMAIN + '/form/center/input[@type="submit"][@name="part_cancel"][@value="Cancel"]'),
	], reason='Verify the deletion Warning/Confirmation page elements')
	t.test()
	
	t = d.getWCUnitTest('Add a New Partition')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=TESTPART&wc_guid=PARTITIONTEST&name=TESTPART&description=Test+Adding+a+Partition&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL adds new partition and redirects to Partition Manager page for test to verify the partition was added')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="information"][contains(., "Partition (TESTPART) successfully added.")]'),
	], reason='Verify successful add of partition')
	t.test()

	t = d.getWCUnitTest('Verify Table Values')
	t.setup(lambda d: d.clickElement(xpath="//a[contains(., 'Show All')]"), reason='Elements being checked for are hidden behind this')
	t.verifyElements([
		wcElement('xpath', '//td[@class="partmanager_Partition_cell"][contains(.,"TESTPART")]'),
		wcElement('xpath', '//td[@class="partmanager_Global_20Identifier_cell"][contains(.,"PARTITIONTEST")]'),
		wcElement('xpath', '//td[@class="partmanager_Name_cell"][contains(.,"TESTPART")]'),
		wcElement('xpath', '//td[@class="partmanager_Description_cell"][contains(.,"Test Adding a Partition")]'),
		wcElement('xpath', '//td[@class="partmanager_MR_20Sequence_cell"][contains(.,"2011")]'),
		wcElement('xpath', '//td[@class="partmanager_View_20Options_cell"][contains(.,"Hidden But Searchable")]'),
		wcElement('xpath', '//td[@class="partmanager_Required_cell"][contains(.,"No")]'),
		wcElement('xpath', '//td[@class="partmanager_Active_20-_20Merge_20Type_cell"][contains(.,"Active With Doc Queue - MDAT")]'),
		wcElement('xpath', '//td[@class="partmanager_Order_cell"][contains(.,"333")]'),
		wcElement('xpath', '//td[@class="partmanager_Restricted_cell"][contains(.,"Yes")]'),
		wcElement('xpath', '//td[@class="partmanager_Identifier_cell"][contains(.,"MR")]'),
	], reason='Verify the all cells contain the correct information for the newly added partition')
	t.test()

	t = d.getWCUnitTest('Warnings - Blank Partition field')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=&wc_guid=WARNPARTITIONTEST&name=WARNTESTPART&description=WarningTest+Adding+a+Partition&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL attempts to add a partition with a blank Partition field and refreshes with the warning')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '[contains(., "A partition is required. Must be in capital case")]'),
	], reason='Verify we get the warning when the Partition field is left blank')
	t.test()

	t = d.getWCUnitTest('Warnings - Blank Name field')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=WARNTESTPART&wc_guid=WARNPARTITIONTEST&name=&description=WarningTest+Adding+a+Partition&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL attempts to add a partition with a blank Name field and refreshes with the warning')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="alert"][contains(., "Partition requires a name.")]'),
	], reason='Verify we get the warning when the Name field is left blank')
	t.test()

	t = d.getWCUnitTest('Warnings - Blank Description field')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=WARNTESTPART&wc_guid=WARNPARTITIONTEST&name=WARNTESTPART&description=&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL attempts to add a partition with a blank Descritption field and refreshes with the warning')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="alert"][contains(., "Partition requires a description.")]'),
	], reason='Verify we get the warning when the Description field is left blank')
	t.test()

	t = d.getWCUnitTest('Warnings - Duplicate Partition')
	d.wcErrorLog.ignore("*Unable to insert partition in the table*Duplicate entry 'TESTPART' for key 'partit'")
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=TESTPART&wc_guid=WARNPARTITIONTEST&name=WARNTESTPART&description=WarningTest+Adding+a+Partition&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL attempts to add a duplicate partition and refreshes with the warning')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="alert"][contains(., "Error: Unable To Insert Record - ") and contains(., "Duplicate entry")]'),
	], reason='Verify we get the warning when a duplicate Partition is entered')
	t.test()

	t = d.getWCUnitTest('Warnings - Duplicate WC GUID ')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=WARNTESTPART&wc_guid=PARTITIONTEST&name=WARNTESTPART&description=WarningTest+Adding+a+Partition&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL attempts to add a partition with a duplicate WC GUID and refreshes with the warning')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="alert"][contains(., "Duplicate WC_GUID. A partition with this WC_GUID already exists.")]'),
	], reason='Verify we get the warning when a duplicate WC GUID is entered ')
	t.test()
	t = d.getWCUnitTest('Warnings - Duplicate Name and MR Sequence')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=add&f=admin&s=partmanager&partition=WARNTESTPART&wc_guid=WARNPARTITIONTEST&name=TESTPART&description=WarningTest+Adding+a+Partition&mr_sequence=2011&echart_opts=S&part_required=0&active=2&mtype=3&part_order=333&part_restrict=1&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=9%12%14&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=Physicians%12%14&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=MR&part_submit=Save'), reason='URL attempts to add a partition with a duplicate Name and/or MR Sequence and refreshes with the warning')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="alert"][contains(., "Duplicate MR sequence. MR sequence already exists for same name.")]'),
	], reason='Verify we get the warning when a duplicate Name and MR Sequence is entered ')
	t.test()

	t = d.getWCUnitTest('Search for the new Partition')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&go=Search&pm_srch_type=C&pm_srch_text=part&pm_srch_by=N'), reason='Search for the new TESTPART partition')
	t.verifyElements([
		wcElement('xpath', '//td[@class="partmanager_Partition_cell"][contains(.,"TESTPART")]'),
		wcElement('xpath', '//td[@class="partmanager_Global_20Identifier_cell"][contains(.,"PARTITIONTEST")]'),
		wcElement('xpath', '//td[@class="partmanager_Name_cell"][contains(.,"TESTPART")]'),
		wcElement('xpath', '//td[@class="partmanager_Description_cell"][contains(.,"Test Adding a Partition")]'),
		wcElement('xpath', '//td[@class="partmanager_MR_20Sequence_cell"][contains(.,"2011")]'),
		wcElement('xpath', '//td[@class="partmanager_View_20Options_cell"][contains(.,"Hidden But Searchable")]'),
		wcElement('xpath', '//td[@class="partmanager_Required_cell"][contains(.,"No")]'),
		wcElement('xpath', '//td[@class="partmanager_Active_20-_20Merge_20Type_cell"][contains(.,"Active With Doc Queue - MDAT")]'),
		wcElement('xpath', '//td[@class="partmanager_Order_cell"][contains(.,"333")]'),
		wcElement('xpath', '//td[@class="partmanager_Restricted_cell"][contains(.,"Yes")]'),
		wcElement('xpath', '//td[@class="partmanager_Identifier_cell"][contains(.,"MR")]'),
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]//div[@id="lv_partmanager_span"]/table/tbody/tr[2]', exists=False),
	], reason='Verify the search finds the newly added partition and nothing else')
	t.test()

	t = d.getWCUnitTest('Edit a partition')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=edit&f=admin&s=partmanager&partition=TESTPART&wc_guid=TESTPARTITION&name=PARTTEST&description=Test+Editing+a+Partition&mr_sequence=2010&echart_opts=A&part_required=0&active=1&mtype=2&part_order=777&le_pm_allowed_users_RecordList_fieldlist=allowed_id%14&le_pm_allowed_users_RecordList_addfield=&le_pm_allowed_users_RecordList_delfield=&le_pm_allowed_users_RecordList_undelfield=&le_pm_allowed_users_RecordList_editfield=&le_pm_allowed_users_allowed_id_value=&le_pm_allowed_users_allowed_id_display=&le_pm_allowed_realms_RecordList_fieldlist=allowed_id%14&le_pm_allowed_realms_RecordList_addfield=&le_pm_allowed_realms_RecordList_delfield=&le_pm_allowed_realms_RecordList_undelfield=&le_pm_allowed_realms_RecordList_editfield=&le_pm_allowed_realms_allowed_id_display=&le_pm_allowed_realms_allowed_id_value=&part_identifier=LN&part_submit=Change'), reason='URL to edit the TESTPART partition and refreshes to Partition Manager listview')
	t.verifyElements([
		wcElement('xpath', WCMAIN + '/div[@class="bannerMsg"]/span[@class="information"][contains(., "Partition (TESTPART) successfully edited.")]'),
	], reason='Verify the partition was not duplicated and the original entries no longer remain')
	t.test()


	t = d.getWCUnitTest('Verify Edited partition changes')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&go=Search&pm_srch_type=E&pm_srch_text=TESTPART&pm_srch_by=P'), reason='URL to search for the TESTPART partition and refreshes to Partition Manager listview to verify values changed')
	t.verifyElements([
		wcElement('xpath', '//td[@class="partmanager_Partition_cell"][contains(.,"TESTPART")]'),
		wcElement('xpath', '//td[@class="partmanager_Global_20Identifier_cell"][contains(.,"PARTITIONTEST")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_Name_cell"][contains(.,"TESTPART")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_Description_cell"][contains(.,"Test Adding a Partition")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_MR_20Sequence_cell"][contains(.,"2011")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_View_20Options_cell"][contains(.,"Hidden But Searchable")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_Active_20-_20Merge_20Type_cell"][contains(.,"Active With Doc Queue - MDAT")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_Order_cell"][contains(.,"333")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_Restricted_cell"][contains(.,"Yes")]', exists=False),
		wcElement('xpath', '//td[@class="partmanager_Identifier_cell"][contains(.,"MR")]', exists=False),
	], reason='Verify the partition was not duplicated and the original entries no longer remain')
	t.verifyElements([
		wcElement('xpath', '//td[@class="partmanager_Partition_cell"][contains(.,"TESTPART")]'),
		wcElement('xpath', '//td[@class="partmanager_Global_20Identifier_cell"][contains(.,"TESTPARTITION")]'),
		wcElement('xpath', '//td[@class="partmanager_Name_cell"][contains(.,"PARTTEST")]'),
		wcElement('xpath', '//td[@class="partmanager_Description_cell"][contains(.,"Test Editing a Partition")]'),
		wcElement('xpath', '//td[@class="partmanager_MR_20Sequence_cell"][contains(.,"2010")]'),
		wcElement('xpath', '//td[@class="partmanager_View_20Options_cell"][contains(.,"Auto")]'),
		wcElement('xpath', '//td[@class="partmanager_Active_20-_20Merge_20Type_cell"][contains(.,"Active")]'),
		wcElement('xpath', '//td[@class="partmanager_Order_cell"][contains(.,"777")]'),
		wcElement('xpath', '//td[@class="partmanager_Restricted_cell"][contains(.,"No")]'),
		wcElement('xpath', '//td[@class="partmanager_Identifier_cell"][contains(.,"LN")]'),
	], reason='Verify the all cells contain the correct information for the edited partition')
	t.test()



	t = d.getWCUnitTest('Delete a partition')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&opp=delete&partition=TESTPART&f=admin&s=partmanager&part_submit=Deactivate'), reason='URL to delete the TESTPART partition')
	t.setup(lambda d: d.navigate('?f=admin&s=partmanager&go=Search&pm_srch_type=C&pm_srch_text=part&pm_srch_by=N'), reason='URL for a search for the deleted partition to verify it was deleted')
	t.verifyElements([
		wcElement('xpath', '//td[@class="partmanager_Partition_cell"][contains(.,"TESTPART")]', exists=False),
		wcElement('xpath', '//table[@id="lv_root_Partition_20Manager"]//div[@id="lv_partmanager_span"]/table/tbody/tr[1]', exists=False),
	], reason='Verify the partition was deleted and the search returns no results')
	t.test()
