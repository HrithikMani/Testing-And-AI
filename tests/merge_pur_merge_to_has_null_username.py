# Test: merge_pur_merge_to_has_null_username.py
# Ticket: Support #18382
# Author: alehmann
# Date: 2-18-2014
# Description: Test that when the MERGE TO patient has a NULL user name and the MERGE FROM patient does not,
#   the MERGE TO patient is given a 502 relationship and the MERGE FROM patient is given a 501

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::font='%(search_cell_text)s']/following-sibling::td/descendant::a[font='%(get_cell_text)s']"

def main( d, WCURL ):
    #$ Setup
    d.navigate( WCURL.QUICKVIEW )

    d.startSection('Set Enable PUR Routine System Setting to 1')
    # Set Enable PUR Routine System Setting to 1
    # Click the 'Control Panel' tab, then the 'System Settings' tab
    d.clickElement( xpath=SIDETAB_XPATH % { 'tabtext': 'Control Panel' } )
    d.clickChartTab( top='System Settings' )
    d.enterFormData( "Enable PUR Routine", id="select_text" )
    d.clickElement( xpath="//input[@type='submit' and @value='Go']" )
    # Click the 'Edit' link on the same row as 'Enable PUR Routine'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'Enable PUR Routine',
        'get_cell_text': 'Edit' } )
    d.enterFormData( "1", id="value" )
    d.enterFormData( "test merge_pur_merge_to_has_null_username", id="reason" )
    d.clickElement( xpath="//input[@type='submit' and @value='Change']" )
#    d.screenshot()
    d.endSection()

    d.startSection('Create patient Aaron Lehmann.')
    # Create patient Aaron Lehmann.
    # Click the 'E-Chart' tab, then the 'Patient Registration' tab
    d.clickElement( xpath=SIDETAB_XPATH % { 'tabtext': 'E-Chart' } )
    d.clickChartTab( top='Patient Registration' )

    d.startSection('Search for the patient.  It will auto-populate a new one, since it does not exist')
    # Search for the patient.  It will auto-populate a new one, since it doesn't exist
    d.enterFormData( "Lehmann", id="patient_last_name" )
    d.enterFormData( "Aaron", id="patient_first_name" )
    d.enterMIEDate( id="patient_birth_date", month=8, day=8, year=1980, time=1314 )
#    d.screenshot()
    d.clickElement( value="Search" )
#    d.screenshot()
    d.endSection()

    d.startSection('Set the MRN and address of the patient and Save')
    # Set the MRN and address of the patient and Save
    d.enterFormData( "20000", name="EDITMR_mrnumber_CCHIT" )
    d.enterFormData( "743 Oldtown Rd.", id="DPI_employer_addr1" )
    d.enterFormData( "22407", id="DPI_employer_zipcode" )
#    d.screenshot( )
    d.clickElement( value="Save" )
    d.endSection()

    d.startSection('Set up user Aaron Lehmann')
    d.startSection('Search for Lehmann, there should be one user')
    # Search for Lehmann, there should be one user
    # Click the 'Control Panel' tab, then the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "Lehmann", id="search" )
    d.clickElement( id="finduser" )
#    d.screenshot()
    d.endSection()

    d.startSection('Give User Aaron Lehmann the Department of Referring Physicians, and security role of View Only')
    # Give User Aaron Lehmann the Department of Referring Physicians, and security role of View Only
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': '22407',
        'get_cell_text': 'Edit' } )
    d.enterFormData( "Referring Physicians", id="realm" )
    d.enterFormData( "View Only", id="security_role_id" )
#    d.screenshot( )
    d.clickElement( value="Submit Edit" )
#    d.screenshot( )
    d.endSection()
    d.endSection()
    d.endSection()

    d.startSection('Create patient Aaron P. Lehmann.')
    # Create patient Aaron P. Lehmann.
    d.startSection('Search for the patient.  It will auto-populate a new one, since it doesn\'t exist')
    # Search for the patient.  It will auto-populate a new one, since it doesn't exist
    # Click the 'E-Chart' tab, then the 'Patient Registration' tab
    d.clickElement( xpath=SIDETAB_XPATH % { 'tabtext': 'E-Chart' } )
    d.clickChartTab( top='Patient Registration' )
    d.enterFormData( "Lehmann", id="patient_last_name" )
    d.enterFormData( "Aaron P.", id="patient_first_name" )
    d.enterMIEDate( id="patient_birth_date", month=8, day=8, year=1980, time=1314 )
#    d.screenshot()
    d.clickElement( value="Search" )
    d.endSection()

    d.startSection('Change the patient\'s first name from Aaron P. to Aaron, set the middle name to Patrick, set the address, and set the MRN#')
    # Change the patient's first name from Aaron P. to Aaron, set the middle name to Patrick, set the address, and set the MRN#
    d.enterFormData( "Aaron", id="DPI_first_name", clear=True )
    d.enterFormData( "Patrick", id="DPI_middle_name" )
    d.enterFormData( "20001", name="EDITMR_mrnumber_CCHIT" )
    d.enterFormData( "46804", id="DPI_employer_zipcode" )
    d.enterFormData( "398 Newcity Place", id="DPI_employer_addr1" )
    d.enterFormData( "Apt 109", id="DPI_employer_addr2" )
#    d.screenshot( )
    d.clickElement( value="Save" )
    d.endSection()

    d.startSection('Search for Lehmann on the Access Control screen, we should find two users with null username')
    # Search for Lehmann on the Access Control screen, we should find two users with null username
    # Click the 'Control Panel' tab, then the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "Lehmann", id="search" )
    d.clickElement( id="finduser" )
