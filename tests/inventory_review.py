# 
# Webchart Inventory Review UnitTest

def main (driver, WCURL):
    """
    Verify the limits placed upon items in inventory
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return

    d.wcutils.SetPermission("Inventory","View Inventory","0",False)
    
    d.navigate(WCURL.INVENTORY_WEEKLY,auto_screenshot=False)
    d.screenshot('noperm')

    d.wcutils.SetPermission("Inventory","View Inventory","1",True)

    d.screenshot('viewperm')
