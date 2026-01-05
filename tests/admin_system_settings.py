# The wcnow_install script does NOT reset the system_settings table
# So I am not basing any locators on default settings, I am simply
# assuming it starts turned off, I turn it on, then back off again
def main(d, WCURL):
    """
    Ensures the editor for system settings is working correctly by
    enabling and then disabling the setting for MIEMessenger,
    'Enable Messenger'
    """
    d.navigate(WCURL.SYSTEM_SETTINGS, auto_screenshot=True)

    #d.clickElement(text='Show All')
    #d.screenshot('Used System Settings')

    d.enterFormData('c',id='select_criteria')
    d.enterFormData('messenger',id='select_text')
    d.clickElement(value='Go')

    d.clickElement(xpath="//td[text()='Enable Messenger']/parent::tr//a[text()='Edit']")
	

    reason = 'Turned on MIEMessenger from a selenium test for system setting check'
    d.enterFormData('1',name='value',clear=True)
    d.enterFormData(reason,name='reason',clear=True)
    d.clickElement(value='Change')

    d.clickElement(xpath="//td[contains(text(),'%s')]/parent::tr//a[text()='Edit']" %reason)
    d.enterFormData('0',name='value',clear=True)
    d.enterFormData('Turned off by selenium',name='reason',clear=True)
    d.clickElement(value='Change')
