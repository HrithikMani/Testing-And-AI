# 
# Webchart System Reports UnitTest
#
def main(driver, WCURL):
    d = driver
    d.navigate(WCURL.ESIGN)

    # 
    # Go to multi review page
    #
    d.clickElement(text='Multi-Review')

    d.verifyElementPresent(value='Mark All as Signed')
    d.verifyElementPresent(value='Sign Marked Documents')

