# 
# Webchart Inventory Control UnitTest

def main (driver, WCURL):
    """
    Add new available Inventory Items
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
  
    d.wcutils.SetPermission("Inventory","Edit Master Inventory List","0",False)
    d.wcutils.SetPermission("Inventory","View Inventory","0",False)
    d.wcutils.SetPermission("Inventory","Merge Inventory Items","0",False)

    d.navigate(WCURL.INVENTORY_CONTROL,auto_screenshot=False)
    d.screenshot('noperms')

    d.wcutils.SetPermission("Inventory","View Inventory","1",True)
    d.screenshot('hasperm')    

    d.wcutils.SetPermission("Inventory","Edit Master Inventory List","1",True)
    d.screenshot('manageperm')

    d.wcutils.SetPermission("Inventory","Merge Inventory Items","1",True)
    d.screenshot('mergeperm')
    
    d.clickElement(text='Add an Item')
    
    d.screenshot('add_item')
    
    d.enterFormData('Multi-Vitamin',id='display_name')
    d.clickElement(name='save')    
    
    d.clickElement(text='Add an Item')
    d.enterFormData('Crutches 48"',id='display_name')
    d.enterFormData('Crutches',id='item_alias')
    d.clickElement(name='save')
    
    d.clickElement(text='Add an Item')
    d.enterFormData('Crutches 60"',id='display_name')
    d.enterFormData('Crutches',id='item_alias')
    d.clickElement(name='save')

    d.clickElement(text='Add an Item')
    d.enterFormData('MMR Vaccine',id='display_name')
    d.clickElement(name='save')

    d.clickElement(text='Add an Item')
    d.enterFormData('DTAP',id='display_name')
    d.clickElement(name='save')
    
    d.clickElement(text='Add an Item')
    d.enterFormData('My Dog Spot',id='display_name')
    d.clickElement(name='save')
    
    d.clickElement(xpath="//div[@id='lv_inv_control_span']/table/tbody[1]/tr[14]/td[6]/a[text()='Edit']")
    
    d.screenshot('edit_item')
    
    d.enterFormData('MicroSpot Dog Remover',id='display_name',clear=True)
    d.clickElement(name='save')
    
    d.screenshot('after_edit')
    
    d.clickElement(xpath="//div[@id='lv_inv_control_span']/table/tbody[1]/tr[14]/td[6]/a[text()='Delete']")
    
    d.screenshot('delete_item')
    
    d.clickElement(name='save')
    
    d.screenshot('after_delete')

    d.clickElement(xpath="//div[@id='lv_inv_control_span']/table/tbody[1]/tr[1]/td[6]/a[text()='Delete']")
        
    d.screenshot('delete_failed')

    d.clickElement(id='multiSearchLink')
    d.screenshot('multisearch')
    
    d.clickElement(id='tS_searchBy0_0')
    d.enterFormData('lisinopril',id='tS_searchVal0')
    d.clickElement(id='tS_searchBy1_0')
    d.enterFormData('lasix',id='tS_searchVal1')
    d.clickElement(id='search')
    
    d.screenshot('multisearch')
    
    d.clickElement(id='searchClear')
    
    d.screenshot('cleared_search')
    
    # switch back from multi/single search options
    d.clickElement(id='multiSearchLink')
    d.screenshot('singleSearch')
    
    d.clickElement(id='tS_searchBy0_2')
    d.enterFormData('5',id='tS_searchVal0')
    d.clickElement(id='search')
    
    d.screenshot('id_search')
    
    d.clickElement(id='tS_searchBy0_1')
    d.enterFormData('crutch',id='tS_searchVal0')
    d.clickElement(id='search')

    d.screenshot('alias_search')
