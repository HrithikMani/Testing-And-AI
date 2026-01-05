#!/usr/bin/env python
# 
# Portlet Test

def main (d, WCURL):
    """
    Select Portlet
    """

    wd = d.getWebDriver()

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import NoSuchElementException
    d.navigate(WCURL.OMNISCOPE, report=False)
    
    # START Open Modules Modals
    d.startSection('Open Modules Modal')
    d.clickElement(xpath="//span[text()='Select Portlets']")
    d.verifyElementPresent(xpath="//div[@class='wc_win_title' and text()='Available Portlets']")
    d.endSection()

    # START Clear all checkboxes in Modules Modal
    d.startSection('Clear all checkboxes in Modules Modal')
    checkboxes = d.getElements(xpath="//div[@class='four-column']//input[@checked]")
    for checkbox in checkboxes:
        checkboxvalue = checkbox.get_attribute('value')
        checkboxstate = checkbox.get_attribute('checked')
        if checkboxstate != None:
            d.startSection('Uncheck' + checkboxvalue)
            d.clickElement(xpath="//input[@type='checkbox' and @value='"+checkboxvalue+"']")
            d.verifyAttribute(xpath="//input[@type='checkbox' and @value='"+checkboxvalue+"']", attr='checked',val='false')
            d.endSection()
    d.endSection()

    # START Select Portlets
    d.startSection('Select Portlets')
    d.clickElement(xpath="//input[@value='Alerts']")
    d.verifyAttribute(attr='checked', val='true',xpath="//input[@value='Alerts']")
    d.clickElement(xpath="//input[@value='Checkin']")
    d.verifyAttribute(attr='checked', val='true',xpath="//input[@value='Checkin']")
    d.clickElement(xpath="//input[@value='Schedule']")
    d.verifyAttribute(attr='checked', val='true',xpath="//input[@value='Schedule']")
    d.clickElement(xpath="//input[@value='Save']")
    d.endSection()

    # START Collapse Portlet
    d.startSection('Collapse Portlet') 
    d.pause(4)
    d.clickElement(xpath="//div[@id='moveable_shade_User_20Portlet_Alerts']")
    d.verifyElementPresent(xpath='//*[@id="moveable_container_User_20Portlet_Alerts" and contains(@class, "shade")]')
    d.endSection()

    # START Move Portlet
    d.startSection('Move Portlet')
    try:
        # Verify that Schedule portlet first exists in the left column:
        d.verifyElementPresent(xpath='//div[@id="User_20Portlet_row0col0"]/div[@id="moveable_container_User_20Portlet_Schedule"]')
        try:
            # Find and define the Schedule portlet's move icon:
            portlet = wd.find_element_by_id('moveable_grab_User_20Portlet_Schedule')
        
            # Find and define the right column:
            column_right = wd.find_element_by_id('User_20Portlet_row0col1')
        except AttributeError:
            from selenium.webdriver.common.by import By
            # Find and define the Schedule portlet's move icon:
            portlet = wd.find_element(By.ID, 'moveable_grab_User_20Portlet_Schedule')
        
            # Find and define the right column:
            column_right = wd.find_element(By.ID, 'User_20Portlet_row0col1')
        
        # Click and hold the Schedule portlet's move icon:
        ActionChains(wd).click_and_hold(portlet).perform()
        
        # Drag the Schedule portlet's move icon over the right column:
        ActionChains(wd).move_to_element(column_right).perform()

        d.pause(4)  # Wait long enough for the drop zone placeholder to appear.
        
        # Release the Schedule portlet's move icon:
        ActionChains(wd).release(portlet).perform()

        # Verify that Schedule portlet now exists in the right column:
        d.verifyElementPresent(xpath='//div[@id="User_20Portlet_row0col1"]/div[@id="moveable_container_User_20Portlet_Schedule"]')
    finally:
        d.endSection()

    # START Close Portlet
    d.startSection('Close Portlet')
    d.clickElement(xpath="//div[@id='moveable_remove_User_20Portlet_Alerts']")
    d.verifyElementPresent(present=False,xpath="//div[@id='moveable_container_User_20Portlet_Alerts']")
    d.endSection()
