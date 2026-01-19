"""
Pytest fixtures for Playwright browser automation.

Provides browser, context, and page fixtures for BDD tests.
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from typing import Generator
import os


# Configuration from environment variables
HEADLESS = os.environ.get('HEADLESS', 'true').lower() == 'true'
BROWSER_TYPE = os.environ.get('BROWSER', 'chromium')
SLOW_MO = int(os.environ.get('SLOW_MO', '0'))
BASE_URL = os.environ.get('BASE_URL', 'https://playwright.dev')


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Create a Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Launch browser for the test session.
    
    Supports: chromium, firefox, webkit
    Set BROWSER env var to change browser.
    Set HEADLESS=false for headed mode.
    """
    browser_types = {
        'chromium': playwright_instance.chromium,
        'firefox': playwright_instance.firefox,
        'webkit': playwright_instance.webkit,
    }
    
    browser_type = browser_types.get(BROWSER_TYPE, playwright_instance.chromium)
    
    browser = browser_type.launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO,
    )
    
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Create a new browser context for each test.
    
    This ensures tests are isolated from each other.
    """
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        base_url=BASE_URL,
    )
    
    # Enable tracing for debugging (optional)
    # context.tracing.start(screenshots=True, snapshots=True)
    
    yield context
    
    # Save trace on failure (optional)
    # context.tracing.stop(path="trace.zip")
    
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Create a new page for each test.
    
    This is the main fixture you'll use in step definitions.
    """
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    yield page
    
    page.close()
