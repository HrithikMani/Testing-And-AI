from wcunittest import wcElement


def goToOmniScope(d, data):
	d.navigate('?func=omniscope')
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wcstatus_warning")]'), expected_return=False, timeout=10)

def goToHart(d, data):
	d.navigate('?f=chart&s=pat&pat_id=18')
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wcstatus_warning")]'), expected_return=False, timeout=10)

def clickHome(d, data):
	d.clickElement(xpath='//a[@id="wc_homeicon" and @title="Home"]')

def clickAlertEsign(d, data):
	d.clickElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "esign") and contains(., "Esign")]')

def clickAlertTasks(d, data):
	d.clickElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "My Tasks")]')

def clickAlertPhysicians(d, data):
	d.clickElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "Physicians")]')

def clickAlertOrders(d, data):
	d.clickElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "Orders") or contains(@href, "orders") and contains(., "Orders")]')

def clickAlertDocQ(d, data):
	d.clickElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "docq") and contains(., "Doc Queue")]')

def waitAlerts(d, data):
	d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "esign") and contains(., "Esign")]/span[@class="count"]'), expected_return=True, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "My Tasks")]/span[@class="count"]'), expected_return=True, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "Physicians")]/span[@class="count"]'), expected_return=True, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "Orders") or contains(@href, "orders") and contains(., "Orders")]'), expected_return=True, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//div[@id="wc_alerts"]//a[contains(@href, "docq") and contains(., "Doc Queue")]/span[@class="count"]'), expected_return=True, timeout=30)

def search(d, text):
	d.clickElement(xpath='//span[@id="wc_search_icon" and @title="Search" and contains(@class, "fa-search")]')
	d.enterFormData(text, id="wc_search_input", blur="False")
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a'), expected_return=True, timeout=5)

def clickTimeZone(d, data):
	d.clickElement(xpath='//div[@id="wc_applicationbar"]//span[@id="header_timezone"]/span[@title="Time Zone"]')
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "wc_win")]'), expected_return=True, timeout=30)

def enterTimeZone(d, data):
	text = data['text']
	idx = data['idx']
	d.enterFormData(text, id='Time_Zone_acinp', blur=False, clear=True)
	acchoice = d.waitFor(d, lambda d: d.getElement(id='Time_Zone_ac_choices_%d' %idx), expected_return=True, timeout=30)
	if not acchoice:
		d.reportCommandStatus('Timeout', '', False, '', 'Autocomplete choices not displayed')
	else:
		d.clickElement(id='Time_Zone_ac_choices_%d' %idx)
	d.clickElement(xpath='//input[@id="WebChart_save_settings" and @value="Save"]')