#    d.screenshot()
    d.endSection()

    d.startSection('Set up user Aaron Patrick Lehmann')
    d.startSection('Give User Aaron Patrick Lehmann the Department of Referring Physicians, security role of View Only, username/password of aaron/aaron, and enable login')
    # Give User Aaron Patrick Lehmann the Department of Referring Physicians, security role of View Only, username/password of aaron/aaron, and enable login
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': '46804',
        'get_cell_text': 'Edit' } )
    d.enterFormData( "Referring Physicians", id="realm" )
    d.enterFormData( "View Only", id="security_role_id" )
    d.enterFormData( "aaron", id="username" )
    d.enterFormData( "selenium", id="oldpassword" )
    d.enterFormData( "aaron", id="password" )
    d.enterFormData( "aaron", id="vpassword" )
    d.enterFormData( "Active", id="status" )
#    d.screenshot( )
    d.clickElement( value="Submit Edit" )
#    d.screenshot( )
    d.endSection()
    d.endSection( )
    d.endSection( )

    #$ Main Test
    d.startSection('Merge Aaron Patrick Lehmann to Aaron Lehmann.')
    # Merge Aaron Patrick Lehmann to Aaron Lehmann.
    # Click on 'E-Chart' Tab
    d.clickElement( xpath=SIDETAB_XPATH % { 'tabtext': 'E-Chart' } )

    d.startSection('Search for Lehmann in E-Chart, we should find two patients')
    # Search for Lehmann in E-Chart, we should find two patients
    d.enterFormData( "Lehmann", name="sstring" )
    d.clickElement( value="Search" )
#    d.screenshot( )
    d.endSection()

    d.startSection('Go to Admin:Demographics for user with MRN# TEST-20000 (Aaron Lehmann)')
    # Go to Admin:Demographics for user with MRN# TEST-20000 (Aaron Lehmann)
    d.clickElement( xpath="//a[font='TEST-20000']" )
#    d.screenshot()
    d.clickChartTab( top='Admin' )
    d.clickElement( id="Demographics_tab" )
#    d.screenshot( )
    d.endSection()

    d.startSection('Click the link for TEST-20001 (Aaron Patrick Lehmann) to bring up the Merge Preview screen')
    # Click the link for TEST-20001 (Aaron Patrick Lehmann) to bring up the Merge Preview screen
    d.clickElement( xpath="//td[descendant::font='TEST-20001']/following-sibling::td/descendant::input[@type='checkbox']" )
    d.clickElement( value="Preview Merge" )
#    d.screenshot( )
    d.endSection()

    d.startSection('Merge the patients')
    # Merge the patients
    d.clickElement( xpath="//input[contains(following-sibling::text(), 'keep all MR Numbers.')]" )
    d.clickElement( value="Merge Using Selected Options" )
#    d.screenshot( )
    d.endSection()
    d.endSection()

    d.startSection('Verify that the merge happened correctly')
    d.startSection('Go to E-Chart screen and searching for the name Lehmann.  It should go straight to Aaron Patrick Lehmann')
    # Go to E-Chart screen and searching for the name Lehmann.  It should go straight to Aaron Patrick Lehmann
    # Click the 'E-Chart' tab, then the 'Patient Registration' tab
    d.clickElement( xpath=SIDETAB_XPATH % { 'tabtext': 'E-Chart' } )
    d.enterFormData( "Lehmann", name="sstring" )
    d.clickElement( value="Search" )
#    d.screenshot( )
    d.clickChartTab( top='Admin' )
    d.clickElement( id="Demographics_tab" )
#    d.screenshot( )
    d.endSection()

    d.startSection('Go to the Access Control page and search for Lehmann.  There should be two users.')
    # Go to the Access Control page and search for Lehmann.  There should be two users.
    # Click the 'Control Panel' tab, then the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "Lehmann", name="search" )
    d.clickElement( value="Go!" )
#    d.screenshot( )
    d.endSection()

    d.startSection('Aaron Lehmann should have a null username and have his Login Disabled. His address should not have changed.')
    # Aaron Lehmann should have a null username and have his Login Disabled. His address should not have changed
    # Click the 'Control Panel' tab, then the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "Lehmann", name="search" )
    d.clickElement( value="Go!" )
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': '(*)',
        'get_cell_text': 'Edit' } )
#    d.screenshot( )
    d.endSection()

    d.startSection('User Aaron Lehmann should be linked to patient Aaron Patrick Lehmann.  The role should be Self-Duplicate.')
    # User Aaron Lehmann should be linked to patient Aaron Patrick Lehmann.  The role should be Self-Duplicate.
    d.clickElement( xpath="//a[font='Edit Patients Linked to User']" )
#    d.screenshot( )
    d.endSection( )

    d.startSection('Aaron Patrick Lehmann should have username of aaron and be Active.')
    # Aaron Patrick Lehmann should have username of aaron and be Active.
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "Lehmann", name="search" )
    d.clickElement( value="Go!" )
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'aaron',
        'get_cell_text': 'Edit' } )
#    d.screenshot( )
    d.endSection( )

    d.startSection('User Aaron Patrick Lehmann should be linked to patient Aaron Patrick Lehmann.  The role should be Self.')
    # User Aaron Lehmann should be linked to patient Aaron Patrick Lehmann.  The role should be Self-Duplicate.
    d.clickElement( xpath="//a[font='Edit Patients Linked to User']" )
#    d.screenshot( )
    d.endSection( )

    d.endSection( )

