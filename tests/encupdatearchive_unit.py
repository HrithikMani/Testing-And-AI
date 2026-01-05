"""
This tests a specific feature in ajaxpost that will update the archived HTML document for an encounter
@owners: dcornewell
@funcdeps: AJAXPOST_EncUpdateArchivedDocument, CreateDocumentTextFromLayout
"""

from wcunittest import wcElement

def createEncounterArchive(d, data):
	d.navigate('?f=chart&s=pat&pat_id=49')
	d.clickElement(text='Add Visit')
	d.waitFor(d, lambda d: d.getElement(xpath='//div[contains(@class, "mask")]'), expected_return=False)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[contains(., "WebChart is currently working")]'), expected_return=False, timeout=30)
	d.waitFor(d, lambda d: d.getElement(xpath='//*[@class="exam_tab"]'), expected_return=True, timeout=30)

	res = d.miedb.dbQuery("SELECT MAX(encounter_id) AS `encounter_id` FROM encounters")
	if res:
		row = res.getRow(0)
		if row:
			enc_id = row['encounter_id']
		else:
			d.reportCommandStatus("Query failure", "", False, "", "Unable to find for last encounter")
			return
	else:
		d.reportCommandStatus("Query failure", "", False, "", "Unable to query for last encounter")
		return

	d.wcutils.waitForMask(expected=False, hook=True)
	d.clickElement(xpath="//div[@id='wc_encnav_buttons']/a[@title='Archive & Close']")
	d.clickElement(xpath="//div[@class='wc_win']//input[@type='button' and @value='Yes']")
	if d.wcutils.waitFor(lambda d: d.getElement(xpath='//div[contains(.,"Encounter has been closed and Archived successfully")]'), expected=True, timeout=60, comments="Wait for the encounter to archive and close"):
		d.navigate('?f=ajaxpost&s=enc_update_archived_doc&encounter_id='+ str(enc_id) +'&test=1')
	else:
		d.reportCommandStatus("Click Failure", "", False, "", "The encounter did not archive within 60s")


def main(d, WCCurl):
	# Test that updating encounter archive HTML produces the same document
	t = d.getWCUnitTest('Test feature that updates archived HTML document w/o full re-archive')
	d.startSection('Create and archive encounter then update HTML and compare')

	t.setup(createEncounterArchive)

	t.verifyFunc(lambda d: d.getElements(xpath='//*[contains(., "Re-Archived")]') is not None, d, 
	reason='Make sure we successfully updated the encounter documents')
	t.verifyFunc(lambda d: d.getElements(xpath='//*[contains(., "Re-Archived")]') is None, d, 
	reason='Make sure documents did not change')

	t.test()

	d.endSection()
