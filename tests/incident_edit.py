def main (d, WCURL):
    """
        Edit an incident from the stand alone screen
    """
    d.navigate(WCURL.CHART_HART_WILLIAM + 'v=encounter')
    d.clickElement(xpath="//div[@id='lv_showpatientencounters_span']//a[text()='Exam']")

    d.clickElement(xpath="//div[@id='lv_pat_inclv_span']//span[text()='Edit']")
    # Confirm that the encounter has been saved
    d.closeAlert(accept=True)

    d.switchToPopup()
    d.screenshot()

    d.clickElement('DII_verified_Yes')

    d.clickElement(value='Save')

    d.screenshot()
    d.closePopup()
