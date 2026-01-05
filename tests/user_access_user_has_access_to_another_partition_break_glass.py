#! /usr/bin/env python
# MIE Test that a user with partition restriction and access to another partition from the patient can break the glass to access the patient
# Written by Aaron Lehmann
# Date: 02-28-2014

"""
user_access_user_has_access_to_another_partition_break_glass -- Test that a user with partition restriction and access to another partition from the patient can break the glass to access the patient
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
    d.enterFormData( "Yes", name="E-Chart_Emergency Access" )
    d.enterFormData( "No", name="E-Chart_Allow Unrestricted Pat Search" )
    d.enterFormData( "Updating for user_access_user_has_no_access_to_partition", id="sec_role_comment" )
    d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )
    d.clickElement( xpath="//a[font='Edit User']" )
    d.clickElement( xpath="//a[font='Customize User Security']" )
    locator = "//td[font='Allow Unrestricted Pat Search:']/following-sibling::td[1]/descendant::select/option[@selected]"
    unrestricted_text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, unrestricted_text == "No", unrestricted_text, "selenium user cannot use unrestricted patient search" )
    locator = "//td[font='Restrict Access by Partition:']/following-sibling::td[1]/descendant::select/option[@selected]"
    partition_restriction_text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, partition_restriction_text == "Yes", partition_restriction_text, "selenium user is restricted by partition" )
    locator = "//td[font='Restrict Access by Partition:']/following-sibling::td[1]/descendant::select/option[@selected]"
    emergency_access_text = d.getAttribute( 'text', xpath=locator )
    d.reportCommandStatus( "d.getAttribute", locator, emergency_access_text == "Yes", emergency_access_text, "selenium user can break the glass" )
#    d.screenshot( )
    if unrestricted_text == "No" and partition_restriction_text == "Yes" and emergency_access_text == "Yes":
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
        d.clickElement( xpath="//td[contains( descendant::font, 'Hart, William S.')]/following-sibling::td/descendant::input[@type='button']" )
        d.clickElement( xpath="//input[@type='submit' and @value='Submit']" )
        locator = "//a[text()='Hart, William S.']"
        el = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", locator, not bool( el ), "", "There is no relationship between user selenium and William S. Hart" )
#        d.screenshot( )
        if not bool( el ):
            # Click 'Control Panel' tab, then the 'Partition Mgr' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
            d.clickChartTab( top='Partition Mgr' )
            # Click on the 'Edit' cell on the same row as 'MIE'
            d.clickElement( xpath=OPTIONCELL_XPATH % {
                'search_cell_text': 'MIE',
                'get_cell_text': 'Edit' } )
            d.clickElement( id="part_restrict" )
            d.clickElement( xpath="//input[@value='Change' and @type='button']" )

            # Click on the 'Edit' cell on the same row as 'CCHIT'
            d.clickElement( xpath=OPTIONCELL_XPATH % {
                'search_cell_text': 'CCHIT',
                'get_cell_text': 'Edit' } )
            d.clickElement( id="part_restrict" )
            d.enterAutocomplete( "userac_pm_allowed_users", "selenium" )
            d.clickElement( id="le_pm_allowed_users_button" )
            d.clickElement( xpath="//input[@value='Change' and @type='button']" )

            locator = (TABLE_ROWCOL_XPATH)% { 'rowtext': 'MIE', 'columntext': 'Restricted' }
            MIE_text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, MIE_text == "Yes", MIE_text, "The MIE partition is restricted" )
            locator = (TABLE_ROWCOL_XPATH)% { 'rowtext': 'CCHIT', 'columntext': 'Restricted' }
            CCHIT_text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, CCHIT_text == "Yes", CCHIT_text, "The CCHIT partition is restricted" )
#            d.screenshot( )
            if MIE_text == "Yes" and CCHIT_text == "Yes":
                d.clickElement( xpath=OPTIONCELL_XPATH % {
                    'search_cell_text': 'MIE',
                    'get_cell_text': 'Edit' } )
                locator = "//legend[descendant::text()='Allowed Users']/following-sibling::table/descendant::td[contains( font, 'Selenium, Selenium' )]"
                mie_el = d.getElement( xpath=locator )
                d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, not bool( mie_el ), "", "User selenium does not have access to the MIE partition" )
#                d.screenshot( )

                # Click 'Control Panel' tab, then the 'Partition Mgr' tab
                d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
                d.clickChartTab( top='Partition Mgr' )
                d.clickElement( xpath=OPTIONCELL_XPATH % {
                    'search_cell_text': 'CCHIT',
                    'get_cell_text': 'Edit' } )
                locator = "//legend[descendant::text()='Allowed Users']/following-sibling::table/descendant::td[contains( font, 'Selenium, Selenium' )]"
                cchit_el = d.getElement( xpath=locator )
                d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, bool( cchit_el ), "", "User selenium does have access to the CCHIT partition" )
#                d.screenshot( )
                if not bool( mie_el ) and bool( cchit_el ):
                    #$ Main Test
                    # Click 'E-Chart' tab
                    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                    d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                    d.enterFormData( "MIE-10019", name="sstring" )
                    d.clickElement( name="pat_search" )
                    locator = "//a[font='MIE-10019']"
                    hart_el = d.getElement( xpath=locator )
                    d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, not bool( hart_el ), "", "Could not find William S. Hart because user selenium does not have access to the MIE partition" )
#                    d.screenshot( )
                    if not bool( hart_el ):
                        d.clickElement( id="show_rest_pats" )
                        d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                        d.enterFormData( "MIE-10019", name="sstring" )
                        d.clickElement( name="pat_search" )
                        locator = "//div[contains( text(),  'Partition Restrictions' )]"
                        restriction_el = d.getElement( xpath=locator )
                        d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, bool( restriction_el ), "", "Could not access William S. Hart because user selenium does not have access to the MIE partition" )
                        locator = "//a[@onclick='EC_EmergencyAccess_OK();']"
                        break_el = d.getElement( xpath=locator )
                        d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, bool( break_el ), "", "selenium can break the glass" )
#                        d.screenshot()
                        if bool( restriction_el ) and bool( break_el ):
                            break_el.click( )
                            d.closeAlert( accept=True )
                            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                            d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                            d.enterFormData( "MIE-10019", name="sstring" )
                            d.clickElement( id="show_rest_pats" )
                            d.clickElement( name="pat_search" )
                            locator = "//a[text()='Hart, William S.']"
                            el = d.getElement( xpath=locator )
                            d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( el ), "", "After breaking the glass, selenium can access William S. Hart's chart." )
#                            d.screenshot( )

