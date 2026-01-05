# 
# Webchart Inventory View UnitTest related to mantis #11352 verifying that Hide/Show out of stock links are now sticky

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

    d.navigate(WCURL.INVENTORY)
    
    d.clickElement(text='Hide Out Of Stock')
    d.pause(2)
    
    d.screenshot('hidingOOS')
    
    d.clickElement(text='Show Out Of Stock')
    d.pause(2)
    
    d.screenshot('showingOOS')
    
