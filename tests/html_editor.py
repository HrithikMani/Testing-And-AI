from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(d, URLS):
    d.navigate('?t=Patient+Summary&v=dashboard&f=chart&s=doc&opp=add&pat_id=18&method=html&doc_type=ADVDIRECT&no_tabs')
    d.startSection('Type into document area')

    wd = d.getWebDriver()
    try:
        wd.switch_to.frame('echtmledit_Editor')
    except Exception as ex:
        d.reportCommandStatus('Unable to switch to editor IFRAME', '', False, '', '')
        return
    try:
        body = wd.find_element_by_tag_name('body')
    except AttributeError:
        from selenium.webdriver.common.by import By
        body = wd.find_element(By.TAG_NAME, 'body')
    if body:
         body.send_keys('My final retort: cremation in ')
    else:
        wd.switch_to.parent_frame()
        d.reportCommandStatus('Could not find body element inside IFRAME', '', False, '', '')
        return
    d.endSection()

    d.startSection('Use a variable from the dropdown')
    wd.switch_to.parent_frame()
    d.sleep(3)
    wd.execute_script("document.body.style.overflow = 'hidden';")
    variable_element = WebDriverWait(wd, 30).until(
        EC.element_to_be_clickable((By.ID, 'echtmleditvariable'))
    )
    d.runJS("arguments[0].click();", variable_element)
    WebDriverWait(wd, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'echtmleditMenu_pop_Document')]"))
    )
    try:
        dictator_element = WebDriverWait(wd, 30).until(
            EC.presence_of_element_located((By.XPATH, "//nobr[text()='Dictator']"))
        )
        d.runJS("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", dictator_element)
        contact_element = WebDriverWait(wd, 30).until(
            EC.presence_of_element_located((By.XPATH, "//nobr[text()='Contact']"))
        )
        d.runJS("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));", contact_element)
        city_element = WebDriverWait(wd, 30).until(
            EC.presence_of_element_located((By.XPATH, "//u[text()='City']"))
        )
        d.runJS("arguments[0].click();", city_element)
        EC.presence_of_element_located((By.XPATH, '//html/body/span[@id="echtmledit.dictator.city" and contains(text(), "Fort Wayne")]'))
    finally:
        d.runJS("document.body.style.overflow = '';")
    d.pause(1)
    d.clickElement(name="submit_document")
    d.endSection()
