def main (d, WCURL):
    """
    Add an order 
    """

    if d.browser == WCURL.BROWSER_IE:
        return

    d.navigate(WCURL.CHART_HART_WILLIAM)
    d.clickElement(xpath='//li/a[text()="Add Order"]')

    d.screenshot(filename='order_form_initial');
    d.enterFormData('2', id='ordering_physician')
    d.enterFormData('Soon', name='schedule_comment')
    d.enterFormData('OFFICE', id='location')
    
    d.enterAutocomplete('conditionac','urination')

    d.enterFormData('Enter witty instructions here.', id='patient_instructions')
    d.enterFormData('Add sarcastic remark here.', id='comments')

    d.enterFormData('Endo Lab Blood Studies', name='set_name')
    d.screenshot(filename='order_form_switch_sets');

    d.enterAutocomplete('ordersac','rh',0)
    d.enterFormData(True, xpath='//input[@name="orders" and @value="204"]')
    d.enterFormData(True, xpath='//input[@name="orders" and @value="213"]')
    d.enterFormData(True, xpath='//input[@name="orders" and @value="347"]')

    d.clickElement(id='bottom_request_btn')

    d.screenshot(filename='confirmation_page');
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_204_0')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_213_1')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_347_2')
    d.enterFormData('Urination painful (R30.0) (788.1)', id='diag_2260_3')

    d.clickElement(id='finish_btn')

    d.screenshot(filename='final_page');
    d.verifyElementPresent(xpath='//span[@style="font-weight:bold" and contains(text(),"Successfully inserted order")]')

