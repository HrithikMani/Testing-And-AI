# 
# Webchart Patient Search by date-of-birth  Test
#

def main (d, WCURL):

    d.navigate(WCURL.PAT_SEARCH_DETAIL)
    d.screenshot('pat_search_detail')
    d.enterFormData('e', id='bdate_crit')
    d.enterFormData('03-09-1943', id='start_bdate')
    d.enterFormData('all', name='partition')
    d.clickElement(name='pat_search')
    d.screenshot('pat_search_dob_no_time')

    d.navigate(WCURL.PAT_SEARCH_DETAIL)
    d.enterFormData('e', id='bdate_crit')
    d.enterFormData('all', name='partition')
    d.enterFormData('06-17-2001', id='start_bdate')
    d.clickElement(name='pat_search')
    d.screenshot('pat_search_dob_has_time')

