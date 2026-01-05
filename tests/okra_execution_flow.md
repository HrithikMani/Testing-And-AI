# Okra Test Execution Flow

This document explains how `.okra` test files are executed in the Python environment, how the `@` syntax works, and how standard actions are processed.

## 1. High-Level Execution Architecture

The execution is driven by `selenium/wctest.py`, which uses the `okra` library (a custom internal or installed package) to parse and run the tests.

1.  **Entry Point**: `selenium/wctest.py` is the main runner.
2.  **Initialization**: It initializes an `Okra` object, pointing it to the "Pod" definitions directory (`selenium/okrapods/webchart`).
    ```python
    # selenium/wctest.py
    o = okra.Okra(podPath=os.path.join(os.path.dirname(__file__), 'okrapods', 'webchart'))
    ```
3.  **Test Loading**: It loads the specific `.okra` file using `o.getTest(...)`.
4.  **Execution**: It calls `t.run()` on the loaded test object.

## 2. Line-by-Line Execution

The `okra` library processes the test file **line by line**. It acts as an interpreter.

### A. The `@` Syntax (Direct Python Execution)

Lines starting with `@` are treated as **Direct Python Injection**.

*   **Syntax**: `@Description Text@python_code`
*   **How it works**:
    1.  The parser identifies the line starts with `@`.
    2.  It splits the line at the second `@`.
    3.  The first part is used as a log message/step description ("Description Text").
    4.  The second part (`python_code`) is executed directly using Python's `eval()` or `exec()` within the context of the test runner.
    5.  The `driver` object is available in this context, allowing access to Selenium methods and extensions (like `driver.wcutils`, `driver.miedb`).

**Example**:
```okra
@Set preference@driver.wcutils.SetPreference('user', 'section', 'item', 'value')
```
*   **Execution**: The runner logs "Set preference" and then executes `driver.wcutils.SetPreference(...)`.

### B. Keyword Commands (Click, Type, Open, etc.)

Lines that look like natural language (e.g., `Click the "Save" button`) are parsed into **Subject**, **Verb**, and **Objects**.

*   **Syntax**: `Verb [the] Subject [objects/parameters]`
*   **Resolution Process**:
    1.  **Identify Subject**: The parser looks for the "Subject" of the sentence (e.g., `sidemenu`, `button`, `input`).
    2.  **Pod Lookup**: It searches the loaded `.pod` files (in `selenium/okrapods/webchart`) for a definition matching the Subject.
        *   *Example*: `Open the sidemenu` -> Looks for `sidemenu` in `sidemenu.pod`.
    3.  **Verb Matching**:
        *   **Custom Verbs**: If the `.pod` file defines a specific block for the Verb (e.g., `@Open` in `sidemenu.pod`), it executes the sequence of commands defined in that block.
            *   *Example*: `Open the sidemenu` triggers the `@Open` block in `sidemenu.pod`, which runs `driver.wcutils.waitForAJAX`, verifies the icon exists, and clicks it.
        *   **Standard Actions**: If no custom Verb is defined, it falls back to standard Selenium actions mapped to the Verb (e.g., `Click` -> `element.click()`, `Type` -> `element.send_keys()`).
    4.  **Element Location**:
        *   The `.pod` files define **XPath locators** for the Subjects.
        *   *Example*: `sidemenu` maps to `//span[@id="wc_menuicon"]`.
        *   Placeholders like `{OKRA_TEXT}` are replaced by the parameters provided in the command (e.g., `Click the "Save" button` -> "Save" replaces `{OKRA_TEXT}` in the generic `button` locator).

## 3. Detailed Flow Example

**Command**: `Click the "E-Chart" sidemenu entry`

1.  **Parse**:
    *   **Verb**: `Click`
    *   **Subject**: `sidemenu entry` (mapped to `entry` in `sidemenu.pod`)
    *   **Parameter**: `"E-Chart"`
2.  **Lookup**:
    *   Finds `entry` definition in `sidemenu.pod`:
        ```perl
        entry://div[@id="wc_sidetabs"].../a[@class="wc_tab"]
        ```
    *   (Note: The actual definition might be more complex or rely on text matching).
3.  **Action**:
    *   Since `sidemenu.pod` doesn't define a special `@Click` block for `entry`, it uses the standard `Click` action.
    *   It constructs the XPath to find the element containing "E-Chart".
    *   It calls `driver.find_element(xpath=...).click()`.

## 4. Summary of Action Types

| Action Type | Example | Mechanism |
| :--- | :--- | :--- |
| **Direct Python** | `@Wait@driver.pause(5)` | Executes `driver.pause(5)` directly. |
| **Custom Verb** | `Open the sidemenu` | Executes the `@Open` block defined in `sidemenu.pod`. |
| **Standard UI** | `Click the "Save" button` | Finds element matching `button` definition with text "Save", then calls `.click()`. |
| **Form Input** | `Type "Hello" into ...` | Finds input element, calls `.send_keys("Hello")`. |
| **Verification** | `Verify exists "Text"` | Checks DOM for element/text presence. |

