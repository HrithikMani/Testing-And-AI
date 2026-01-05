# 
# Webchart Inventory View UnitTest related to mantis #12239 verifying that mappings aren't causing duplicate rows

def main (driver, WCURL):
    """
    View the available inventory items
    """

    d = driver
  
    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
  
    d.wcutils.SetPermission("Inventory","View Inventory","1",False)
    
    d.wcutils.SetPreference("Inventory","User Interface","Hide Out of Stock Items","showAll")

    d.navigate(WCURL.INVENTORY_MAPPINGS,auto_screenshot=False)

    d.navigate(WCURL.INVENTORY)
