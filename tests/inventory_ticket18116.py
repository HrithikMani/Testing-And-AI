# 
# Webchart Inventory View UnitTest related to ticket #18116 verifying 
# that items added without a lot number are placed into the same 'lot' record

def main (driver, WCURL):
    """
    View the available inventory items
    """

    d = driver
  
    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
  
    d.wcutils.SetPermission("Inventory","Receive Inventory","1",False)

    d.wcutils.SetSystemSetting("E-Chart","Inventory","By Site","1",False)
    
    d.wcutils.SetSystemSetting("E-Chart","Inventory","Use Lot Numbers","1",False)

    d.wcutils.SetSystemSetting("Inventory","Lot Numbers","Are Required","0",False)
    	
    d.navigate(WCURL.INVENTORY_RECEIVE,auto_screenshot=False)
    
    
    d.enterFormData('Office',id='inv_transloc0')
    
    d.enterAutocomplete('inv_medac0', 'Crutches 48', 0, 'Crutches 48" qty: ')
    
    d.enterFormData('5',id='inv_quantity0')
    
    #d.enterAutocomplete('inv_lot_id0_ac','',-1)
    
    #d.enterFormData('',id='inv_manufacturer0')
    
    #d.enterMIEDate('inv_exp_date0',1,1,15)

    d.clickElement(value='Add to Inventory')
    
    d.pause(3)
    

    d.enterFormData('Office',id='inv_transloc0')
    
    d.enterAutocomplete('inv_medac0', 'Crutches 48', 0, 'Crutches 48" qty: 5.00')
    
    d.enterFormData('8',id='inv_quantity0')
    
    #d.enterAutocomplete('inv_lot_id0_ac','',-1)
    
    #d.enterFormData('',id='inv_manufacturer0')
    
    #d.enterMIEDate('inv_exp_date0',1,1,15)

    d.clickElement(value='Add to Inventory')
    
    d.pause(3)

    d.navigate(WCURL.INVENTORY,auto_screenshot=False)
    d.clickElement(text='SHOW ALL')
    
    d.pause(3)
    d.screenshot('all_listing')
