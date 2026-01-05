"""
    Unit Tests for System Reports
    @owners: mpierzchala
    @filedeps: src/system_report.*,jsbin/system_report_editor.js
"""
from wcunittest import wcElement
from selenium.webdriver.common.keys import Keys


def editPermission(d, value):
    d.miedb.dbExec(
        "UPDATE security_role_acl SET security_value=%s "
        "WHERE module_name='Control' AND category_name='Manage System Reports' "
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "
        "username=%s)",
        value,
        d.getUserData("selenium_username"),
    )
    d.wcutils.flushMemcache()


def openReport(d, data):
    d.navigate("?f=layout&module=SystemReport&name=Editor&tabmodule=admin&t=System+Report&report_name={0}".format(data["name"]))
    d.wcutils.waitForAJAX(timeout=60, quiet=5)
    d.wcutils.waitForEle(expected=False, xpath="//div[contains(@class,'blockUI')]", timeout=60)
    d.wcutils.waitForEle(expected=True, id="editorPane", timeout=60)
    d.wcutils.waitForEle(expected=False, xpath="//div[contains(@class,'blockUI')]", timeout=60)
    if data.get("wait_for_content", True):
        # assumption: report has content - wait until it loads
        d.wcutils.waitForEle(expected=True, xpath="//div[contains(@class,'cm-content')]//div[contains(@class,'cm-line')]//span")

def editReport(d):
    d.clickElement(id="save")
    d.wcutils.waitForAJAX(timeout=60, quiet=5)


def executeReport(d):
    d.clickElement(id="run")
    d.wcutils.waitForAJAX(timeout=60, quiet=5)


def addRestriction(d):
    user = "Acardi, Sergio"

    report_info_tab = "//div[@id='infoPane']//a[contains(., 'Report Info')]"
    d.wcutils.waitForEle(xpath=report_info_tab,timeout=60)
    d.clickElement(xpath=report_info_tab)
    d.clickElement(xpath=report_info_tab)  # to ensure report info tab was clicked

    add_user_input = "//*[@id='metadata' and not(contains(@style, 'display: none'))]//*[@id='addUserTxt']"
    d.wcutils.waitForEle(xpath=add_user_input,timeout=60)
    d.wcutils.waitForEle(expected=True, xpath=add_user_input, timeout=60)

    d.runJS('arguments[0].scrollIntoView(true)', d.getElement(xpath=add_user_input))

    d.enterFormData(user, id="addUserTxt", blur=False)
    d.getElement(id="addUserTxt").send_keys(Keys.DOWN)
    ddl = "//*[contains(@class, 'ui-menu-item-wrapper') and text()='{0}']".format(user)
    d.wcutils.waitForEle(xpath=ddl, timeout=60)
    d.clickElement(xpath=ddl)
    d.clickElement(id="save")
    d.wcutils.waitForAJAX(timeout=60, quiet=5)


def insertReport(d, data):
    sql = "REPLACE INTO system_reports (%s) VALUES (%s)" % (
        ",".join(data.keys()),
        ",".join(["%s"] * len(data)),
    )
    d.miedb.dbExec(sql, *data.values())
    d.wcutils.SetSystemSetting("System", "WebChart", "All Reports Table Update Time", "0", False)


