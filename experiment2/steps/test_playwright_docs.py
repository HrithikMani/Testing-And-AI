open reports/gherkin-report.html"""
Step definitions for Playwright documentation website tests.

Uses YAML selectors from selectors/playwright_docs.yaml
"""

import re
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector

# Import shared steps so they're registered with pytest-bdd
from steps.common_steps import *

# Load all scenarios from feature file
scenarios('../features/playwright_docs.feature')

# All step definitions are now in common_steps.py
# Add any playwright_docs-specific steps here if needed
