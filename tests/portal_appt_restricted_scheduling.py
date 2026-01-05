from selenium import webdriver
import requests
from datetime import date
import re

def main (d, WCURL):
	d.wcutils.insertWCTSession('employee')
	d.clickElement(xpath="//a[contains(., 'Better Corp.')]")

	todaysdate = date.today()
	nextyear = todaysdate.year + 1
	testday = 10 - date(nextyear, 2, 1).weekday()

	pat_id = d.runJS('return pat_id')

	postdata = "f=ajaxpost&s=apt&apptdata_xml=%3CAPPTS%3E%3CAPT%20pat_id%3D%22"
	postdata = postdata + pat_id
	postdata = postdata + "%22%20apt_id%3D%22%22%20email_pat%3D%221%22%20attach_ics%3D%221%22%20location%3D%22OFFICE%22%20res_id%3D%22-1%22%20startdate%3D%22"
	postdata = postdata + str(nextyear) + "-02-" + str(testday)
	postdata = postdata + "%2009%3A00%3A00%22%20comment%3D%22%22%20duration%3D%2210%22%20pat_duration%3D%2210%22%20enddate%3D%220000-00-00%2000%3A00%3A00%22%3E%3CAPTTYPE%20code%3D%22BP%22%20%2F%3E%3CRESOURCE%20user_id%3D%2216%22%20%2F%3E%3C%2FAPT%3E%3C%2FAPPTS%3E&email_pat=1&layout_name=Apt%20Confirmation&attach_ics=1&nosched_unk_pat=1&session_id=WCTESTSESSION"

	baseurl = d._base_urls[-1] + '/webchart.cgi'

# Go to portal and try to schedule, verify we do NOT return this error when days out is not set.

	d.miedb.dbExec("UPDATE patient_extended_values SET value = '' WHERE ext_id = (SELECT ext_id FROM patient_extended_index WHERE name = 'nmcmd_days_out_to_search');")

	r = requests.post(baseurl, data = postdata)

	lt = re.compile('<')
	gt = re.compile('>')

	resultText = gt.sub('&gt;', lt.sub('&lt;', r.text))

	p = re.compile(r'Appointment is too far in the future')

	# <wcajaxpost><error message="You do not have access to this patient: pat_id [82]. Permission code (3)"> </error></wcajaxpost>
	if p.search(resultText):
		d.screenshot()
		d.reportCommandStatus("HTTP response invalid (error when not configured)",resultText,False,'','')

# Configure portal with this limitation

	d.miedb.dbExec("UPDATE patient_extended_values SET value = '30' WHERE ext_id = (SELECT ext_id FROM patient_extended_index WHERE name = 'nmcmd_days_out_to_search');")
	d.miedb.dbExec("UPDATE patient_extended_values SET value = '1' WHERE ext_id = (SELECT ext_id FROM patient_extended_index WHERE name = 'nmcmd_sched_disable_calendar');")

# Go to portal and try to schedule, verify you get this error

	r = requests.post(baseurl, data = postdata)

	resultText = gt.sub('&gt;', lt.sub('&lt;', r.text))

	if not p.search(resultText):
		d.screenshot()
		d.reportCommandStatus("HTTP response invalid (error message not detected)",resultText,False,'','')
