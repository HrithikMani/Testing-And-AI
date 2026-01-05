# 
# Webchart UnitTest ensuring all Iventory Add fields are cleared

def main(driver, WCURL):

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return

    d.navigate(WCURL.INVENTORY_ADD,auto_screenshot=False)

    d.enterAutocomplete('inv_medac0','activella',0)
    d.enterAutocomplete('inv_formac0','tablet',0) 
    d.enterFormData('12345', name='inv_lot_id0_vis')
    d.enterFormData('10', name='inv_quantity0')
    d.enterAutocomplete('inv_manufac0','some',0)
    #d.screenshot('DataEntered')

    d.clickElement(id='clear_0')
    d.verifyAttribute('value', "", 'inv_acval0')
    d.verifyAttribute('value', "", 'inv_formacval0')
    d.verifyAttribute('value', "", 'inv_lot_id0_vis')
    d.verifyAttribute('value', "", 'inv_quantity0')
    d.verifyAttribute('value', "", 'inv_manufacturer0')
    #d.screenshot('DataCleared')

