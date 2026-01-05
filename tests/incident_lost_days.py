"""
@owners: aaronc
@filedeps: system/upgrade/dbroutines/wc_incident_lost_days.sql
"""

from wcunittest import wcElement, wcDBRecord
from datetime import datetime, timedelta

def setupIncident(d):
	d.miedb.dbExec(f'INSERT INTO incidents (inc_id, pat_id, case_number, case_type, inc_datetime, verified, osha_work_related, osha_completed_dt, status) VALUES ("10", "18", "S2020-0001", "Injury", "{d.getUserData("seven_years_one_day_behind")}", "Yes", "Yes", "{d.getUserData("seven_years_one_day_behind")}", 1)')


def setupRestriction(d, args):
	res = d.miedb.dbExec('INSERT INTO patient_clinical_restriction (pat_id, type_id, type_option, affect_work, occ_wc, start_date, end_date) VALUES ("18", "4", "No Climbing stairs", 1, 1, "{0}", "{1}")'.format(args[0], args[1]))
	d.miedb.dbExec('INSERT INTO incident_links (inc_id, link_id, module) VALUES ("10", %s, 9)', res.lastrowid)


def setupAccommodation(d, args):
	res = d.miedb.dbExec('INSERT INTO accommodations (pat_id, accom_type, start_date, end_date) VALUES ("18", "5", "{0}", "{1}")'.format(args[0], args[1]))
	d.miedb.dbExec('INSERT INTO incident_links (inc_id, link_id, module) VALUES ("10", %s, 16)', res.lastrowid)

def goToOSHALog(d):
	d.navigate('?f=layout&s=pat&module=SystemReport&name=OSHA+Log&tabmodule=reports&t=Safety&search=1&case_number=S2020-0001')


def cleanupRestrictions(d):
	d.miedb.dbExec("DELETE FROM patient_clinical_restriction WHERE pat_id = 18")
	d.miedb.dbExec("DELETE FROM accommodations WHERE pat_id = 18")


def main(d, WCURL):
	t = d.getWCUnitTest('Lost Days Only')
	t.setup(setupIncident) # Incident date 2020-02-01
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ]) # 59 days, make sure date of incident is excluded
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"59")]'),
	], reason='Check that 59 lost days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Restricted Days Only')
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ]) # 59 days, make sure date of incident is excluded
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"59")]'),
	], reason='Check that 59 restricted days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Permanent Restriction Started Over 180 Days Ago')
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind')}", "0000-00-00" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"180")]'), # Cap of 180 days
	], reason='Check that 180 restricted days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	res = d.miedb.dbQuery("SELECT value FROM system_settings WHERE module='WebChart' AND section='Demo' AND item='Demo Date'")
	if not res:
		d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
		return
	if not res.getRow(0) or not res.getRow(0)['value']:
		d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
		return
	demo_date = res.getRow(0)['value']
	perm_start_date = (datetime.strptime(demo_date, '%Y-%m-%d %H:%M:%S') - timedelta(days=10)).strftime('%Y-%m-%d')
	t = d.getWCUnitTest('Permanent Restriction Started Recently with No End Date')
	t.setup(setupRestriction, [ perm_start_date, "0000-00-00" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"11")]'),
	], reason='Check that 11 restricted days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost then Restricted Days')
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ]) # 59 days, make sure date of incident is excluded
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind_two_month_ahead')}", f"{d.getUserData('seven_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"59")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"30")]'),
	], reason='Check lost and restricted days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Restricted then Lost Days')
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ])
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind_two_month_ahead')}", f"{d.getUserData('seven_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"59")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"30")]'),
	], reason='Check restricted and days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost overlapping Restricted Days')
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ])
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind_one_month_ahead')}", f"{d.getUserData('seven_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"59")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"30")]'),
	], reason='Check lost and restricted days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Restricted overlapping Lost Days')
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ])
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind_one_month_ahead')}", f"{d.getUserData('seven_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"28")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"61")]'),
	], reason='Check restricted and days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost then Restricted Days cap')
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ])
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind_two_month_ahead')}", f"{d.getUserData('six_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"59")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"121")]'),
	], reason='Check lost and restricted days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Restricted then Lost Days cap')
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')}" ])
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind_one_month_ahead')}", f"{d.getUserData('six_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"28")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"152")]'),
	], reason='Check restricted and days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('180 Restricted days then Lost Days')
	t.setup(setupRestriction, [ f"{d.getUserData('seven_years_one_day_behind')}", f"{d.getUserData('six_years_behind_one_month_twentynine_days_ahead')}" ])
	t.setup(setupAccommodation, [ f"{d.getUserData('six_years_one_day_behind_two_month_ahead')}", f"{d.getUserData('six_years_behind_two_month_twentyeight_day_ahead')}" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"180")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"1")]'),
	], reason='Check restricted and lost days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost Day only on incident')
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind')} 11:20:00", f"{d.getUserData('seven_years_one_day_behind')} 23:59:00" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"0")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"0")]'),
	], reason='Check restricted and lost days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost Days in the future')
	t.setup(setupAccommodation, [ f"{d.getUserData('one_month_behind_twentynine_day_ahead')} 11:20:00", f"{d.getUserData('six_day_ahead')} 23:59:00" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"0")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"3")]'),
	], reason='Check restricted and lost days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost Days start in the future')
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_day_behind')} 11:20:00", f"{d.getUserData('seven_years_behind_one_month_twentynine_days_ahead')} 23:59:00" ])
	t.setup(setupAccommodation, [ f"{d.getUserData('one_month_ahead_one_day_behind')} 11:20:00", f"{d.getUserData('one_month_twentyeight_day_ahead')} 23:59:00" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"0")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"59")]'),
	], reason='Check restricted and lost days are counted')
	t.teardown(cleanupRestrictions)
	t.test()

	t = d.getWCUnitTest('Lost Days end before incident date')
	t.setup(setupAccommodation, [ f"{d.getUserData('seven_years_one_month_one_day_behind')} 11:20:00", f"{d.getUserData('seven_years_one_month_behind_twentythree_day_ahead')} 23:59:00" ])
	t.setup(goToOSHALog)
	t.verifyElements([
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Restricted_cell" and contains(.,"0")]'),
		wcElement('xpath', '//td[@class="OSHA_20300_Days_20Away_20from_20work_cell" and contains(.,"0")]'),
	], reason='Check restricted and lost days are counted')
	t.teardown(cleanupRestrictions)
	t.test()
