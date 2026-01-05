# 
# Webchart Injection Add UnitTest

def main (d, WCURL):
    """
    Verify Add Injection layout can be replaced by custom layout
    """

    #$ Layout Add
    d.wcutils.SetPermission("Control","Manage Layouts","1",False)
    d.wcutils.SetPermission("Control","Manage System Layouts","1",False)
    d.navigate(WCURL.LAYOUT_MANAGER)

    d.clickElement(text='Add Layout')
    module = 'injections'
    name    = 'Dialog'
    dt      = 'None'
    comment = 'This is a new layout with new default name to make the Add Injection screen a layout'
    html    = ("""<WCTABLE TYPE="narrow" TITLE="Patient Information">""",
               """<WCTR><WCTD CELLTYPE="field">First Name</WCTD>""",
               """<WCTD><WCPATDATAENTRY FIELD="first_name"/></WCTD></WCTR>""",
               """<WCTR><WCTD CELLTYPE="field">Middle Name</WCTD>""",
               """<WCTD><WCPATDATAENTRY FIELD="middle_name"/></WCTD></WCTR>""",
               """<WCTR><WCTD CELLTYPE="field">Last Name</WCTD>""",
               """<WCTD><WCPATDATAENTRY FIELD="last_name"/></WCTD></WCTR>""",
               """<WCTR><WCTD CELLTYPE="field">Mother Maiden Name</WCTD>""",
               """<WCTD><WCPATDATAENTRY FIELD="mother_maiden_name"/></WCTD></WCTR>""",
               """</WCTABLE>""",
               """<WCPATINJADD NAME="allinj" SHOW_NEXT_DUE="0" NO_WIDGET="1">""")

    d.enterFormData(module,id='module')
    d.enterFormData(name,id='name')
    d.enterFormData(dt,id='doc_type')
    d.enterFormData(comment,id='change_comment')
    d.runJS("layout_editor.setValue('%s');" % ''.join(html))
    d.clickElement(value='Save & Close')

    #$ Add basic injection record - using new layout

    d.wcutils.SetPermission("E-Chart","Document Permissions","2",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Use Contraindications","0",False)
    d.wcutils.SetSystemSetting("E-Chart","CHIRP","Use Chirp","0",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Additional Warning Fields","",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Additional Warning Message","",False)
    d.wcutils.SetSystemSetting("E-Chart","Injections","Patient Required Fields","",False)
  
    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT)
  
    d.clickElement(text='Add Inj/Imm')
    d.pause(2)
    d.screenshot('adddialog')
    
    d.enterAutocomplete('description_ac','Hep C',0,'Hep C')
    d.enterFormData('Office',id='service_location')
    d.enterMIEDate('service_date',4,23,2006)
    d.enterFormData('IM',id='route')
    d.enterFormData('RA',id='site')
    d.enterAutocomplete('doseac','10',-1,'10')
    d.enterAutocomplete('strengthac','1',-1,'1')
    d.enterAutocomplete('manufacturer_ac_inject_manufact','MedI',0,'MedImmune, Inc.')
    d.enterFormData('ABC9876',id='vial')
    d.enterMIEDate('expiration_date',5,1,2015)
    d.enterFormData('I am a comment!',id='reaction')

    d.enterFormData('Phillips',id='DPI_mother_maiden_name', clear=True)
    
    d.clickElement(value='Submit')
    d.pause(2)
    d.screenshot('injection_added')

    d.wcutils.SetSystemSetting("E-Chart","Injections","Use Contraindications","1",False)

    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT, auto_screenshot='contra_view')

    d.clickElement(text='Add Inj/Imm')
    
    d.enterAutocomplete('description_ac','IPV',0,'IPV')
    d.enterFormData('Parent or Patient Refusal: Personal',id='contraindication')
    d.enterMIEDate('service_date',4,23,2006)
    d.enterFormData('Makes me sneeze!',id='reaction')
    
    d.screenshot('contra_add')
    
    d.clickElement(value='Submit')
    d.pause(2)
    d.screenshot('contraindication_added')
    
    lv = d.getMIEListview('Immunizations','Injection')
    if lv:
        lv.clickCell('Hep C','Injection','Hep C')
        d.pause(3)
        d.screenshot('edit_load')
   
    d.navigate(WCURL.LAYOUT_MANAGER)
    d.clickElement(text='Advanced')
    d.enterFormData(module,id='src_module')
    d.enterFormData(name,id='src_name')
    d.enterFormData(comment,id='src_change_comment')
    d.enterFormData(dt,id='src_doc_type')
    d.enterFormData(html,id='src_layout_html')
    d.clickElement(value='Search')

    d.clickElement(xpath="//div[@id='lv_layout_manager_span']//td[text()='%s']/parent::tr//a[text()='Delete']" %comment)
    d.clickElement(value='Yes')


