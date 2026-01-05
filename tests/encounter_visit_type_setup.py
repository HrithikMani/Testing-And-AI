# 
# Webchart Encounter Visit Types Editor Test

def main (driver, WCURL):
    """
    Dispense a medication
    """

    d = driver

    d.navigate(WCURL.ENC_TYPES)
    
    d.clickElement(text='Add Visit Type')

    d.pause(2)
    
    d.screenshot('add_visit_type')
    
    d.enterFormData('CCREXAM',id='visit_type')
    d.enterFormData('CCR Creation',id='description')
    d.enterFormData('CCR',name='cda_template')
    
    d.clickElement(name='vt_save')
    
    d.pause(2)
    
    d.screenshot('visit_types_list')
    