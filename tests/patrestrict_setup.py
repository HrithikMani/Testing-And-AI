def main (d, WCURL):
    """
    Add some things to test with. 2 tasks. One on a UHS-partition patient
    and one on a MR-partition patient. Then we'll restrict the UHS partition.
    """
    #
    # Before restricting things add some data
    #
    d.navigate(WCURL.CHART_HART_WILLIAM)
    note = 'This task is always available'
    d.clickElement(text='Add Task')
    d.clickElement(text='Phone Note')
    d.enterFormData(note,id='notes',clear=True)
    d.enterFormData('Physicians',id='le_task_assign_realm_value')
    d.clickElement(value='Add Task')

    d.navigate(WCURL.CHART_TEMP_HART_WILLIAM)
    note = 'This task is available when user has access to partition: HOSPITAL'
    d.clickElement(text='Add Task')
    d.clickElement(text='Phone Note')
    d.enterFormData(note,id='notes',clear=True)
    d.enterFormData('Physicians',id='le_task_assign_realm_value')
    d.clickElement(value='Add Task')



    #
    # Once we have some things to go look at, restrict the system.
    # 
    # Partitions restricted:
    # - HOSPITAL is restricted to dept: Reception/Office
    d.navigate(WCURL.PARTITION_MANAGER + "&opp=edit&partition=UHS")
    d.clickElement(id='part_restrict')
    d.enterFormData('Reception/Office',id='le_pm_allowed_realms_allowed_id_value')
    d.clickElement(value='Change')

    # Security setting:
    # - selenium 
    d.navigate(WCURL.CONTROL_PANEL + "&t=security&opp=esecuser&user_id=8")
    d.enterFormData('1',name='E-Chart_Restrict Access by Partition')
    d.enterFormData('Restrict partition',id='sec_role_comment')
    d.clickElement(value='Update Individual Security')
    
    # System setting: MAYBE LATER
    # - Limit users to Provider Organization


