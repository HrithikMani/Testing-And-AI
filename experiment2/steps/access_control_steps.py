"""
Access Control Step Definitions
Department management and user access control for WebChart.
"""

import re
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from steps.login_steps import wait_for_ajax


# ============== Viewable Departments Steps ==============

@when('I uncheck all viewable departments')
def uncheck_all_viewable_departments(page: Page):
    """Uncheck all checkboxes in the Viewable Departments section."""
    wait_for_ajax(page)
    
    viewable_section = page.locator('fieldset:has-text("Viewable Departments")')
    checked_boxes = viewable_section.locator('input[type="checkbox"]:checked')
    count = checked_boxes.count()
    
    for i in range(count):
        checked_boxes.first.uncheck()
        page.wait_for_timeout(100)
    
    page.wait_for_timeout(300)


@when(parsers.parse('I check the "{dept_name}" viewable department checkbox'))
def check_viewable_department_checkbox(page: Page, dept_name: str):
    """Check a specific department's checkbox in the Viewable Departments section.
    
    This allows users of this department to view users in the specified department.
    """
    wait_for_ajax(page)
    
    viewable_section = page.locator('fieldset:has-text("Viewable Departments")')
    
    # Try exact match first
    checkbox = viewable_section.locator(f'td:has-text("{dept_name}") input[type="checkbox"]')
    if checkbox.count() == 1:
        checkbox.check()
    elif checkbox.count() > 1:
        # Multiple matches - find exact match
        cells = viewable_section.locator('td')
        for i in range(cells.count()):
            cell_text = cells.nth(i).text_content().strip()
            if cell_text == dept_name:
                cb = cells.nth(i).locator('input[type="checkbox"]')
                if cb.count() > 0:
                    cb.check()
                    break
    else:
        # Try by value attribute
        checkbox = viewable_section.locator(f'input[type="checkbox"][value="{dept_name}"]')
        if checkbox.count() > 0:
            checkbox.first.check()


# ============== Department User Management Steps ==============

@when(parsers.parse('I add user "{username}" to the department'))
@given(parsers.parse('I add user "{username}" to the department'))
def add_user_to_department(page: Page, username: str):
    """Add a user to the department using autocomplete and Add button."""
    wait_for_ajax(page)
    
    # Enter username in the user autocomplete field
    field = 'le_user_realm_le_ur_user_id_display'
    ac_input = page.locator(f'#{field}')
    
    if ac_input.count() == 0:
        selector = get_selector('webchart', 'autocomplete_input_by_id', field)
        ac_input = page.locator(selector).first
    
    ac_input.fill('')
    ac_input.press_sequentially(username, delay=50)
    page.wait_for_timeout(800)
    
    # Click on autocomplete suggestion
    try:
        option = page.get_by_role('option', name=re.compile(re.escape(username), re.IGNORECASE))
        if option.count() > 0 and option.first.is_visible(timeout=2000):
            option.first.click()
        else:
            page.keyboard.press('Enter')
    except Exception:
        page.keyboard.press('Enter')
    
    wait_for_ajax(page)
    
    # Click the Add button
    listedit_section = page.locator('table.dlg_root').last
    button = listedit_section.get_by_role('button', name='Add', exact=True)
    if button.count() > 0 and button.first.is_visible(timeout=2000):
        button.first.click()
    else:
        selector = get_selector('webchart', 'listedit_button', 'Add')
        page.locator(selector).first.click()
    
    wait_for_ajax(page)


# ============== Department Management Steps ==============

@when(parsers.parse('I click the "{dept}" department edit link'))
def click_dept_edit_link(page: Page, dept: str):
    """Click the edit link for a specific department."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'dept_edit_link', dept)
    page.locator(selector).first.click()
    wait_for_ajax(page)


@given(parsers.parse('I delete the "{dept}" department if it exists'))
@when(parsers.parse('I delete the "{dept}" department if it exists'))
def delete_department_if_exists(page: Page, dept: str):
    """Delete a department if it exists (cleanup step).
    
    This navigates to Access Control, looks for the department,
    and deletes it if found.
    """
    wait_for_ajax(page)
    
    # First, click "Show All" to see all departments if visible
    show_all_selector = get_selector('webchart', 'link', 'Show All')
    show_all = page.locator(show_all_selector).first
    try:
        if show_all.is_visible(timeout=2000):
            show_all.click()
            wait_for_ajax(page)
    except:
        pass
    
    # Look for the department's Delete link
    delete_selector = f'//td/a[normalize-space(text())="{dept}"]/parent::td/following-sibling::td//a[text()="Delete"]'
    delete_link = page.locator(delete_selector).first
    
    try:
        if delete_link.is_visible(timeout=2000):
            delete_link.click()
            wait_for_ajax(page)
            
            # Confirm deletion on the confirmation page
            confirm_btn = page.get_by_role("button", name="Delete")
            if confirm_btn.is_visible(timeout=2000):
                confirm_btn.click()
                wait_for_ajax(page)
    except:
        pass  # Department doesn't exist, nothing to delete


@then(parsers.parse('the "{dept}" department should not exist'))
def verify_department_not_exists(page: Page, dept: str):
    """Verify a department does not exist in the list."""
    wait_for_ajax(page)
    
    show_all_selector = get_selector('webchart', 'link', 'Show All')
    try:
        show_all = page.locator(show_all_selector).first
        if show_all.is_visible(timeout=1000):
            show_all.click()
            wait_for_ajax(page)
    except:
        pass
    
    dept_selector = get_selector('webchart', 'listview_link', dept)
    expect(page.locator(dept_selector).first).not_to_be_visible()
