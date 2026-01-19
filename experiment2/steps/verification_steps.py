"""
Verification Step Definitions
Assertion and verification steps for WebChart.
"""

import re
from pytest_bdd import then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from steps.login_steps import wait_for_ajax


# ============== Text Verification Steps ==============

@then(parsers.parse('I should see "{text}" text'))
def verify_text_visible(page: Page, text: str):
    """Verify text is visible on the page."""
    selector = get_selector('webchart', 'text', text)
    expect(page.locator(selector).first).to_be_visible()


# ============== List View Verification Steps ==============

@then(parsers.parse('I should see "{text}" listview link'))
def verify_listview_link(page: Page, text: str):
    """Verify a link exists in the listview."""
    selector = get_selector('webchart', 'listview_link', text)
    expect(page.locator(selector).first).to_be_visible()


@then(parsers.parse('I should see "{text}" listview row'))
def verify_listview_row(page: Page, text: str):
    """Verify a row exists in the listview."""
    selector = get_selector('webchart', 'listview_row', text)
    expect(page.locator(selector).first).to_be_visible()


# ============== Form Verification Steps ==============

@then("I should be on the add department form")
def verify_add_dept_form(page: Page):
    """Verify we are on the add department form."""
    selector = get_selector('webchart', 'department_name_input')
    expect(page.locator(selector).first).to_be_visible()


@then("I should see a success message")
def verify_success_message(page: Page):
    """Verify a success action completed (generic)."""
    wait_for_ajax(page)
    expect(page).not_to_have_url(re.compile(".*error.*"))
