"""
Step definitions for API documentation tests.
"""

import re
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from steps.common_steps import *

# Load scenarios from feature file
scenarios('../features/api_docs.feature')


@then(parsers.parse('I should see the heading "{text}"'))
def verify_heading(page: Page, text: str):
    """Verify a heading with specific text is visible."""
    selector = get_selector('common', 'heading', text)
    expect(page.locator(selector).first).to_be_visible()
