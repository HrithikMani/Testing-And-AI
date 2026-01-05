# 
# E-Chart Encounter Creation Test

def main (d, WCURL):
    """
    Dispense a medication
    """
    d.miedb.dbExec("INSERT INTO layout SET module='E-Chart',name='EncounterAddDropin',active=1,create_date='2007-02-02 09:15:00',revision_date='2007-02-02 09:15:00',layout_html='<b>Boo!</b>'")
    
    d.navigate(WCURL.CHART_HART_WILLIAM + 'v=encounter')
    
    d.clickElement(text='Add Encounter')
    
    d.pause(2)
        
    d.screenshot('add_custom')

    d.miedb.dbExec("""REPLACE INTO layout SET module='E-Chart',name='EncounterAddDropin',active=1,create_date='2007-02-02 09:15:00',revision_date='2007-02-02 09:15:00',layout_html='<b>Boo!</b><WCPRIVATEDATASET NAME="ENC_MANAGE_DISPLAY_LIST" VALUE="1">'""")
    
    d.navigate(WCURL.CHART_HART_WILLIAM + 'v=encounter')
    
    d.clickElement(text='Add Encounter')
    
    d.pause(2)
        
    d.screenshot('add_custom_with_list')
