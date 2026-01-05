# 
# Webchart Partition Manager UnitTest
#
def main (d, WCURL):
    """
    Add a partition, then update existing partitions
    """

    d.navigate(WCURL.PARTITION_MANAGER)
    d.screenshot('part_manager_origin')
    lv = d.getMIEListview('Partition Manager', 'Partition')
    if lv:
        lv.clickCell('Edit', 'Options', 'CCME')
        d.enterFormData('R', id='echart_opts')
        d.clickElement(name='change_btn')


    lv = d.getMIEListview('Partition Manager', 'Partition')
    if lv:
        lv.clickCell('Edit', 'Options', 'MIE')
        d.enterFormData('X', id='echart_opts')
        d.clickElement(name='change_btn')

    lv = d.getMIEListview('Partition Manager', 'Partition')
    if lv:
        lv.clickCell('Edit', 'Options', 'MR')
        d.enterFormData('A', id='echart_opts')
        d.clickElement(name='change_btn')

    lv = d.getMIEListview('Partition Manager', 'Partition')
    if lv:
        lv.clickCell('Edit', 'Options', 'NMC')
        d.enterFormData('P', id='echart_opts')
        d.clickElement(name='change_btn')

    d.screenshot('part_manager_updated')
    if d.clickElement(xpath="//div[@id='wc_main']/div/a[2][text()='Add Partition']"):
        d.screenshot('part_manager_add')
        d.enterFormData('TP', id='partition')
        d.enterFormData('TP', id='name')
        d.enterFormData('Test Partition', id='description')
        d.enterFormData('A', id='echart_opts')
        d.clickElement(name='save_btn')
        d.screenshot('part_manager_success')
