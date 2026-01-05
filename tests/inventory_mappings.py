# 
# Webchart Inventory Item Mapping UnitTest

def main (driver, WCURL):
    """
    Add Mappings to inventory items
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
  
    d.wcutils.SetPermission("Inventory","Edit Inventory Mappings","0",False)
    d.wcutils.SetPermission("Inventory","Merge Inventory Items","0",False)
    d.wcutils.SetPermission("Inventory","View Inventory","0",False)

    d.navigate(WCURL.INVENTORY_MAPPINGS,auto_screenshot=False)
    d.screenshot('noperms')

    d.wcutils.SetPermission("Inventory","View Inventory","1",True)
    d.screenshot('hasperm')

    d.wcutils.SetPermission("Inventory","Edit Inventory Mappings","1",True)
    d.screenshot('manageperm')

    d.wcutils.SetPermission("Inventory","Merge Inventory Items","1",True)
    d.screenshot('mergeperm')
    
    d.enterFormData('Medication',id='map_type',blur=False)

    d.clickElement(text='Add a Mapping')
        
    d.pause(2)
    
    d.screenshot('add_medication')
    
    d.enterAutocomplete('medac','multivitamin',0,'multivitamin (New)')
    d.pause(2)
    d.enterAutocomplete('formac','tablet',0,'tablet  (Oral)')
    
    d.enterAutocomplete('inv_ac','multi',0,'Multi-Vitamin')
    
#    d.pause(2)
# don't take this screenshot. the forms autocomplete can't decide if it should be showing the choices div or not
#    d.screenshot('medication_chosen')

    d.clickElement(name='save')

    d.screenshot('medication_mapped')
    
    d.clickElement(name='cancel')
    
    d.enterFormData('Injection',id='map_type',blur=False)
    
    d.clickElement(text='Add a Mapping')
    
    d.screenshot('add_injection')
    
    d.enterAutocomplete('injac','dtap',0,'DTaP')
    d.enterAutocomplete('inv_ac','dtap',0,'DTAP')
    
    d.clickElement(name='save')
    
    d.enterAutocomplete('injac','MMR',0,'MMR')
    d.enterAutocomplete('inv_ac','MMR',0,'MMR Vaccine')
    
    if not d.getAttribute('value',id='injac_txt') == 'MMR' or not d.getAttribute('value',id='mapped_id') == '03':
        d.enterAutocomplete('injac','MMR',0,'MMR')

    # The AC likes to select M/R instead of MMR, so make sure that if it did, we don't continue on getting diffs/failures        
    if not d.verifyAttribute('value','03',id='mapped_id'):
        d.setUserData('inventory_failure',True)
        return
 
# not really needed. was useful for debug       
#    d.screenshot('injection_chosen')
    
    d.clickElement(name='save')

    d.enterAutocomplete('injac','japan',0,'Japanese Encephalitis IM')
    d.enterAutocomplete('inv_ac','japan',0,'japanese encephalitis vaccine (PF) 6 mcg/0.5 mL IM Syringe')
    
    d.clickElement(name='save')

    d.screenshot('injections_mapped')

    d.clickElement(name='cancel')
    
    d.miedb.dbExec("INSERT INTO order_list SET name='Crutches 48 inches'")
    d.miedb.dbExec("INSERT INTO order_list SET name='Crutches 60 inches'")
        
    d.enterFormData('Order',id='map_type',blur=False)
    
    d.clickElement(text='Add a Mapping')
    
    d.pause(2)
    
    d.screenshot('add_order')
    
    d.enterAutocomplete('orderac','crutches 48',0,'Crutches 48 inches')
    d.enterAutocomplete('inv_ac','crutch',0,'Crutches (Crutches 48")')
    
# not really needed. was useful for debug       
#    d.screenshot('order_chosen')
    
    d.clickElement(name='save')
    
    d.enterAutocomplete('orderac','crutches 60',0,'Crutches 60 inches')
    d.enterAutocomplete('inv_ac','crutch',1,'Crutches (Crutches 60")')
    
    d.clickElement(name='save')
    
    d.screenshot('orders_mapped')
    
    d.clickElement(name='cancel')
    
    d.enterFormData('Barcode',id='map_type',blur=False)
    
    d.clickElement(text='Add a Mapping')
    
    d.pause(2)
    
    d.enterFormData('208357236152',id='barcode_value')
    d.enterAutocomplete('inv_ac','crutch',0,'Crutches (Crutches 48")')
    
    d.screenshot('add_barcode')

    d.clickElement(name='save')

    d.enterFormData('347682184476',id='barcode_value')
    d.enterAutocomplete('inv_ac','diphenhydramine',0,'diphenhydramine 25 mg capsule')
    
    d.clickElement(name='save')

    d.enterFormData('4251500101001',id='barcode_value')
    d.enterAutocomplete('inv_ac','japan',0,'japanese encephalitis vaccine (PF) 6 mcg/0.5 mL IM Syringe')
    
    d.clickElement(name='save')
    
    d.screenshot('barcode_mapped')
    
    d.clickElement(name='cancel')

    d.enterFormData('Medication',id='map_type',blur=False)
    
    d.clickElement(id='multiSearchLink')
    d.screenshot('search_multi')
    
    d.clickElement(id='tS_searchBy0_0')
    d.enterFormData('lisinopril',id='tS_searchVal0')
    d.clickElement(id='tS_searchBy1_0')
    d.enterFormData('lasix',id='tS_searchVal1')
    d.clickElement(id='search')
    
    d.screenshot('search_multi_result')
    
    d.clickElement(id='searchClear')
    
    d.screenshot('search_cleared')
    
    # switch back from multi/single search options
    d.clickElement(id='multiSearchLink')
    d.screenshot('search_single')
    
    d.clickElement(id='tS_searchBy0_2')
    d.enterFormData('5',id='tS_searchVal0')
    d.clickElement(id='search')

    d.clickElement(id='multiSearchLink')
    
    d.screenshot('search_by_id')

