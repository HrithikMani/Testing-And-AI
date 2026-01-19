from playwright.sync_api import Page, expect

def fill_autocomplete(page: Page, field_id: str, search_text: str):
    """Helper to fill autocomplete field and select the first matching option.
    
    WebChart autocomplete requires typing character by character to trigger
    the dropdown. The dropdown appears as a listbox with options.
    """
    # Find the field by ID (strip # if present) or name
    if field_id.startswith('#'):
        field = page.locator(field_id)
    else:
        field = page.locator(f'#{field_id}')
    
    # Clear any existing value and type slowly to trigger autocomplete
    field.fill('')
    field.press_sequentially(search_text, delay=50)
    
    # Wait for autocomplete dropdown to appear
    page.wait_for_timeout(800)
    
    # Try to click on autocomplete suggestion - WebChart uses listbox > option
    try:
        # Wait for the listbox to appear and click the first matching option
        dropdown = page.get_by_role('listbox')
        if dropdown.is_visible(timeout=2000):
            # Get first option that contains our search text
            option = dropdown.get_by_role('option').first
            option.click()
        else:
            # Fallback: press Tab to dismiss and accept value
            field.press("Tab")
    except Exception:
        # If no dropdown appears, press Tab to move focus away
        field.press("Tab")
    
    page.wait_for_timeout(300)

def test_add_user_dept(page: Page):
    # Begin "Add a department"
    
    # Click the "Control Panel" link (directly visible in OmniScope layout)
    page.get_by_role("link", name="Control Panel").click()
    page.wait_for_load_state("networkidle")

    # Click the Access charttab
    page.click('xpath=//ul[@id="wc_tabwrapper"]//span[contains(@class, "wc_tab")]/*[contains(@class, "wc_tab_title")][contains(., "Access")]')

    # Click the "Access Control" charttab subtab
    page.click('xpath=//ul[@class="wc_tab_submenu"]//a[contains(., "Access Control")]')
    page.wait_for_load_state("networkidle")

    # --- Cleanup: Delete "Testing" department if it already exists ---
    # First check if "Show All" link exists and click it to see all departments
    show_all_link = page.locator('text="Show All"')
    if show_all_link.is_visible(timeout=2000):
        show_all_link.click()
        page.wait_for_load_state("networkidle")
    
    # Check if "Testing" department exists (exact match) and delete it
    delete_link = page.locator('xpath=//td/a[normalize-space(text())="Testing"]/parent::td/following-sibling::td//a[text()="Delete"]')
    if delete_link.count() > 0 and delete_link.first.is_visible(timeout=2000):
        delete_link.first.click()
        page.wait_for_load_state("networkidle")
        # Confirm deletion on the confirmation page
        confirm_delete_btn = page.get_by_role("button", name="Delete")
        if confirm_delete_btn.is_visible(timeout=2000):
            confirm_delete_btn.click()
            page.wait_for_load_state("networkidle")
    # --- End Cleanup ---

    # Click the "Add Department" link
    page.click('text="Add Department"')

    # Type "Testing" in the input
    page.locator('//input[not(@type="hidden") and not(@type="submit") and not(@type="button") and not(@disabled)]').first.fill("Testing")

    # Begin "Add one user to department upon dept creation"

    # Enter "Acardi" in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Acardi")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Click the "Submit Dept" button
    page.click('text="Submit Dept"')
    page.wait_for_load_state("networkidle")

    # Click the "Show All" link if visible (only appears when > 20 departments)
    show_all_link = page.locator('text="Show All"')
    if show_all_link.is_visible(timeout=2000):
        show_all_link.click()
        page.wait_for_load_state("networkidle")

    # Verify exists "Testing" listview link
    expect(page.locator('xpath=//table[contains(@class,"lv_root")]/tbody//*[not(self::th)]//tr//td//a[contains(., "Testing")]')).to_be_visible()

    # Begin "Add more users to the Testing dept"

    # Click the @Testing "Edit" link
    page.click('xpath=//td[@class="depts_Department_cell" and contains(., "Testing")]/following-sibling::td/a[contains(., "Edit")]')

    # Enter "Butler" in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Butler")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Morrison" in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Morrison")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Selenium" in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Selenium")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Garza" in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Garza")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Thomas, Dave" in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Thomas, Dave")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Better Corp." in the autocomplete and select it
    fill_autocomplete(page, "le_user_realm_le_ur_user_id_display", "Better Corp.")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Click the "Submit Dept" button
    page.click('text="Submit Dept"')
    page.wait_for_load_state("networkidle")

    # Begin "Verify all users added to the new department"

    # Click the "Testing" listview link
    page.click('xpath=//table[contains(@class,"lv_root")]/tbody//*[not(self::th)]//tr//td//a[contains(., "Testing")]')
    page.wait_for_load_state("networkidle")

    # Verify users exist (using contains match for partial name matching)
    # Use .first to handle multiple matches
    expect(page.locator('text=Acardi').first).to_be_visible()

    # Verify exists "Better Corp." text
    expect(page.locator('text=Better Corp.').first).to_be_visible()

    # Verify exists "Butler" text
    expect(page.locator('text=Butler').first).to_be_visible()

    # Verify exists "Garza" text
    expect(page.locator('text=Garza').first).to_be_visible()

    # Verify exists "Morrison" text
    expect(page.locator('text=Morrison').first).to_be_visible()

    # Verify exists "Selenium" text
    expect(page.locator('text=Selenium').first).to_be_visible()

    # Verify exists "Thomas" text
    expect(page.locator('text=Thomas').first).to_be_visible()

    # --- Cleanup: Delete the Testing department at the end ---
    # Navigate back to View Departments
    page.get_by_role("link", name="View Departments").click()
    page.wait_for_load_state("networkidle")

    # Click "Show All" if visible to see all departments
    show_all_link = page.locator('text="Show All"')
    if show_all_link.is_visible(timeout=2000):
        show_all_link.click()
        page.wait_for_load_state("networkidle")

    # Find and click the Delete link for Testing department
    delete_link = page.locator('xpath=//td/a[normalize-space(text())="Testing"]/parent::td/following-sibling::td//a[text()="Delete"]')
    if delete_link.count() > 0 and delete_link.first.is_visible(timeout=2000):
        delete_link.first.click()
        page.wait_for_load_state("networkidle")
        # Confirm deletion on the confirmation page
        confirm_delete_btn = page.get_by_role("button", name="Delete")
        if confirm_delete_btn.is_visible(timeout=2000):
            confirm_delete_btn.click()
            page.wait_for_load_state("networkidle")
    # --- End Cleanup ---
