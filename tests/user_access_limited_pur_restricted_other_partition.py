#! /usr/bin/env python
# MIE test that when a user with limited access and restricted partition attempts to access a patient he has a relationship
#     with that is in a partition he does not have access to.  Access is granted.
# Written by Aaron Lehmann
# Date: 01-30-2014 = initial creation
# Date: 01-31-2014 = update to include partition restrictions

"""
user_access_limited_pur_restricted_other_partition.py -- User with limited access and restricted partition attempts to access a patient he has a relationship
    with that is in a partition he does not have access to.  Access is granted.
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::font='%(search_cell_text)s']/following-sibling::td/descendant::a[font='%(get_cell_text)s']"

def main (d, WCURL):
    #$ Setup
    d.navigate(WCURL.QUICKVIEW)

    # Click on 'Control Panel' tab, then on 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "selenium", id="search" )
    d.clickElement( id="finduser" )
    # Click on the 'Edit' link that is on the same row as 'selenium'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'selenium',
        'get_cell_text': 'Edit' } )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
    d.enterFormData( "Updating for user_access_limited_pur_restricted_other_partition test", id="sec_role_comment" )
    d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )

    # Click on 'Control Panel' tab, then on 'Partition Mgr' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Partition Mgr' )
    # Click on the 'Edit' link that is on the same row as 'MIE'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'MIE',
        'get_cell_text': 'Edit' } )
    d.clickElement( id="part_restrict" )
#    d.screenshot( )
    d.clickElement( xpath="//input[@value='Change' and @type='button']" )
#    d.screenshot( )

    # Click on the 'Edit' link that is on the same row as 'CCHIT'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'CCHIT',
        'get_cell_text': 'Edit' } )
    d.clickElement( id="part_restrict" )
    d.enterFormData( "selenium", id="le_pm_allowed_users_allowed_id_display" )
    d.clickElement( id="le_pm_allowed_users_button" )
#    d.screenshot( )
    d.clickElement( xpath="//input[@value='Change' and @type='button']" )
#    d.screenshot( )

    # Click on 'Control Panel' tab, then on 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "selenium", id="search" )
    d.clickElement( id="finduser" )
    # Click on the 'Edit' link that is on the same row as 'selenium'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'selenium',
        'get_cell_text': 'Edit' } )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    d.enterFormData( "Yes", name="E-Chart_Limited Access" )
    d.enterFormData( "Yes", name="E-Chart_Restrict Access by Partition" )
    d.enterFormData( "Updating for user_access_limited_pur_restricted_other_partition", id="sec_role_comment" )
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
#    d.screenshot( )

    #$ Main Test
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
    d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
    d.enterFormData( "MIE-10019", name="sstring" )
    d.clickElement( name="pat_search" )
#    d.screenshot( )
