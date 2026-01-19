"""
Test file for Add User Department feature.

This test file binds the feature file to step definitions and
provides any test-specific configuration.

Migrated from: tests/add_user_dept.okra

Configuration:
    Set these environment variables or modify support/config.py:
    - WEBCHART_URL: WebChart instance URL
    - WEBCHART_USERNAME: Login username
    - WEBCHART_PASSWORD: Login password

Run tests:
    pytest steps/test_add_user_dept.py --headed
    pytest steps/test_add_user_dept.py -k "add_department" --headed
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page

# Import WebChart step definitions (registers all steps)
from steps.webchart_steps import *

# Import components for more complex scenarios
from components import LoginComponent, BaseComponent, AccessControlComponent

# Load all scenarios from the feature file
scenarios('../features/add_user_dept.feature')


# ============== Test Fixtures ==============

@pytest.fixture
def access_control_component(page: Page) -> AccessControlComponent:
    """Provide an AccessControlComponent instance."""
    return AccessControlComponent(page)


# ============== Test-Specific Configuration ==============

# Mark all tests in this file with the webchart marker
pytestmark = [
    pytest.mark.webchart,
    pytest.mark.access_control,
]
