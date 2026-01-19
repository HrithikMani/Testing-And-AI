"""
WebChart Components
Provides component classes for WebChart automation.

Components are organized by functionality and include URL patterns
they handle, since WebChart uses query parameters like ?func=xyz
for navigation rather than distinct URL paths.
"""

from components.login_component import LoginComponent
from components.base_component import BaseComponent
from components.access_control_component import AccessControlComponent

__all__ = [
    'LoginComponent',
    'BaseComponent',
    'AccessControlComponent',
]
