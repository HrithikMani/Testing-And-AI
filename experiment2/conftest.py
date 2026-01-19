"""
Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and makes fixtures
available to all test files.
"""

import pytest
import sys
from pathlib import Path

# Add the experiment2 directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import fixtures from support module - these will be available to all tests
from support.fixtures import playwright_instance, browser, context, page

# Re-export fixtures so pytest can find them
__all__ = ['playwright_instance', 'browser', 'context', 'page']


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "playwright: Playwright browser tests")
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "theme: Theme-related tests")
    config.addinivalue_line("markers", "navigation: Navigation tests")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Handle step errors - can be used for screenshots on failure."""
    print(f"\n❌ Step failed: {step}")
    print(f"   Scenario: {scenario.name}")
    print(f"   Feature: {feature.name}")
    print(f"   Error: {exception}")
