def main (d, WCURL):
    """
    Edit an order 
    """
    if d.browser == WCURL.BROWSER_IE:
        return

    hart_recent_orders = WCURL.CHART_HART_WILLIAM + WCURL.RECENT_ORDERS
    d.navigate(hart_recent_orders, auto_screenshot=False)

#   d.scrollTo()

    d.clickElement(id='edit_req_15_link_3')

    d.screenshot(filename='order_form_initial')
    d.enterFormData('Quick Visit Orders', name='set_name')

    d.screenshot(filename='order_form_switch_sets')
    d.clickElement(id='bottom_request_btn')

    d.screenshot(filename='confirmation_page')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_204_0')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_213_1')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_347_2')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_2260_3')

    d.clickElement(id='finish_btn')

    d.verifyElementPresent(xpath='//span[@style="font-weight:bold" and contains(text(),"Successfully updated order")]')
    d.screenshot(filename='final_page')

