def main(d, WCURL):
    d.navigate(WCURL.CHART_HART_WILLIAM, auto_screenshot=False)

    d.clickElement(id='new_user')
    d.pause(3)
    d.screenshot('dialog_open')
