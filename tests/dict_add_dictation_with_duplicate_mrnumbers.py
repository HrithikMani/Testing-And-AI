# MIE test that dictation via pin number uses the doctor's preferences for partition rather than the system-wide default
# Written by Aaron Lehmann
# Date: 01-17-2014

import re
import os

SIDETAB_XPATH = "//div[@id='wc_sidetabs']/descendant::a[contains( @class, 'wc_tab' ) and text()='%s']"

def main(d, WCURL):
    """
    Verifies that dictation can be uploaded using user pin number and will use the
    user's starting partion rather than the system's starting partition to find users.

    Assumptions:
        1) user exists as administrator
        2) patient Jane Doe exists with MR# 10006 in MIE partition

    Steps:
        1) add pin 8080 to user.
        2) set users's default partition to MIE.
        2) set set the default user's default partition to MIE.
        3) add patient MR# 10006 to partition MR.  Verify the patient exists by searching.
            a) set partition MR as the only editable partition in partition manager
            b) add MRPatient to MR with #10006
        4) upload dictation for patient MR# 10006 using pin 8080.  Verify the dictation is added to MRPatient using the Dictation link on the sidebar.
    """
    d.navigate(WCURL.QUICKVIEW)
    #$ Set up pin for user selenium
    d.miedb.dbExec("UPDATE users "
                   "SET pin=8080 "
                   "WHERE username='%s'" % d.getUserData('username') )

    d.clickElement( xpath=SIDETAB_XPATH % 'Control Panel' )
    d.clickChartTab( top='Partition Mgr' )

    #$ Set up CCHIT as View
    d.clickElement( xpath="//td[contains(@class, 'partmanager_Partition_cell') and text()='CCHIT']/following-sibling::td[descendant::a='Edit']/descendant::a" )
    d.enterFormData( "V", id="echart_opts" )
    d.clickElement( name="change_btn" )

    #$ Set up MR as Edit( Optional )
    d.clickElement( xpath="//td[contains(@class, 'partmanager_Partition_cell') and text()='MR']/following-sibling::td[descendant::a='Edit']/descendant::a" )
    d.enterFormData( "10006", id="mr_sequence" )
    d.enterFormData( "O", id="echart_opts" )
    d.clickElement( name="change_btn" )
    d.screenshot()

    #$ Set up selenium's default starting partition to be MIE
    d.clickChartTab( top='My Settings' )
    d.enterFormData( "MIE", name="E-ChartDefaultsStarting Partition" )
    d.clickElement( name="change_settings" )

    #$ Set up system's default starting partition to be MR
    d.clickChartTab( top='My Settings' )
    d.enterFormData( "0", xpath="//font[text()='You can edit preferences for: ']/select" )
    d.enterFormData( "MR", name="E-ChartDefaultsStarting Partition" )
    d.clickElement( name="change_settings" )

    #$ Set up user MRPatient in partition MR
    d.clickElement( xpath=SIDETAB_XPATH % 'E-Chart' )
    d.clickChartTab( top='Patient Registration' )
    d.enterFormData( "MRPatient", id="patient_last_name" )
    d.enterFormData( "MR", id="patient_first_name" )
    d.enterMIEDate("patient_birth_date", 1, 1, 2014, 13)
    d.enterFormData( "222-22-2222", id="patient_ssn" )
    d.clickElement( xpath="//input[@type='submit'][@value='Search']" )
    d.enterFormData( "10006", name="EDITMR_mrnumber_MR" )
    d.clickElement( xpath="//input[@type='submit'][@value='Save']" )

    #$ Verify that we have patients for MR# 10006 in both MR and MIE partitions
    d.clickElement( xpath=SIDETAB_XPATH % 'E-Chart' )
    d.clickChartTab( top='Patient Search' )
    d.clickElement( xpath="//text()[.=' MR # ']/preceding-sibling::input[@type='radio']" )
    d.enterFormData( "10006", name="sstring" )
    d.clickElement( value="Search" )
    d.screenshot( )

    """
    #$ upload the file using curl
    ulaw = "dict_add_dictation_with_duplicate_mrnumbers.ul"

    command = 'curl -F "f=dicup" -F "s=add" -F "duration=1" -F "pin=8080" -F "uploaddate=20140109-143520" -F "mrnumber=10006" -F "format=8,1,8000,ulaw" -F "file=@%s/%s;type=sound/ulaw" %s/webchart.cgi' % ( d.driverOptions.uploadDir, ulaw, d.driverOptions.baseurl )
    success_message = "\n".join(d.zeus.command( command ))

    dictation_id = re.split( "[()]", success_message )[1]
    succeeded = bool(dictation_id)
    d.reportCommandStatus(
        "",
        "",
        succeeded,
        succeeded and ("dictation_id=%s" % dictation_id) or "",
        succeeded and success_message or "Dictation was not successfully uploaded" )

    #$ Make sure that the dictation attached to Jane Doe
    d.clickElement( xpath=SIDETAB_XPATH % 'Dictation' )
    d.clickElement( xpath="//td[descendant::font[.='%06d'] and contains( @class, 'di__mypending_Dict_20ID_cell' )]/following-sibling::td[contains(@class, 'di__mypending_Last_cell')]/descendant::a[1]" % int(dictation_id) )
    d.screenshot()

    d.navigate(WCURL.QUICKVIEW)
    """
