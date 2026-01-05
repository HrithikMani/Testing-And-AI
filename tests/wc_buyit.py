# 
# WebChart BuyIt Checkout Process Test
# This page is heavy on interaction and animations with lots of static data
# and prices. Let's just let screenshots take care of this whole test
#
def main (d, WCURL):
    d.navigate(WCURL.OMNISCOPE)
    d.clickElement(id='buyitlink')

    d.pause(1)
    d.clickElement(xpath="(//div[@class='checkme'])[1]/span")
    d.clickElement(xpath="(//div[@class='checkme'])[2]/span")
    d.clickElement(xpath="(//div[@class='checkme'])[3]/span")
    d.pause(1)

    d.clickElement(xpath="//input[@id='yes']/preceding-sibling::span")
    d.pause(2)

    d.clickElement(id='continue')
    d.pause(1)

    d.enterFormData('1234 Selenium Way',id='payeraddress1')
    d.enterFormData('Fort Wayne',id='payercity')
    d.enterFormData('IN',id='payerstate')
    d.enterFormData('46804',id='payerzip')
    d.enterFormData('Visa',id='creditcardtype')
    d.enterFormData('1111222233334444',id='creditcardacct')
    d.enterFormData('1',id='cc_expmo')
    d.enterFormData('2016',id='cc_expyr')
    d.enterFormData('111',id='creditcardcvv2')
    d.clickElement(id='roSubmit')
