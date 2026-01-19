"""
WebChart Step Definitions
Re-exports all WebChart-related step definitions for backward compatibility.

Steps are organized into separate modules:
- login_steps: Login/logout and authentication
- navigation_steps: Sidemenu, chart tabs, links, buttons
- form_steps: Input, autocomplete, list edit controls
- access_control_steps: Department management, user access
- verification_steps: Assertions and verifications
"""

# Re-export all steps for backward compatibility
from steps.login_steps import *
from steps.navigation_steps import *
from steps.form_steps import *
from steps.access_control_steps import *
from steps.verification_steps import *

# Re-export helper functions
from steps.login_steps import wait_for_ajax, wait_for_animation
