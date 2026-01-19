"""
WebChart Base Component
Provides methods for common WebChart interactions.

This is the base class for all WebChart components.
It provides shared functionality like navigation, sidemenu, chart tabs, etc.
"""

import time
from typing import List, Optional
from playwright.sync_api import Page, expect

from support.selector_loader import get_selector
from support.config import config


class BaseComponent:
    """
    Base component for WebChart application.
    Provides methods for common WebChart interactions.
    
    All other components should extend this class.
    """
    
    # URL patterns this component handles (override in subclasses)
    URL_PATTERNS: List[str] = []
    
    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url or config.BASE_URL
        self.ajax_timeout = config.AJAX_TIMEOUT
        self.animation_wait = config.ANIMATION_WAIT
    
    # ============== Navigation ==============
    
    def goto(self, path: str = ""):
        """Navigate to a WebChart URL."""
        url = f"{self.base_url}{path}" if self.base_url else path
        self.page.goto(url)
        self.wait_for_ajax()
    
    def wait_for_ajax(self, timeout: Optional[int] = None):
        """Wait for AJAX requests to complete."""
        timeout = timeout or self.ajax_timeout
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_animation(self, duration: Optional[float] = None):
        """Wait for CSS animations."""
        duration = duration or self.animation_wait
        time.sleep(duration)
    
    # ============== Sidemenu ==============
    
    def open_sidemenu(self):
        """Open the sidemenu."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'sidemenu_icon')
        self.page.locator(selector).first.click()
        self.wait_for_animation()
    
    def close_sidemenu(self):
        """Close the sidemenu if open."""
        open_selector = get_selector('webchart', 'sidemenu_open')
        if self.page.locator(open_selector).count() > 0:
            icon_selector = get_selector('webchart', 'sidemenu_icon')
            self.page.locator(icon_selector).first.click()
            self.wait_for_animation()
    
    def pin_sidemenu(self):
        """Pin the sidemenu."""
        selector = get_selector('webchart', 'sidemenu_pin')
        self.page.locator(selector).first.click()
    
    def click_sidemenu_link(self, text: str):
        """Click a link in the sidemenu."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'sidemenu_entry_text', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    # ============== Chart Tabs ==============
    
    def click_charttab(self, text: str):
        """Click a chart tab."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'charttab', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    def click_charttab_subtab(self, text: str):
        """Click a chart subtab."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'charttab_subtab', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    # ============== Links and Buttons ==============
    
    def click_link(self, text: str):
        """Click a link by text."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'link', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    def click_button(self, text: str):
        """Click a button by text/value."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'button', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    # ============== Autocomplete ==============
    
    def enter_autocomplete(self, field: str, value: str):
        """
        Enter a value in an autocomplete field and select the option.
        
        Args:
            field: The autocomplete field ID/name or label
            value: The value to enter and select
        """
        self.wait_for_ajax()
        
        # Try by ID/name first
        selector = get_selector('webchart', 'autocomplete_input_by_id', field)
        ac_input = self.page.locator(selector).first
        
        if ac_input.count() == 0:
            selector = get_selector('webchart', 'autocomplete_input', field)
            ac_input = self.page.locator(selector).first
        
        ac_input.scroll_into_view_if_needed()
        ac_input.click()
        ac_input.clear()
        
        # Type partial string for better matching
        search_text = value[:int(len(value) * 0.66)] if len(value) >= 3 else value
        ac_input.fill(search_text)
        
        time.sleep(0.5)
        
        # Wait for pending to clear
        try:
            pending = get_selector('webchart', 'autocomplete_pending')
            self.page.wait_for_selector(pending, state="detached", timeout=5000)
        except:
            pass
        
        # Click matching option
        option_selector = get_selector('webchart', 'autocomplete_option', value)
        try:
            option = self.page.locator(option_selector).first
            if option.is_visible():
                option.click()
            else:
                ac_input.clear()
                ac_input.fill(value)
                time.sleep(0.5)
                self.page.locator(option_selector).first.click()
        except:
            ac_input.clear()
            ac_input.fill(value)
    
    # ============== List Edit ==============
    
    def click_listedit_button(self, text: str):
        """Click a button in a listedit."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'listedit_button', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    def click_listedit_edit(self, text: str):
        """Click edit button for a listedit row."""
        selector = get_selector('webchart', 'listedit_editbutton', text)
        self.page.locator(selector).first.click()
    
    def verify_listedit_row(self, text: str):
        """Verify a row exists in listedit."""
        selector = get_selector('webchart', 'listedit_row', text)
        expect(self.page.locator(selector).first).to_be_visible()
    
    # ============== List View ==============
    
    def click_listview_link(self, text: str):
        """Click a link in a listview."""
        self.wait_for_ajax()
        selector = get_selector('webchart', 'listview_link', text)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
    
    def verify_listview_link(self, text: str):
        """Verify a link exists in listview."""
        selector = get_selector('webchart', 'listview_link', text)
        expect(self.page.locator(selector).first).to_be_visible()
    
    # ============== Verification ==============
    
    def verify_text(self, text: str):
        """Verify text is visible on the page."""
        selector = get_selector('webchart', 'text', text)
        expect(self.page.locator(selector).first).to_be_visible()
    
    def verify_link(self, text: str):
        """Verify a link is visible."""
        selector = get_selector('webchart', 'link', text)
        expect(self.page.locator(selector).first).to_be_visible()
