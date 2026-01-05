# 
# Webchart Inventory View UnitTest

def main (driver, WCURL):
    """
    View the available inventory items
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return

    d.wcutils.SetPermission("Inventory","View Transactions","0",False)
    
    d.navigate(WCURL.INVENTORY_TRANSACTIONS,auto_screenshot=False)

    d.screenshot('noperm')
    
    d.wcutils.SetPermission("Inventory","View Transactions","1",True)
    
    d.screenshot('viewperm')
    
    d.clickElement(text='Hide')
    
    d.screenshot('search_hidden')
    
    d.clickElement(text='Show Search')

    d.screenshot('search_shown')
    
    d.enterFormData(False,id='tS_t.trans_type1')
    d.enterFormData(False,id='tS_t.trans_type2')
    d.enterFormData(False,id='tS_t.trans_type3')
    d.enterFormData(False,id='tS_t.trans_type4')
    d.enterFormData(False,id='tS_t.trans_type5')
    d.enterFormData(False,id='tS_t.trans_type6')

    d.clickElement(name='search')
    
    d.screenshot('search_type')
    
    d.clickElement(name='searchClear')
    
    d.enterFormData('SomeManu Co',id='tS_t.manufacturer')
    
    d.clickElement(name='search')
    
    d.screenshot('search_manu')    

    d.clickElement(name='searchClear')

    d.enterAutocomplete('tS_p_last_name_patac','Hart',0)
    
    d.clickElement(name='search')
    
    d.screenshot('search_patient')

    d.clickElement(name='searchClear')
    
    #d.enterFormData('Hospital',id='tS_t.trans_loc_label')
    
    #d.clickElement(name='search')
    
    #d.screenshot('search_loc')

    #d.clickElement(name='searchClear')
    
    d.navigate(WCURL.INVENTORY,auto_screenshot=False)
    
    d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[1]/tr[14]/td[2]/a[1]")

    d.screenshot('search_item')
    
    d.navigate(WCURL.INVENTORY,auto_screenshot=False)
    
    d.clickElement(xpath="//div[@id='lv_inv_curr_gen_span']/table/tbody[1]/tr[11]/td[5]/a[1]")
    
    d.screenshot('search_lot')
    
