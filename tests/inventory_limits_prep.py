# 
# Webchart Inventory Receive More UnitTest
#

def setAcRow(driver, num, med, mrow, med_full, form, frow, form_full, qty, lot, manu, supplier, m, dy, y):
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
    
    d.enterAutocomplete('inv_lot_id'+num+'_ac', lot, -1)
    
    d.enterAutocomplete('inv_manufac'+num,manu,-1)
    
    d.enterMIEDate('inv_exp_date'+num,m,dy,y)

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
    Receive an assortment of inventory items as preparation for the warning level limits test
    """

    d = driver

    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
    
    d.navigate(WCURL.INVENTORY_RECEIVE)

    setAcRow(d,'0','lisino',0,'lisinopril (New)','tablet 5',0,'tablet 5mg','35','abc123','SomeManu Co','Dem Med Distributers',1,1,15)

    setAcRow(d,'1','lisino',0,'lisinopril (New)','tablet 1',0,'tablet 10mg','125','abc987','SomeManu Co','Dem Med Distributers',6,1,15)

    setAcRow(d,'2','amox',0,'amoxicillin (New)','cap',0,'capsule 500mg','300','npqdl812','AnyMed Inc','QuickMed Co',3,15,14)
    setAcRow(d,'3','las',0,'Lasix (New)','tablet 2',0,'tablet 20mg (Oral)','10','988lwlke','SomeManu Co','QuickMed Co',4,30,14)
    setAcRow(d,'4','las',0,'Lasix (New)','tablet 8',0,'tablet 80mg (Oral)','15','7892oasd','AnyMed Inc','Dem Med Distributors',9,1,13)
    setAcRow(d,'5','diphenhydramine HCL',0,'diphenhydramine HCl (New)','capsule 25',0,'capsule 25mg (Oral)','200','afosidl1198','Medique','QuickMed Co',5,5,15)
    if d.getAttribute('value',id='inv_medication_id5') != '238770':
        d.enterAutocomplete('inv_formac5', 'capsule 25', 0, 'capsule 25mg')
    setAcRow(d,'6','japan',0,'japanese enceph vaccine (PF) (New)','s',0,'Syringe 6mcg/0.5 mL','12','djf113921','Ixiaro','QuickMed Co',6,15,14)

    inventory_failure=False
    if not verifyRow(d,'0','HOSP','1','268801'):
        inventory_failure=True
    if not verifyRow(d,'1','HOSP','1','244899'):
        inventory_failure=True
    if not verifyRow(d,'2','HOSP','1','152729'):
        inventory_failure=True
    if not verifyRow(d,'3','HOSP','1','237799'):
        inventory_failure=True
    if not verifyRow(d,'4','HOSP','1','153306'):
        inventory_failure=True
    if not verifyRow(d,'5','HOSP','1','238770'):
        inventory_failure=True
    if not verifyRow(d,'6','HOSP','1','558948'):
        inventory_failure=True

    if not inventory_failure:
        d.clickElement(id='recvMeds')
    else:
        d.setUserData('inventory_failure',True)
