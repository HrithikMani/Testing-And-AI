def main (d, WCURL):
    """ Test for the new 'exit alert' feature of HS panels.
        
    """
    
    d.navigate(WCURL.ADMIN + 't=panels&opp=panel&job=edit&panel_id=OSHA+Noise')
    d.enterFormData('Employees should NOT normally exit this panel.', id='exit_alert')
    d.enterFormData('Testing Exit Alert', id='change_reason')
    d.clickElement(name='submit')

    d.navigate(WCURL.ADMIN + 't=panels&panel_id=OSHA+Noise&opp=panel_membership&job=add_employee')
    d.enterAutocomplete('pat_id_patac', 'Hart, W', 0)
    d.enterFormData('Exit Alert Test', id='change_reason')
    d.clickElement(name='submit')

    d.navigate(WCURL.CHART_HART_WILLIAM + 't=Health+Surveillance%3AHS+Membership&v=dashboard')

    d.clickElement(id='HSPPM_I_OSHA Noise_18_check')
    
    d.screenshot('hs_exit_osha_noise')
    d.clickElement(value='Cancel')

    d.clickElement(id='HSPPM_I_OSHA Noise_18_check')
    d.clickElement(value='Remove')

