def main(d, WCURL):
    """
    Ensures that the dication control is working properly.
    Enters data into the fields and makes sure that the 
    control buttons are present, but does NOT actually
    add a dictation.
    """
    d.navigate(WCURL.DICTATION)

    d.clickElement(text='Add Dictation')
    d.switchToPopup()

    d.enterAutocomplete('pat_id_patac','Har',0)
    d.enterFormData('03031981',id='pat_dob')
    d.enterFormData('Office',id='location_code')
    d.enterFormData('3',id='priority')
    d.enterFormData('No Job Type',id='job_type')

    d.verifyElementPresent(id='rewind_end')
    d.verifyElementPresent(id='rewind')
    d.verifyElementPresent(id='play')
    d.verifyElementPresent(id='record')
    d.verifyElementPresent(id='stop')
    d.verifyElementPresent(id='fastforward')
    d.verifyElementPresent(id='fastforward_end')
    d.verifyElementPresent(id='dict_save')

    d.closePopup()
