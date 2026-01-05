"""
@owners: pepperson
"""
from wcunittest import wcElement, wcDBRecord

def clearRoutes(d, data):
	d.miedb.dbExec('TRUNCATE datasend_route')

def autocompleteInj(d, val):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.enterFormData(val, name='description_vis', clear=True, blur=False)
	if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=5):
		d.clickElement(xpath='//div[@class="defaultacdiv"]//div')

def checkDocProperties(d, val):
	d.wcutils.waitFor(lambda d: d.getElement(xpath="//a[text()='Properties']"), expected=True, timeout=60)
	d.clickElement(xpath="//a[text()='Properties']")
	d.wcutils.waitFor(lambda d: d.getElement(xpath="//legend[contains(., 'Properties for Document')]"), expected=True, timeout=60)


def main(d, WCURL):
	t = d.getWCUnitTest ('Create Injection AutoRoutes')
	t.setup(lambda d: d.miedb.dbExec("INSERT INTO datasend_auto_route SET trigger_type=0,description='Route All Injections On Add',custom_join='LEFT JOIN injections i ON i.doc_id=d.doc_id',where_clause='1',recipient_type=0,recipient_name='All Out',method=23,method_detail='ALLOUT'"), reason='Create an On-Add Document Auto Route which processes All Injections')
	t.setup(lambda d: d.miedb.dbExec("INSERT INTO datasend_auto_route SET trigger_type=0,description='Route Moderna Covid Injections On Add',custom_join='LEFT JOIN injections i ON i.doc_id=d.doc_id',where_clause='i.inject_code=207',recipient_type=0,recipient_name='Moderna Out',method=23,method_detail='MODOUT'"), reason='Create an On-Add Document Auto Route which processes only Moderna Injections')
	t.setup(lambda d: d.miedb.dbExec("INSERT INTO datasend_auto_route SET trigger_type=15,description='Route Pfizer Covid Injections On Update',custom_join='LEFT JOIN injections i ON i.doc_id=d.doc_id',where_clause='i.inject_code=208',recipient_type=0,recipient_name='Pfizer Out',method=23,method_detail='PFROUT'"), reason='Create an On-Update Document Auto Route which processes only Pfizer Injections')
	t.setup(lambda d: d.navigate('?f=chart&s=dar_editor'), reason='View Auto Routes')
	t.verifyElements([
		wcElement('xpath', "//td[text()='Route All Injections On Add']"),
		wcElement('xpath', "//td[text()='Route Moderna Covid Injections On Add']"),
		wcElement('xpath', "//td[text()='Route Pfizer Covid Injections On Update']"),
	], reason='The Auto Routes are set up correctly.')
	t.test()

	# Add a generic injection document: no covid routes, All Injections Route
	t = d.getWCUnitTest ('Create Generic Injection Document')
	t.setup(lambda d: d.navigate(WCURL.CHART_HART_WILLIAM + 't=Medical+Record%3AMAR%2FInjections&v=inject&injopp=add'), reason='Injection Add Screen')
	t.setup(lambda d: autocompleteInj(d, 'Hep A'), reason='Set the Injection Type')
	t.setup(lambda d: d.enterFormData('123456', name='vial'), reason='Set the Lot Number')
	t.setup(lambda d: d.enterFormData('Abbott Laboratories', name='manufacturer'), reason='Set the Manufacturer')
	t.setup(lambda d: d.enterFormData('02', name='expiration_dateMONTH'), reason='Set the Expiration Date')
	t.setup(lambda d: d.enterFormData('28', name='expiration_dateDAY'), reason='Set the Expiration Date')
	t.setup(lambda d: d.enterFormData('2030', name='expiration_dateYEAR'), reason='Set the Expiration Date')
	t.setup(lambda d: d.enterFormData('02', name='service_dateMONTH'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('02', name='service_dateDAY'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('2007', name='service_dateYEAR'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('09:15', name='service_dateTIME'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('SC', name='route'), reason='Set the Route')
	t.setup(lambda d: d.enterFormData('LA', name='site'), reason='Set the Site')
	t.setup(lambda d: d.clickElement(xpath='//input[@value="Submit"]'), reason='Create the Document')
	t.setup(lambda d: d.navigate(WCURL.CHART_HART_WILLIAM + 't=Documents&v=list&lv_lv_wc_order=`Doc+ID`&lv_lv_wc_dir=DESC'), reason='View Documents List, Newest First')
	t.setup(lambda d: d.clickElement(xpath="//a[text()='Injection']"), reason='View the Newest Injection Document')
	t.setup(checkDocProperties)
	t.verifyElements([
		wcElement('xpath', "//td[contains(.,'All Out')]"),
		wcElement('xpath', "//td[contains(.,'Moderna Out')]", exists=False),
		wcElement('xpath', "//td[contains(.,'Pfizer Out')]", exists=False),
	], reason='The All Documents Add Auto Routes are set up correctly.')
	t.test()
	
	# Add a Moderna injection document: Moderna Injection Route, All Injections Route
	t = d.getWCUnitTest ('Create Moderna Injection Document')
	t.setup(lambda d: d.navigate(WCURL.CHART_HART_WILLIAM + 't=Medical+Record%3AMAR%2FInjections&v=inject&injopp=add'), reason='Injection Add Screen')
	t.setup(lambda d: autocompleteInj(d, 'COVID-19 (Moderna)'), reason='Set the Injection Type')
	t.setup(lambda d: d.enterFormData('123456', name='vial'), reason='Set the Lot Number')
	t.setup(lambda d: d.enterFormData('Moderna, Inc.', name='manufacturer'), reason='Set the Manufacturer')
	t.setup(lambda d: d.enterFormData('02', name='expiration_dateMONTH'), reason='Set the Expiration Date')
	t.setup(lambda d: d.enterFormData('28', name='expiration_dateDAY'), reason='Set the Expiration Date')
	t.setup(lambda d: d.enterFormData('2030', name='expiration_dateYEAR'), reason='Set the Expiration Date')
	t.setup(lambda d: d.enterFormData('02', name='service_dateMONTH'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('02', name='service_dateDAY'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('2007', name='service_dateYEAR'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('09:15', name='service_dateTIME'), reason='Set the Administration Date')
	t.setup(lambda d: d.enterFormData('IM', name='route'), reason='Set the Route')
	t.setup(lambda d: d.enterFormData('RA', name='site'), reason='Set the Site')
	t.setup(lambda d: d.clickElement(xpath='//input[@value="Submit"]'), reason='Create the Document')
	t.setup(lambda d: d.navigate(WCURL.CHART_HART_WILLIAM + 't=Documents&v=list&lv_lv_wc_order=`Doc+ID`&lv_lv_wc_dir=DESC'), reason='View Documents List, Newest First')
	t.setup(lambda d: d.clickElement(xpath="//a[text()='Injection']"), reason='View the Newest Injection Document')
	t.setup(checkDocProperties)
	t.verifyElements([
		wcElement('xpath', "//td[contains(.,'All Out')]"),
		wcElement('xpath', "//td[contains(.,'Moderna Out')]"),
		wcElement('xpath', "//td[contains(.,'Pfizer Out')]", exists=False),
	], reason='The On Document Add Auto Routes are set up correctly.')
	t.test()

	# Update Generic injection to be Pfizer: Pfizer Injection Route, All Injections Route
	t = d.getWCUnitTest ('Update Generic Injection Document to be Pfizer')
	t.setup(lambda d: d.navigate(WCURL.CHART_HART_WILLIAM + 't=Medical+Record%3AMAR%2FInjections&v=inject'), reason='Injection Add Screen')
	t.setup(lambda d: d.clickElement(xpath="//a[text()='Hep A, adult']"), reason='Edit the non-Covid Injection Document')
	t.setup(lambda d: autocompleteInj(d, 'COVID-19 (Pfizer) Vaccine'), reason='Change the Injection Type')
	t.setup(lambda d: d.clickElement(xpath='//input[@value="Submit"]'), reason='Update the Document')
	t.setup(lambda d: d.navigate(WCURL.CHART_HART_WILLIAM + 't=Documents&v=list&lv_lv_wc_order=`Doc+ID`&lv_lv_wc_dir=DESC'), reason='View Documents List, Newest First')
	t.setup(lambda d: d.clickElement(xpath="//a[contains(., 'COVID-19 (Pfizer) Vaccine')]"), reason='View the Updated Injection Document')
	t.setup(checkDocProperties)
	t.verifyElements([
		wcElement('xpath', "//td[contains(.,'All Out')]"),
		wcElement('xpath', "//td[contains(.,'Moderna Out')]", exists=False),
		wcElement('xpath', "//td[contains(.,'Pfizer Out')]"),
	], reason='The On Document Update Auto Routes are set up correctly.')
	t.test()
