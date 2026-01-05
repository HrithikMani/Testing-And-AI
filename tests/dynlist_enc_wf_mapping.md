# Test Mapping: `selenium/tests/dynlist_enc_wf.okra`

This document maps the high-level Okra test commands used in `dynlist_enc_wf.okra` to their underlying actions and implementations.

## Overview

The test file uses the **Okra** framework, a keyword-driven testing tool built on top of Selenium and Python.
- **Keywords**: Natural language-like commands (e.g., `Click`, `Type`, `Verify`).
- **Direct Execution**: Lines starting with `@` execute Python code directly against the `driver` object.
- **Structure**: Tests are organized into blocks using `Begin "..."`.

## Command Mapping

| Command Pattern | Description | Underlying Implementation (Inferred) |
| :--- | :--- | :--- |
| `Begin "Title"` | Starts a new logical test block/step. | `okra.py` parser logs the step start. |
| `@Description@driver.method(...)` | Executes a Python method on the driver. | Direct Python `eval` or execution. |
| `Open the sidemenu` | Opens the application's side navigation menu. | `driver.find_element(...)` + `.click()` on the menu icon. |
| `Click the "X" sidemenu entry` | Clicks a specific link in the side menu. | Finds link with text "X" in the menu container and clicks it. |
| `Type "X" into the Y input` | Types text "X" into an input field identified by "Y". | `driver.find_element(name/id=Y).send_keys(X)` |
| `Click the Search button` | Clicks the button labeled "Search". | `driver.find_element(xpath="//button[text()='Search']").click()` |
| `Open the quicklink list` | Opens a list of quick links. | Clicks the quicklink toggle element. |
| `Click the X quicklink` | Clicks a specific quick link. | Finds link with text "X" in quicklinks and clicks it. |
| `Select "X" from the Y field` | Selects option "X" from a dropdown "Y". | `Select(driver.find_element(name/id=Y)).select_by_visible_text(X)` |
| `Click the Save button` | Clicks the "Save" button. | `driver.find_element(xpath="//button[text()='Save']").click()` |
| `Click the Logout sidemenu entry` | Logs out via the side menu. | Clicks the "Logout" link in the side menu. |
| `Wait for ajax` | Waits for all AJAX requests to complete. | `driver.wcutils.waitForAJAX()` |
| `Wait for page` | Waits for the page load to complete. | `driver.wcutils.waitForPageLoad()` |
| `Switch to Encounters Window` | Switches focus to a popup window. | `driver.switchToPopup()` |
| `Close this window` | Closes the current popup. | `driver.closePopup()` |
| `Verify exists "X" text` | Verifies that text "X" is present on the page. | `driver.verifyTextPresent("X")` or `wcUnitTest.verifyElements` |
| `Verify !exists "X" ...` | Verifies that "X" is NOT present. | `driver.verifyElementNotPresent(...)` |
| `Unmask dynamicsection` | Unmasks a dynamic section in the UI. | Specific UI interaction to remove an overlay/mask. |
| `Add "X" "Y" quicklist item` | Adds item "Y" from quicklist group "X". | Complex interaction: finds group X, item Y, clicks "Add". |
| `Prescribe "X" "Y" dynamicitem` | Prescribes medication Y from section X. | Interaction with the prescription module UI. |
| `Order "X" "Y" dynamicitem` | Orders item Y from section X. | Interaction with the ordering module UI. |
| `Remove "X" "Y" dynamicitem` | Removes item Y from section X. | Clicks "Remove" icon for the specific item. |
| `Advance the dynamicsection` | Moves to the next section in a workflow. | Clicks "Next" or "Continue" button. |
| `Toggle the "X" quicklist` | Expands/collapses quicklist "X". | Clicks the header of the quicklist. |

## Detailed Line-by-Line Analysis (First 100 Lines)

