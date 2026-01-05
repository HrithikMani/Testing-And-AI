from selenium.webdriver.common.keys import Keys

def main (driver, WCURL):
    """
    Add a medication for the patient.
    """

    d = driver

    driver.navigate(WCURL.CHART_HART_WILLIAM + WCURL.MEDS_QUICK_PRESCRIBE)

    textbox = driver.getElement(id = 'qp_sig0')
    textbox.clear()

    textbox.send_keys('asdf')
    value = textbox.get_attribute('value')
    if value != 'asdf':
        driver.reportCommandStatus('', '', False, value, 'simple insertion failed')
        return False

    textbox.send_keys(Keys.HOME + 'x')
    value = textbox.get_attribute('value')
    if value != 'xasdf':
        driver.reportCommandStatus('', '', False, value, 'home insertion failed')
        return False

    textbox.send_keys(Keys.HOME + Keys.RIGHT + Keys.RIGHT + 'y')
    value = textbox.get_attribute('value')
    if value != 'xaysdf':
        driver.reportCommandStatus('', '', False, value, 'middle insertion failed')
        return False

    return True
