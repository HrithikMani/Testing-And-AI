import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="function", autouse=True)
def setup_teardown(page: Page):
    # Before test
    page.goto("https://zeus.med-web.com/webchart/wcthkonda/")

    # Click Standard Login button
    page.get_by_role("button", name="Standard Login").click()

    # Login with credentials
    page.locator("#login_user").fill("selenium")
    page.locator("#login_passwd").fill("selenium")
    page.get_by_role("button", name="Next").click()
    
    # Click Next again to complete login
    page.get_by_role("button", name="Next").click()
    
    # Wait for the page to load after login
    page.wait_for_selector('text="Logout"', timeout=30000)

    yield

    # After test - Logout
    try:
        page.get_by_role("link", name="Logout").click()
    except:
        pass  # If logout fails, continue
