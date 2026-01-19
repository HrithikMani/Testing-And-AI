"""
Access Control Page Object
Handles department management in WebChart.
"""

from playwright.sync_api import Page

from pages.webchart_base_page import WebChartPage
from support.selector_loader import get_selector


class AccessControlPage(WebChartPage):
    """
    Page object for Access Control section of WebChart.
    Extends WebChartPage with department management methods.
    """
    
    def navigate_to_access_control(self):
        """Navigate to Access Control from anywhere."""
        self.open_sidemenu()
        self.click_sidemenu_link("Control Panel")
        self.click_charttab("Access")
        self.click_charttab_subtab("Access Control")
    
    def add_department(self, name: str):
        """Click Add Department and enter name."""
        self.click_link("Add Department")
        self.page.locator("input[type='text']").first.fill(name)
    
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
