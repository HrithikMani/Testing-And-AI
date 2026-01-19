"""
Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and makes fixtures
available to all test files.
"""

import pytest
import sys
import time
from pathlib import Path

# Add the experiment2 directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import fixture configurations (extends pytest-playwright's built-in fixtures)
from support.fixtures import browser_context_args, browser_type_launch_args
from support.gherkin_report import GherkinReportGenerator

# Global report generator instance
_report_generator = None


def get_report_generator():
    """Get or create the report generator singleton."""
    global _report_generator
    if _report_generator is None:
        _report_generator = GherkinReportGenerator()
    return _report_generator


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "playwright: Playwright browser tests")
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "theme: Theme-related tests")
    config.addinivalue_line("markers", "navigation: Navigation tests")
    config.addinivalue_line("markers", "search: Search tests")
    config.addinivalue_line("markers", "api: API documentation tests")
    config.addinivalue_line("markers", "failure: Intentional failure tests")


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
