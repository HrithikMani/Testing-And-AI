# 
# Webchart Encounter Exams Editor test

def main (driver, WCURL):
    """
    Dispense a medication
    """

    d = driver
    
    d.navigate(WCURL.ENC_EXAMS)
    
    d.clickElement(text='Add Exam')

    d.pause(2)
    
    d.screenshot('add_exam')
    
    d.enterFormData('CCR Creation',id='visit_type')
    d.enterFormData('Office Visit',id='layout_name')
    d.enterFormData('Exam',id='is_view')
    
    d.clickElement(name='exam_save')
    
    d.pause(2)

    d.clickElement(text='Add Exam')

    d.pause(2)

    d.enterFormData('CCR Creation',id='visit_type')
    d.enterFormData('Blank Layout',id='layout_name')
    d.enterFormData('View Office Visit',name='exam_name',clear=True)
    d.enterFormData('View',id='is_view')
    
    d.clickElement(name='exam_save')

    d.pause(2)
    
    d.clickElement(text='Add Exam')

    d.pause(2)
    d.enterFormData('CCR Creation',id='visit_type')
    d.enterFormData('View Office Visit',id='layout_name')
    d.enterFormData('Additional View',id='is_view')
    
    d.clickElement(name='exam_save')

    d.pause(2)
    
    d.screenshot('exam_setup_done')
