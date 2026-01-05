# 
# Webchart Inventory View UnitTest related to mantis #11352 verifying that Hide/Show out of stock links are now sticky
from selenium.webdriver.common.keys import Keys

def setAcRow(driver, num, med, mrow, med_full, form, frow, form_full, qty):
    """
    Fills in an inventory row
    """

    d = driver

    d.enterFormData('HOSP',id='inv_transloc'+num)
    d.pause(2)
    d.enterFormData('1',id='inv_stockpile_id'+num)
    
    d.enterAutocomplete('inv_medac'+num, med, mrow, med_full)
    d.pause(1)
    d.enterAutocomplete('inv_formac'+num, form, frow, form_full)
    
    d.enterFormData(qty,id='inv_quantity'+num)
    
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
    View the available inventory items
    """

    d = driver
  
    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
  
    d.wcutils.SetPermission("Inventory","View Inventory","1",False)
    
    d.navigate(WCURL.INVENTORY_RECEIVE)

    setAcRow(d, '0', 'lisinopril', 0, 'lisinopril (New)', 'tablet 40mg', 0, 'tablet 40mg', 25)
    
    d.enterAutocomplete('inv_lot_id0_ac', '', -1)
    
    d.enterAutocomplete('inv_manufac0','Another Manufacturer',-1)
    
    d.enterMIEDate('inv_exp_date0',9,23,2017)

    
    d.clickElement(value='Add to Inventory')
    
    d.pause(3)
    
    d.navigate(WCURL.INVENTORY)

    d.navigate(WCURL.INVENTORY_RECEIVE)

    setAcRow(d, '0', 'lisinopril', 0, 'lisinopril (New)', 'tablet 40mg', 0, 'tablet 40mg', 5)
    
    d.enterAutocomplete('inv_lot_id0_ac',Keys.ARROW_DOWN,0,'Unknown (Another Manufacturer 09-23-2017) qty: 25')
    
    d.screenshot('lot_autofilled')
    
    d.clickElement(value='Add to Inventory')
    
    d.pause(3)

    d.navigate(WCURL.INVENTORY)
