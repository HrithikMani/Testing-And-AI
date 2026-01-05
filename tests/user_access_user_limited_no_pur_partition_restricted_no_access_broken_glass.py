#! /usr/bin/env python
# Written by Aaron Lehmann
# MIE Test that a user with limited access, partition restricted without access, no PUR, and ability to
#     break glass can access a patient if the glass is broken
# Date: 02-05-2014

"""
user_access_user_limited_no_pur_partition_restricted_no_access_broken_glass -- Test that a
    user with limited access, partition restricted without access, no PUR, and ability to
    break glass can access a patient if the glass is broken
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[text()='%(search_cell_text)s' or descendant::*[text()='%(search_cell_text)s']]/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"
TABLE_ROWCOL_XPATH ="//tr[td='%(rowtext)s']/td[count(//th[descendant::text()='%(columntext)s']/preceding-sibling::th) + 1]"

def main (d, WCURL):
    #$ Setup
    d.navigate(WCURL.QUICKVIEW)

    # Click the 'Control Panel' tab, then the 'Access Control' tab
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
    d.clickChartTab( top='Access Control' )
    d.enterFormData( "selenium", id="search" )
    d.clickElement( id="finduser" )
    # Click the 'Edit' link on the same row as 'selenium'
    d.clickElement( xpath=OPTIONCELL_XPATH % {
        'search_cell_text': 'selenium',
        'get_cell_text': 'Edit' } )
    d.clickElement( xpath="//a[font='Edit Patients Linked to User']" )
    d.clickElement( id="UPatsuser_RecordList_rmbutton0" )
    d.clickElement( xpath="//input[@type='submit' and @value='Submit']" )
    locator = "//a[text()='Hart, William S.']"
    el = d.getElement( xpath=locator )
    d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, not bool( el ), "", "User selenium has no PUR with William S. Hart." )
#    d.screenshot( )
    if not bool( el ):
        # Click on 'Control Panel' tab, then on 'Partition Mgr' tab
        d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
        d.clickChartTab( top='Partition Mgr' )
        # Click on the 'Edit' link that is on the same row as 'MIE'
        d.clickElement( xpath=OPTIONCELL_XPATH % {
            'search_cell_text': 'MIE',
            'get_cell_text': 'Edit' } )
        d.clickElement( id="part_restrict" )
        d.clickElement( xpath="//input[@value='Change' and @type='button']" )
        d.clickElement( xpath=OPTIONCELL_XPATH % {
            'search_cell_text': 'MIE',
            'get_cell_text': 'Edit' } )
        locator = "//td[text()='Allow Access to Restricted Users']/following-sibling::td/input[@type='checkbox']"
        restricted = d.getAttribute( 'checked', xpath=locator )
        d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, restricted, "", "MIE partition is restricted" )
        locator = "//fieldset[legend/descendant::text()='Allowed Users']/descendant::td[font='Selenium, Selenium']"
        selenium_allowed = d.getElement( xpath=locator )
        d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, not bool( selenium_allowed ), "", "selenium does not have access to the MIE partiton" )
#        d.screenshot( )
        if restricted and not bool( selenium_allowed ):
            # Click the 'Control Panel' tab, then the 'Access Control' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
            d.clickChartTab( top='Access Control' )
            d.enterFormData( "selenium", id="search" )
            d.clickElement( id="finduser" )
            # Click the 'Edit' link on the same row as 'selenium'
            d.clickElement( xpath=OPTIONCELL_XPATH % {
                'search_cell_text': 'selenium',
                'get_cell_text': 'Edit' } )
            d.clickElement( xpath="//a[font='Customize User Security']" )
            d.enterFormData( "Yes", name="E-Chart_Limited Access" )
            d.enterFormData( "Yes", name="E-Chart_Restrict Access by Partition" )
            d.enterFormData( "Yes", name="E-Chart_Emergency Access" )
            d.enterFormData( "Updating for user_access_user_limited_no_pur_partition_restricted_no_access_broken_glass test", id="sec_role_comment" )
            d.clickElement( xpath="//input[@type='submit' and @value='Update Individual Security']" )

            # Click the 'Control Panel' tab, then the 'Access Control' tab
            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'Control Panel'} )
            d.clickChartTab( top='Access Control' )
            d.enterFormData( "selenium", id="search" )
            d.clickElement( id="finduser" )
            # Click the 'Edit' link on the same row as 'selenium'
            d.clickElement( xpath=OPTIONCELL_XPATH % {
                'search_cell_text': 'selenium',
                'get_cell_text': 'Edit' } )
            d.clickElement( xpath="//a[font='Customize User Security']" )
            locator = "//td[font='Limited Access:']/following-sibling::td[1]/descendant::option[@selected]"
            limitted_text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, limitted_text == "Yes", limitted_text, "User selenium has limited access" )
            locator = "//td[font='Restrict Access by Partition:']/following-sibling::td[1]/descendant::option[@selected]"
            partition_restriction_text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, partition_restriction_text == "Yes", partition_restriction_text, "User selenium is restricted by partition" )
            locator = "//td[font='Allow Emergency Access to charts:']/following-sibling::td[1]/descendant::option[@selected]"
            emergency_access_text = d.getAttribute( 'text', xpath=locator )
            d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, emergency_access_text == "Yes", emergency_access_text, "User selenium has emergency access" )
#            d.screenshot()
            if limitted_text == "Yes" and partition_restriction_text == "Yes" and emergency_access_text == "Yes":
                # Click on the 'E-Chart' tab
                d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                d.enterFormData( "MIE-10019", name="sstring" )
                d.clickElement( name="pat_search" )
                locator = "//a[font='MIE-10019']"
                el = d.getElement( xpath=locator )
                d.reportCommandStatus( "d.getElement", locator, not bool( el ), "", "selenium user is unable to find William S. Hart" )
#                d.screenshot( )
                if not bool( el ):
                    d.clickElement( id="show_rest_pats" )
                    d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                    d.enterFormData( "MIE-10019", name="sstring" )
                    d.clickElement( name="pat_search" )
                    locator = '//div[contains(text(), "\'E-Chart: Limited Access Restrictions\'")]'
                    deny_el = d.getElement( xpath=locator )
                    d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( deny_el ), "", "selenium denied access to William S. Hart's chart" )
                    locator = "//a[@onclick='EC_EmergencyAccess_OK();']"
                    breakglass_el = d.getElement( xpath=locator )
                    d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( breakglass_el ), "", "selenium allowed to break glass" )
#                    d.screenshot( )
                    if bool( deny_el ) and bool( breakglass_el ):
                        breakglass_el.click( )
                        d.closeAlert( accept=True )

                        locator = "//*[text()='You have been granted access.']"
                        text = d.getAttribute( 'text', xpath=locator )
                        d.reportCommandStatus( "d.getAttribute", "xpath=%s" % locator, text=="You have been granted access.", text, "selenium broke glass and was granted access." )
#                        d.screenshot( )
                        if text=="You have been granted access.":
                            d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
                            d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]=' MR # ']" )
                            d.clickElement( id="show_rest_pats" )
                            d.enterFormData( "MIE-10019", name="sstring" )
                            d.clickElement( name="pat_search" )
                            locator="//a[text()='Hart, William S.']"
                            el = d.getElement( xpath=locator )
                            d.reportCommandStatus( "d.getElement", "xpath=%s" % locator, bool( el ), "", "selenium can access William S. Hart's chart after breaking the glass" )
#                            d.screenshot( )