### Setup & Preferences
```okra
Begin "Turn on the needed settings"
	@Set the ICD10Calculator preference to Icon@driver.wcutils.SetPreference('{selenium_username}', 'E-Chart', 'Conditions', 'ICD10 Calculator', 1)
    ...
```
- **Action**: Sets user preferences directly in the database/backend using `driver.wcutils.SetPreference`.
- **Purpose**: Ensures the environment is configured correctly for the test (e.g., enabling ICD10 Calculator).

### Data Setup
```okra
Begin "Add unconfirmed conditions to test with later"
	@Add UnconfirmedCondition1@driver.miedb.dbExec("INSERT INTO ...")
    ...
```
- **Action**: Executes SQL `INSERT` statements via `driver.miedb.dbExec`.
- **Purpose**: Seeds the database with specific patient conditions needed for the test scenarios.

### Employee Check-in
```okra
Begin "Employee Checks in Christine Harris to the Waiting Room"
	Open the sidemenu
	Click the "E-Chart" sidemenu entry
	Type "Harris, Christine" into the sstring input
	Click the Search button
    ...
```
- **Action**: Simulates a user (Employee) logging in, searching for a patient, and checking them into the "Waiting Room".
- **Key Steps**:
    - Navigation via Side Menu.
    - Patient Search (`sstring` input).
    - Quicklink navigation (`Checkin`).
    - Dropdown selection (`Station`).

### Receptionist Workflow
```okra
Begin "Login as Receptionist to Move Patient to a Visit Encounter"
	@Setup WCTestSession for Reception@driver.wcutils.insertWCTSession('{reception_username}')
    ...
	Click the "Open" grid link
	@Switch to Encounters Window@driver.switchToPopup()
	Select Visit from the DEI_visit_type dropdown
    ...
```
- **Action**: Switches session to "Receptionist", opens the patient's record from the grid, and converts the check-in to a "Visit".
- **Key Steps**:
    - Session switching (`insertWCTSession`).
    - Grid interaction (`Click the "Open" grid link`).
    - Popup handling (`switchToPopup`, `closePopup`).

### Nurse Workflow - Vitals & Dynamic Sections
```okra
Begin "Nurse Begins the Visit Encounter"
	@Setup WCTestSession for Nurse@driver.wcutils.insertWCTSession('{nurse_username}')
    ...
	Begin "Fill Out Dynamic Sections"
		@Switch windows@driver.switchToPopup()
		Begin "Encounter"
			@Wait for the dynamic encounter section to open@driver.wcutils.waitForAJAX(30)
			Begin "Tasking"
				Click the "Add Task" icon
                ...
```
- **Action**: Nurse logs in, moves patient to "Exam Room 1", and starts filling out the encounter.
- **Key Steps**:
    - **Tasking**: Adds a task within the encounter (`Click the "Add Task" icon`, `Type ...`, `Enter ... date`).
    - **Smart Plan**: Interacts with the "Smart Plan" section to add problems, prescribe meds, and place orders.
        - `Add "Smart Plan:Problem List" "Anxiety" quicklist item`
        - `Prescribe "Smart Plan" "Anxiety" dynamicitem`

## Specific Function Implementations

### Database Actions
- **Syntax**: `@...@driver.miedb.dbExec("SQL")`
- **Implementation**: Uses `selenium/extensions/miedb.py`. Connects to the MySQL database and executes the provided query.

### Wait Actions
- **Syntax**: `Wait for ajax` or `@Wait@driver.pause(5)`
- **Implementation**:
    - `Wait for ajax`: Checks `jQuery.active` or similar JS flags to ensure no pending requests.
    - `driver.pause(N)`: Simple `time.sleep(N)`.

### Dynamic Items (Add/Prescribe/Order)
- **Syntax**: `Action "Section" "Item" dynamicitem`
- **Implementation**: These are likely high-level abstractions in the Okra parser or specific helper functions that:
    1.  Locate the "Section" (e.g., "Smart Plan").
    2.  Search for the "Item" (e.g., "Anxiety").
    3.  Perform the specific action (Click "Add", "Prescribe" icon, etc.).

### Verification
- **Syntax**: `Verify exists "Text"`
- **Implementation**: Scans the DOM for the specified text. If not found, the test fails.
