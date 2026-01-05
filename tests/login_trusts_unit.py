from wcunittest import wcElement

def editPermission(d, value):
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
        "WHERE module_name='Control' AND category_name='Manage Login Trusts' "\
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
        "username=%s)", value, d.getUserData('username'))

def editScriptedPerm(d, value):
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
        "WHERE module_name='Control' AND category_name='Manage Scripted Rules' "\
        "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
        "username=%s)", value, d.getUserData('username'))

def goToLoginTrusts(d):
    d.navigate('?f=admin&s=login_trusts')

def main(d, WCURL):
    addLink = wcElement('text', 'Add Login Trust')
    listview = wcElement('xpath', "//span[@class='LVTitle' and text()='All Login Trusts']")

    u = d.getWCUnitTest('Verify Login Trusts Respects No Permission')
    u.setup(editPermission, 0)
    u.verifyElements([
        wcElement('xpath', """//*[contains(., "A permission level of 'Yes' is required")]"""),
    ], reason='Ensure the message shows about insufficient permission')
    u.verifyElements([
        wcElement(addLink, None, exists=False),
        wcElement(listview, None, exists=False),
    ], reason='Ensure no ui elements show for a restricted user')
    u.test(goToLoginTrusts)

    u = d.getWCUnitTest('Verify Login Trusts Respects Yes Permission')
    u.setup(editPermission, 1)
    u.setup(editScriptedPerm, 2)
    u.verifyElements([
        addLink,
        listview,
    ], reason='Ensure UI elements show for an allowed user')
    u.test(goToLoginTrusts)

