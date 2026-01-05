#! /usr/bin/env python
# MIE test that when a user with limited access attempts to access a patient he has a relationship with, access is granted.
# Written by Aaron Lehmann
# Date: 01-30-2014

"""
user_access_limited_pur.py -- User with limited access attempts to access a patient he has a relationship with.  Access is granted.$
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
        locator = "//a[text()='Hart, William S.']"
        el = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( el ), "", "There is a relationship between user selenium and William S. Hart" )
#        d.screenshot( )
        if bool( el ):
            #$ Main Test
            # Click 'E-Chart' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
            d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
            d.enterFormData( "MIE-10019", name="sstring" )
            d.clickElement( name="pat_search" )
            locator = "//a[text()='Hart, William S.']"
            d.reportCommandStatus( "d.getElement", locator, bool( d.getElement( xpath=locator ) ), "", "selenium user is able to access William S. Hart" )
#            d.screenshot( )
