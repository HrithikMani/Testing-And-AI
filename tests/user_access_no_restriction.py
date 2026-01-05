#! /usr/bin/env python
# MIE test that when a user with no access restrictions attempts to access an unrestricted patient, access is granted.
# Written by Aaron Lehmann
# Date: 01-30-2014

"""
user_access_no_restriction -- User with no access restrictions attempts to access an unrestricted patient.  Access is granted.
"""

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%(tabtext)s']"
OPTIONCELL_XPATH = "//td[descendant::a='%(search_cell_text)s']/following-sibling::td/descendant::*[text()='%(get_cell_text)s']"

def main (d, WCURL):
    #$ Setup
    d.navigate(WCURL.QUICKVIEW)

    #$ Main Test
    # Click on the 'E-Chart' tab on the side
    d.clickElement( xpath=SIDETAB_XPATH % {'tabtext': 'E-Chart'} )
    # Search by name for Hart, William
    d.clickElement( xpath="//input[@type='radio' and following-sibling::text()[1]='Name']" )
    d.enterFormData( "Hart, William", name="sstring" )
    d.clickElement( name="pat_search" )
    locator = "//a[text()='Hart' and following-sibling::a/text()='William' and following-sibling::a/text()='S.']"
    el = d.getElement( xpath=locator )
    d.reportCommandStatus("d.getElement", "xpath=%s" % locator, bool( el ), "", "Found patient William S. Hart")
#    d.screenshot( )
    if bool( el ):
        el.click( )
        locator = "//a[text()='Hart, William S.']"
        d.reportCommandStatus("d.getElement", "xpath=%s" % locator, bool( el ), "", "Accessed patient William S. Hart")
#        d.screenshot( )
