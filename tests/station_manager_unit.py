from wcunittest import wcElement

def goToStationMgrPage(d, data):
    d.navigate('?f=chart&s=checkin&t=station_manager&tabmodule=checkin&tabselect=Station+Manager')

def goToAddStationPage(d, data):
    d.navigate('?f=chart&s=checkin&t=station_manager&opp=add')

def goToEditStationPage(d, data):
    d.navigate('?f=chart&s=checkin&t=station_manager&opp=edit&id=14')

def clickGoBackToCheckin(d, data):
    d.clickElement(text='Go Back To Checkin')

def clickAddStation(d, data):
    d.clickElement(text='Add Station')

def clickEditStation(d, data):
    d.clickElement(xpath='//*[@id="lv_stationmanager_span"]/table/tbody/tr[5]/td[4]/a')

def enterStationDetails(d, data):
    d.enterFormData('NEWST', id='station_id')
    d.enterFormData('New Station', id='station_name')

def editStation(d, data):
    d.enterFormData('EDITED', id='station_id')
    d.enterFormData('Edited Station', id='station_name')
    d.enterFormData(False, id='station_active')

def enterIncomplete(d, data):
    d.enterFormData('ggg', id='station_id')
    d.enterFormData('', id='station_name')

def enterBlank(d, data):
    d.enterFormData('', id='station_id')
    d.enterFormData('', id='station_name')

def clickSave(d, data):
    d.clickElement(value='Save')

def clickChange(d, data):
    d.clickElement(value='Change')

def main(d, WCCurl):
# Test default station manager page layout
    t = d.getWCUnitTest('Default Station Manager Page Layout')

    t.setup(goToStationMgrPage)
    layout_basics = [
        wcElement('id', 'Station_20Manager_tab'),
        wcElement('text', 'Add Station'),
        wcElement('text', 'Go Back To Checkin'),
        wcElement('id', 'lv_root_Station_20Manager', width='100%'),
        wcElement('text', 'STATION ID'),
        wcElement('text', 'STATION NAME'),
        wcElement('text', 'ACTIVE'),
        wcElement('xpath', "//*[contains(., 'Options')]"),
        wcElement('xpath', "//*[contains(., 'Displaying')]"),
    ]

    showhide_show = [
        wcElement('id', 'lv_stationmanager_hide_link', onclick="hideShowlistview('webchart.cgi?f=chart&s=checkin&t=station_manager',8,'stationmanager',true,false);") # Show/Hide link-HIDE link is displayed, listview is shown
    ]

    showhide_hidden = [
        wcElement('id', 'lv_stationmanager_hide_link', onclick="hideShowlistview('webchart.cgi?f=chart&amp;s=checkin&amp;t=station_manager',8,'stationmanager',false,true);") # Show/Hide link-SHOW link is displayed, listview is hidden
    ]

    t.verifyElements(layout_basics, reason='Make sure the basic layout is correct')
    t.verifyElements(showhide_show, reason='Make sure the listview is shown by default')

    t.test()

# Test the 'Go Back to Checkin' link
    t = d.getWCUnitTest('Test the "Go Back to Checkin" link')

    t.setup(goToStationMgrPage)
    t.setup(clickGoBackToCheckin)

    checkin_page = [
        wcElement('id', 'Station_20Manager_tab'),
        wcElement('xpath', "//*[contains(., 'Criteria')]"),
        wcElement('id', 'location'),
        wcElement('id', 'selected_provider'),
        wcElement('id', 'PatientsInWaitingRoom'),
        wcElement('id', 'PatientsCheckedIn')
    ]

    t.verifyElements(checkin_page, reason='Make sure the link took us back to Checkin page')

    t.test()

# Test the Add Station Link and Add Station Page Layout
    t = d.getWCUnitTest('Test the Add Station Link and Page Layout')

    t.setup(goToStationMgrPage)
    t.setup(clickAddStation)

    add_station_page = [
        wcElement('id', 'Station_20Manager_tab'),
        wcElement('xpath', "//*[contains(., 'Station Add')]"),
        wcElement('id', 'station_id', size='20'),
        wcElement('id', 'station_name', size='30'),
        wcElement('name', 'station_submit', value='Save'),
        wcElement('name', 'station_cancel', value='Cancel'),
    ]

    t.verifyElements(add_station_page, reason='Make sure the Station Add page layout is correct')

    t.test()

# Test Adding a Station
    t = d.getWCUnitTest('Test Adding a New Station to Station Manager')

    t.setup(enterStationDetails)

    t.verifyElements([
        wcElement('xpath', "//*[contains(., 'Station was successfully inserted')]"),
        wcElement('xpath', "//*[contains(., 'NEWST')]"),
        wcElement('xpath', "//*[contains(., 'New Station')]"),
        wcElement('xpath', "//*[contains(., 'Yes')]/table/tbody/tr[5]/td[3]"),
    ], reason='Verify the new station was added successfully')

    t.test(clickSave)

# Test the Edit link and Edit Station Page Layout
    t = d.getWCUnitTest('Test the Add Station Link and Page Layout')

    t.setup(goToStationMgrPage)
    t.setup(clickEditStation)

    edit_station_page = [
        wcElement('id', 'Station_20Manager_tab'),
        wcElement('xpath', "//*[contains(., 'Station Edit')]"),
        wcElement('id', 'station_id', size='20'),
        wcElement('id', 'station_name', size='30'),
        wcElement('name', 'station_submit', value='Change'),
        wcElement('name', 'station_cancel', value='Cancel'),
    ]

    t.verifyElements(edit_station_page, reason='Make sure the Station Edit page layout is correct')

    t.test()

# Test Adding an Incomplete Station
    t = d.getWCUnitTest('Test Adding a Station with Incomplete Form Data')

    t.setup(goToAddStationPage)
    t.setup(enterIncomplete)

    t.verifyElements([
        wcElement('xpath', "//*[contains(., 'You must enter a valid Station ID and Name')]"),
    ], reason='Verify error message')

    t.test(clickSave)

# Test Editing Station with empty data
    t = d.getWCUnitTest('Test Editing a Station with Blank Form Data')

    t.setup(goToEditStationPage)
    t.setup(enterBlank)

    t.verifyElements([
        wcElement('xpath', "//*[contains(., 'You must enter a valid Station ID and Name')]"),
    ], reason='Verify error message')

    t.test(clickChange)

# Test Editing and setting a Station Inactive
    t = d.getWCUnitTest('Test Editing a Station in Station Manager')

    t.setup(goToEditStationPage)
    t.setup(editStation)

    t.verifyElements([
        wcElement('xpath', "//*[contains(., 'Station was successfully edited')]"),
        wcElement('xpath', "//*[contains(., 'EDITED')]"),
        wcElement('xpath', "//*[contains(., 'Edited Station')]"),
        wcElement('xpath', "//*[contains(., 'Yes')]/table/tbody/tr[2]/td[3]"),
    ], reason='Verify the new station was edited')

    t.test(clickChange)
