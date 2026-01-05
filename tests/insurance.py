from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
import uuid

def printEltInfo(elt):
    print(elt)
    print(elt.tag_name)
    print(elt.text)

def editInsurance(driver, plan_name):
    """ Select the link from the insurance listview to edit the insurance with
    the specified name. """

    insurance_table = driver.getElement(id = 'lv_insurance_policy_span')

    show_all = driver.getElement(xpath = '//#lv_insurance_policy_span//font[text() = "Show All"]')
    if show_all != None:
        show_all.click()
    try:
        plan_popup_link = insurance_table.find_element_by_xpath('//font[text() = "%s"]' % (plan_name))
        #printEltInfo(plan_popup_link)

        edit_link = plan_popup_link.find_element_by_xpath('../../../..//font[text() = "Edit"]')
        #printEltInfo(edit_link)
    except AttributeError:
        from selenium.webdriver.common.by import By
        plan_popup_link = insurance_table.find_element(By.XPATH, '//font[text() = "%s"]' % (plan_name))
        #printEltInfo(plan_popup_link)
        edit_link = plan_popup_link.find_element(By.XPATH, '../../../..//font[text() = "Edit"]')
        #printEltInfo(edit_link)

    edit_link.click()

def makeNewPlan(driver, WCURL):
    """ Do whatever needs to be done to generate a new insurance plan with a
    random name. This is so you can call this function as many times as you
    want to create as many plans as you need. Returns the name of the plan
    created. """

    plan_name = uuid.uuid4().hex
    add_url = WCURL.ECHART + '&t=Admin%3ADemographics&v=demo&pat_id=18&s=inspolicy&opp=add'

    driver.navigate(add_url)
    driver.enterFormData(plan_name, id = 'insurance1')
    #driver.clickElement(xpath = '//*[@id="policy_number"]')
    driver.getWebDriver().switch_to_alert().accept()
    driver.clickElement(xpath = '//input[@type="button" and @value="Save Plan"]')
    driver.clickElement(xpath = '//input[@type="submit" and @value="Save"]')

    return plan_name

def main (driver, WCURL):
    """
    Various tests of the insurance.
    """

    d = driver

    list_url = WCURL.ECHART + '&t=Admin%3ADemographics&v=demo&pat_id=18&s=pat'

    plan_name = makeNewPlan(driver, WCURL)

    editInsurance(driver, plan_name)

    # Uncheck the 'Patient is holder' checkbox.
    driver.clickElement(xpath = '//input[@id="self_as_holder"]')
    driver.clickElement(xpath = '//input[@type="button" and @value="Change"]')

    # Focus and unfocus the 'Enter Holder' textbox.
    driver.enterFormData('', id = 'holder_pat_id_patac_input')
    driver.clickElement(xpath = '//*[@id="policy_number"]')

    # Click the 'Non-Patient Holder Details' button.
    driver.clickElement(xpath = '//input[@value="Non-Patient Holder Details"]')

    driver.clickElement(xpath = '//input[@id="holder_sex_U"]')

    # Click the 'Save' button.
    driver.clickElement(xpath = '//input[@type="submit" and @value="Save"]')

    # Edit the policy we just saved.
    editInsurance(driver, plan_name)

    # Click the 'Non-Patient Holder Details' button.
    driver.clickElement(xpath = '//input[@value="Non-Patient Holder Details"]')

    if not driver.getElement(id = 'holder_sex_U').is_selected():
        driver.reportCommandStatus('', '', False, None, 'holder gender should be "unknown"')
        return False

    driver.clickElement(xpath = '//input[@id="holder_sex_M"]')

    # Click the 'Save' button.
    driver.clickElement(xpath = '//input[@type="submit" and @value="Save"]')

    # Edit the policy we just saved.
    editInsurance(driver, plan_name)

    # Click the 'Non-Patient Holder Details' button.
    driver.clickElement(xpath = '//input[@value="Non-Patient Holder Details"]')

    if not driver.getElement(id = 'holder_sex_M').is_selected():
        driver.reportCommandStatus('', '', False, None, 'holder gender should be "male"')
        return False

    driver.clickElement(xpath = '//input[@id="holder_sex_F"]')

    # Click the 'Save' button.
    driver.clickElement(xpath = '//input[@type="submit" and @value="Save"]')

    # Edit the policy we just saved.
    editInsurance(driver, plan_name)

    # Click the 'Non-Patient Holder Details' button.
    driver.clickElement(xpath = '//input[@value="Non-Patient Holder Details"]')

    if not driver.getElement(id = 'holder_sex_F').is_selected():
        driver.reportCommandStatus('', '', False, None, 'holder gender should be "female"')
        return False

    return True
