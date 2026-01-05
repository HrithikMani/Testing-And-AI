# 
# Webchart Inventory Quantity Management UnitTest

def main (driver, WCURL):
    """
    Manage the available quantities for inventory items
    """

    d = driver

    if d.getUserData('inventory_failure'):
        return

    d.navigate(WCURL.INVENTORY)

    d.wcutils.setNeverConfirm(True)
    
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
        
    lv.clickCell('Expire','Options','50')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[4]/td[7]/font/a[2]/font[text()='Expire']")
    
    d.screenshot('expiredlg')
    
    d.enterFormData('2',id='quantity',clear=True)
    d.enterFormData('Dropped on the Floor',id='transComment')
    
    d.clickElement(name='save')
    
    d.screenshot('expired')
    
    d.wcutils.setNeverConfirm(True)

    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    #
    #
    lv.clickCell('Transfer','Options','48')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[4]/td[7]/font/a[3]/font[text()='Transfer']")
    
    d.screenshot('transferdlg')
    
    d.enterFormData('12',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
    d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Hospital)')
    d.enterFormData('Gave to Sue',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '2':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
        d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Hospital)')

    if not d.verifyAttribute('value','2',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return
        
    d.clickElement(name='save')
    
    d.wcutils.setNeverConfirm(True)
    
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    lv.clickCell('Transfer','Options','20')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[4]/td[7]/font/a[3]/font[text()='Transfer']")

    d.enterFormData('6',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
    d.enterAutocomplete('transfer_pat_ac', 'None', 1, 'None (Hospital:Store Room A)')
    d.enterFormData('Gave to Jen',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '3':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
        d.enterAutocomplete('transfer_pat_ac', 'None', 1, 'None (Hospital:Store Room A)')

    if not d.verifyAttribute('value','3',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')
    
    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    
    lv.clickCell('Transfer','Options','36')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[6]/td[7]/font/a[3]/font[text()='Transfer']")

    d.enterFormData('8',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
    d.enterAutocomplete('transfer_pat_ac', 'None', 2, 'None (Hospital:Store Room B)')
    d.enterFormData('Gave to Bob',id='transComment')

    if d.getAttribute('value',id='dest_bucket_id') == '4':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
        d.enterAutocomplete('transfer_pat_ac', 'None', 2, 'None (Hospital:Store Room B)')

    if not d.verifyAttribute('value','4',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')

    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    
    lv.clickCell('Transfer','Options','30')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[1]/td[7]/font/a[3]/font[text()='Transfer']")

    d.enterFormData('14',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
    d.enterAutocomplete('transfer_pat_ac', 'None', 1, 'None (Hospital:Store Room A)')
    d.enterFormData('Gave to Alice',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '3':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
        d.enterAutocomplete('transfer_pat_ac', 'None', 1, 'None (Hospital:Store Room A)')

    if not d.verifyAttribute('value','3',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')
    
    d.screenshot('transferred')
    
    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    

    lv.clickCell('Transfer','Options','12')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[4]/td[7]/font/a[3]/font[text()='Transfer']")
    
    d.screenshot('transferdlg')
    
    d.enterFormData('12',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Office', 0, 'Office')
    d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Office)')
    d.enterFormData('Gave to Mike',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '1':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Office', 0, 'Office')
        d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Office)')
    
    if not d.verifyAttribute('value','1',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')
    
    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    
    lv.clickCell('Transfer','Options','6')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[5]/td[7]/font/a[3]/font[text()='Transfer']")

    d.enterFormData('6',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
    d.enterAutocomplete('transfer_pat_ac', 'None', 2, 'None (Hospital:Store Room B)')
    d.enterFormData('Gave to Bob',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '4':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
        d.enterAutocomplete('transfer_pat_ac', 'None', 2, 'None (Hospital:Store Room B)')

    if not d.verifyAttribute('value','4',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')
    
    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    
    lv.clickCell('Transfer','Options','28')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[6]/td[7]/font/a[3]/font[text()='Transfer']")

    d.enterFormData('8',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Off', 0, 'Office')
    d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Office)')
    d.enterFormData('Gave to Mike',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '1':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Off', 0, 'Office')
        d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Office)')

    if not d.verifyAttribute('value','1',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')

    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    
    lv.clickCell('Transfer','Options','14')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[2]/td[7]/font/a[3]/font[text()='Transfer']")

    d.enterFormData('14',id='quantity',clear=True)
    
    d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
    d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Hospital)')
    d.enterFormData('Gave to Sue',id='transComment')
    
    if d.getAttribute('value',id='dest_bucket_id') == '2':
        # ac didn't work
        d.enterAutocomplete('transfer_site_ac', 'Hosp', 0, 'Hospital')
        d.enterAutocomplete('transfer_pat_ac', 'None', 0, 'None (Hospital)')

    if not d.verifyAttribute('value','2',id='dest_bucket_id'):
        d.setUserData('inventory_failure',True)
        return

    d.clickElement(name='save')
    
    d.screenshot('returned')
    
    d.wcutils.setNeverConfirm(True)
    lv = d.getMIEListview('General Inventory','Qty')
    if lv == None:
        d.setUserData('inventory_failure')
        return
    
    lv.clickCell('Edit','Options','48')
    #d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[2]/tr[7]/td[7]/font/a[1]/font[text()='Edit']")
    
    d.enterFormData('46',id='quantity')
    d.enterFormData('miscounted',id='transComment')
    
    d.clickElement(name='save')
    
    d.wcutils.setNeverConfirm(True)
    
    d.clickElement(text='Hide Out Of Stock')
    
    d.screenshot('hideoos')
    
    d.wcutils.setNeverConfirm(True)
