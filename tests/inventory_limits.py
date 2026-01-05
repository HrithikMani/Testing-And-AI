# 
# Webchart Inventory Stock Levels UnitTest
#

def main (driver, WCURL):
    """
    Dispense a medication
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return

    d.wcutils.SetPermission("Inventory","Manage Stock Warning Levels","0",False)

    d.navigate(WCURL.INVENTORY_LIMITS_MANAGER,auto_screenshot=False)
    d.screenshot('noperm')

    d.wcutils.SetPermission("Inventory","Manage Stock Warning Levels","1",True)

    d.screenshot('viewperm')

    d.wcutils.SetPermission("Inventory","Manage Stock Warning Levels","4",True)

    d.screenshot('editperm')
    
    d.enterFormData('HOSP',id='srch_transloc0')
    d.enterFormData('1',id='srch_stockpile_id0')
    d.clickElement(id='search')
    
    d.clickElement(text='Manage Levels')
    
    d.enterFormData('All',id='srch_set0')
    d.clickElement(id='search')
    
    d.screenshot('manage_start')
    
    d.clickElement(id='items_link_1')
    d.clickElement(id='items_link_2')
    d.clickElement(id='items_link_3')
    
    d.clickElement(id='allow_high_4')
    
    d.enterFormData('10',id='value_low_2',clear=True)
    
    d.enterFormData('250',id='value_high_4',clear=True)
    
    d.screenshot('limits_set')
    
    d.clickElement(id='save')
    
    d.screenshot('limits_saved')
    
    d.enterAutocomplete('srch_invac0','amox',0,'amoxicillin 500 mg capsule qty: 300')
    d.clickElement(id='search')

    d.screenshot('filter_by_item')
    
    d.enterAutocomplete('srch_invac0','',-1,'')
    d.clickElement(id='search')

    d.clickElement(xpath="//div[@id='lv_isl_list_span']/table/tbody[1]/tr[2]/td[1]/a[1][text()='lisinopril 10 mg tablet']")
    
    d.screenshot('manage_lisinopril10')
    
    d.enterAutocomplete('srch_invac0','',-1,'')
    
    d.enterFormData('No',id='srch_set0')
    d.clickElement(id='search')
    
    d.screenshot('manage_limits_no')
    
    d.enterFormData('Yes',id='srch_set0')
    d.clickElement(id='search')
    
    d.screenshot('manage_limits_yes')
    
    d.enterFormData('All',id='srch_set0')
    d.clickElement(id='search')
    
    d.screenshot('manage_limits_all')
    
