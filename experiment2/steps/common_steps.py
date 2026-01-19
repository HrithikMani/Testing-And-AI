"""
Shared step definitions used across multiple feature files.

These are common steps like navigation that are reused.
"""

import re
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector


# ============== GIVEN Steps ==============

@given("I am on the Playwright website")
def navigate_to_playwright(page: Page):
    """Navigate to the Playwright homepage."""
    page.goto("https://playwright.dev")
    page.wait_for_load_state("networkidle")


# ============== WHEN Steps ==============

@when("I click the theme toggle button")
def click_theme_toggle(page: Page):
    """Click the dark/light theme toggle button."""
    selector = get_selector('playwright_docs', 'theme_toggle')
    page.locator(selector).first.click()


@when(parsers.parse('I click on "{link_text}" in the navigation'))
def click_nav_link(page: Page, link_text: str):
    """Click a navigation link by text."""
    selector = get_selector('common', 'nav_link', link_text)
    page.locator(selector).first.click()
    page.wait_for_load_state("networkidle")


# ============== THEN Steps ==============

@then(parsers.parse('I should see the page title contains "{text}"'))
def verify_page_title(page: Page, text: str):
    """Verify the page title contains expected text."""
    expect(page).to_have_title(re.compile(f".*{text}.*"))


@then(parsers.parse('I should see the "{link_text}" link'))
def verify_link_visible(page: Page, link_text: str):
    """Verify a link with specific text is visible."""
    selector = get_selector('common', 'link', link_text)
    locator = page.locator(selector).first
    expect(locator).to_be_visible()


@then("the theme should change")
def verify_theme_changed(page: Page):
    """Verify the theme has changed."""
    selector = get_selector('playwright_docs', 'theme_toggle')
    expect(page.locator(selector).first).to_be_visible()


@then("I should be on the documentation page")
def verify_docs_page(page: Page):
    """Verify we're on the documentation page."""
    expect(page).to_have_url(re.compile(".*docs.*"))


@then("I should see the main content area")
def verify_main_content(page: Page):
    """Verify the main content area is visible."""
    selector = get_selector('playwright_docs', 'main_content')
    expect(page.locator(selector).first).to_be_visible()
