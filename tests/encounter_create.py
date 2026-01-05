# 
# E-Chart Encounter Creation Test

def main (driver, WCURL):
    """
    Dispense a medication
    """

    d = driver

    d.navigate(WCURL.CHART_HART_WILLIAM)
    
    d.clickElement(text='Add Document')

    d.pause(2)
    
    d.screenshot('select_doctype')

    d.clickElement(text='Encounter')

    d.screenshot('select_encountertype')
        
    #d.clickElement(xpath="//div[@id='wc_main']/table[1]/tbody/tr/td/[fieldset]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/fieldset/table/tbody/tr[5]/td[2]/a/font[text()='New']")
    d.clickElement(xpath="//a[text()='Office Visit']/parent::td/following-sibling::td/a")
    
    d.pause(2)

    d.screenshot('add_encounter_dialog')
    
    d.enterFormData('Office Visit-Initial',id='ae_visit_type')
    
    d.clickElement(name='ae_encsubmit')
    
    d.pause(2)
    
    d.screenshot('exam_doc')
    
    d.navigate(WCURL.CHART_HART_WILLIAM + 'v=encounter')
    
    d.clickElement(text='Add Encounter')
    
    d.pause(2)
    
    d.enterFormData('CCR Creation',id='ae_visit_type')
    
    d.clickElement(name='ae_encsubmit')
    
    d.pause(2)
    
    d.screenshot('exam_enc')
