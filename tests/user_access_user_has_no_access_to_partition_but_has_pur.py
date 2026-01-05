#! /usr/bin/env python
# MIE Test that a user with partition restriction and no access to an unrestricted patient's partition but has PUR is granted access
# Written by Aaron Lehmann
# Date: 02-05-2014

"""
user_access_user_has_no_access_to_partition_but_has_pur -- Test that if a user has pur, is partition restricted,
    and does not have access to the patient's partition, access is granted
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[text()='%(search_cell_text)s' or descendant::*[text()='%(search_cell_text)s']]/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"
TABLE_ROWCOL_XPATH ="//tr[td='%(rowtext)s']/td[count(//th[descendant::text()='%(columntext)s']/preceding-sibling::th) + 1]"

def main (d, WCURL):
    d.navigate(WCURL.QUICKVIEW)

    #$ Setup
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
    d.enterFormData( "Yes", name="E-Chart_Restrict Access by Partition" )
    d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
    d.enterFormData( "Updating for user_access_user_has_no_access_to_partition_but_has_pur", id="sec_role_comment" )
    d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )
    d.clickElement( xpath="//a[font='Edit User']" )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    locator = "//td[font='Allow Unrestricted Pat Search:']/following-sibling::td[1]/descendant::select/option[@selected]"
    unrestricted_text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, unrestricted_text == "No", unrestricted_text, "selenium user cannot use unrestricted patient search" )
    locator = "//td[font='Restrict Access by Partition:']/following-sibling::td[1]/descendant::select/option[@selected]"
    partition_restriction_text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, partition_restriction_text == "Yes", partition_restriction_text, "selenium user is restricted by partition" )
#    d.screenshot( )
    if unrestricted_text == "No" and partition_restriction_text == "Yes":
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
        d.clickElement( xpath="//input[@value='Submit']" )
        locator = "//a[text()='Hart, William S.']"
        el = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", locator, bool( el ), "", "There is a relationship between user selenium and William S. Hart" )
#        d.screenshot( )
        if bool( el ):
            # Click 'Control Panel' tab, then the 'Partition Mgr' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
            d.clickChartTab( top='Partition Mgr' )
            # Click on the 'Edit' cell on the same row as 'MIE'
            d.clickElement( xpath=OPTIONCELL_XPATH % {
                'search_cell_text': 'MIE',
                'get_cell_text': 'Edit' } )
            d.clickElement( id="part_restrict" )
            d.clickElement( xpath="//input[@value='Change' and @type='button']" )
            locator = (TABLE_ROWCOL_XPATH)% { 'rowtext': 'MIE', 'columntext': 'Restricted' }
            text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getAttribute", locator, text == "Yes", text, "The MIE partition is restricted" )
#            d.screenshot( )
            if text == "Yes":
                d.clickElement( xpath=OPTIONCELL_XPATH % {
                    'search_cell_text': 'MIE',
                    'get_cell_text': 'Edit' } )
                locator = "//legend/descendant::span[text()='Allowed Users']/following-sibling::table/descendant::td[contains( font, 'Selenium, Selenium' )]"
                el = d.getElement( xpath=locator )
                d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, not bool( el ), "", "User selenium does not have access to the MIE partition" )
#                d.screenshot( )
                if not bool( el ):
                    #$ Main Test
                    # Click 'E-Chart' tab
                    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                    d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                    d.enterFormData( "MIE-10019", name="sstring" )
                    d.clickElement( name="pat_search" )
                    locator = "//a[text()='Hart, William S.']"
                    el = d.getElement( xpath=locator )
                    d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, bool( el ), "", "Could find and access William S. Hart because user selenium has a relationship with William S. Hart" )
#                    d.screenshot()
