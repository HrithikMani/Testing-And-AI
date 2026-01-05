#! /usr/bin/env python
# MIE test that when a user with limited access attempts to access a patient he has no relationship with, access is denied.
# Written by Aaron Lehmann
# Date: 01-31-2014

"""
user_access_limited_no_pur.py -- User with limited access attempts to access a patient he has no relationship with.  Access is denied.$
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::a='%(search_cell_text)s']/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"
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
    d.clickElement( xpath="//a[font='Customize User Security']" )
    d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
    d.enterFormData( "Yes", name="E-Chart_Limited Access" )
    d.enterFormData( "Updating for user_access_limited_pur", id="sec_role_comment" )
    d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )
    d.clickElement( xpath="//a[font='Edit User']" )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    locator = "//td[font='Limited Access:']/following-sibling::td[1]/descendant::select/option[@selected]"
    text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, text == "Yes", text, "selenium user has limitted access" )
#    d.screenshot( )
    if text == "Yes":
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
        d.clickElement( xpath="//td[descendant::a='Hart, William S.']/following-sibling::td/descendant::input[@type='button']" )
        d.clickElement( xpath="//input[@type='submit' and @value='Submit']" )
        locator = "//a[text()='Hart, William S.']"
        el = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", locator, not bool( el ), "", "There is no relationship between user selenium and William S. Hart" )
#        d.screenshot( )
        if not bool( el ):
            #$ Main Test
            # Click 'E-Chart' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
            d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
            d.enterFormData( "MIE-10019", name="sstring" )
            d.clickElement( name="pat_search" )
            locator = "//a[text()='Hart, William S.']"
            d.reportCommandStatus( "d.getElement", locator, not bool( d.getElement( xpath=locator ) ), "", "selenium user is unable to find William S. Hart" )
#            d.screenshot( )
