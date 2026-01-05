# 
# Webchart Inventory File Import UnitTest

def main (driver, WCURL):
    """
    Verify the import of csv data into inventory
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return

    d.wcutils.SetPermission("Inventory","Receive Inventory","0",False)
    d.wcutils.SetSystemSetting("E-Chart","Inventory","Show Quantity In AutoComplete","1",False)
    
    d.navigate(WCURL.INVENTORY_IMPORT,auto_screenshot=False)
    d.screenshot('noperm')

    d.wcutils.SetPermission("Inventory","Receive Inventory","1",True)

    d.screenshot('hasperm')

    d.enterFormData('inventory_scanner_import.csv',name='file')
    
    d.clickElement(value='Upload')
    
    d.pause(3)
    d.screenshot('translations_needed')
    
    d.clickElement(text='Create Translation')
    
    d.pause(3)
    d.switchToPopup()
    d.screenshot('trans_manager')
    
    d.clickElement(text='Edit')
    
    d.pause(3)
    d.screenshot('trans_edit')
    
    d.enterFormData('Location',name='type')
    
    d.enterFormData('OFFICE',name='trans_to')
    
    d.clickElement(value='Edit')
    
    d.pause(3)
    d.screenshot('translated')
    
    d.closePopup()
    
    d.clickElement(value='Continue')
    
    d.pause(3)
    
    d.screenshot('cgi_load_1')
    

    d.navigate(WCURL.INVENTORY_IMPORT,auto_screenshot=False)

    d.enterFormData('inventory_scanner_import.csv',name='file')
    
    d.clickElement(value='Upload')
    
    d.pause(3)
    d.screenshot('csv_load_1')
    
    
    d.enterAutocomplete('inv_medac1', 'oxycodone', 0, 'oxycodone (New) qty: 0')
    d.pause(1)
    d.enterAutocomplete('inv_formac1', 'c', 0, 'capsule 5mg (Oral) qty: 0')
    d.pause(1)
    d.enterAutocomplete('inv_lot_id1_ac', '4657X91', -1)
    d.enterAutocomplete('inv_manufac1','GlaxoSmithKline',-1)
    d.enterMIEDate('inv_exp_date1',1,1,20)
    
    d.enterAutocomplete('inv_medac4', 'aten', 0, 'atenolol (New) qty: 0')
    d.pause(1)
    d.enterAutocomplete('inv_formac4', 'tab', 0, 'tablet 25mg (Oral) qty: 0')
    
    d.clickElement(value='Save')
    
    d.screenshot('first_submission')
    
    
    d.enterAutocomplete('inv_medac5', 'amox', 0, 'amoxicillin (New) qty: 300')
    d.pause(1)
    d.enterAutocomplete('inv_formac5', 'c', 0, 'capsule 500mg qty: 300')
    d.pause(1)
    d.enterAutocomplete('inv_lot_id5_ac', 'NGKJ921B', -1)
    d.enterAutocomplete('inv_manufac5','Merywhether',-1)
    d.enterMIEDate('inv_exp_date5',3,2,19)
    
    d.enterAutocomplete('inv_medac8', 'crutch', 0, 'Crutches 48" qty: ')
    d.pause(1)
    d.verifyAttribute('value','10',id='inv_inventory_id8')
    d.enterAutocomplete('inv_lot_id8_ac', '', -1)
    
    d.enterAutocomplete('inv_medac9', 'Demerol O', 0, 'Demerol oral (New) qty: 0')
    d.pause(1)
    d.enterAutocomplete('inv_formac9', 'S', 0, 'Solution 50mg/5 mL - OBSOLETE qty: 0')
    d.pause(1)
    d.enterAutocomplete('inv_lot_id9_ac', 'BBB9191', -1)
    d.enterAutocomplete('inv_manufac9','Pythagoras',-1)
    d.enterMIEDate('inv_exp_date9',1,9,18)
    
    d.screenshot('filled_in')
    
    d.clickElement(value='Save')
    
    d.screenshot('second_submission')

    d.wcutils.SetSystemSetting("Inventory","Lot Numbers","Are Required","0",False)
    
    
    d.navigate(WCURL.INVENTORY_IMPORT,auto_screenshot=False)

    d.enterFormData('inventory_scanner_import.csv',name='file')
    
    d.clickElement(value='Upload')
    
    d.pause(3)
    d.screenshot('csv_load_2')
    
    d.enterAutocomplete('inv_lot_id1_ac', '4657X91', 0)
    d.enterAutocomplete('inv_lot_id6_ac', 'NGKJ921B', 0)
    d.enterAutocomplete('inv_lot_id10_ac', 'BBB9191', 0)
    
    d.enterAutocomplete('inv_lot_id10_ac', 'XXX1919', -1)
    d.enterMIEDate('inv_exp_date10',2,5,18)
    
    d.screenshot('filled_in2')
    
    d.clickElement(value='Save')

    d.screenshot('third_submission')

    d.navigate(WCURL.INVENTORY,auto_screenshot=False)
    d.clickElement(text='SHOW ALL')
    
    d.pause(3)
    d.screenshot('all_listing')