def main(d, WCCurl):
	d.startSection('Application bar')
	d.startSection('TODO-Side Menu icon')
	d.endSection()



	d.startSection('Home icon')
	t = d.getWCUnitTest('Verify the Home icon is present from OmniScope')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//a[@id="wc_homeicon" and @title="Home"]'),
		wcElement('xpath', '//title[contains(., "OmniScope") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Home icon is present')
	t.test()

	t = d.getWCUnitTest('Verify the Home icon is present from a patient\'s chart')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//a[@id="wc_homeicon" and @title="Home"]'),
		wcElement('xpath', '//title[contains(., "Summary") and (contains(., "WebChart") or contains(., "Enterprise Health"))]'),
		wcElement('xpath', '//div[@id="wc_pat_bar"]//a[contains(., "Hart, William")]')
	], reason='Verify the Home icon is present')
	t.test()

	t = d.getWCUnitTest('Test navigating to OmniScope from a patient\'s chart')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "OmniScope") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Home icon is present')
	t.test(clickHome)
	d.endSection()



	d.startSection('Alerts')
	d.startSection('From OmniScope')
	t = d.getWCUnitTest('Verify Alerts and their counts are present from OmniScope')
	t.setup(goToOmniScope)
	wctoolbaralerts = [
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "esign") and contains(., "Esign")]/span[@class="count"]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "My Tasks")]/span[@class="count"]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "Physicians")]/span[@class="count"]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "Orders") or contains(@href, "orders") and contains(., "Orders")]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "docq") and contains(., "Doc Queue")]/span[@class="count"]'),
	]
	t.verifyElements(wctoolbaralerts, reason='Verify the Alerts are present')
	t.test(waitAlerts)

	t = d.getWCUnitTest('Navigate to Esign Alert from OmniScope')
	t.setup(goToOmniScope)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "E-Signature") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Esign Alert link navigates to the appropriate page')
	t.test(clickAlertEsign)

	t = d.getWCUnitTest('Navigate to My Tasks Alert from OmniScope')
	t.setup(goToOmniScope)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "tasklist") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the My Tasks Alert link navigates to the appropriate page')
	t.test(clickAlertTasks)

	t = d.getWCUnitTest('Navigate to Physicians Alert from OmniScope')
	t.setup(goToOmniScope)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "tasklist") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Physicians Alert link navigates to the appropriate page')
	t.test(clickAlertPhysicians)

	t = d.getWCUnitTest('Navigate to Orders Alert from OmniScope')
	t.setup(goToOmniScope)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[(contains(., "Orders") or contains(., "SystemReport") or contains(., "Unordered Orders")) and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Orders Alert link navigates to the appropriate page')
	t.test(clickAlertOrders)

	t = d.getWCUnitTest('Navigate to Doc Queue Alert from OmniScope')
	t.setup(goToOmniScope)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "Document Queue") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Doc Queue Alert link navigates to the appropriate page')
	t.test(clickAlertDocQ)
	d.endSection()

	d.startSection('From a Patient\'s Chart')
	t = d.getWCUnitTest('Verify Alerts and their counts are present from Patient\'s Chart')
	t.setup(goToHart)
	wctoolbaralerts = [
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "esign") and contains(., "Esign")]/span[@class="count"]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "My Tasks")]/span[@class="count"]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "tlist") and contains(., "Physicians")]/span[@class="count"]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "Orders") or contains(@href, "orders") and contains(., "Orders")]'),
		wcElement('xpath', '//div[@id="wc_alerts"]//a[contains(@href, "docq") and contains(., "Doc Queue")]/span[@class="count"]'),
	]
	t.verifyElements(wctoolbaralerts, reason='Verify the Alerts are present')
	t.test(waitAlerts)

	t = d.getWCUnitTest('Navigate to Esign Alert from Hart')
	t.setup(goToHart)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "E-Signature") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Esign Alert link navigates to the appropriate page')
	t.test(clickAlertEsign)

	t = d.getWCUnitTest('Navigate to My Tasks Alert from Hart')
	t.setup(goToHart)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "tasklist") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the My Tasks Alert link navigates to the appropriate page')
	t.test(clickAlertTasks)

	t = d.getWCUnitTest('Navigate to Physicians Alert from Hart')
	t.setup(goToHart)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "tasklist") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Physicians Alert link navigates to the appropriate page')
	t.test(clickAlertPhysicians)

	t = d.getWCUnitTest('Navigate to Orders Alert from Hart')
	t.setup(goToHart)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[(contains(., "Orders") or contains(., "SystemReport") or contains(., "Unordered Orders")) and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Orders Alert link navigates to the appropriate page')
	t.test(clickAlertOrders)

	t = d.getWCUnitTest('Navigate to Doc Queue Alert from Hart')
	t.setup(goToHart)
	t.setup(waitAlerts)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "Document Queue") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify the Doc Queue Alert link navigates to the appropriate page')
	t.test(clickAlertDocQ)
	d.endSection()
	d.endSection()



	d.startSection('User icon')
	t = d.getWCUnitTest('Verify the User icon is present from OmniScope')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "OmniScope") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on OmniScope page')
	t.verifyElements([
		wcElement('xpath', '//span[@title="User"]/following-sibling::span[contains(., "Selenium, Selenium")]/em[contains(., "System Owner")]')
	], reason='Verify the User icon is present and displays the currently set User and User role')
	t.test()

	t = d.getWCUnitTest('Verify the User icon is present from Hart')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "Summary") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on Patient\'s page')
	t.verifyElements([
		wcElement('xpath', '//span[@title="User"]/following-sibling::span[contains(., "Selenium, Selenium")]/em[contains(., "System Owner")]')
	], reason='Verify the User icon is present and displays the currently set User and User role')
	t.test()
	d.endSection()



	d.startSection('Time Zone icon')

	d.startSection('Verify presence from OmniScope and from a Patient\'s chart')
	t = d.getWCUnitTest('Verify the Time Zone icon is present from OmniScope')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "OmniScope") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on OmniScope page')
	t.verifyElements([
		wcElement('xpath', '//span[@title="Time Zone"]/parent::span[contains(., "US/Eastern")]')
	], reason='Verify the Time Zone icon is present and displays the currently set time zone')
	timezonepopup = [
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[@class="wc_win_title" and contains(., "WebChart Preferences")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//td[@class="subtitle" and contains(., "User Interface")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//td[@class="field" and contains(., "Time Zone")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//td[@class="field" and contains(., "Time Zone")]/following-sibling::td[@class="value"]//input[contains(@class, "autocomplete") and contains(@name, "Time_Zone_acinp")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//input[@id="WebChart_save_settings" and @value="Save"]')
	]
	t.verifyElements(timezonepopup, reason='Verify elements present for the WebChart Preferences-Time Zone popup')
	t.test(clickTimeZone)

	t = d.getWCUnitTest('Verify the Time Zone icon is present from Hart')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "Summary") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on Patient\'s page')
	t.verifyElements([
		wcElement('xpath', '//span[@title="Time Zone"]/parent::span[contains(., "US/Eastern")]')
	], reason='Verify the Time Zone icon is present and displays the currently set time zone')
	timezonepopup = [
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[@class="wc_win_title" and contains(., "WebChart Preferences")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//td[@class="subtitle" and contains(., "User Interface")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//td[@class="field" and contains(., "Time Zone")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//td[@class="field" and contains(., "Time Zone")]/following-sibling::td[@class="value"]//input[contains(@class, "autocomplete") and contains(@name, "Time_Zone_acinp")]'),
		wcElement('xpath', '//div[@id="WebChartprefs_win"]//div[contains(@class, "wc_win_body")]//input[@id="WebChart_save_settings" and @value="Save"]')
	]
	t.verifyElements(timezonepopup, reason='Verify elements present for the WebChart Preferences-Time Zone popup')
	t.test(clickTimeZone)
	d.endSection()

	d.startSection('Test changing the time zone from the Time Zone icon')
	t = d.getWCUnitTest('Change from US/Eastern to US/Pacific time zone')
	t.setup(goToOmniScope)
	t.setup(clickTimeZone)
	t.verifyElements([
		wcElement('xpath', '//span[@title="Time Zone"]/parent::span[contains(., "US/Pacific")]')
	], reason='Verify the Time Zone change from US/Eastern to US/Pacific is reflected next to the Time Zone icon', timeout=6)
	t.test(enterTimeZone, {'text':'US/Pacific', 'idx':0})

	t = d.getWCUnitTest('Change from US/Pacific to Australia/Brisbane time zone')
	t.setup(goToOmniScope)
	t.setup(clickTimeZone)
	t.verifyElements([
		wcElement('xpath', '//span[@title="Time Zone"]/parent::span[contains(., "Australia/Brisbane")]')
	], reason='Verify the Time Zone change from US/Pacific to Australia/Brisbane is reflected next to the Time Zone icon', timeout=6)
	t.test(enterTimeZone, {'text':'Australia/Brisbane', 'idx':0})

	t = d.getWCUnitTest('Change back to US/Eastern from Australia/Brisbane time zone')
	t.setup(goToOmniScope)
	t.setup(clickTimeZone)
	t.verifyElements([
		wcElement('xpath', '//span[@title="Time Zone"]/parent::span[contains(., "US/Eastern")]')
	], reason='Verify the Time Zone change from Australia/Brisbane to US/Eastern is reflected next to the Time Zone icon', timeout=6)
	t.test(enterTimeZone, {'text':'US/Eastern', 'idx':0})
	d.endSection()
	d.endSection()



	d.startSection('Search')
	d.startSection('Verify presence from OmniScope and from a Patient\'s chart')
	t = d.getWCUnitTest('Verify the Search icon is present from OmniScope')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "OmniScope") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on OmniScope page')
	t.verifyElements([
		wcElement('xpath', '//span[@title="Search"]')
	], reason='Verify the Search icon is present')
	t.test()

	t = d.getWCUnitTest('Verify the Search icon is present from Hart')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "Summary") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on Patient\'s page')
	t.verifyElements([
		wcElement('xpath', '//span[@title="Search"]')
	], reason='Verify the Search icon is present')
	t.test()
	d.endSection()

	d.startSection('Perform Searches')

	d.startSection('Search for a Document Type')
	t = d.getWCUnitTest('Search for a Document Type')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "doc_types")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "Task Note")]')
	], reason='Verify the search results find a Document Type')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'task')
	d.endSection()

	d.startSection('Search for a Layout')
	t = d.getWCUnitTest('Search for a Layout')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "layouts")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "View Absence Management")]')
	], reason='Verify the search results find a Layout')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'absence')
	d.endSection()

	d.startSection('Search for a Provider')
	t = d.getWCUnitTest('Search for a Provider')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "providers")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "Selenium Selenium")]')
	], reason='Verify the search results find a Provider')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'sel')
	d.endSection()

	d.startSection('Search for a Employees/Patients')
	t = d.getWCUnitTest('Search for a Employee/Patient')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "patients")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "William Hart")]')
	], reason='Verify the search results find a Patient')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'Hart')
	d.endSection()

	d.startSection('Search for a Employee/Provider Organizations')
	t = d.getWCUnitTest('Search for a Employee/Provider Organization')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "eopo")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "Better Corp.")]')
	], reason='Verify the search results find a Employee/Provider Organization')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'bet')
	d.endSection()

	d.startSection('Search for a Menu Tabs')
	t = d.getWCUnitTest('Search for a Tab')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "tabs")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "Health Surveillance")]')
	], reason='Verify the search results find a Menu Tabs')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'hea')
	d.endSection()

	d.startSection('Search for Chart Tabs')
	t = d.getWCUnitTest('Search for a Chart Tab from Omniscope')
	t.setup(goToOmniScope)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]//strong[contains(., "Chart Tabs")]')
	], reason='Verify the results don\'t produce any chart tabs', exists=False)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'hea')

	t = d.getWCUnitTest('Search for a Chart Tab from Patient')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "charttabs")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "Health Surveillance")]')
	], reason='Verify the search results finds a Chart Tab')
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section") and contains(@class, "charttabs")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/div/a[contains(., "Health Assessment Plan")]')
	], reason='Verify the search results don\'t find a Chart Tab from a different chart type', exists=False)
	t.verifyElements([
		wcElement('xpath', '//div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]/parent::div/following-sibling::div[contains(@class, "search-sub-section")]/div[contains(@class, "search-sub-title")]/following-sibling::div[contains(@class, "search-sub-results")]')
	], reason='Verify the results produce multiple results and more than one section, title, and results')
	t.test(search, 'hea')
	d.endSection()
	d.endSection()
	d.endSection()



	d.startSection('Subscription')
        # systemAlerts is no longer a global subscription and since it was the only one
        # on this page, we may or may not expect the link icon, so no point in checking it
	#t = d.getWCUnitTest('Verify the Subscription Status icon is present from OmniScope')
	#t.setup(goToOmniScope)
	#t.verifyElements([
	#	wcElement('xpath', '//title[contains(., "OmniScope") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	#], reason='Verify we are on OmniScope page')
	#t.verifyElements([
	#	wcElement('xpath', '//span[@id="wc_subscriptionstatus" and contains(@title, "Connected") or contains(@title, "connected")]')
	#], reason='Verify the Subscription Status icon is present')
	#t.test()

	t = d.getWCUnitTest('Verify the Subscription Status icon is present from Hart')
	t.setup(goToHart)
	t.verifyElements([
		wcElement('xpath', '//title[contains(., "Summary") and (contains(., "WebChart") or contains(., "Enterprise Health"))]')
	], reason='Verify we are on Patient\'s page')
	t.verifyElements([
		wcElement('xpath', '//span[@id="wc_subscriptionstatus" and contains(@title, "Connected") or contains(@title, "connected")]')
	], reason='Verify the Subscription Status icon is present')
	t.test()
	d.endSection()



	d.startSection('TODO - Macros')
	d.endSection()



	d.startSection('TODO - Language')
	d.startSection('Verify presence from OmniScope and from a Patient\'s chart')
	d.endSection()

	d.startSection('Test changing languages')
	d.startSection('Simplified Chinese')
	d.endSection()

	d.startSection('Dutch')
	d.endSection()

	d.startSection('Indonesian')
	d.endSection()

	d.startSection('Portuguese')
	d.endSection()

	d.startSection('Spanish')
	d.endSection()

	d.startSection('Russian')
	d.endSection()

	d.startSection('Thai')
	d.endSection()

	d.startSection('Vietnamese')
	d.endSection()

	d.startSection('Change back to English')
	d.endSection()
	d.endSection()

	d.startSection('Adding Translations')
	d.startSection('Adding Translations from the Languages popup')
	d.endSection()

	d.startSection('Adding Translations from within Webchart')
	d.endSection()
	d.endSection()

	d.startSection('Close Languages')
	d.endSection()
	d.endSection()



	d.startSection('TODO - Keyboard Shortcuts')
	d.endSection()



	d.startSection('TODO - Help')
	d.endSection()



	d.startSection('TODO - Show Errors')
	d.endSection()

	d.endSection()
