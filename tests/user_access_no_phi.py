#! /usr/bin/env python
# MIE test that when a user with no access restrictions but with revoked PHI attempts to access an unrestricted patient, access is denied.
# Written by Aaron Lehmann
# Date: 01-30-2014

"""
user_access_no_phi -- User with no access restrictions but with revoked PHI attempts to access an unrestricted patient, access is denied.
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::a='%(search_cell_text)s']/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"

def main (d, WCURL):
    #$ Setup
    d.navigate(WCURL.QUICKVIEW)

    # Click the 'Control Panel' tab, then the 'Access Conrol' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "selenium", id="search" )
    d.clickElement( id="finduser" )
    # Click the 'Edit' link on the same row as 'selenium'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'selenium',
        'get_cell_text': 'Edit' } )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    locator = "//legend[descendant::text()='Editing individual security for user (' and descendant::b='selenium']"
    el = d.getElement( xpath=locator )
    d.reportCommandStatus( "d.getElement", locator, bool( el ), "", "Was able to reach the page for customizing the selenium user's security" )
    if bool( el ):
        d.enterFormData( "Yes", name="WebChart_Revoke PHI Access" )
        d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
        d.enterFormData( "Updating for user_access_no_phi test", id="sec_role_comment" )
        d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )
        d.clickElement( xpath="//a[font='Edit User']" )
        d.clickElement( xpath="//a[font='Customize User Security']" )
#        d.screenshot( )
        locator = "//td[font='Revoke PHI Access:']/following-sibling::td[1]/descendant::select/option[@selected and .='Yes']"
        el = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", locator, bool( el ), "", "PHI is revoked for user selenium" )
        if bool( el ):
            #$ Main Test
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext':'E-Chart'} )
#            d.screenshot( )
            locator = "//td[font='Revoke PHI Access:']/following-sibling::td[1]/descendant::select/option[@selected and .='Yes']"
            el = d.getElement( xpath="//div[contains(text(), 'You Currently Do Not Have Access' )]" ) 
            d.reportCommandStatus( "d.getElement", locator, bool( el ), "", "User selenium cannot access E-Chart" )
