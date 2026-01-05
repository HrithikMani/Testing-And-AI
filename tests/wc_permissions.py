# 
# Webchart Permissions UnitTest
#
def main (driver, WCURL):
    d = driver
    d.navigate(WCURL.CONTROL_PANEL)
    d.clickElement(text='Access Control')
    d.enterFormData('selenium',id='search')
    d.clickElement(value='Go!')
    d.clickElement(text='Edit')
    d.clickElement(text='Customize User Security')

    # Add system report access
    d.enterFormData('Add/Edit',name='Control_Manage System Reports')
    # And system layout access
    d.enterFormData('Yes',name='Control_Manage System Layouts')
    # delete mrns
    d.enterFormData('Yes',name='E-Chart_Delete Patient MRs')

    d.enterFormData('Changed so that Selenium can perform tests on multiple modules',id='sec_role_comment')
    d.clickElement(value='Update Individual Security')
