def main (d, WCURL):
    """
    Complete an order 
    """
    if d.browser == WCURL.BROWSER_IE:
        return

    hart_recent_orders = WCURL.CHART_HART_WILLIAM + WCURL.RECENT_ORDERS
    d.navigate(hart_recent_orders, auto_screenshot=False)

    d.clickElement(id='complete_req_15_link_3')

    d.screenshot(filename='complete_page')
    d.clickElement(xpath='//font/input[@type="radio" and @name="completed_204" and @value="-1"]')
    d.enterMIEDate(id='completed_dt_204', month=3, day=24, year=2012, time=-1)
    d.enterMIEDate(id='completed_dt_213', month=3, day=24, year=2012, time=-1)
    d.enterMIEDate(id='completed_dt_347', month=3, day=24, year=2012, time=-1)
    d.enterMIEDate(id='completed_dt_2260', month=3, day=24, year=2012, time=-1)
    
    d.clickElement(xpath='//input[@type="submit" and @name="complete_order" and @value="Complete"]')

    d.verifyElementPresent(xpath='//span[@style="font-weight:bold" and contains(text(),"Successfully updated order")]')
    d.screenshot(filename='final_page')


