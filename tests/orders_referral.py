def orderTest(driver,WCURL,referral_note,order_dialog_ssname,order_doc_id):
    """
    Perform the steps for setting up a Referral Order.
    Tests functionality for https://pm.mieweb.com/issues/19415
    """
    
    d = driver

    d.navigate(WCURL.ENCOUNTER_HART_WILLIAM)
    lv = d.getMIEListview('Encounters','Enc ID')
    if lv == None:
        return
    
    lv.clickCell('Office Visit-Initial','Options','11')
    
    d.pause(5)
    d.clickElement(text='Create Referral Order')
    d.pause(5)
    
    d.enterAutocomplete('ref_user_ac_create','sample',0,'Sample, John M. ( Fort Wayne, IN United States 46804 - 6302 Constitution Drive  )')
    
    d.enterFormData(referral_note,id='comments')
    d.clickElement(id='order_id_2414_REFERRAL_697_0')
    
    d.screenshot(order_dialog_ssname)
    
    d.clickElement(value='Request Orders')
    
    d.clickElement(value='Finish')
    
    d.clickElement(value='Save Incomplete')
    
    d.navigate(WCURL.DOCUMENT_HART_WILLIAM+'doc_id='+order_doc_id)

def main (d, WCURL):
    """
    Test CDA archiving of Referral Orders
    """

    if d.browser == WCURL.BROWSER_IE:
        return

    d.navigate(WCURL.ACCESS_CONTROL)
    d.enterFormData('sample',id='search')
    d.clickElement(id='finduser')
    
    d.pause(2)
    
    lv = d.getMIEListview('WebChart Users','Username')
    if lv == None:
        return
    lv.clickCell('Edit','Options','jsample')
    d.pause(2)
    
    d.enterFormData('Referring Physician',id='user_role_id')
    
    d.clickElement(value='Submit Edit')
    
    orderTest(d,WCURL,'Unused Referral Notes','order_creation','491')
    
    d.clickElement(text='Properties')
    
    d.screenshot('no_cda_attachment')
    
    d.wcutils.SetSystemSetting("Orders","Settings","Referral Doc Type","ORDREF",False)

    orderTest(d,WCURL,'Custom Referral Notes','order_creation_to_be_xml','491')
    
    d.clickElement(text='Properties')
    
    d.clickElement(xpath="//a/font[contains(text(), 'CDA Document')]")
    
    if d.switchToPopup():
        #d.screenshot('xml_output')
        #d.runJS("return document.getElementsByTagName('text')[1].textContent==='\\nCustom Referral Notes'")
        
        d.closePopup()
    
