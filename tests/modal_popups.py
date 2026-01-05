#!/usr/bin/env python
# 
# Modal Popups Test

def main (d, WCURL):
    """
    Select Portlet
    """

    wd = d.getWebDriver()

    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import NoSuchElementException
    d.navigate(WCURL.OMNISCOPE, report=False)

    # START Open Popup Modal
    d.startSection('Open Popup Modal')
    d.clickElement(xpath='//*[@id="wc_macro"]')
    d.pause(4)
    d.verifyElementPresent(xpath='//div[@class="wc_win"]', present=True)
    d.endSection()

    # START Move Popup Modal
    try:
        d.startSection('Move Popup Modal Down and to the Right') # START Move Popup Modal Again
        d.pause(4)
        try:
            modal = wd.find_element_by_xpath('//*[@id="macros_help"]/div/div[1]')
        except AttributeError:
            from selenium.webdriver.common.by import By
            modal = wd.find_element(By.XPATH, '//*[@id="macros_help"]/div/div[1]')
        original_location = modal.location
        ActionChains(wd).drag_and_drop_by_offset(modal, 30,15).perform()
        move_to_location = modal.location
        change_x = 30
        change_y = 15
        d.reportCommandStatus('Move X position by ' + str(change_x), 'actual X position | should be ', move_to_location['x'] == original_location['x'] + change_x, move_to_location['x'], original_location['x'] + change_x)
        d.reportCommandStatus('Move Y position by ' + str(change_y), 'actual Y position | should be ', move_to_location['y'] == original_location['y'] + change_y, move_to_location['y'], original_location['y'] + change_y)
    finally:
        d.endSection()

    # START Move Popup Modal
    try:
        d.startSection('Move Popup Modal Up and to the Left')
        original_location = modal.location
        change_x = -20
        change_y = -20
        ActionChains(wd).drag_and_drop_by_offset(modal, change_y, change_x).perform()
        move_to_location = modal.location
        d.reportCommandStatus('Move X position by ' + str(change_x), 'actual X position | should be ', move_to_location['x'] == original_location['x'] + change_x, move_to_location['x'], original_location['x'] + change_x)
        d.reportCommandStatus('Move Y position by ' + str(change_y), 'actual Y position | should be ', move_to_location['y'] == original_location['y'] + change_y, move_to_location['y'], original_location['y'] + change_y)
    finally:
        d.endSection()

    # START Resize Popup Modal Again
    try:
        d.startSection('Make Popup Modal Larger')
        try:
            modal = wd.find_element_by_xpath('//*[@id="macros_help"]')
            move_element = wd.find_element_by_xpath('//*[@id="macros_help"]/div/div/div[3]')
        except AttributeError:
            from selenium.webdriver.common.by import By
            modal = wd.find_element(By.XPATH, '//*[@id="macros_help"]')
            move_element = wd.find_element(By.XPATH, '//*[@id="macros_help"]/div/div/div[3]')
        original_size = modal.size
        change_x = 2
        change_y = 2
        ActionChains(wd).drag_and_drop_by_offset(move_element, change_y, change_x).perform()
        size = modal.size
        d.reportCommandStatus('Change width by ' + str(change_x), 'actual width | should be ', size['width'] == original_size['width'] + change_x, size['width'], original_size['width'] + change_x)
        d.reportCommandStatus('Change height by ' + str(change_y), 'actual height | should be ', size['height'] == original_size['height'] + change_y, size['height'], original_size['height'] + change_y)
    finally:
        d.endSection()

    # START Resize Popup Modal
    d.startSection('Make Popup Modal Smaller')
    try:
        try:
            modal = wd.find_element_by_xpath('//*[@id="macros_help"]')
            move_element = wd.find_element_by_xpath('//*[@id="macros_help"]/div/div/div[3]')
        except AttributeError:
            from selenium.webdriver.common.by import By
            modal = wd.find_element(By.XPATH, '//*[@id="macros_help"]')
            move_element = wd.find_element(By.XPATH, '//*[@id="macros_help"]/div/div/div[3]')
        original_size = modal.size
        change_x = -20
        change_y = -20
        ActionChains(wd).drag_and_drop_by_offset(move_element, change_y, change_x).perform()
        size = modal.size
        d.reportCommandStatus('Change width by ' + str(change_x), 'actual width | should be ', size['width'] == original_size['width'] + change_x, size['width'], original_size['width'] + change_x)
        d.reportCommandStatus('Change height by '+ str(change_y), 'actual height | should be ', size['height'] == original_size['height'] + change_y, size['height'], original_size['height'] + change_y)
    finally:
        d.endSection()

    # START Move Popup Modal
    d.startSection('Close Popup Modal')
    d.clickElement(xpath='//*[@id="macros_help"]//div/button[@class="xclose"]')
    d.verifyElementPresent(present=False,xpath="//div[@id='macros_help']")
    d.endSection()
