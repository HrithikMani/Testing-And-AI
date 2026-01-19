# Okra to Playwright Test Converter

This project converts Okra DSL tests (`.okra` files) to Playwright Python tests using an MCP (Model Context Protocol) server and GitHub Copilot.

## Project Structure

```
experiment1/
├── generated_tests/          # Generated Playwright tests
│   ├── conftest.py           # pytest fixtures (login/logout)
│   └── test_*.py             # Generated test files
├── okra_mcp/                  # MCP server for Okra element lookups
│   ├── server.py             # MCP server implementation
│   ├── pod_loader.py         # Loads .pod element definitions
│   └── requirements.txt      # Python dependencies
└── README.md
```

## Prerequisites

1. **Python 3.9+** installed
2. **Playwright** installed:
   ```bash
   pip install pytest-playwright playwright
   playwright install chromium
   ```
3. **VS Code** with GitHub Copilot extension

## Running Tests

### Run all tests
```bash
cd /Users/hkonda/mie/Testing-And-AI
python3 -m pytest experiment1/generated_tests/ -v
```

### Run a specific test
```bash
python3 -m pytest experiment1/generated_tests/test_add_user_dept.py -v
```

### Run tests in headed mode (visible browser)
```bash
python3 -m pytest experiment1/generated_tests/test_add_user_dept.py -v --headed
```

### Run tests with slow motion
```bash
python3 -m pytest experiment1/generated_tests/test_add_user_dept.py -v --headed --slowmo=500
```

## Setting Up the Okra MCP Server

The Okra MCP server provides element lookups from `.pod` files to help convert Okra DSL to Playwright selectors.

### 1. Install dependencies
```bash
cd experiment1/okra_mcp
pip install -r requirements.txt
```

### 2. Configure VS Code MCP
Add to your VS Code settings (`.vscode/mcp.json` or settings.json):
```json
{
  "servers": {
    "my-okra-mcp": {
      "type": "stdio",
      "command": "python3",
      "args": ["/Users/hkonda/mie/Testing-And-AI/experiment1/okra_mcp/server.py"],
      "env": {}
    }
  }
}
```

### 3. Restart VS Code
After configuring, restart VS Code to activate the MCP server.

---

## Converting Okra Tests to Playwright

### Prompt for GitHub Copilot Agent

Copy and paste the following prompt to GitHub Copilot in VS Code (Agent mode) to convert an Okra test:

---

**PROMPT TO CONVERT OKRA TEST TO PLAYWRIGHT:**

```
I need you to convert an Okra DSL test file to a Playwright Python test. Follow these steps:

## Step 1: Read the Okra Test File
Read the Okra test file at: `tests/<filename>.okra`

## Step 2: Understand Okra DSL Syntax
Okra DSL uses these patterns:
- `begin "<section name>"` - Start a test section (becomes a comment)
- `click <element> "<text>"` - Click an element with text
- `enter "<text>" <element>` - Type text into a field
- `verify exists "<text>" <element>` - Assert element is visible
- `@<variable>` - Reference a variable defined earlier

## Step 3: Use the Okra MCP Tools
For each element reference in the Okra file, use these MCP tools:
- `mcp_my-okra-mcp_get_element_definition` - Get the XPath for an element type
- `mcp_my-okra-mcp_resolve_selector` - Get a ready-to-use selector for element + text
- `mcp_my-okra-mcp_explain_okra_line` - Explain variables and selectors in a line

## Step 4: Generate Playwright Test
Create a Playwright test file with:
1. Import statements: `from playwright.sync_api import Page, expect`
2. Helper functions for autocomplete fields (WebChart requires `press_sequentially` with delay)
3. Test function: `def test_<name>(page: Page):`
4. Navigation and actions using Playwright locators
5. Assertions using `expect()`

## Step 5: Handle WebChart-Specific Patterns
- **Autocomplete fields**: Use `press_sequentially(text, delay=50)` to trigger dropdown, then click the listbox option
- **Charttabs**: Use XPath like `//ul[@id="wc_tabwrapper"]//span[contains(@class, "wc_tab")]/*[contains(@class, "wc_tab_title")][contains(., "TabName")]`
- **Subtabs**: Use XPath like `//ul[@class="wc_tab_submenu"]//a[contains(., "SubtabName")]`
- **Listview links**: Use XPath like `//table[contains(@class,"lv_root")]/tbody//a[contains(., "Text")]`
- **Wait for network**: Add `page.wait_for_load_state("networkidle")` after navigation

