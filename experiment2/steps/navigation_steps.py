"""
Navigation Step Definitions
Sidemenu, chart tabs, links, and buttons for WebChart.
"""

from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from steps.login_steps import wait_for_ajax, wait_for_animation


# ============== Sidemenu Steps ==============

@given("I open the WebChart sidemenu")
@when("I open the WebChart sidemenu")
def open_sidemenu(page: Page):
    """Open the WebChart sidemenu (left navigation)."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'sidemenu_icon')
    page.locator(selector).first.click()
    wait_for_animation(page, 1.0)


@when("I close the WebChart sidemenu")
def close_sidemenu(page: Page):
    """Close the WebChart sidemenu."""
    open_selector = get_selector('webchart', 'sidemenu_open')
    if page.locator(open_selector).count() > 0:
        icon_selector = get_selector('webchart', 'sidemenu_icon')
        page.locator(icon_selector).first.click()
        wait_for_animation(page, 1.0)


@when("I pin the WebChart sidemenu")
def pin_sidemenu(page: Page):
    """Pin the sidemenu so it stays open."""
    selector = get_selector('webchart', 'sidemenu_pin')
    page.locator(selector).first.click()


@given(parsers.parse('I click the "{text}" sidemenu link'))
@when(parsers.parse('I click the "{text}" sidemenu link'))
def click_sidemenu_link(page: Page, text: str):
    """Click a link in the sidemenu."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'sidemenu_entry_text', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


# ============== Chart Tab Steps ==============

@given(parsers.parse('I click the "{text}" charttab'))
@when(parsers.parse('I click the "{text}" charttab'))
def click_charttab(page: Page, text: str):
    """Click a chart tab by name."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'charttab', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


@given(parsers.parse('I click the "{text}" charttab subtab'))
@when(parsers.parse('I click the "{text}" charttab subtab'))
def click_charttab_subtab(page: Page, text: str):
    """Click a chart subtab by name."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'charttab_subtab', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


@then(parsers.parse('I should see the "{text}" charttab'))
def verify_charttab_exists(page: Page, text: str):
    """Verify a chart tab exists."""
    selector = get_selector('webchart', 'charttab', text)
    expect(page.locator(selector).first).to_be_visible()


# ============== Link Steps ==============

@given(parsers.parse('I click the "{text}" link'))
@when(parsers.parse('I click the "{text}" link'))
def click_link(page: Page, text: str):
    """Click a link by text."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'link', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


@given(parsers.parse('I click the "{text}" link if visible'))
@when(parsers.parse('I click the "{text}" link if visible'))
def click_link_if_visible(page: Page, text: str):
    """Click a link by text only if it's visible (optional click)."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'link', text)
    locator = page.locator(selector).first
    try:
        if locator.is_visible(timeout=2000):
            locator.click()
            wait_for_ajax(page)
    except:
        pass  # Link not visible, skip


# ============== Button Steps ==============

@when(parsers.parse('I click the "{text}" button'))
def click_button(page: Page, text: str):
    """Click a button by text/value."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'button', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


# ============== List View Steps ==============

@when(parsers.parse('I click the "{text}" listview link'))
def click_listview_link(page: Page, text: str):
    """Click a link in a listview."""
    wait_for_ajax(page)
    selector = get_selector('webchart', 'listview_link', text)
    page.locator(selector).first.click()
    wait_for_ajax(page)


@when(parsers.parse('I click the "{text}" listview header'))
def click_listview_header(page: Page, text: str):
    """Click a header in a listview (for sorting)."""
    selector = get_selector('webchart', 'listview_header', text)
    page.locator(selector).first.click()
