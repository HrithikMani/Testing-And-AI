# 
# Webchart Injection Extended Add UnitTest

def main (driver, WCURL):
    """
    Add an injection record with immunization registry options enabled
    """

    d = driver

    d.navigate(WCURL.DOCUMENT + 'doc_id=493&opp=properties' ,auto_screenshot='properties')

    d.clickElement(text='Export as VXU')
    d.pause(2)
    d.screenshot('export_initial')
    
    d.enterFormData('MIE',id='partition')
    
    d.clickElement(id='adv_opt_expand')
    # this input defaults to the system handle. clear it before taking the screenshot
    d.enterFormData('',id='hl7_sending_facility',clear=True)
    d.screenshot('expanded')
    
    d.clickElement(value='Generate VXU')
    d.pause(2)
    # this input defaults to the system handle. clear it before taking the screenshot
    d.enterFormData('',id='hl7_sending_facility',clear=True)
    d.screenshot('VXU_error')
    
    d.miedb.dbExec("UPDATE translate SET trans_to='SKB' where name='WebChart Testing System-manufacturer' and trans_from='SKB'")
    
    d.clickElement(value='Generate VXU')
    d.pause(2)
    # this input defaults to the system handle. clear it before taking the screenshot
    d.enterFormData('',id='hl7_sending_facility',clear=True)
    d.screenshot('VXU_success')