## Step 6: Add Cleanup Logic
For idempotent tests, add cleanup at the beginning AND end:
- Check if test data exists and delete it before creating
- Delete test data at the end to leave system clean

## Step 7: Save the Test
Save the generated test to: `experiment1/generated_tests/test_<name>.py`

## Step 8: Run and Fix
Run the test with `python3 -m pytest experiment1/generated_tests/test_<name>.py -v --headed`
If it fails, debug using the Playwright MCP browser tools and fix the selectors.

---

Now convert this Okra file: `tests/<filename>.okra`
```

---

### Example Conversion

**Okra DSL (`tests/add_user_dept.okra`):**
```okra
begin "Add a department"
click link "Control Panel"
click charttab "Access"
click charttab_subtab "Access Control"
click link "Add Department"
enter "Testing" input
```

**Playwright Python (`test_add_user_dept.py`):**
```python
from playwright.sync_api import Page, expect

def test_add_user_dept(page: Page):
    # Begin "Add a department"
    page.get_by_role("link", name="Control Panel").click()
    page.wait_for_load_state("networkidle")
    
    # Click the Access charttab
    page.click('xpath=//ul[@id="wc_tabwrapper"]//span[contains(@class, "wc_tab")]/*[contains(@class, "wc_tab_title")][contains(., "Access")]')
    
    # Click the "Access Control" charttab subtab
    page.click('xpath=//ul[@class="wc_tab_submenu"]//a[contains(., "Access Control")]')
    page.wait_for_load_state("networkidle")
    
    # Click the "Add Department" link
    page.click('text="Add Department"')
    
    # Type "Testing" in the input
    page.locator('input:visible').first.fill("Testing")
```

---

## Troubleshooting

### Test fails with "strict mode violation"
- Multiple elements match the locator
- Add `.first` to the locator or make the selector more specific

### Autocomplete doesn't trigger
- Use `press_sequentially(text, delay=50)` instead of `fill()`
- Add `page.wait_for_timeout(800)` after typing
- Click the option from `page.get_by_role('listbox').get_by_role('option').first`

### Modal overlay blocks click
- Wait for loading overlays to disappear
- Add `page.wait_for_load_state("networkidle")`

### Element not found
- Use the Playwright MCP browser tools to inspect the page
- Take a snapshot with `mcp_microsoft_pla_browser_snapshot`
- Find the correct ref and selector

---

## MCP Tools Reference

### Okra MCP Tools
| Tool | Description |
|------|-------------|
| `mcp_my-okra-mcp_get_element_definition` | Get XPath for an element type (e.g., 'link') |
| `mcp_my-okra-mcp_resolve_selector` | Get selector for element + text (e.g., 'link', 'Save') |
| `mcp_my-okra-mcp_explain_okra_line` | Explain a full Okra line |

### Playwright MCP Tools
| Tool | Description |
|------|-------------|
| `mcp_microsoft_pla_browser_navigate` | Navigate to a URL |
| `mcp_microsoft_pla_browser_snapshot` | Get page accessibility tree |
| `mcp_microsoft_pla_browser_click` | Click an element |
| `mcp_microsoft_pla_browser_type` | Type into an element |
| `mcp_microsoft_pla_browser_fill_form` | Fill multiple form fields |

---

## License

Internal use only - Medical Informatics Engineering
