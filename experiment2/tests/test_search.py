"""
Step definitions for search functionality tests.
"""

import re
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from steps.common_steps import *

# Load scenarios from feature file
scenarios('../features/search.feature')


@when("I click the search button")
def click_search_button(page: Page):
    """Click the search button to open search dialog."""
    selector = get_selector('playwright_docs', 'search_button')
    page.locator(selector).first.click()


@then("I should see the search input")
def verify_search_input(page: Page):
    """Verify the search input is visible."""
    selector = get_selector('playwright_docs', 'search_input')
    expect(page.locator(selector).first).to_be_visible()
