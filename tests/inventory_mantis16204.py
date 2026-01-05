# 
# Webchart Inventory View/Weekly UnitTest related to mantis #16204 verifying that the drug class system setting works

def main (driver, WCURL):
    """
    View the available inventory items
    """

    d = driver
  
    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
  
    d.wcutils.SetPermission("Inventory","View Inventory","1",False)
    d.wcutils.SetSystemSetting("E-Chart","Inventory","Show Drug Classes","1",False)
    
    d.navigate(WCURL.INVENTORY)

    d.navigate(WCURL.INVENTORY_WEEKLY)
    
    d.navigate(WCURL.INVENTORY_TRANSACTIONS,auto_screenshot=False)
    
    d.clickElement(value='Search')
    d.pause(3)
    d.screenshot()
