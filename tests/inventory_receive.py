# 
# Webchart Inventory Receive UnitTest

def verifyRow(driver, row, location, stockpile, medid):
    """
    Verifies in an inventory row
    """
    
    d = driver

    ret=True

    if not d.verifyAttribute('value',location,id='inv_transloc'+row):
        ret=False
    if stockpile:
        if not d.verifyAttribute('value',stockpile,id='inv_stockpile_id'+row):
            ret=False
    if not d.verifyAttribute('value',medid,id='inv_medication_id'+row):
        ret=False
    return ret

def main (driver, WCURL):
    """
    Receive a quantity of an inventory item
    """

    d = driver
    
    d.wcutils.SetPermission("Inventory","Receive Inventory","0",False)

    d.wcutils.SetSystemSetting("E-Chart","Inventory","By Site","1",False)
    
    d.wcutils.SetSystemSetting("E-Chart","Inventory","Use Lot Numbers","1",False)
	
    d.navigate(WCURL.INVENTORY_RECEIVE,auto_screenshot=False)
    d.screenshot('noperm')

    d.wcutils.SetPermission("Inventory","Receive Inventory","1",True)

    d.screenshot('hasperm')
        
    d.enterFormData('Office',id='inv_transloc0')
    
    d.enterAutocomplete('inv_medac0', 'lisino', 0, 'lisinopril (New)')
    d.pause(1)
    d.enterAutocomplete('inv_formac0', 'tablet 5', 0, 'tablet 5mg')
    
    d.enterFormData('50',id='inv_quantity0')
    
    d.enterAutocomplete('inv_lot_id0_ac','abc123',-1)
    
    d.enterAutocomplete('inv_manufac0','SomeManu Co',-1)
    
    d.enterMIEDate('inv_exp_date0',1,1,2030)
    
    d.enterFormData('Hospital',id='inv_transloc1')
    
    d.enterAutocomplete('inv_medac1', 'lisino', 0, 'lisinopril (New)')
    d.pause(1)
    d.enterAutocomplete('inv_formac1', 'tablet 1', 0, 'tablet 10mg')
    
    d.enterFormData('30',id='inv_quantity1')
    
    d.enterAutocomplete('inv_lot_id1_ac','987xzy',-1)
    
    d.enterAutocomplete('inv_manufac1','MediPill Co',-1)
    
    d.enterMIEDate('inv_exp_date1',6,1,2030)

    d.enterFormData('Hospital',id='inv_transloc2')
    d.pause(2)
    d.enterFormData('Store Room A',id='inv_stockpile_id2')
    
    d.enterAutocomplete('inv_medac2', 'lisino', 0, 'lisinopril (New)')
    d.pause(1)
    d.enterAutocomplete('inv_formac2', 'tablet 2', 0, 'tablet 20mg')
    
    d.enterFormData('15',id='inv_quantity2')
    
    d.enterAutocomplete('inv_lot_id2_ac','axy391',-1)
    
    d.enterAutocomplete('inv_manufac2','MediPill Co',-1)
    
    d.enterMIEDate('inv_exp_date2',3,15,2030)
    
    d.enterFormData('Hospital',id='inv_transloc3')
    d.pause(2)
    d.enterFormData('Store Room B',id='inv_stockpile_id3')
    
    d.enterAutocomplete('inv_medac3', 'lisino', 0, 'lisinopril (New)')
    d.pause(1)
    d.enterAutocomplete('inv_formac3', 'tablet 5', 0, 'tablet 5mg')
    
    d.enterFormData('20',id='inv_quantity3')
    
    d.enterAutocomplete('inv_lot_id3_ac','abc123',-1)
    
    d.enterAutocomplete('inv_manufac3','SomeManu Co',-1)
    
    d.enterMIEDate('inv_exp_date3',1,1,2030)

    inventory_failure=False
    if not verifyRow(d,'0','OFFICE',None,'268801'):
        inventory_failure=True
    if not verifyRow(d,'1','HOSP',None,'244899'):
        inventory_failure=True
    if not verifyRow(d,'2','HOSP','1','183474'):
        inventory_failure=True
    if not verifyRow(d,'3','HOSP','2','268801'):
        inventory_failure=True

    if not inventory_failure:
        d.clickElement(id='recvMeds')
    
        d.screenshot('received')
    else:
        d.setUserData('inventory_failure',True)

