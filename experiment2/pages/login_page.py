"""
Login Page Object
Handles all login/logout operations for WebChart.
"""

from playwright.sync_api import Page

from support.config import config


class LoginPage:
    """
    Page object for WebChart login page.
    Handles all login/logout operations.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = config.BASE_URL
    
    def goto(self):
        """Navigate to the WebChart login page."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("networkidle")
    
    def login(self, username: str, password: str, method: str = 'standard'):
        """
        Login to WebChart.
        
        Args:
            username: WebChart username
            password: WebChart password  
            method: Login method - 'standard' or 'miedev'
        """
        if method == 'miedev':
            self._login_miedev()
        else:
            self._login_standard(username, password)
    
    def _login_standard(self, username: str, password: str):
        """Perform standard login with username/password."""
        # Click Standard Login button
        self.page.get_by_role("button", name="Standard Login").click()
        self.page.wait_for_timeout(500)
        
        # Fill credentials
        self.page.get_by_role("textbox", name="Username/Email").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        
        # Click Next
        self.page.get_by_role("button", name="Next").click()
        self.page.wait_for_timeout(500)
        
        # Click Next again to complete login
        self.page.get_by_role("button", name="Next").click()
    
    def _login_miedev(self):
        """Perform MIE Dev login (SSO)."""
        self.page.get_by_role("link", name="MIE Dev Login").click()
    
    def wait_for_dashboard(self, timeout: int = 30000):
        """Wait for the dashboard to load after login."""
        # Wait for Logout link to appear (indicates successful login)
        self.page.wait_for_selector('text="Logout"', timeout=timeout)
        # Wait for DOM to be ready - don't use networkidle as WebChart has persistent WebSocket
        self.page.wait_for_load_state("domcontentloaded")
        # Small wait for any initial JS to execute
        self.page.wait_for_timeout(1000)
    
    def logout(self):
        """Logout from WebChart."""
        try:
            # Try clicking the Logout link
            logout_link = self.page.get_by_role("link", name="Logout")
            if logout_link.is_visible(timeout=5000):
                logout_link.click()
                self.page.wait_for_load_state("domcontentloaded")
        except Exception:
            # If logout link not found, navigate to logout URL
            self.page.goto(f"{self.base_url}?func=logout")
    
    def is_logged_in(self) -> bool:
        """Check if currently logged in."""
        try:
            return self.page.get_by_role("link", name="Logout").is_visible(timeout=2000)
        except:
            return False
