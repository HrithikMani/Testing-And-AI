#! /usr/bin/env python
# MIE test that when a user with access restriction to partition but with access to the an unrestricted patient's partition, access is allowed.
# Written by Aaron Lehmann
# Date: 01-30-2014

"""
user_access_user_has_access_to_patient_partition -- User with access restriction to partition but with access to the an unrestricted patient's partition,
    access is allowed.
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[text()='%(search_cell_text)s' or descendant::*[text()='%(search_cell_text)s']]/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"
TABLE_ROWCOL_XPATH ="//tr[td='%(rowtext)s']/td[count(//th[descendant::text()='%(columntext)s']/preceding-sibling::th) + 1]"

def main (d, WCURL):
    #$ Setup
    d.navigate(WCURL.QUICKVIEW)

    # Click the 'Control Panel' tab then click the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "selenium", id="search" )
    d.clickElement( id="finduser" )
    # Click the 'Edit' link that is in the same row as 'selenium'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'selenium',
        'get_cell_text': 'Edit' } )
    d.clickElement( xpath="//a[font='Edit Patients Linked to User']" )
    # Click the button that is on the same row as a link that says 'Hart, William S.'
    d.clickElement( xpath="//td[descendant::a='Hart, William S.']/following-sibling::td/descendant::input[@type='button']" )
    d.clickElement( xpath="//input[@type='submit' and @value='Submit']" )
    locator = "//a[text()='Hart, William S.']"
    el = d.getElement( xpath=locator )
    d.reportCommandStatus( "d.getElement", locator, not bool( el ), "", "There is no relationship between user selenium and William S. Hart" )
#    d.screenshot( )
    if not bool( el ):
        # Click 'Control Panel' tab, then the 'Partition Mgr' tab
        d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
        d.clickChartTab( top='Partition Mgr' )
        # Click on the 'Edit' cell on the same row as 'MIE'
        d.clickElement( xpath=OPTIONCELL_XPATH % {
            'search_cell_text': 'MIE',
            'get_cell_text': 'Edit' } )
        d.clickElement( id="part_restrict" )
        d.waitFor(d, lambda d: d.getElement( id="le_pm_allowed_users_allowed_id_display" ))
        d.enterAutocomplete( "userac_pm_allowed_users", "selenium" )
        d.clickElement( id="le_pm_allowed_users_button" )
#        d.screenshot( )

        d.clickElement( xpath="//input[@value='Change' and @type='button']" )
        locator = (TABLE_ROWCOL_XPATH )% { 'rowtext': 'MIE', 'columntext': 'Restricted' }
        text = d.getAttribute( 'text', xpath=locator )
        d.reportCommandStatus( "d.getAttribute", locator, text == "Yes", text, "The MIE partition is restricted" )
#        d.screenshot( )
        if text == "Yes":
            # Click 'Control Panel' tab, then the 'Access Controle' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
            d.clickChartTab( top='Access Control' )
            d.enterFormData( "selenium", id="search" )
            d.clickElement( id="finduser" )
            # Click on the 'Edit' cell on the same row as 'selenium'
            d.clickElement( xpath=OPTIONCELL_XPATH % {
                'search_cell_text': 'selenium',
                'get_cell_text': 'Edit' } )
            d.clickElement( xpath="//a[font='Customize User Security']" )
            d.enterFormData( "Yes", name="E-Chart_Restrict Access by Partition" )
            d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
            d.enterFormData( "Updating for user_access_user_has_access_to_patient_partition", id="sec_role_comment" )
            d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )
            d.clickElement( xpath="//a[font='Edit User']" )
            d.clickElement( xpath="//a[font='Customize User Security']" )
            locator = "//td[font='Restrict Access by Partition:']/following-sibling::td[1]/descendant::select/option[@selected]"
            text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getAttribute", locator, text == "Yes", text, "selenium user is restricted by partition" )
#            d.screenshot( )
            if text == "Yes":
                #$ Main Test
                # Click 'E-Chart' tab
                d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                d.enterFormData( "MIE-10019", name="sstring" )
                d.clickElement( name="pat_search" )
                locator = "//a[text()='Hart, William S.']"
                d.reportCommandStatus( "d.getElement", locator, bool( d.getElement( xpath=locator ) ), "", "selenium user is able to access William S. Hart" )
#                d.screenshot( )
