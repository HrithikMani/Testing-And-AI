"""
Access Control Component
Handles department and user access management in WebChart.

URL Patterns:
- ?f=admin&subfunc=access_control - Access Control list
- ?f=admin&subfunc=access_control&t=user_realms - Departments tab
- ?f=admin&subfunc=access_control&opp=add - Add department
- ?f=admin&subfunc=access_control&opp=edit - Edit department
"""

from typing import List
from playwright.sync_api import Page

from components.base_component import BaseComponent
from support.selector_loader import get_selector


class AccessControlComponent(BaseComponent):
    """
    Component for Access Control section of WebChart.
    Extends BaseComponent with department management methods.
    """
    
    # URL patterns this component handles
    URL_PATTERNS: List[str] = [
        '?f=admin&subfunc=access_control',           # Access Control main
        '?f=admin&subfunc=access_control&t=user_realms',  # Departments
        '?f=admin&subfunc=access_control&opp=add',   # Add department
        '?f=admin&subfunc=access_control&opp=edit',  # Edit department
    ]
    
    def navigate_to_access_control(self):
        """Navigate to Access Control from anywhere."""
        self.open_sidemenu()
        self.click_sidemenu_link("Control Panel")
        self.click_charttab("Access")
        self.click_charttab_subtab("Access Control")
    
    def add_department(self, name: str):
        """Click Add Department and enter name."""
        self.click_link("Add Department")
        selector = get_selector('webchart', 'department_name_input')
        self.page.locator(selector).first.fill(name)
    
    def add_user_to_department(self, username: str):
        """Add a user to the department being edited."""
        self.enter_autocomplete("le_user_realm_le_ur_user_id_display", username)
        self.click_listedit_button("Add")
    
    def submit_department(self):
        """Submit the department form."""
        self.click_button("Submit")
    
    def click_dept_edit(self, dept_name: str):
        """Click edit link for a department."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'dept_edit_link', dept_name)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    def show_all_departments(self):
        """Click Show All to display all departments."""
        self.click_link("Show All")
    
    def verify_department_exists(self, name: str):
        """Verify a department exists in the list."""
        self.verify_listview_link(name)
    
    def verify_user_in_department(self, username: str):
        """Verify a user is listed in the department."""
        self.verify_text(username)
