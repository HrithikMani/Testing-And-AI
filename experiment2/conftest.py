"""
Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and makes fixtures
available to all test files.

Features:
- Centralized configuration via support/config.py
- Before/After test hooks for login/logout
- Screenshot on failure
- Custom BDD reporting
"""

import pytest
import sys
import time
import os
from pathlib import Path
from datetime import datetime

# Add the experiment2 directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import fixture configurations (extends pytest-playwright's built-in fixtures)
from support.fixtures import browser_context_args, browser_type_launch_args
from support.gherkin_report import GherkinReportGenerator
from support.config import config, env

# Global report generator instance
_report_generator = None


def get_report_generator():
    """Get or create the report generator singleton."""
    global _report_generator
    if _report_generator is None:
        _report_generator = GherkinReportGenerator()
    return _report_generator


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-feature",
        action="store",
        default=None,
        help="Run tests for a specific feature file (e.g., --run-feature add_user_dept)"
    )


def pytest_collection_modifyitems(session, config, items):
    """Filter tests based on --run-feature option."""
    feature_filter = config.getoption("--run-feature")
    if feature_filter:
        # Remove .feature extension if provided
        feature_name = feature_filter.replace(".feature", "")
        
        # Map feature name to test file name
        feature_test_name = f"test_{feature_name}"
        
        # Filter items to only those matching the feature
        items[:] = [item for item in items 
                   if feature_test_name in str(item.fspath) or feature_name in str(item.fspath)]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "playwright: Playwright browser tests")
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "theme: Theme-related tests")
    config.addinivalue_line("markers", "navigation: Navigation tests")
    config.addinivalue_line("markers", "search: Search tests")
    config.addinivalue_line("markers", "api: API documentation tests")
    config.addinivalue_line("markers", "failure: Intentional failure tests")
    # WebChart markers
    config.addinivalue_line("markers", "webchart: WebChart application tests")
    config.addinivalue_line("markers", "access_control: Access control tests")
    config.addinivalue_line("markers", "add_department: Add department tests")
    config.addinivalue_line("markers", "add_user_on_creation: Add user on creation tests")
    config.addinivalue_line("markers", "add_more_users: Add more users tests")
    config.addinivalue_line("markers", "verify_users: Verify users tests")
    config.addinivalue_line("markers", "skip_login: Skip automatic login for this test")


# ============== WebChart Login/Logout Fixtures ==============

@pytest.fixture(scope="function")
def webchart_login(page):
    """
    Fixture that handles WebChart login before test and logout after.
    
    This is automatically used by tests marked with @webchart.
    Use @pytest.mark.skip_login to skip automatic login.
    
    Usage in test:
        def test_something(webchart_login, page):
            # page is now logged in
            pass
    """
    from components import LoginComponent
    
    login_component = LoginComponent(page)
    
    # Before test: Login
    print(f"\n🔐 Logging into WebChart as '{config.USERNAME}'...")
    login_component.goto()
    login_component.login(config.USERNAME, config.PASSWORD)
    login_component.wait_for_dashboard()
    print("✅ Login successful")
    
    yield page  # Test runs here
    
    # After test: Logout
    print("\n🔓 Logging out...")
    try:
        login_page.logout()
        print("✅ Logout successful")
    except Exception as e:
        print(f"⚠️ Logout failed: {e}")


@pytest.fixture(scope="function")
def webchart_page(page):
    """
    Fixture that provides a logged-in WebChart page.
    Handles login/logout automatically.
    """
    from components import LoginComponent, BaseComponent
    
    login_component = LoginComponent(page)
    
    # Login
    login_component.goto()
    login_component.login(config.USERNAME, config.PASSWORD)
    login_component.wait_for_dashboard()
    
    # Provide BaseComponent instance
    wc_component = BaseComponent(page)
    
    yield wc_component
    
    # Logout
    try:
        login_component.logout()
    except:
        pass


