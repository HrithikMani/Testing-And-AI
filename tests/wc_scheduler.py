# 
# Webchart System Reports UnitTest
#
def main(driver, WCURL):
    d = driver
    d.navigate(WCURL.SCHEDULER)

    # Pick a date way in the future so we don't get any warnings about being before current time
    #d.clickElement(id='submitButton')

    d.clickElement(text='13:00')

    d.enterFormData('01',name='startdateMONTH',clear=True)
    d.enterFormData('01',name='startdateDAY',clear=True)
    d.enterFormData('2037',name='startdateYEAR',clear=True)

    reason = 'I am pregnant obviously'
    comment = 'This is the appointment comment'
    d.enterAutocomplete('pat_id_patac_input','pat_id_patac_span_choices','Pregnant',0)
    d.enterFormData(value=reason,id='reason')
    d.enterFormData(value=comment,id='comment')
    d.enterAutocomplete('typeacinp','typeac_choices','Off',1,'Office Visit New')
    d.enterAutocomplete('locationacinp','locationac_choices','Off',0,'Office')
    d.clickElement(id='addclear')
    d.clickElement(name='savebtn')

    # Now make sure everything stuck
    d.clickElement(xpath="//nobr[text()='13:00 - 13:15']")
    d.verifyAttribute('value',comment,id='comment')
    d.verifyAttribute('value',reason,id='reason')
    d.verifyAttribute('value','Office',id='locationac_txt')
    d.verifyAttribute('value','OFFVISITNEW',id='type')

    # And cancel it
    d.enterFormData('PATCANCEL',id='cancel_code')
    d.clickElement(name='savebtn')
