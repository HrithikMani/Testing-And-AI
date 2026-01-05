#! /usr/bin/env python
# MIE Test that a user with a patient-user relationship cannot access a restricted patient if he is not exempt
# Written by Aaron Lehmann
# Date: 02-04-2014 = initial creation

"""
user_access_restriction_pur.py -- Test that a user with a patient-user relationship cannot access a restricted patient if he is not exempt
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::a='%(search_cell_text)s']/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"

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
    d.clickElement( xpath="//a[font='Customize User Security']" )
    d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
    d.enterFormData( "Updating for user_access_restriction_pur", id="sec_role_comment" )
    d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )
    d.clickElement( xpath="//a[font='Edit User']" )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    locator = "//td[font='Allow Unrestricted Pat Search:']/following-sibling::td[1]/descendant::select/option[@selected]"
    text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, text == "No", text, "selenium user cannot use unrestricted patient search" )
#    d.screenshot( )
    if text == "No":
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
        locator = "//a[text()='Hart, William S.']"
        el = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", locator, bool( el ), "", "There is a relationship between user selenium and William S. Hart" )
#        d.screenshot( )
        if bool( el ):
            # Click on the 'Control Panel' tab on the side, then the 'Patient Restrictions' tab on top
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
            d.clickChartTab( top='Patient Restrictions' )
            d.clickElement( xpath="//a[font='Add New Lock']" )
            d.enterAutocomplete( "pat_id_patac", "Hart, William" )
            d.enterAutocomplete( "user_id_ac", "dave" )
            d.enterFormData( "test user_access_restriction_exemption", id="le_patrestrict_reason_value" )
            d.clickElement( id="le_patrestrict_button" )
            locator = "//td[contains(font, 'Selenium, Selenium')]"
            el = d.getElement( xpath=locator )
            d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, not bool( el ), "", "William S. Hart is restricted, and user selenium is not exempt" )
#            d.screenshot( )
            d.clickElement( value="Submit" )
            if not bool( el ):
                #$ Main Test
                # Click on the 'E-Chart' tab
                d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                d.enterFormData( "MIE-10019", name="sstring" )
                d.clickElement( name="pat_search" )
                locator = "//span[@style='background-color:#FFD52D;' and font='Locked']"
                el = d.getElement( xpath=locator )
                d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( el ), "", "William S. Hart is locked" )
#                d.screenshot( )
                if bool( el ):
                    d.clickElement( xpath="//a[text()='MIE-10019']" )
                    locator = """//div[contains( text(), "The patient's chart is restricted" )]"""
                    d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( d.getElement( xpath=locator ) ), "", "User selenium cannot access William S. Hart because he is locked" )
#                    d.screenshot( )
