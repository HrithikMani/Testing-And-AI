# 
# Webchart Inventory Stockpile Add UnitTest

def main (driver, WCURL):
    """
    Add a stockpile, then verify that it's been added
    """

    d = driver

    d.wcutils.SetPermission("Inventory","Manage Stockpiles","0",False)
    
    d.navigate(WCURL.INVENTORY_STOCKPILE_MANAGER,auto_screenshot=False)
    d.screenshot('noperm')

    d.wcutils.SetPermission("Inventory","Manage Stockpiles","1",True)

    d.screenshot('viewperm')
    
    d.wcutils.SetPermission("Inventory","Manage Stockpiles","2",True)
	
    d.screenshot('addperm')
    
    d.miedb.dbExec("INSERT INTO locations SET code='HOSP',description='Hospital',active=1")
    
    d.clickElement(text='Add Stockpile')
    
    d.enterFormData('',id='description')
    
    d.clickElement(id='isp_save')
    
    d.screenshot('enterdescription')
    
    d.enterFormData('Hospital',id='location')
    d.enterFormData('Store Room A',id='description')
    
    d.clickElement(id='isp_save')

    d.clickElement(text='Add Stockpile')
    d.enterFormData('Hospital',id='location')
    d.enterFormData('Store Rome B',id='description')
    d.clickElement(id='isp_save')
    
    d.screenshot('addlist')