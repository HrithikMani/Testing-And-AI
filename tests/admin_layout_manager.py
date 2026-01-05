def main (d, WCURL):
    """
    Verifies that the layout manager is functioning correctly.
    Adds a new layout named Selenium, verifies that it appears in
    the search and then deletes it.
    """
    #$ Layout Permissions
    d.wcutils.SetPermission("Control","Manage Layouts","0",False)
    d.wcutils.SetPermission("Control","Manage System Layouts","0",False)
    d.navigate(WCURL.LAYOUT_MANAGER)
    d.screenshot('NoPerm')

    d.wcutils.SetPermission("Control","Manage Layouts","1",False)
    d.wcutils.SetPermission("Control","Manage System Layouts","1",False)
    d.navigate(WCURL.LAYOUT_MANAGER)
    d.screenshot('WithPerm')

    #$ Layout Add
    d.clickElement(text='Add Layout')
    module = 'Selenium'
    name = 'Selenium'
    dt = 'Sleep Study'
    comment = 'This is a new layout from selenium'
    html = 'I am a layout created from a selenium test'
    d.enterFormData(module,id='module')
    d.enterFormData(name,id='name')
    d.enterFormData(dt,id='doc_type')
    d.enterFormData(comment,id='change_comment')
    d.runJS('layout_editor.setValue("'+html+'");')
    d.screenshot('add_dialog')
    d.clickElement(value='Save & Close')

    #$ Search
    d.enterFormData('selenium test', id='search_for')
    d.enterFormData(True,id='search_html')
    d.clickElement(value='Go')
    d.screenshot('BasicSearch')
    
    d.clickElement(text='Advanced')
    d.enterFormData(module,id='src_module')
    d.enterFormData(name,id='src_name')
    d.enterFormData(comment,id='src_change_comment')
    d.enterFormData(dt,id='src_doc_type')
    d.enterFormData(html,id='src_layout_html')
    d.clickElement(value='Search')
    d.screenshot('AdvancedSearch')

    #$ Edit
    d.clickElement(xpath="//div[@id='lv_layout_manager_span']//td[text()='%s']/parent::tr//a[text()='Edit']" %comment)
    comment = 'Selenium Edited'
    d.enterFormData(comment,id='change_comment',clear=True)
    d.screenshot('edit_dialog')
    d.clickElement(value='Save & Close')
    d.screenshot('Edited')

    #$ De-Activate
    d.enterFormData(comment,id='src_change_comment',clear=True)
    d.clickElement(value='Search')
    d.clickElement(xpath="//div[@id='lv_layout_manager_span']//td[text()='%s']/parent::tr//a[text()='Set In-Active']" %comment)
    d.clickElement(value='Yes')
    d.enterFormData(name, id='search_for')
    d.clickElement(value='Go')
    d.screenshot('NotShowingInactiveLayouts')

    #$ Re-activate
    d.clickElement(text='Show In-Active')
    d.clickElement(xpath="//div[@id='lv_layout_manager_span']//td[text()='%s']/parent::tr//a[text()='Set Active']" %comment)
    d.clickElement(value='Yes')
    d.screenshot('ReActivated')
    d.enterFormData(name, id='search_for')
    d.clickElement(value='Go')
    d.screenshot('LayoutActive')
    
    #$ Delete
    d.clickElement(xpath="//div[@id='lv_layout_manager_span']//td[text()='%s']/parent::tr//a[text()='Delete']" %comment)
    d.screenshot('Layout Delete Confirm')
    d.clickElement(value='Yes')

    #$ Editing System Layout
    d.navigate(WCURL.LAYOUT_MANAGER_SYSTEM)
    d.screenshot('SysLayout')
