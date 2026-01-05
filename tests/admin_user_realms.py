def main (d, WCURL):

    d.navigate(WCURL.ACCESS_CONTROL)


    d.clickElement(id='toggle_user_counts_link');

    d.screenshot('realms with user counts')


    d.enterFormData('Butler', id='search')
    d.enterFormData('name', id='by')
    d.clickElement(id='finduser')

    d.screenshot('Find User Internist E. Butler')
