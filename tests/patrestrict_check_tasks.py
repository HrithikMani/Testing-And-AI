def main (d, WCURL):
    """
    Check that we see the task on the non-restricted patient
    and don't see the restricted one.
    """
    d.navigate(WCURL.TASK_LIST)
    d.verifyElementPresent(True,xpath="//div[@id='lv_tasklist_realm_Physicians_span']//td[text()='This task is always available']")

    d.verifyElementPresent(False,xpath="//div[@id='lv_tasklist_realm_Physicians_span']//td[text()='This task is available when user has access to partition: HOSPITAL']")

