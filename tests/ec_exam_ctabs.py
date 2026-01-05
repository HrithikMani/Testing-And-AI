# 
# Webchart Login UnitTest
#
def main (driver, WCURL):
    d = driver

    d.navigate(WCURL.CHART_GROWING_JOSEPH + "v=encounter&encopp=exam&enc_lay_id=Pediatric+Exam&encounter_id=26&set_curr_enc=26")

    # This little block of code will make sure that if for some reason the Back to Exam
    # tab isn't toggled the right way to start with, we will toggle it manually
    # The functions we're using here do not log any results, so it won't change the results file
    try:
        ele = d.getElement(text='Back to Exam')
        if not ele:
            d.getElement(text='Back to Chart').click()
    except:
        pass

    # make sure the 'Back to Exam' link exists
    d.verifyElementPresent(text='Back to Exam')

    # verify that chart tabs are present
    d.verifyAttribute('href','*t=Patient+Summary&v=dashboard*',text='Patient Summary')
    d.verifyAttribute('href','*v=parent&t=Current*',text='Current')
    # and that they have been redirected to new windows
    d.verifyAttribute('target','_blank',text='Patient Summary')
    d.verifyAttribute('target','_blank',text='Current')

    # switch to exam tabs
    d.clickElement(text='Back to Exam')

    # make sure the 'Back to Chart' link exists
    d.verifyElementPresent(text='Back to Chart')
    # Check some of the exam links
    d.verifyAttribute('href','*#extan*',text='Reason for Visit')
    d.verifyAttribute('href','*#extan*',text='Physical Exam')
    d.verifyAttribute('href','*#extan*',text='Plan')
    d.verifyAttribute('href','*#extan*',text='CC')

    # Now toggle back so that Back to Exam is showing
    d.clickElement(text='Back to Chart')
    d.verifyElementPresent(text='Back to Exam')
