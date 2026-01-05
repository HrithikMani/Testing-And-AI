#! /usr/bin/env python
# MIE test that when a user in a realm with limited access attempts to access a patient he has no relationship with, access is denied.
# Written by Aaron Lehmann
# Date: 02-10-2014

"""
user_access_realm_limited_no_pur.py -- User in a realm with limited access attempts to access a patient he has no relationship with, access is denied.
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::font='%(search_cell_text)s']/following-sibling::td/descendant::a[font='%(get_cell_text)s']"

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
    d.enterFormData( "Updating for user_access_realm_limited_no_pur", id="sec_role_comment" )
#    d.screenshot( )
    d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )

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
#    d.screenshot( )

    # Click the 'Control Panel' tab then click the 'Security Roles' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    # Click the 'Edit' link that is in the same row as 'Physicians'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'Physicians',
        'get_cell_text': 'Edit' } )
    d.enterFormData( "Yes", name="E-Chart_Limited Access" )
    d.enterFormData( "Updating for user_access_realm_limited_no_pur", id="sec_role_comment" )
#    d.screenshot( )
    d.clickElement( xpath="//input[@type='SUBMIT' and @value='Update Role']" )

    # Click the 'Control Panel' tab then click the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "selenium", id="search" )
    d.clickElement( id="finduser" )
    # Click the 'Edit' link that is in the same row as 'selenium'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'selenium',
        'get_cell_text': 'Edit' } )
    for el in d.getElements( xpath="//input[@checked and @name!='Physicians']" ):
        # Click all checked checkboxes that aren't named Physician
        el.click()
#    d.screenshot()
    d.clickElement( xpath='//input[@type="button" and @value="Submit Edit"]' )

    #$ Main Test
    # Click the tab for 'E-Chart'
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
    d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]='Name']" )
    d.enterFormData( "Hart, William", name="sstring" )
    d.clickElement( name="pat_search" )
#    d.screenshot( )
