"""
Pytest fixtures for Playwright browser automation.

Uses pytest-playwright's built-in fixtures which handle parallelization automatically.
Each test gets its own browser context for isolation.
"""

import pytest
import os

# pytest-playwright provides these fixtures automatically:
# - playwright: Playwright instance
# - browser: Browser instance (shared per worker)
# - context: BrowserContext (new per test) 
# - page: Page (new per test)

# We just need to configure them via pytest hooks and conftest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context settings."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, request):
    """Configure browser launch settings.
    
    Respects --headed flag from command line.
    Can also use SLOW_MO env var to slow down actions.
    """
    slow_mo = int(os.environ.get('SLOW_MO', '0'))
    
    return {
        **browser_type_launch_args,
        "slow_mo": slow_mo,
    }

