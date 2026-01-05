"""
    Tests Patient Restrictions and Emergency Access (Break the glass)
    @owners: sgrider
"""
from wcunittest import wcDBRecord, wcElement


def goToChart(d, pat_id):
    d.navigate('?f=chart&pat_id={0}'.format(pat_id))

def restrictPatient(d, opts):
    d.miedb.dbExec("INSERT INTO patient_restrictions (pat_id, user_id) VALUES "\
        "(%s, (SELECT user_id FROM users WHERE username=%s))", opts['pat_id'], opts['username'])

def main(d, WCURL):
    u = d.getWCUnitTest('Verify access to William Hart')
    u.verifyElements([
        wcElement('id', 'wc_pat_bar'),
        wcElement('xpath', "//*[contains(., 'You currently do not have access to:')]", exists=False),
        wcElement('xpath', "//*[contains(., 'E-Chart: The chart is restricted')]", exists=False),
    ], reason='Ensure chart is visible and unrestricted')
    u.test(goToChart, 18)

    u = d.getWCUnitTest('Restrict access to William Hart with an exception and verify access')
    u.setup(restrictPatient, {
        'pat_id': 18,
        'username': 'selenium',
    }, reason='Restrict William Hart with access to selenium')
    u.verifyElements([
        wcElement('id', 'wc_pat_bar', exists=True),
        wcElement('xpath', "//*[contains(., 'You currently do not have access to:')]", exists=False),
        wcElement('xpath', "//*[contains(., 'E-Chart: The chart is restricted')]", exists=False),
    ], reason='Ensure access')
    u.test(goToChart, 18)

    u = d.getWCUnitTest('Restrict access to William Hart and without an exception and verify no access')
    u.setup(lambda d: d.miedb.dbExec('DELETE FROM patient_restrictions WHERE pat_id=18 AND user_id=(SELECT user_id FROM users WHERE username="selenium")'), reason='Delete selenium exception')
    u.setup(restrictPatient, {
        'pat_id': 18,
        'username': 'nurse',
    }, reason='Restrict William Hart with access to nurse')
    u.verifyElements([
        wcElement('id', 'wc_pat_bar', exists=False),
        wcElement('xpath', "//*[contains(., 'You currently do not have access to:')]"),
        wcElement('xpath', "//*[contains(., 'E-Chart: The chart is restricted')]"),
    ], reason='Ensure no access')
    u.verifyElements([
        wcElement('xpath', "//input[contains(@value, 'emergency access')]", exists=False),
    ], reason='We do not have emergency access, so verify no way to break the glass')
    u.test(goToChart, 18)

    u = d.getWCUnitTest('Verify we get a break the glass prompt when we have the emergency access permission on a restricted patient')
    u.setup(lambda d: d.wcutils.SetPermission('E-Chart', 'Emergency Access', 1), reason='Allow emergency access')
    u.verifyElements([
        wcElement('xpath', "//input[contains(@value, 'emergency access')]"),
    ], reason='We have emergency access, so verify we get the button')
    u.test(goToChart, 18)

    u = d.getWCUnitTest('Break the glass and ensure we now have patient access')
    u.setup(goToChart, 18)
    u.setup(lambda d: d.enterFormData('break', id='appendReason'), reason='Give a reason')
    u.setup(lambda d: d.clickElement(xpath='//input[contains(@value, "emergency access")]'), reason='Click the break the glass button')
    u.verifyElements([
        wcElement('id', 'wc_pat_bar'),
        wcElement('xpath', "//*[contains(., 'You currently do not have access to:')]", exists=False),
        wcElement('xpath', "//*[contains(., 'E-Chart: The chart is restricted')]", exists=False),
    ], reason='Ensure chart is visible and unrestricted')
    u.verifyDB([
        wcDBRecord("FROM audit_log_chart WHERE event_desc='Bypassing Limited Access Permission' AND pat_id=18", {
            'ref_type': 19,
            'session_id': 'WCTESTSESSION',
            'userfname': 'selenium',
            'granted': 1,
            'event': 'View'
        }),
    ], reason='Ensure db record for audit_log_chart now exists')
    u.test(lambda d: d.clickElement(value='Yes'), reason='Confirm')

    u = d.getWCUnitTest('Verify patient restriction code checks against emergency access (use a system report to validate)')
    u.setup(lambda d: d.miedb.dbExec("""INSERT INTO system_reports (name, sql_query) VALUES ('_restrictReport', 'SELECT p.pat_id, CONCAT(p.last_name, ", ", p.first_name) FROM patients p $pat_restrict_join$ WHERE p.pat_id IN (18) $pat_restrict_where$ GROUP BY p.pat_id ORDER BY p.pat_id ASC')"""), reason='Insert the system report')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM system_reports WHERE name='_restrictReport'"), reason='Delete report')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM patient_restrictions WHERE pat_id=18"), reason='Unrestrict William Hart'            "patient_restrictions_unit.py"
)
    u.verifyElements([
        wcElement('xpath', "//td[text()='Hart, William']")
    ], reason='Ensure William Hart shows up in the list')
    u.test(lambda d: d.navigate('?f=admin&s=system_report&report_name=_restrictReport&submit_query'), reason='Run the report')
