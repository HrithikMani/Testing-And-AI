# 
# Webchart Inventory Stockpile Edit UnitTest

def main (driver, WCURL):
    """
    Edit a stockpile, then verify that it's been updated
    """

    d = driver

    d.navigate(WCURL.INVENTORY_STOCKPILE_MANAGER,auto_screenshot=False)
    d.screenshot('noeditperm')
    
    d.wcutils.SetPermission("Inventory","Manage Stockpiles","4",True)
    
    d.screenshot('editperm')
    
    d.clickElement(text='Edit')
    
    d.enterFormData('',id='description')

    d.clickElement(id='isp_save')

    d.screenshot('enterdescription')
    
    d.enterFormData('Store Room B',id='description')
    
    d.clickElement(id='isp_save')
    
    d.screenshot('updatedlist')
