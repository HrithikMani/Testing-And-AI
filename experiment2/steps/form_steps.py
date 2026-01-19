"""
Form Step Definitions
Input fields, autocomplete, and list edit controls for WebChart.
"""

import re
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from steps.login_steps import wait_for_ajax


# ============== Input Steps ==============

@when(parsers.parse('I type "{value}" in the input'))
def type_in_input(page: Page, value: str):
    """Type value in the first visible input."""
    selector = "//input[not(@type='hidden') and not(@disabled)][@type='text']"
    page.locator(selector).first.fill(value)


@when(parsers.parse('I type "{value}" in the department name input'))
def type_department_name(page: Page, value: str):
    """Type value in the department name input field."""
    page.locator("input[type='text']:not([disabled])").first.fill(value)


@when(parsers.parse('I type "{value}" in the "{field}" input'))
def type_in_named_input(page: Page, value: str, field: str):
    """Type value in a named input field."""
    selector = get_selector('webchart', 'input', field)
    page.locator(selector).first.fill(value)


# ============== Autocomplete Steps ==============

@given(parsers.parse('I enter "{value}" in the "{field}" autocomplete'))
@when(parsers.parse('I enter "{value}" in the "{field}" autocomplete'))
def enter_autocomplete(page: Page, value: str, field: str):
    """
    Enter a value in an autocomplete field and select the matching option.
    
    WebChart autocomplete requires typing character by character to trigger
    the dropdown. The dropdown appears as a listbox with options.
    """
    wait_for_ajax(page)
    
    # Find the field by ID
    ac_input = page.locator(f'#{field}')
    
    if ac_input.count() == 0:
        # Fall back to selector-based lookup
        selector = get_selector('webchart', 'autocomplete_input_by_id', field)
        ac_input = page.locator(selector).first
    
    # Clear any existing value and type slowly to trigger autocomplete
    ac_input.fill('')
    ac_input.press_sequentially(value, delay=50)
    
    # Wait for autocomplete dropdown to appear
    page.wait_for_timeout(800)
    
    # Try to click on autocomplete suggestion - WebChart uses listbox > option
    try:
        dropdown = page.get_by_role('listbox')
        if dropdown.is_visible(timeout=2000):
            option = dropdown.get_by_role('option').first
            option.click()
        else:
            ac_input.press("Tab")
    except Exception:
        ac_input.press("Tab")
    
    page.wait_for_timeout(300)


@then(parsers.parse('I should see "{value}" in the "{field}" autocomplete'))
def verify_autocomplete_value(page: Page, value: str, field: str):
    """Verify an autocomplete field contains expected value."""
    selector = get_selector('webchart', 'autocomplete_input_by_id', field)
    expect(page.locator(selector).first).to_have_value(re.compile(f".*{value}.*"))


# ============== List Edit Steps ==============

@when(parsers.parse('I click the "{text}" listedit button'))
def click_listedit_button(page: Page, text: str):
    """Click a button in a listedit control.
    
    Uses role-based selector first (more reliable), then falls back to XPath.
    This handles both <button> and <input type='button'> elements.
    """
    wait_for_ajax(page)
    
    try:
        listedit_section = page.locator('table.dlg_root').last
        button = listedit_section.get_by_role('button', name=text, exact=True)
        if button.count() > 0 and button.first.is_visible(timeout=2000):
            button.first.click()
            wait_for_ajax(page)
            return
    except Exception:
        pass
    
    # Fallback to XPath selector
    selector = get_selector('webchart', 'listedit_button', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


@when(parsers.parse('I click the "{text}" listedit edit button'))
def click_listedit_edit(page: Page, text: str):
    """Click the edit button for a listedit row."""
    selector = get_selector('webchart', 'listedit_editbutton', text)
    page.locator(selector).first.click()


@when(parsers.parse('I click the "{text}" listedit minus button'))
def click_listedit_minus(page: Page, text: str):
    """Click the minus/remove button for a listedit row."""
    selector = get_selector('webchart', 'listedit_minusbutton', text)
    page.locator(selector).first.click()


@then(parsers.parse('I should see "{text}" listedit row'))
def verify_listedit_row(page: Page, text: str):
    """Verify a row exists in the listedit."""
    selector = get_selector('webchart', 'listedit_row', text)
    expect(page.locator(selector).first).to_be_visible()