def main(d, WCURL):
    report_name = "unitTestReport"
    report_content = "SELECT 1"
    # Manage System Reports: No
    u = d.getWCUnitTest("No Permission (Run)")
    u.setup(insertReport, {"name": report_name, "sql_query": report_content})
    u.setup(editPermission, 0)

    u.setup(openReport, {"name": report_name, "wait_for_content": False})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]"),
            wcElement("xpath", "//*[contains(., 'Enter new report name')]"),
            wcElement("id", "resultsGrid_gridContainer", exists=False),
        ],
        reason="Looking for non-existent report view",
    )
    u.test(executeReport)

    u = d.getWCUnitTest("No Permission (Edit)")
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]"),
            wcElement("xpath", "//*[contains(., 'Enter new report name')]"),
        ],
        reason="Looking for non-existent report view",
    )
    u.test(editReport)

    # Manage System Reports: Run only
    # Realtime: 0
    u = d.getWCUnitTest("Run Only Permission (Run)")
    u.setup(
        insertReport, {"name": report_name, "sql_query": report_content, "realtime": "0"}
    )
    u.setup(editPermission, 1)
    u.setup(openReport, {"name": report_name, "wait_for_content": False})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]", exists=False),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]"),
            wcElement("id", "resultsGrid_gridContainer", exists=False),
        ],
        reason="User does not have the ability to run the report in the new version, this is done through legacy editor",
    )
    u.test(executeReport)

    u = d.getWCUnitTest("Run Only Permission (Edit)")
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]"),
            wcElement("xpath", "//input[@disabled and @id='realtime']"),
        ],
    )
    u.test(editReport)

    # Realtime: 1
    u = d.getWCUnitTest("Run Only Permission (Run)")
    u.setup(
        insertReport, {"name": report_name, "sql_query": report_content, "realtime": "1"}
    )
    u.setup(editPermission, 1)
    u.setup(openReport, {"name": report_name})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]", exists=False),
            wcElement("xpath","//*[contains(., 'You do not have permission to add/edit reports')]"),
            wcElement("id", "resultsGrid_gridContainer", exists=False),
        ],
        reason="User does not have the ability to run the report in the new version, this is done through legacy editor",
    )

    u = d.getWCUnitTest("Run Only Permission (Edit)")
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]"),
            wcElement("xpath", "//input[@disabled and @id='realtime']"),
            wcElement("xpath", "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]",exists=False),
        ],
    )
    u.test(editReport)

    # Manage System Reports: Add/Edit
    # Realtime: 0
    u = d.getWCUnitTest("Add/Edit Permission, Realtime: 0 (Run)")
    u.setup(
        insertReport, {"name": report_name, "sql_query": report_content, "realtime": "0"}
    )
    u.setup(editPermission, 2)
    u.setup(openReport, {"name": report_name})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]", exists=False),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]",exists=False),
            wcElement("id", "resultsGrid_gridContainer"),
        ],
    )
    u.test(executeReport)

    u = d.getWCUnitTest("Add/Edit Permission, Realtime: 0 (Edit)")
    u.verifyElements(
        [
            wcElement("id", "editorPane"),
            wcElement("xpath", "//input[@disabled and @id='realtime']"),
            wcElement("xpath", "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=False),
            wcElement("xpath", "//*[contains(., 'No changes have been made, nothing to save')]"),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]", exists=False),
        ],
    )
    u.test(editReport)

    u = d.getWCUnitTest("Add/Edit Permission, Realtime: 0 (Add restrictions)")
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'Only Allowed Users/Realms section was updated')]",),
        ],
    )
    u.test(addRestriction)

    # Realtime: 1
    u = d.getWCUnitTest("Add/Edit Permission, Realtime: 1 (Run)")
    u.setup(
        insertReport, {"name": report_name, "sql_query": report_content, "realtime": "1"}
    )
    u.setup(openReport, {"name": report_name})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]", exists=False),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]"),
            wcElement("id", "resultsGrid_gridContainer", exists=False),
        ],
    )
    u.test(executeReport)

    u = d.getWCUnitTest("Add/Edit Permission, Realtime: 1 (Edit)")
    u.verifyElements(
        [
            wcElement("id", "editorPane"),
            wcElement("xpath", "//input[@disabled and @id='realtime']"),
            wcElement("xpath", "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]"),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]"),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'No changes have been made, nothing to save')]", exists=False),
        ],
    )
    u.test(editReport)

    u = d.getWCUnitTest("Add/Edit Permission, Realtime: 1 (Add restrictions)")
    u.setup(openReport, {"name": report_name})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]"),
        ],
    )
    u.test(addRestriction)

    # Manage System Reports: Add/Edit Realtime
    # Realtime: 0
    u = d.getWCUnitTest("Realtime Permission, Realtime: 0 (Run)")
    u.setup(editPermission, 3)
    u.setup(
        insertReport, {"name": report_name, "sql_query": report_content, "realtime": "0"}
    )
    u.setup(openReport, {"name": report_name})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]", exists=False),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]", exists=False),
            wcElement("id", "resultsGrid_gridContainer"),
        ],
    )
    u.test(executeReport)

    u = d.getWCUnitTest("Realtime Permission, Realtime: 0 (Edit)")
    u.verifyElements(
        [
            wcElement("id", "editorPane"),
            wcElement("xpath", "//input[not(@disabled) and @id='realtime']"),
            wcElement("xpath", "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=False),
            wcElement("xpath", "//*[contains(., 'No changes have been made, nothing to save')]"),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]", exists=False),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
        ],
    )
    u.test(editReport)

    u = d.getWCUnitTest("Realtime Permission, Realtime: 0 (Add restrictions)")
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'Only Allowed Users/Realms section was updated')]"),
        ],
    )
    u.test(addRestriction)

    # Realtime: 1
    u = d.getWCUnitTest("Realtime Permission, Realtime: 1 (Run)")
    u.setup(
        insertReport, {"name": report_name, "sql_query": report_content, "realtime": "1"}
    )
    u.setup(openReport, {"name": report_name})
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'No such report')]", exists=False),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]", exists=False),
            wcElement("id", "resultsGrid_gridContainer"),
        ],
    )
    u.test(executeReport)

    u = d.getWCUnitTest("Realtime Permission, Realtime: 1 (Edit)")
    u.verifyElements(
        [
            wcElement("id", "editorPane"),
            wcElement("xpath", "//input[not(@disabled) and @id='realtime']"),
            wcElement("xpath", "//*[contains(., 'This is currently realtime, but you do not have access to save it as realtime')]", exists=False),
            wcElement("xpath", "//*[contains(., 'No changes have been made, nothing to save')]"),
            wcElement("xpath", "//*[contains(., 'You do not have permission to add/edit reports')]", exists=False),
            wcElement("xpath", "//*[contains(., 'Are you sure you want to do this?')]", exists=False),
        ],
    )
    u.test(editReport)

    u = d.getWCUnitTest("Realtime Permission, Realtime: 1 (Add restrictions)")
    u.verifyElements(
        [
            wcElement("xpath", "//*[contains(., 'Only Allowed Users/Realms section was updated')]"),
        ],
    )
    u.test(addRestriction)
