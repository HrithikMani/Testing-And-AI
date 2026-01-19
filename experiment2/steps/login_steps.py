"""
Login Step Definitions
Authentication steps for WebChart.
"""

import time
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page

from support.config import config
from components import LoginComponent


# ============== Helper Functions ==============

def wait_for_ajax(page: Page, timeout: int = None):
    """Wait for AJAX requests to complete.
    
    Note: We use domcontentloaded instead of networkidle because 
    WebChart has persistent WebSocket connections that prevent networkidle.
    """
    timeout = timeout or config.AJAX_TIMEOUT
    page.wait_for_load_state("domcontentloaded", timeout=timeout)
    # Brief wait for any pending JavaScript
    page.wait_for_timeout(500)


def wait_for_animation(page: Page, duration: float = None):
    """Wait for CSS animations to complete."""
    duration = duration or config.ANIMATION_WAIT
    time.sleep(duration)


# ============== Login/Logout Steps ==============

@given("I am logged into WebChart")
@given("I login to WebChart")
def login_to_webchart(page: Page):
    """Login to WebChart with configured credentials."""
    login_component = LoginComponent(page)
    login_component.goto()
    login_component.login(config.USERNAME, config.PASSWORD)
    login_component.wait_for_dashboard()


@given(parsers.parse('I login to WebChart as "{username}" with password "{password}"'))
def login_to_webchart_with_creds(page: Page, username: str, password: str):
    """Login to WebChart with specific credentials."""
    login_component = LoginComponent(page)
    login_component.goto()
    login_component.login(username, password)
    login_component.wait_for_dashboard()


@when("I logout from WebChart")
@then("I logout from WebChart")
def logout_from_webchart(page: Page):
    """Logout from WebChart."""
    login_component = LoginComponent(page)
    login_component.logout()
