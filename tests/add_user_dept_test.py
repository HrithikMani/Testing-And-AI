from playwright.sync_api import Page, expect

def test_add_user_dept(page: Page):
    # Begin "Add a department"
    
    # Open the sidemenu
    page.locator('//span[@id="wc_menuicon"]').click()
    page.wait_for_timeout(1000) # Wait for animation

    # Click the "Control Panel" link
    page.click('text="Control Panel"')

    # Click the Access charttab
    page.click('xpath=//ul[@id="wc_tabwrapper"]//span[contains(@class, "wc_tab")]/*[contains(@class, "wc_tab_title")][contains(., "Access")]')

    # Click the "Access Control" charttab subtab
    page.click('xpath=//ul[@class="wc_tab_submenu"]//a[contains(., "Access Control")]')

    # Click the "Add Department" link
    page.click('text="Add Department"')

    # Type "Testing" in the input
    page.locator('//input[not(@type="hidden") and not(@type="submit") and not(@type="button") and not(@disabled)]').first.fill("Testing")

    # Begin "Add one user to department upon dept creation"

    # Enter "Acardi" in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Acardi")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Click the "Submit Dept" button
    page.click('text="Submit Dept"')

    # Click the "Show All" link
    page.click('text="Show All"')

    # Verify exists "Testing" listview link
    expect(page.locator('xpath=//table[contains(@class,"lv_root")]/tbody//*[not(self::th)]//tr//td//a[contains(., "Testing")]')).to_be_visible()

    # Begin "Add more users to the Testing dept"

    # Click the @Testing "Edit" link@xpath='//td[@class="depts_Department_cell" and contains(., "Testing")]/following-sibling::td/a[contains(., "Edit")]'
    page.click('xpath=//td[@class="depts_Department_cell" and contains(., "Testing")]/following-sibling::td/a[contains(., "Edit")]')

    # Enter "Butler" in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Butler")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Morrison" in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Morrison")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Selenium" in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Selenium")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Garza" in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Garza")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Thomas, Dave" in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Thomas, Dave")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Enter "Better Corp." in the "le_user_realm_le_ur_user_id_display" autocomplete
    page.fill('[name="le_user_realm_le_ur_user_id_display"]', "Better Corp.")

    # Click the "Add" listedit button
    page.click('xpath=//table[contains(@class,"dlg_root")]//input[@type="button"][contains(@value, "Add")]')

    # Click the "Submit Dept" button
    page.click('text="Submit Dept"')

    # Begin "Verify all users added to the new department"

    # Click the "Testing" listview link
    page.click('xpath=//table[contains(@class,"lv_root")]/tbody//*[not(self::th)]//tr//td//a[contains(., "Testing")]')

    # Verify exists "Acardi" text
    expect(page.locator('text="Acardi"')).to_be_visible()

    # Verify exists "Better Corp." text
    expect(page.locator('text="Better Corp."')).to_be_visible()

    # Verify exists "Butler" text
    expect(page.locator('text="Butler"')).to_be_visible()

    # Verify exists "Garza" text
    expect(page.locator('text="Garza"')).to_be_visible()

    # Verify exists "Morrison" text
    expect(page.locator('text="Morrison"')).to_be_visible()

    # Verify exists "Selenium" text
    expect(page.locator('text="Selenium"')).to_be_visible()

    # Verify exists "Thomas" text
    expect(page.locator('text="Thomas"')).to_be_visible()
