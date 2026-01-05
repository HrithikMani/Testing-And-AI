"""
Unit test to verify behavior of the layout based virtual waiting room
@owners: dcornewell
@filedeps: system/layouts/No Login/VirtualWaitingRoom.html
@funcdeps: virtWaitingRoomAllowedIn, virtWaitingRoom, virtWaitingRoomRemoveFromQueue, virtWaitingRoomGetQueue, virtWaitingRoomSetQueue, virtWaitingRoomAddToQueue, virtWaitingRoomRemoveFromQueue
"""
from wcunittest import wcElement
import json

def logout(d, WCURL):
	d.navigate(WCURL.LOGOUT)

def setMaxLogins(d, maxLogins):
    d.wcutils.SetSystemSetting('System', 'Virtual Waiting Room', 'Portal Max Active Logins', maxLogins, False)

def insertLogins(d, numLogins):
	# clear our test logins, leaving one for the test
	d.miedb.dbExec("DELETE FROM logins WHERE session_id!='WCTESTSESSION'")
	d.miedb.dbExec("INSERT INTO logins (session_id,user_id,login_dt) SELECT UUID(),user_id, (SELECT value FROM system_settings WHERE item='Demo Date') FROM users WHERE status=1 LIMIT %d" % (numLogins))

def goToPortal(d, queueToken=None):
	# If we have a queue token, we need to append it in the URL
	if queueToken:
		d.navigate('?f=layout&name=Home&pat_id=42&svar_cobrand_patid=43&cobrand_patid=43&module=Patient+Portal&queue_token=%s' % queueToken)
	else:
		d.navigate('?f=layout&name=Home&pat_id=42&svar_cobrand_patid=43&cobrand_patid=43&module=Patient+Portal')

def goToPortalWithToken(d, data):
	# Get and parse the queue. Grab the first token
	# JSON will look like this: { "queue": [ { "queue_token": "a8f7cef4-3ce1-4a91-899d-e28d07eeb89b", "queued_dt": "2025-04-05 09:03:28", "admitted_dt": "2025-04-05 09:05:24" } ] }
	res = d.miedb.dbQuery("SELECT value FROM system_settings WHERE module='System' AND section='Virtual Waiting Room' AND item='Queue Data'");
	if res:
		if res.getRow(0) and res.getRow(0)['value']:
			queue = json.loads(res.getRow(0)['value'])
			if queue and 'queue' in queue and len(queue['queue']) > 0:
				queueToken = queue['queue'][0]['queue_token']
				# Now we can go to the portal with the token
				goToPortal(d,queueToken)
	else:
		d.reportCommandStatus('GetUserID', '', False, '', d.miedb.dbError())

def main(d, WCURL):
	t = d.getWCUnitTest('Confirm users land in virtual queue when there are too many logins')
	t.setup(logout, WCURL)
	t.setup(setMaxLogins, '10')
	t.setup(insertLogins, 11)
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"YOU ARE IN THE QUEUE")]'),
	], reason='Verify we landed on the virtual queue page')
	t.test(goToPortal)

	t = d.getWCUnitTest('Confirm queued user goes back to queue when there are too many logins')
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"YOU ARE IN THE QUEUE")]'),
	], reason='Verify we landed on the virtual queue page')
	t.test(goToPortalWithToken)

	t = d.getWCUnitTest('Confirm users land in virtual queue when there are users in the queue ahead of them')
	# 9 logins + 1 queued user = 10 logins
	t.setup(insertLogins, 9)
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"YOU ARE IN THE QUEUE")]'),
	], reason='Verify we landed on the virtual queue page')
	t.test(goToPortal)

	t = d.getWCUnitTest('Confirm user in the queue goes to login when there is room')
	t.setup(insertLogins, 6)
	t.verifyElements([
		wcElement('xpath', '//*[contains(.,"Username")]'),
	], reason='Verify we landed on the login')
	t.test(goToPortalWithToken)
