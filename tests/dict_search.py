def main(d, WCURL):
    """
    Verifies that the dictation search function is working.
    Fills out all of the dictation search fields and makes sure
    that a listview appears after searching.
    """
    d.navigate(WCURL.DICTATION)

    d.clickElement(text='Search')
    d.clickElement(value='Search')

    # A listview should show up
    d.verifyElementPresent(id='lv_di_mypending_span')

    # Now fill out the search form
    d.enterFormData('123',id='dic_id')
    d.enterAutocomplete('search_pat_id_patac','Har',0)
    d.enterFormData('Selenium',id='comment')
    d.enterAutocomplete('search_username_ac', 'Selen', 0);
    d.enterFormData('No Job Type',id='job_type')
    d.enterFormData('>5m',id='durationInput')
    d.clickElement(id='uploaddateNOW')
    d.clickElement(id='uploaddate_endNOW')
    d.enterFormData('1',id='priority')
    d.enterMIEDate('dob',12,25,2012)
    d.enterFormData('Selenium',id='transcriber')
    d.enterFormData('Office',id='location_code')
    d.enterFormData('All',id='status')
    d.enterFormData('1',id='encounter_id')
    d.clickElement(id='transdateNOW')
    d.clickElement(id='transdate_endNOW')

    d.clickElement(value='Search')

    d.verifyElementPresent(id='lv_di_mypending_span')
