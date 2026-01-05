"""
@owners: dhaneline
"""

from wcunittest import wcElement, wcDBRecord

def clickElement(d, text):
    if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete'):
        d.reportCommandStatus('LayoutOps', driver.runJS('return wcutils._layoutOps'), None, 'isWaiting()', driver.runJS('return miehttp.isWaiting()'))
    d.clickElement(text=text)
    if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete'):
        d.reportCommandStatus('LayoutOps', driver.runJS('return wcutils._layoutOps'), None, 'isWaiting()', driver.runJS('return miehttp.isWaiting()'))

def insertDoeAppt(d):
	d.miedb.dbExec(f'INSERT INTO appointments (id, pat_id, startdate, enddate, pat_duration, reason, location, user_id, createdate, recurrence) VALUES ("94", "6", "{d.getUserData("run_date")} 09:00:00", "{d.getUserData("run_datetime")}", "15", "test", "OFFICE", "2", "{d.getUserData("run_date")} 08:00:00", "0")')
	d.miedb.dbExec('INSERT INTO multi_resource_apt (apt_id, res_id) VALUES ("94", "8")')

def enterNewStation(d, data):
	d.clickElement(xpath='//span[contains(@class, "checkinlink")]/a[contains(text(),"Checkin")]')
	d.wcutils.waitForEle(xpath='//span[contains(@class, "checkinlink")]/a[contains(text(),"Waiting Room (0s)")]', timeout=60)
	d.clickElement(xpath='//span[contains(@class, "checkinlink")]/a[contains(text(),"Waiting Room (0s)")]')
	d.enterFormData('Exam Room 2', id='station_id')
	d.enterFormData('Moved to exam room 2', xpath='//td[@class="field"][contains(.,"Comment")]/following-sibling::td/textarea')
	d.clickElement(xpath='//div[@class="wc_win"]//input[@type="button" and @value="Save"]')

def goToHart(d, data):
	d.navigate('?f=chart&s=pat&pat_id=18')
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.wcutils.waitForEle(xpath='//div[@id="wc_pat_bar"]//span/span[contains(., "Hart, William")]', timeout=60)

def goToAppt(d, data):
	d.navigate('?f=sched&s=appointment&pat_id=18&startdateDAY=2&startdateMONTH=2&startdateYEAR=2007&startdateTIME=09%3A15am')

def goToSchedule(d, data):
	d.navigate('?func=scheduler&res_id=8#Now')

def goToCheckinPage(d, data):
	d.navigate('?f=chart&s=checkin')

def clickCheckinQuickLink(d, data):
	d.clickElement(xpath='//div[@class="portlet"]/div[contains(., "Quick Links")]/following-sibling::div//div//a[contains(.,"Checkin")]')
	d.wcutils.waitForEle(xpath='//title[contains(.,"E-Chart CheckIn")]', timeout=60)

def clickExamRoomQuickLink(d, data):
	d.clickElement(xpath='//div[@class="portlet"]/div[contains(., "Quick Links")]/following-sibling::div//div//a[contains(.,"Exam Room")]')
	d.wcutils.waitForEle(xpath='//div[@class="wc_win_title" and contains(.,"Enter New Station Details")]', timeout=120)

def enterCheckinDetails(d, data):
	d.wcutils.waitForAJAX(timeout=60, quiet=5)
	d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath='//td[contains(text(),"Notes")]'))
	d.waitFor(d, lambda d: d.getElement(xpath='//select[@id="station_id"]'), expected_return=True, timeout=30)
	d.enterFormData('Exam Room 1', id='station_id')
	d.enterFormData('Checkin', id='patient_type')
	d.clickElement(value='Save')
	d.waitFor(d, lambda d: d.runJS("return MIE.WC_DataVis.grids['PatientsCheckedIn'].isIdle()"), expected_return=True, timeout=30)

