# 
# E-Chart Encounter Archival Test

def main (driver, WCURL):
    """
    Dispense a medication
    """

    d = driver

    d.navigate(WCURL.CHART_HART_WILLIAM + 'v=encounter&encopp=exam&enc_lay_id=View+Office+Visit&encounter_id=64&set_curr_enc=64',auto_screenshot='encounter_view_doc') 
    d.clickElement(text='Archive and Close Encounter')
    
    d.pause(2)

    d.screenshot('archived_from_doc')
    
    d.navigate(WCURL.CHART_HART_WILLIAM + 'v=encounter&encopp=exam&enc_lay_id=Blank+Layout&encounter_id=65&set_curr_enc=65',auto_screenshot='encounter_view_enc')
   
    d.screenshot('archived_from_enc')
