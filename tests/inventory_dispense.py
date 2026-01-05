# 
# Webchart Inventory Dispense UnitTest

def main (driver, WCURL):
    """
    Dispense a medication
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return

    d.wcutils.SetPermission("Inventory","Fill Prescriptions","0",False)
    d.wcutils.SetPermission("Inventory","View Inventory","0",False)

    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.DISPENSE)
    d.screenshot('noperm')

    d.wcutils.SetPermission("Inventory","View Inventory","1",True)

    d.screenshot('viewperm')

    d.wcutils.SetPermission("Inventory","Fill Prescriptions","2",True)

    d.screenshot('hasperm')
    
    d.clickElement(id='pap_51')
    d.clickElement(id='pap_61')
    d.clickElement(value='Update PAP Applications')
    d.pause(2)
    
    d.screenshot('pap_submitted')
    
    d.clickElement(id='pap_51')
    d.clickElement(value='Update PAP Applications')
    d.pause(2)
    
    d.screenshot('pap_remove')
    
    
    d.clickElement(xpath="//div[@id='lv_inv_disp_span']/table/tbody[1]/tr[3]/td[11]/a[text()='Fill From General']")
    

    d.screenshot('fill_dialog')
    
    d.enterFormData('Office',id='disp_transloc')
    
    d.enterAutocomplete('disp_invac', 'lisi', 0, 'lisinopril 5 mg tablet qty: 46')
    d.clickElement(value='Close')
    
    d.enterFormData('50',id='disp_quantity')
    
    d.enterAutocomplete('disp_lot_id_ac', 'abc', 0, 'abc123 (SomeManu Co 01-01-2030) qty: 46')
    
    d.verifyAttribute('value', 'SomeManu Co', id='disp_manufacturer')
    d.verifyAttribute('value', '01', id='disp_exp_dateMONTH')
    d.verifyAttribute('value', '01', id='disp_exp_dateDAY')
    d.verifyAttribute('value', '2030', id='disp_exp_dateYEAR')
    
    d.verifyAttribute('value', '25', id='disp_equiv')

    d.clickElement(value='Clear')
    
    
    d.enterFormData('Hospital',id='disp_transloc')
    d.enterFormData('n/a',id='disp_stockpile_id')
    
    d.enterAutocomplete('disp_invac', 'lisi', 0, 'lisinopril 10 mg tablet qty: 30')
    d.clickElement(value='Close')
    
    d.enterFormData('25',id='disp_quantity')
    
    d.enterAutocomplete('disp_lot_id_ac', '987', 0, '987xzy (MediPill Co 06-01-2030) qty: 30')
    
    d.verifyAttribute('value', 'MediPill Co', id='disp_manufacturer')
    d.verifyAttribute('value', '06', id='disp_exp_dateMONTH')
    d.verifyAttribute('value', '01', id='disp_exp_dateDAY')
    d.verifyAttribute('value', '2030', id='disp_exp_dateYEAR')
    
    d.verifyAttribute('value', '25', id='disp_equiv')
    
#    d.clickElement(value='Clear')
    
    
#    d.enterFormData('Hospital',id='disp_transloc')
#    d.enterFormData('Store Room A',id='disp_stockpile_id')
        
#    d.enterAutocompleteNew('disp_invac', 'lisi', 2, 'lisinopril 20 mg tablet qty: 15') -- autocomplete's .src is not being updated by disp_stockpile_id's onblur. fixme and then uncomment the other test steps
#    d.clickElement(value='Close')
 
#    d.enterFormData('12.5',id='disp_quantity')
   
#    d.enterAutocompleteNew('disp_lot_id_ac', 'axy', 0, 'axy391 (MediPill Co 03-15-2015) qty: 15')
    
#    d.verifyAttribute('value', 'MediPill Co', id='disp_manufacturer')
#    d.verifyAttribute('value', '06', id='disp_exp_dateMONTH')
#    d.verifyAttribute('value', '01', id='disp_exp_dateDAY')
#    d.verifyAttribute('value', '2015', id='disp_exp_dateYEAR')
    
#    d.verifyAttribute('value', '25', id='disp_equiv')
    
    
#    d.enterAutocompleteNew('disp_sig_ac_sig', '0.5 tabs qd', -1, '0.5 tabs qd') -- this is the correct sig when dispensing 20mg tablets
    d.enterAutocomplete('disp_sig_ac_sig', '1 tabs qd', -1, '1 tabs qd')
    
    # enterFormData treats the string 'selenium' as a temporary file, so we have to break it up in order to enter it into a text box
    d.enterFormData(d.getUserData('username')[0:2],id='userDispName')
    d.enterFormData(d.getUserData('username')[2:],id='userDispName',clear=False)
    d.enterFormData(d.getUserData('password')[0:2],id='userDispPass')
    d.enterFormData(d.getUserData('password')[2:],id='userDispPass',clear=False)

    d.clickElement(name='save')
    
    d.screenshot('success')
    
    if d.switchToPopup():
    
#        d.clickElement(id='lbl_3warning2') -- this is the correct id when dispensing 20mg tablets
        d.clickElement(id='lbl_2warning2')
    
#        d.clickElement(id='lbl_3aka1') -- this is the correct id when dispensing 20mg tablets
        d.clickElement(id='lbl_2aka1')
    
        d.screenshot('label_warnings')
    
        d.clickElement(name='printLbl')
    
        d.screenshot('label')
    
        d.closePopup()
