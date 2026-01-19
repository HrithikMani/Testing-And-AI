# Okra to Experiment2 Migration Guide

This guide helps GitHub Copilot (and developers) migrate Okra tests to the experiment2 Playwright-BDD framework. The migration converts Okra DSL scripts into Gherkin feature files with Python step definitions, using Playwright MCP for browser automation.

---

## Table of Contents

1. [Overview](#overview)
2. [Migration Workflow](#migration-workflow)
3. [File Mapping](#file-mapping)
4. [Converting Okra Pods to YAML Selectors](#converting-okra-pods-to-yaml-selectors)
5. [Converting Okra Syntax to Gherkin](#converting-okra-syntax-to-gherkin)
6. [Reusing Existing Steps](#reusing-existing-steps)
7. [Creating New Components](#creating-new-components)
8. [Using Playwright MCP for Navigation](#using-playwright-mcp-for-navigation)
9. [Complete Migration Example](#complete-migration-example)
10. [Okra Pod Reference](#okra-pod-reference)

---

## Overview

### Source (Okra)
- **Test files**: `tests/*.okra`
- **Pod definitions**: `okrapods/webchart/*.pod`
- **Syntax**: Custom DSL with `Begin`, `Click`, `Type`, `Verify` commands

### Target (experiment2)
- **Feature files**: `experiment2/features/*.feature` (Gherkin)
- **Step definitions**: `experiment2/steps/*.py` (pytest-bdd)
- **Components**: `experiment2/components/*.py` (Page Object Model)
- **Selectors**: `experiment2/selectors/*.yaml` (centralized XPaths)
- **Browser automation**: Playwright with MCP support

---

## Migration Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        OKRA MIGRATION WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

1. ANALYZE OKRA TEST
   ├── Read the .okra file
   ├── Identify Okra pods used (sidemenu, charttab, listedit, etc.)
   └── Note any custom XPath selectors (@xpath='...')

2. ADD SELECTORS TO YAML
   ├── Check if selectors exist in selectors/webchart.yaml
   ├── Add missing selectors from okrapods/webchart/*.pod
   └── Use {TEXT} placeholder for parameterized selectors

3. CREATE/UPDATE GHERKIN FEATURE
   ├── Convert Begin blocks → Scenarios
   ├── Convert commands → Given/When/Then steps
   └── Use English-readable step names

4. REUSE OR CREATE STEPS
   ├── Check existing steps in steps/*.py
   ├── Create new step definitions if needed
   └── Use components for complex interactions

5. TEST WITH PLAYWRIGHT MCP
   ├── Run: python3 -m pytest --headed
   ├── Use MCP browser tools to debug selectors
   └── Verify navigation and interactions work
```

---

## File Mapping

| Okra Source | Experiment2 Target | Purpose |
|-------------|-------------------|---------|
| `tests/xyz.okra` | `features/xyz.feature` | Test scenarios in Gherkin |
| `okrapods/webchart/sidemenu.pod` | `selectors/webchart.yaml` → `sidemenu_*` | Sidemenu selectors |
| `okrapods/webchart/charttab.pod` | `selectors/webchart.yaml` → `charttab_*` | Chart tab selectors |
| `okrapods/webchart/listedit.pod` | `selectors/webchart.yaml` → `listedit_*` | List edit selectors |
| `okrapods/webchart/listview.pod` | `selectors/webchart.yaml` → `listview_*` | List view selectors |
| `okrapods/webchart/autocomplete.pod` | `selectors/webchart.yaml` → `autocomplete_*` | Autocomplete selectors |
| `okrapods/webchart/_std.pod` | `selectors/webchart.yaml` → standard elements | Links, buttons, inputs |

---

## Converting Okra Pods to YAML Selectors

### Pod Syntax → YAML Format

**Okra Pod (sidemenu.pod)**:
```perl
entry://div[@id="wc_sidetabs"]/div[@id="wc_sidemenu_height"]/a[@class="wc_tab"]
```

**YAML Selector (webchart.yaml)**:
```yaml
elements:
  sidemenu_entry: "//div[@id='wc_sidetabs']/div[@id='wc_sidemenu_height']/a[@class='wc_tab']"
  sidemenu_entry_text: "//div[@id='wc_sidetabs']/div[@id='wc_sidemenu_height']/a[@class='wc_tab'][contains(text(), '{TEXT}')]"
```

### Pod Text Matching → YAML {TEXT} Placeholder

Okra uses `{OKRA_TEXT}` or `{OKRA_TEXT_CLS}` for text matching. In YAML, use `{TEXT}`:

**Okra Pod**:
```perl
link://a{OKRA_TEXT_CLS}|//span[@class="link"]{OKRA_TEXT_CLS}
```

**YAML Selector**:
```yaml
link: "//a[contains(text(), '{TEXT}')] | //span[@class='link'][contains(text(), '{TEXT}')]"
```

### Using the Selector in Steps

```python
from support.selector_loader import get_selector

# Get selector with text substitution
selector = get_selector('webchart', 'link', 'Control Panel')
# Result: "//a[contains(text(), 'Control Panel')] | //span[@class='link'][contains(text(), 'Control Panel')]"
```

---

## Converting Okra Syntax to Gherkin

### Command Mapping Table

| Okra Command | Gherkin Step | Existing Step Location |
|--------------|--------------|------------------------|
| `Begin "Test Name"` | `Scenario: Test Name` | N/A (structural) |
| `Open the sidemenu` | `When I open the WebChart sidemenu` | `navigation_steps.py` |
| `Click the "X" link` | `When I click the "X" link` | `navigation_steps.py` |
| `Click the "X" charttab` | `When I click the "X" charttab` | `navigation_steps.py` |
| `Click the "X" charttab subtab` | `When I click the "X" charttab subtab` | `navigation_steps.py` |
| `Click the "X" sidemenu entry` | `When I click the "X" sidemenu link` | `navigation_steps.py` |
| `Click the "X" button` | `When I click the "X" button` | `navigation_steps.py` |
| `Click the "X" listview link` | `When I click the "X" listview link` | `navigation_steps.py` |
| `Type "X" in the "Y" input` | `When I type "X" in the "Y" input` | `form_steps.py` |
| `Enter "X" in the "Y" autocomplete` | `When I enter "X" in the "Y" autocomplete` | `form_steps.py` |
| `Click the "Add" listedit button` | `When I click the "Add" listedit button` | `form_steps.py` |
| `Verify exists "X" text` | `Then I should see "X" text` | `verification_steps.py` |
| `Verify exists "X" link` | `Then I should see "X" link` | `verification_steps.py` |
| `Verify exists "X" listview link` | `Then I should see "X" listview link` | `verification_steps.py` |
| `Verify !exists "X" text` | `Then I should not see "X" text` | `verification_steps.py` |
| `Navigate "?f=..."` | `Given I navigate to "?f=..."` | `login_steps.py` |

### Nested Begin Blocks → Scenario Outline or Multiple Scenarios

**Okra**:
```plaintext
Begin "Simple Search"
    Begin "Search for Jane Doe by MR"
        Navigate "?f=chart&s=pat&s=search"
        Type "10006" in the "sstring" input
        Click the "Search" button
        Verify exists "Doe, Jane" text
```

**Gherkin**:
```gherkin
@search
Feature: Simple Search
  As a user
  I want to search for patients
  So that I can find their records

  @search_by_mr
  Scenario: Search for Jane Doe by MR
    Given I navigate to "?f=chart&s=pat&s=search"
    When I type "10006" in the "sstring" input
    And I click the "Search" button
    Then I should see "Doe, Jane" text
```

### Custom XPath in Okra → Selector in YAML

**Okra with inline XPath**:
```plaintext
Click the @"MR# or EMP#" radio button@xpath='//input[@value="m"][@type="radio"]'
```

**Step 1: Add to webchart.yaml**:
```yaml
elements:
  search_mr_radio: "//input[@value='m'][@type='radio']"
```

**Step 2: Create step or use generic**:
```gherkin
When I click the "MR#" search radio button
```

```python
@when(parsers.parse('I click the "{option}" search radio button'))
def click_search_radio(page: Page, option: str):
    radios = {
        'MR#': 'search_mr_radio',
        'Name': 'search_name_radio',
        # ...
    }
    selector = get_selector('webchart', radios.get(option, option))
    page.locator(selector).first.click()
```

---

## Reusing Existing Steps

### Available Step Modules

| Module | Steps Available |
|--------|-----------------|
| `steps/login_steps.py` | Login, logout, navigation to base URL |
| `steps/navigation_steps.py` | Sidemenu, chart tabs, links, buttons |
| `steps/form_steps.py` | Input fields, autocomplete, list edit |
| `steps/access_control_steps.py` | Department management, user access |
| `steps/verification_steps.py` | Text/element visibility assertions |
| `steps/common_steps.py` | Shared utility steps |

### Check Before Creating New Steps

Before creating a new step, search existing steps:

```bash
# Search for existing step patterns
grep -r "I click" experiment2/steps/
grep -r "I type" experiment2/steps/
grep -r "I should see" experiment2/steps/
```

### Generic Steps That Handle Many Okra Commands

```python
# These steps handle most Okra commands with parameters:

@when(parsers.parse('I click the "{text}" link'))
@when(parsers.parse('I click the "{text}" button'))
@when(parsers.parse('I click the "{text}" charttab'))
@when(parsers.parse('I click the "{text}" charttab subtab'))
@when(parsers.parse('I click the "{text}" sidemenu link'))
@when(parsers.parse('I click the "{text}" listview link'))
@when(parsers.parse('I type "{value}" in the "{field}" input'))
@when(parsers.parse('I enter "{value}" in the "{field}" autocomplete'))
@then(parsers.parse('I should see "{text}" text'))
@then(parsers.parse('I should see "{text}" link'))
```

---

## Creating New Components

### When to Create a Component

Create a component when:
- Multiple scenarios interact with the same WebChart section
- Complex multi-step interactions are repeated
- You need to encapsulate page-specific logic

### Component Template

```python
"""
{SectionName} Component
Handles {description} in WebChart.

URL Patterns:
- ?f=... - Description
"""

from typing import List
from playwright.sync_api import Page

from components.base_component import BaseComponent
from support.selector_loader import get_selector


class {SectionName}Component(BaseComponent):
    """
    Component for {SectionName} section of WebChart.
    """
    
    URL_PATTERNS: List[str] = [
        '?f=...',  # Add URL patterns this component handles
    ]
    
    def navigate_to_{section}(self):
        """Navigate to {SectionName} from anywhere."""
        self.open_sidemenu()
        self.click_sidemenu_link("...")
        self.click_charttab("...")
    
    def perform_action(self, param: str):
        """Description of action."""
        selector = get_selector('webchart', 'element_name', param)
        self.page.locator(selector).first.click()
        self.wait_for_ajax()
```

### Example: Chart Search Component

```python
"""
Chart Search Component
Handles patient search functionality in WebChart.
"""

from components.base_component import BaseComponent
from support.selector_loader import get_selector


class ChartSearchComponent(BaseComponent):
    URL_PATTERNS = ['?f=chart&s=pat&s=search']
    
    def navigate_to_simple_search(self):
        """Navigate to simple search."""
        self.goto("?f=chart&s=pat&s=search&search_method=simple")
    
    def search_by_mr(self, mr_number: str):
        """Search by MR number."""
        selector = get_selector('webchart', 'search_mr_radio')
        self.page.locator(selector).first.click()
        self.type_in_input('sstring', mr_number)
        self.click_button('Search')
    
    def verify_patient_in_results(self, patient_name: str):
        """Verify patient appears in search results."""
        self.verify_text(patient_name)
```

---

## Using Playwright MCP for Navigation

### Browser Navigation with MCP

Use Playwright MCP tools to explore the page and find correct selectors:

```bash
# Navigate to a page
mcp_microsoft_pla_browser_navigate --url "https://your-webchart.com/webchart.cgi?f=admin"

# Get page snapshot to see elements
mcp_microsoft_pla_browser_snapshot

# Click an element
mcp_microsoft_pla_browser_click --element "Control Panel link" --ref "ref123"

# Type in a field
mcp_microsoft_pla_browser_type --element "search input" --ref "ref456" --text "test"
```

### Finding Selectors with MCP

1. **Take a snapshot**: `mcp_microsoft_pla_browser_snapshot`
2. **Look for element refs** in the snapshot output
3. **Test clicking/typing** with MCP tools
4. **Extract the XPath** and add to `webchart.yaml`

### Using Okra MCP for Selector Resolution

The Okra MCP can resolve element definitions:

```bash
# Get XPath for an Okra element type
mcp_my-okra-mcp_get_element_definition --element_name "link"

# Get resolved selector for specific text
mcp_my-okra-mcp_resolve_selector --element_name "link" --target_text "Control Panel"

# Explain an Okra line
mcp_my-okra-mcp_explain_okra_line --line 'Click the "Submit" button'
```

---

## Complete Migration Example

### Source: `tests/add_user_dept.okra`

```plaintext
Begin "Add a department"
    Open the sidemenu
    Click the "Control Panel" link
    Click the Access charttab
    Click the "Access Control" charttab subtab
    Click the "Add Department" link
    Type "Testing" in the input
Begin "Add one user to department upon dept creation"
    Enter "Acardi" in the "le_user_realm_le_ur_user_id_display" autocomplete
    Click the "Add" listedit button
    Click the "Submit Dept" button
    Click the "Show All" link
    Verify exists "Testing" listview link
```

### Step 1: Check/Add Selectors (`selectors/webchart.yaml`)

```yaml
elements:
  # Sidemenu (already exists)
  sidemenu_icon: "//span[@id='wc_menuicon']"
  sidemenu_entry_text: "//div[@id='wc_sidetabs']//a[@class='wc_tab'][contains(text(), '{TEXT}')]"
  
  # Chart tabs (already exists)
  charttab: "//ul[@id='wc_tabwrapper']//span[contains(@class, 'wc_tab')]//a[contains(text(), '{TEXT}')]"
  charttab_subtab: "//ul[@class='wc_tab_submenu']//a[contains(text(), '{TEXT}')]"
  
  # Links and buttons (already exists)
  link: "//a[contains(text(), '{TEXT}')]"
  button: "//input[(@type='button' or @type='submit')][contains(@value, '{TEXT}')] | //button[contains(text(), '{TEXT}')]"
  
  # List edit (already exists)
  listedit_button: "//table[contains(@class,'dlg_root')]//input[@type='button'][contains(@value, '{TEXT}')]"
  
  # Autocomplete (already exists)
  autocomplete_input_by_id: "//input[contains(@class, 'autocomplete')][@id='{TEXT}']"
  
  # Department-specific (add if missing)
  department_name_input: "input[type='text']:not([disabled])"
  add_department_link: "//a[contains(text(), 'Add Department')]"
  submit_dept_button: "//input[@type='button'][contains(@value, 'Submit')]"
```

### Step 2: Create Feature File (`features/add_user_dept.feature`)

```gherkin
@webchart @access_control
Feature: Add User Department
  As an administrator
  I want to manage departments and users
  So that I can organize access control effectively

  Background: Login and navigate to Access Control
    Given I am logged into WebChart
    And I click the "Control Panel" link
    And I click the "Access" charttab
    And I click the "Access Control" charttab subtab

  @add_department @smoke
  Scenario: Add a department and one user
    Given I delete the "Testing" department if it exists
    When I click the "Add Department" link
    And I type "Testing" in the department name input
    And I add user "Acardi" to the department
    And I click the "Submit Dept" button
    And I click the "Show All" link if visible
    Then I should see "Testing" listview link
```

### Step 3: Verify Steps Exist or Create New Ones

Check `steps/access_control_steps.py` - most steps already exist:

```python
# Already exists:
@when(parsers.parse('I add user "{username}" to the department'))
def add_user_to_department(page: Page, username: str):
    # ... handles autocomplete + Add button

@when(parsers.parse('I click the "{dept}" department edit link'))
def click_dept_edit_link(page: Page, dept: str):
    # ... handles department edit link
```

### Step 4: Run and Verify

```bash
cd experiment2
python3 -m pytest features/add_user_dept.feature --headed -v
```

---

## Okra Pod Reference

### Quick Reference: Pod Elements → YAML Selectors

| Pod File | Element | YAML Key | XPath Pattern |
|----------|---------|----------|---------------|
| `sidemenu.pod` | sidemenu | `sidemenu_icon` | `//span[@id='wc_menuicon']` |
| `sidemenu.pod` | entry | `sidemenu_entry_text` | `//a[@class='wc_tab'][contains(text(), '{TEXT}')]` |
| `sidemenu.pod` | pin | `sidemenu_pin` | `//span[@id='thumbtack']` |
| `charttab.pod` | charttab | `charttab` | `//span[contains(@class, 'wc_tab')]//a[contains(text(), '{TEXT}')]` |
| `charttab.pod` | subtab | `charttab_subtab` | `//ul[@class='wc_tab_submenu']//a[contains(text(), '{TEXT}')]` |
| `listedit.pod` | row | `listedit_row` | `//table[contains(@class,'dlg_root')]//strong[contains(text(), '{TEXT}')]` |
| `listedit.pod` | button | `listedit_button` | `//table[contains(@class,'dlg_root')]//input[@type='button'][contains(@value, '{TEXT}')]` |
| `listview.pod` | link | `listview_link` | `//table[contains(@class,'lv_root')]//a[contains(text(), '{TEXT}')]` |
| `listview.pod` | row | `listview_row` | `//table[contains(@class,'lv_root')]//td[contains(text(), '{TEXT}')]` |
| `autocomplete.pod` | input | `autocomplete_input` | `//input[contains(@class, 'autocomplete')]` |
| `_std.pod` | link | `link` | `//a[contains(text(), '{TEXT}')]` |
| `_std.pod` | text | `text` | `//*[contains(text(), '{TEXT}')]` |
| `_std.pod` | button | `button` | `//input[(@type='button' or @type='submit')][contains(@value, '{TEXT}')]` |
| `_std.pod` | input | `input` | `//input[not(@type='hidden')][@id='{TEXT}']` |
| `_std.pod` | dropdown | `dropdown` | `//select[not(@disabled)][@id='{TEXT}']` |
| `_std.pod` | checkbox | `checkbox` | `//input[@type='checkbox'][@id='{TEXT}']` |
| `_std.pod` | radio | `radio` | `//input[@type='radio'][@value='{TEXT}']` |

### Okra Verb Mapping

| Okra Verb | Gherkin Pattern | Notes |
|-----------|-----------------|-------|
| `Open the sidemenu` | `When I open the WebChart sidemenu` | Uses `@Open` verb from sidemenu.pod |
| `Close the sidemenu` | `When I close the WebChart sidemenu` | Uses `@Close` verb from sidemenu.pod |
| `Pin the sidemenu` | `When I pin the WebChart sidemenu` | Uses `@Pin` verb from sidemenu.pod |
| `Wait for AJAX` | Built into steps | Automatic in all navigation steps |

---

## Migration Checklist

Use this checklist when migrating an Okra test:

- [ ] **Read the Okra file** and understand the test flow
- [ ] **Identify all pod elements** used (sidemenu, charttab, listedit, etc.)
- [ ] **Check `selectors/webchart.yaml`** for existing selectors
- [ ] **Add missing selectors** from the pod files
- [ ] **Create the feature file** with proper Gherkin syntax
- [ ] **Check existing steps** before creating new ones
- [ ] **Create new steps** only if needed, following existing patterns
- [ ] **Create a component** if the section has complex logic
- [ ] **Run the test** with `--headed` to verify
- [ ] **Use Playwright MCP** to debug selector issues
- [ ] **Update this guide** if you add new patterns

---

## Tips for Copilot

When asked to migrate an Okra test:

1. **First read the `.okra` file** to understand the test
2. **Check existing features** in `experiment2/features/` for similar patterns
3. **Search existing steps** with `grep` before creating new ones
4. **Add selectors to `webchart.yaml`** - don't hardcode XPaths in steps
5. **Use parameterized steps** with `{TEXT}` placeholders
6. **Keep Gherkin readable** - use plain English descriptions
7. **Reuse components** from `experiment2/components/` for complex interactions
8. **Test incrementally** - run after each scenario to catch issues early
