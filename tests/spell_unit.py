"""
@owners: aaronc
"""
from wcunittest import wcJSCode, wcElement, wcDBRecord
from selenium.webdriver.common.keys import Keys

def setupSpellLayout(d, data):
	d.miedb.dbExec("INSERT INTO layout SET module='Test', name='SpellCheck', active=1, layout_html='<WCENCOBSADD OBSNAME=\"MDDictation\" InputType=\"textarea\" NOTABLE=\"Y\" SETFOCUS=\"N\" ROWS=\"15\" COLUMNS=\"90\" DOS_LINK=\"0\">'")

def typeBadWords(d, data):
	d.navigate('?f=layout&module=Test&name=SpellCheck')
	d.enterFormData('Tset for splel chek', id='MDDictation')
	d.clickElement(id='MDDictation_spellcheck')
	if not d.wcutils.waitFor(lambda d: d.runJS('return wcutils._layoutOps === 0 && miehttp.isWaiting() === false'), timeout=60, comments='Wait for ajax and layoutInsert operations to complete prior to adding'):
		d.reportCommandStatus('LayoutOps', d.runJS('return wcutils._layoutOps'), None, 'isWaiting()', d.runJS('return miehttp.isWaiting()'))

def correctWords(d, data):
	box = d.waitFor(d, lambda d: d.getElement(xpath='//span[@id="speller_MDDictation_1"]/parent::div/following-sibling::div[contains(., "Test")]'), expected_return=True, timeout=30)
	if not box:
		d.reportCommandStatus('Timeout', '', False, '', 'Spell choices for Tset were not displayed')
		return False
	else:
		spellBox = d.getElement(id='speller_comm_input')
		spellBox.send_keys('1')
	
	box = d.waitFor(d, lambda d: d.getElement(xpath='//span[@id="speller_MDDictation_2"]/parent::div/following-sibling::div[contains(., "spell")]'), expected_return=True, timeout=30)
	if not box:
		d.reportCommandStatus('Timeout', '', False, '', 'Spell choices for splel were not displayed')
		return False
	else:
		spellBox = d.getElement(id='speller_comm_input')
		spellBox.send_keys(Keys.ENTER)

	box = d.waitFor(d, lambda d: d.getElement(xpath='//span[@id="speller_MDDictation_3"]/parent::div/following-sibling::div[contains(., "check")]'), expected_return=True, timeout=30)
	if not box:
		d.reportCommandStatus('Timeout', '', False, '', 'Spell choices for chek were not displayed')
		return False
	else:
		spellBox = d.getElement(id='speller_comm_input')
		spellBox.send_keys(Keys.DOWN + Keys.DOWN + Keys.DOWN + Keys.ENTER)

def main(d, WCURL):
	t = d.getWCUnitTest('Check for misspelled words')
	t.setup(setupSpellLayout)
	t.setup(typeBadWords)
	t.verifyElements([
		wcElement('id', 'speller_MDDictation_1'),
		wcElement('id', 'speller_MDDictation_2'),
		wcElement('id', 'speller_MDDictation_3')
	], reason='Make sure we caught three misspelled words.')
	t.test()

	t = d.getWCUnitTest('Correct misspelled words')
	t.setup(typeBadWords)
	t.setup(correctWords)
	t.verifyJS([
		wcJSCode('document.getElementById("MDDictation").value', 'Test for spell check')
	], reason="Make sure final spelling is correct")
	t.test()