# ============== Screenshot on Failure ==============

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Take screenshot on test failure."""
    outcome = yield
    
    if outcome.excinfo is not None and config.SCREENSHOT_ON_FAILURE:
        # Get the page fixture if available
        page = item.funcargs.get('page')
        if page:
            try:
                # Create screenshots directory
                screenshot_dir = Path(config.SCREENSHOT_DIR)
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name.replace('[', '_').replace(']', '_')
                filename = f"{test_name}_{timestamp}.png"
                filepath = screenshot_dir / filename
                
                # Take screenshot
                page.screenshot(path=str(filepath))
                print(f"\n📸 Screenshot saved: {filepath}")
            except Exception as e:
                print(f"\n⚠️ Failed to take screenshot: {e}")


# Track current test's steps
_current_test_steps = []
_current_step_start = None


def pytest_sessionstart(session):
    """Reset report generator at start of session."""
    global _report_generator
    _report_generator = GherkinReportGenerator()


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    """Called before each BDD step."""
    global _current_step_start
    _current_step_start = time.time()


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """Called after each BDD step (on success)."""
    global _current_test_steps, _current_step_start
    duration = time.time() - _current_step_start if _current_step_start else 0
    
    _current_test_steps.append({
        'keyword': step.keyword,
        'name': step.name,
        'status': 'passed',
        'duration': duration
    })


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Handle step errors - capture for report."""
    global _current_test_steps, _current_step_start
    duration = time.time() - _current_step_start if _current_step_start else 0
    
    _current_test_steps.append({
        'keyword': step.keyword,
        'name': step.name,
        'status': 'failed',
        'duration': duration,
        'error': str(exception)
    })
    
    print(f"\n❌ Step failed: {step}")
    print(f"   Scenario: {scenario.name}")
    print(f"   Feature: {feature.name}")
    print(f"   Error: {exception}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results for custom report."""
    global _current_test_steps
    
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        # Get BDD info from markers
        feature_name = "Unknown Feature"
        scenario_name = item.name
        
        # Try to get feature/scenario from pytest-bdd
        for marker in item.iter_markers():
            if marker.name == 'usefixtures':
                continue
        
        # Parse from nodeid: steps/test_file.py::test_scenario_name
        if '::' in item.nodeid:
            scenario_name = item.nodeid.split('::')[-1].replace('test_', '').replace('_', ' ').title()
        
        # Get feature from parent if available
        if hasattr(item, '_obj') and hasattr(item._obj, '__self__'):
            pass  # Could extract more info here
        
        # Try to get from pytest-bdd scenario
        if hasattr(item, 'callspec') and 'scenario' in item.callspec.params:
            scenario_obj = item.callspec.params['scenario']
            scenario_name = scenario_obj.name
            feature_name = scenario_obj.feature.name
        
        # Get from _pytest_bdd markers
        for marker in item.iter_markers('parametrize'):
            pass
        
        # Use item's parent for feature name
        if hasattr(item, 'parent') and item.parent:
            module_name = item.parent.name.replace('test_', '').replace('.py', '').replace('_', ' ').title()
            feature_name = f"Feature: {module_name}"
        
        # Get error message if failed
        error_msg = None
        if report.failed and call.excinfo:
            error_msg = str(call.excinfo.value)
        
        # Add to report
        report_gen = get_report_generator()
        report_gen.add_result(
            feature=feature_name,
            scenario=scenario_name,
            steps=list(_current_test_steps),
            status='passed' if report.passed else 'failed',
            duration=report.duration,
            error=error_msg
        )
        
        # Reset steps for next test
        _current_test_steps = []


def pytest_sessionfinish(session, exitstatus):
    """Generate the Gherkin HTML report at end of session."""
    report_gen = get_report_generator()
    if report_gen.results:
        report_path = Path(__file__).parent / 'reports' / 'gherkin-report.html'
        report_gen.generate_html(str(report_path))
        print(f"\n📊 Gherkin Report: file://{report_path}")
