"""
    Unit Test for f=wcversion and self upgrade
    @owners: dcornewell
    @filedeps: src/wcversion.c, src/webchartdb/webchartdb.c
"""

def main (d, WCURL):
    """
    Test the wcversion page
    """
    d.startSection('Login as Dave')
    d.navigate("?f=logout")
    d.wcutils.insertWCTSession('dave')
    d.endSection()
    d.startSection('Check wc version page')
    d.navigate("?f=wcversion")
    d.verifyElementPresent(True,xpath="//span[contains(.,'Refresh Stored Procedures')]")
    d.verifyElementPresent(True,xpath="//span[contains(.,'Reevaluate Security Permissions')]")
    d.endSection()

    d.startSection('Test refreshing stored procedures, Triggers, and Views')
    d.clickElement(text='Refresh')
    d.clickElement(xpath="//a[contains(.,'Refresh Stored Procedures')]")
    d.verifyElementPresent(xpath="//div[contains(.,'Started updating')]", )
    old = d.timeout
    d.setTimeout(300)
    d.verifyElementPresent(xpath="//div[contains(.,'COMPLETE: WebChart database')]")
    d.setTimeout(old)
    d.endSection()
