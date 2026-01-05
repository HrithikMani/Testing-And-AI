
def main (d, WCURL):
    """
    Verifies that the chart tab editor is working properly.
    Adds a new chart tab named 'selenium test tab'
    """
    d.navigate(WCURL.CHARTTABS)

    # This line should not be here, but this page is overly complex and is killing the JS engine
    # This should prevent us from getting intermittent test failures, but this page (not the test) needs to be optimized
    d.setTimeout(10)

    # verify that changing from a docbearing view with doctypes to a view that
    # does not permit documents produces a confirmation box
    #The raison d'atre for this portion of the test is 
    # 1. broken in Chrome
    # 2. not implemented yet in our selenium API
    #
#   d.clickElement(text='Email Log')
#   d.clickElement(value='Edit')
#   d.setNeverConfirm(True)
#
#   # broken in Chrome
#   d.enterFormData(value='apts', id='default_view')
#   #
#   ##   confirmation box not an alert -- need to fix this
#   ##   need method
#   ##   d.verifyAlert('This tab currently posseses * document types.*')
#   d.clickElement(id='cancel_btn')

    d.clickElement(text='Add Chart Tab')

    d.pause(2)

#   d.setNeverConfirm(True)
    d.clickElement(value='Save')
#    d.verifyAlert('Missing required field(s):*Tab Name')
    d.verifyElementPresent(xpath='//div[@class="wc_win"]//div[contains(@class, "wc_win_body")]/div[contains(text(), "Missing required field")]', present=True)
    d.clickElement(xpath='//div[@class="wc_win"]//input[@type="button" and contains(@value,"OK")]')

    d.enterFormData('selenium test tab', id='tabname')

    d.enterFormData(True, id='restricted')
    d.verifyAttribute(attr='disabled', val='true',id='edit_mode_0')

    d.enterFormData(False, id='restricted')

    #
    #A lot more will be added to this section
    #

    d.clickElement(value='Save')

    d.resetTimeout()
