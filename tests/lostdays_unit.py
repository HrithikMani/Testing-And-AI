"""
	@owner: aaronc
"""
from wcunittest import wcElement, wcDBRecord

SELENIUM_USER_ID = 8

def goToReport(d):
	d.navigate('?f=layout&s=pat&module=SystemReport&name=OSHA+Log&tabmodule=reports&t=Safety&search=1')

def insertAccommodation(d, start_date, end_date):
	if not d.miedb.dbExec("INSERT INTO accommodations (pat_id, accom_type, status, start_date, end_date) VALUES "\
		"(18, 5, 1, '{0}', '{1}')".
		format(start_date, end_date)):
		d.reportCommandStatus('DB Statement Failed', d.miedb.dbError(), False, '', '')
	else:
		d.miedb.dbExec("INSERT IGNORE INTO incident_links (inc_id, link_id, module) SELECT 1, accom_id, 16 FROM accommodations WHERE pat_id = 18")
		d.miedb.dbExec("UPDATE incidents SET days_away=-1, days_restricted=-1 WHERE inc_id = 1")


def insertRestriction(d, start_date, end_date):
	if not d.miedb.dbExec("INSERT INTO patient_clinical_restriction (pat_id, type_id, active, start_date, end_date, affect_work) VALUES "\
		"(18, 1, 1, '{0}', '{1}', 1)".
		format(start_date, end_date)):
		d.reportCommandStatus('DB Statement Failed', d.miedb.dbError(), False, '', '')
	else:
		d.miedb.dbExec("INSERT IGNORE INTO incident_links (inc_id, link_id, module) SELECT 1, cr_id, 9 FROM patient_clinical_restriction WHERE pat_id = 18")
		d.miedb.dbExec("UPDATE incidents SET days_away=-1, days_restricted=-1 WHERE inc_id = 1")
	
def verifyDays(wcunit, restricted_days, lost_days):
	wcunit.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell"][contains(., "{0}")]'.format(restricted_days), exists=True),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell"][contains(., "{0}")]'.format(lost_days), exists=True)
	], reason='Ensure correct counts')

def main(d, WCURL):
	# Turn off demo date so the lost days routine doesn't think things are in the future
	d.miedb.dbExec("DELETE FROM system_settings WHERE module='WebChart' AND "\
				"section='Demo' AND item='Demo Date'")
	d.miedb.dbExec("UPDATE users SET pwd_expire=DATE_ADD(CURDATE(), INTERVAL 1 YEAR) "\
				"WHERE user_id={0}".format(SELENIUM_USER_ID))
	# Remove Lost Time entry from patient_clinical_restriction
	d.miedb.dbExec("DELETE FROM patient_clinical_restriction WHERE type_option='Lost Time'")
	# Update the login date to now since the demo data has been removed
	d.miedb.dbExec("UPDATE logins SET login_dt=NOW() WHERE session_id = 'WCTESTSESSION'")

	wcunit = d.getWCUnitTest('Validate one accomodation on the day of incident')
	wcunit.setup(lambda d: insertAccommodation(d, '2015-09-10 11:30:00', '2015-09-10 23:59:00'), reason="Add a single accommodation on date of incident")
	verifyDays(wcunit, 0, 0)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate one restriction')
	wcunit.setup(lambda d: insertRestriction(d, '2019-02-01', '2019-02-07'), reason="Add a single restriction")
	verifyDays(wcunit, 7, 0)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate non-overlapping restrictions')
	wcunit.setup(lambda d: insertRestriction(d, '2019-02-14', '2019-02-15'), reason="Add a distinct restriction")
	verifyDays(wcunit, 9, 0)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate overlapping restrictions')
	wcunit.setup(lambda d: insertRestriction(d, '2019-02-05', '2019-02-09'), reason="Add an overlapping restriction")
	verifyDays(wcunit, 11, 0)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate restrictions with same dates')
	wcunit.setup(lambda d: insertRestriction(d, '2019-02-14', '2019-02-15'), reason="Add a restriction with identical dates")
	verifyDays(wcunit, 11, 0)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate one accommodation')
	wcunit.setup(lambda d: insertAccommodation(d, '2019-01-01', '2019-01-07'), reason="Add a single lost time record")
	verifyDays(wcunit, 11, 7)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate non-overlapping accommodations')
	wcunit.setup(lambda d: insertAccommodation(d, '2019-01-14', '2019-01-15'), reason="Add a distinct accommodation")
	verifyDays(wcunit, 11, 9)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate overlapping accommodations')
	wcunit.setup(lambda d: insertAccommodation(d, '2019-01-05', '2019-01-09'), reason="Add an overlapping accommodation")
	verifyDays(wcunit, 11, 11)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate accommodations with same dates')
	wcunit.setup(lambda d: insertRestriction(d, '2019-01-14', '2019-01-15'), reason="Add an accommodation with identical dates")
	verifyDays(wcunit, 11, 11)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate accommodations overwriting restriction')
	wcunit.setup(lambda d: insertAccommodation(d, '2019-02-08', '2019-02-10'), reason="Add an overlapping accommodation")
	verifyDays(wcunit, 9, 14)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate accommodations overwriting a whole restriction')
	wcunit.setup(lambda d: insertAccommodation(d, '2019-02-13', '2019-02-15'), reason="Add an overlapping accommodation")
	verifyDays(wcunit, 7, 17)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate accommodations splitting a restriction')
	wcunit.setup(lambda d: insertRestriction(d, '2019-01-12', '2019-01-17'), reason="Add a splitting accommodation")
	verifyDays(wcunit, 11, 17)
	wcunit.test(goToReport)

	wcunit = d.getWCUnitTest('Validate accommodation overlapping multiple restrictions')
	wcunit.setup(lambda d: insertRestriction(d, '2019-03-01', '2019-03-03'), reason="Add a new restriction")
	wcunit.setup(lambda d: insertRestriction(d, '2019-03-05', '2019-03-07'), reason="Add a distinct restriction")
	wcunit.setup(lambda d: insertAccommodation(d, '2019-03-02', '2019-03-06'), reason="Add an overlapping accommodation")
	verifyDays(wcunit, 13, 22)
	wcunit.test(goToReport)
