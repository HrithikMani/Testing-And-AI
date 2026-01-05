# 
# Webchart Inventory View UnitTest

def main (driver, WCURL):
    """
    View the available inventory items
    """

    d = driver
  
    if d.getUserData('inventory_failure'):
        return
  
    d.wcutils.SetPermission("Inventory","View Inventory","0",False)
    d.wcutils.SetPermission("Inventory","Edit Inventory","0",False)
    d.wcutils.SetPermission("Inventory","Expire Inventory","0",False)
    d.wcutils.SetPermission("Inventory","Transfer Inventory","0",False)

    d.navigate(WCURL.INVENTORY,auto_screenshot=False)
    d.screenshot('noperms')

    d.wcutils.SetPermission("Inventory","View Inventory","1",True)

    d.screenshot('viewperm')

    d.wcutils.SetPermission("Inventory","Expire Inventory","1",True)
    
    d.screenshot('expireperm')

    d.wcutils.SetPermission("Inventory","Edit Inventory","1",True)
    
    d.screenshot('editperm')

    d.wcutils.SetPermission("Inventory","Transfer Inventory","1",True)
    
    d.screenshot('transferperm')

#    d.enterFormData('Lisinopril 5',id='searchVal')
#    d.clickElement(name='search')
#    d.screenshot('itemsearch')
    
#    d.clickElement(id='searchBy_il.lot_number')
#    d.enterFormData('axy',id='searchVal')
#    d.clickElement(name='search')
#    d.screenshot('lotsearch')
    
#    d.clickElement(id='searchBy_ib.location')
#    d.enterFormData('Hospital',id='searchVal')
#    d.clickElement(name='search')
#    d.screenshot('sitesearch')