def main(d, WCURL):
	t = d.getWCUnitTest('One-Click Checkin')
	t.setup(insertDoeAppt)
	t.setup(goToSchedule)
	t.test(enterNewStation)

	t = d.getWCUnitTest('Non One-Click Checkin')
	t.setup(goToHart)
	t.setup(clickCheckinQuickLink)
	t.verifyElements([
		wcElement('id', 'location', name='location'),
		wcElement('id', 'selected_provider'),
	], reason='Make sure the page has two criteria dropdowns')
	t.verifyElements([
		wcElement('id', 'PatientsInWaitingRoom'),
		wcElement('id', 'PatientsCheckedIn'),
	], reason='Verify 2 listviews appear')
	t.verifyElements([
		wcElement('text', 'TEST-10019'),
		wcElement('xpath', '//tr[@id="PatientsCheckedIn_gridContainer_1"]//a[contains(text(),"Open")]'),
	], reason='Make sure Hart is now in the listview')
	t.test(enterCheckinDetails)

	t = d.getWCUnitTest('Verify Doe and Hart are both checked into exam rooms on the Checkin page')
	t.setup(goToCheckinPage)
	t.verifyElements([
		wcElement('text', 'TEST-10019'),
		wcElement('text', 'TEST-10007'),
		wcElement('text', 'Hart, William, S.'),
		wcElement('text', 'Doe, John, L.'),
		wcElement('text', 'N/A'),
		wcElement('text', '02-02-2007 09:00'),
		wcElement('text', 'Moved to exam room 2'),
		wcElement('text', 'Exam Room 1'),
		wcElement('text', 'Exam Room 2'),
	], reason='Make sure William Hart and John Doe have been moved to Exam Rooms 1 & 2 on the Checkin page')
	t.test

	t = d.getWCUnitTest('Default Checkin Sidemenu Page Layout/Elements')
	t.setup(goToCheckinPage)
	dropdowns = [
		wcElement('id', 'location', name='location'),
		wcElement('id', 'selected_provider'),
	]
	t.verifyElements(dropdowns, reason='Make sure the page has two criteria dropdowns')
	t.verifyElements([
		wcElement('id', 'PatientsInWaitingRoom'),
		wcElement('id', 'PatientsCheckedIn'),
	], reason='Verify 2 listviews appear')
	t.test()

	t = d.getWCUnitTest('Checkin Form From E-Chart Layout/Elements')
	t.setup(goToHart)
	t.verifyElements([wcElement('id', 'station_id')], reason='Station dropdown has to be there')
	t.test(clickExamRoomQuickLink)

	t = d.getWCUnitTest("New Station Details popup Layout/Elements")
	t.setup(goToHart)
	t.setup(clickElement, 'Exam Room 1 (0s)')
	t.verifyElements([
		wcElement('xpath', '//div[@class="wc_win"]//div[@class="wc_win_title"][contains(.,"Enter New Station Details")]'),
		wcElement('xpath', '//div[@class="wc_win"]//div[contains(@class,"wc_win_body")]/table/tbody/tr/td[@class="field"][contains(.,"New Station")]'),
		wcElement('xpath', '//div[@class="wc_win"]//div[contains(@class,"wc_win_body")]/table/tbody/tr/td[@class="field"][contains(.,"Comment")]'),
		wcElement('id', 'station_id'),
		wcElement('xpath', '//td[@class="field"][contains(.,"Comment")]/following-sibling::td/textarea'),
		wcElement('value', 'Save'),
		wcElement('value', 'Cancel'),
		wcElement('xpath', '//select/option[contains(.,"Checkout")]'),
		wcElement('xpath', '//select/option[contains(.,"Completing Questionnaire")]'),
		wcElement('xpath', '//select/option[contains(.,"Exam Room 1")]'),
		wcElement('xpath', '//select/option[contains(.,"Exam Room 2")]', exists=False),
		wcElement('xpath', '//select/option[contains(.,"Exam Room 3")]'),
		wcElement('xpath', '//select/option[contains(.,"Waiting Room")]'),
	], reason='Check that the New Station Details wc_win elements are present except Exam Room 2 because John Doe is already checked into Exam Room 2')
	t.test()

	t = d.getWCUnitTest("Station Manager Page Layout/Elements")
	t.setup(goToCheckinPage)
	t.setup(clickElement, 'Station Manager')
	t.verifyElements([
		wcElement('xpath', '//a[contains(.,"Add Station")]'),
		wcElement('xpath', '//a[contains(.,"Go Back To Checkin")]'),
		wcElement('text', 'Station Manager'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/thead/tr/th/a[contains(.,"Station Name")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/thead/tr/th/a[contains(.,"Station Name")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/thead/tr/th/a[contains(.,"Active")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/thead/tr/th[contains(.,"Options")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"STATION1")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"STATION2")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"STATION3")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"STATION4")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"STATION5")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"Completing Questionnaire")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"Waiting Room")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"Exam Room 1")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"Exam Room 2")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"Exam Room 3")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tbody/tr/td[contains(.,"Yes")]'),
		wcElement('xpath', '//a[contains(.,"Edit")]'),
		wcElement('xpath', '//div[@id="lv_stationmanager_span"]/table/tfoot/tr/td[contains(.,"Displaying 1-5 / 5")]'),
	], reason='Check Station Manager Page Elements')
	t.test()

	t = d.getWCUnitTest("Station Add Page Layout/Elements")
	t.setup(goToCheckinPage)
	t.setup(clickElement, 'Station Manager')
	t.setup(clickElement, 'Add Station')
	t.verifyElements([
		wcElement('xpath', '//fieldset//span[contains(.,"Station Add")]'),
		wcElement('xpath', '//fieldset//table/tbody/tr/td[contains(.,"Station ID")]'),
		wcElement('xpath', '//fieldset//table/tbody/tr/td[contains(.,"Station Name")]'),
		wcElement('xpath', '//fieldset//table/tbody/tr/td[contains(.,"Active")]'),
		wcElement('value', 'Save'),
		wcElement('value', 'Cancel'),
		wcElement('id', 'station_id'),
		wcElement('id', 'station_name'),
		wcElement('id', 'station_active'),
	], reason='Check Station Add Page Elements')
	t.test()

	t = d.getWCUnitTest("Station Edit Page Layout/Elements")
	t.setup(goToCheckinPage)
	t.setup(clickElement, 'Station Manager')
	t.setup(clickElement, 'Edit')
	t.verifyElements([
		wcElement('xpath', '//fieldset//span[contains(.,"Station Edit")]'),
		wcElement('xpath', '//fieldset//table/tbody/tr/td[contains(.,"Station ID")]'),
		wcElement('xpath', '//fieldset//table/tbody/tr/td[contains(.,"Station Name")]'),
		wcElement('xpath', '//fieldset//table/tbody/tr/td[contains(.,"Active")]'),
		wcElement('value', 'Change'),
		wcElement('value', 'Cancel'),
		wcElement('id', 'station_id'),
		wcElement('id', 'station_name'),
		wcElement('id', 'station_active'),
	], reason='Check Station Edit Page Elements')
	t.test()
