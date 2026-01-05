# 
# Webchart Injection Add UnitTest

def main (driver, WCURL):
    """
    Add a basic injection record
    """

    d = driver

    d.wcutils.SetPermission("E-Chart","Document Permissions","0",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Use Contraindications","0",False)
    d.wcutils.SetSystemSetting("E-Chart","CHIRP","Use Chirp","0",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Additional Warning Fields","",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Additional Warning Message","",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Patient Required Fields","",False)
  
    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT,auto_screenshot='noperms')

    d.wcutils.SetPermission("E-Chart","Document Permissions","2",True)
    d.screenshot('hasperm')
  
    d.clickElement(text='Add Inj/Imm')
    d.pause(2)
    d.screenshot('adddialog')
    
    d.enterAutocomplete('description_ac','Hep A',0,'Hep A, adult')
    d.enterFormData('Office',id='service_location')
    d.enterMIEDate('service_date',5,1,2006)
    d.enterFormData('IM',id='route')
    d.enterFormData('RA',id='site')
    d.enterAutocomplete('doseac','10',-1,'10')
    d.enterAutocomplete('strengthac','1',-1,'1')
    d.enterAutocomplete('manufacturer_ac_inject_manufact','MedI',0,'MedImmune, Inc.')
    d.enterFormData('ABC1239',id='vial')
    d.enterMIEDate('expiration_date',5,1,2015)
    d.enterFormData('I am a comment!',id='reaction')
    
    d.clickElement(value='Submit')
    d.pause(2)
    d.screenshot('injection_added')

    d.wcutils.SetSystemSetting("E-Chart","Injections","Use Contraindications","1",False)

    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT,auto_screenshot='contra_view')

    d.clickElement(text='Add Inj/Imm')
    d.pause(2)
    d.screenshot('contra_adddialog')
    
    d.enterAutocomplete('description_ac','IPV',0,'IPV')
    d.enterFormData('Parent or Patient Refusal: Personal',id='contraindication')
    d.enterMIEDate('service_date',5,1,2006)
    d.enterFormData('Makes me sneeze!',id='reaction')
    
    d.screenshot('contra_add')
    
    d.clickElement(value='Submit')
    d.pause(2)
    d.screenshot('contraindication_added')
    
    lv = d.getMIEListview('Immunizations','Injection')
    if lv:
        lv.clickCell('Hep A, adult','Injection','Hep A, adult')
        d.pause(3)
        d.screenshot('edit_load')
        
    

