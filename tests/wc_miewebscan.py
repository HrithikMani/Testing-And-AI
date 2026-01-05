# 
# Webchart Web Scanning/indexing UnitTest
#
def main(driver, WCURL):
    d = driver
    d.navigate(WCURL.MIEWEBSCAN)

    # 
    # Search for all status'
    #
    d.enterFormData('-1',id='status')
    d.clickElement(name='Search')

    # Click first batch
    #d.clickElement(xpath="//div[@id='lv_miews_batches_span']//font[text()='10']/parent::td/parent::tr//font[text()='Open']")

    #d.pause(2)
    #driver = d.getWebDriver()
    #driver.switch_to_window(driver.window_handles[1])
    #d.pause(2)

    #d.clickElement(name='close')
    #d.pause(02)
    #d.verifyElementPresent(True, name='popup_okbutton')
    #d.clickElement(name='popup_okbutton')

