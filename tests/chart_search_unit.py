"""
	Chart Search Unit Test
	Ensures that all available chart search forms are rendered as expected
	Verifies that search functionality works correctly
	@owners:
"""

from wcunittest import wcElement


def navSimple(d, data):
	d.navigate('?f=chart&s=pat&s=search&search_method=simple&tabmodule=patsearch')

def navDetailed(d, data):
	d.navigate('?f=chart&s=pat&s=search&search_method=detail&tabmodule=patsearch')

def clickSearch(d, data):
	d.clickElement(name="pat_search")



jdoe = wcElement('xpath', '//*[contains(.,"Doe") and contains(.,"Jane")]', exists=True)
crogers = wcElement('xpath', '//*[contains(.,"Rogers") and contains(.,"Cory")]', exists=True)
jpregnant = wcElement('xpath', '//*[contains(.,"Pregnant") and contains(.,"Jennifer")]', exists=True)
# apatel = wcElement('xpath', '//*[contains(.,"Patel") and contains(.,"Ashish")]', exists=True)
cmorrison = wcElement('xpath', '//*[contains(.,"Morrison") and contains(.,"Catherine")]', exists=True)
jgrowing = wcElement('xpath', '//*[contains(.,"Growing") and contains(.,"Joseph")]', exists=True)

def main(d, WCURL):
	u = d.getWCUnitTest('Verify Simple Search Form')
	u.setup(lambda d: d.navigate('?f=chart'), reason='Go to EChart')
	u.verifyElements([
		wcElement('xpath', "//input[@name='by' and @type='radio' and @value='m']"),
		wcElement('xpath', "//input[@name='by' and @type='radio' and @value='n']"),
		wcElement('xpath', "//input[@name='by' and @type='radio' and @value='b']"),
		wcElement('xpath', "//input[@name='by' and @type='radio' and @value='p']"),
		wcElement('xpath', "//input[@name='by' and @type='radio' and @value='d']"),
		wcElement('name', 'sstring'),
		wcElement('value', 'Search'),
	], reason='Look for standard simple search fields')
	u.test()

	u = d.getWCUnitTest('Verify Detailed Search Form')
	u.setup(lambda d: d.navigate('?f=chart'), reason='Go to EChart')
	u.setup(lambda d: d.clickElement(text='Detailed'), reason='Click the Detailed link')
	u.verifyElements([
		wcElement('name', 'name_crit'),
		wcElement('xpath', "//select[@name='name_crit']/option[@value='b' and text()='Begins With']"),
		wcElement('xpath', "//select[@name='name_crit']/option[@value='x' and text()='Exact']"),
		wcElement('name', 'last_name', size='15'),
		wcElement('name', 'first_name', size='15'),
	], reason='Verify Name Fields')
	u.verifyElements([
		wcElement('name', 'bdate_crit'),
		wcElement('xpath', "//select[@name='bdate_crit']/option[@value='e' and text()='Exact']"),
		wcElement('xpath', "//select[@name='bdate_crit']/option[@value='g' and text()='Greater Than']"),
		wcElement('xpath', "//select[@name='bdate_crit']/option[@value='l' and text()='Less Than']"),
		wcElement('xpath', "//select[@name='bdate_crit']/option[@value='b' and text()='Between']"),
		wcElement('name', 'start_bdate', size='10', maxlength='10'),
		wcElement('name', 'end_bdate', size='10', maxlength='10'),
	], reason='Verify DOB Fields')
	u.verifyElements([
		wcElement('name', 'mr_crit'),
		wcElement('xpath', "//select[@name='mr_crit']/option[@value='b' and text()='Begins With']"),
		wcElement('xpath', "//select[@name='mr_crit']/option[@value='x' and text()='Exact']"),
		wcElement('name', 'mr_sstring', size='15')
	], reason='Verify MR Number Fields')
	u.verifyElements([
		wcElement('name', 'phone_list'),
		wcElement('xpath', "//select[@name='phone_list']/option[@value='Home Phone' and text()='Home Phone']"),
		wcElement('xpath', "//select[@name='phone_list']/option[@value='Alternate Phone' and text()='Alternate Phone']"),
		wcElement('xpath', "//select[@name='phone_list']/option[@value='Mobile Phone' and text()='Mobile Phone']"),
		wcElement('xpath', "//select[@name='phone_list']/option[@value='Work Phone' and text()='Work Phone']"),
		wcElement('name', 'hphone_crit'),
		wcElement('xpath', "//select[@name='hphone_crit']/option[@value='b' and text()='Begins With']"),
		wcElement('xpath', "//select[@name='hphone_crit']/option[@value='x' and text()='Exact']"),
		wcElement('name', 'phone', size='19')
	], reason='Verify Phone Fields')
	u.verifyElements([
		wcElement('name', 'doc_crit'),
		wcElement('xpath', "//select[@name='doc_crit']/option[@value='e' and text()='Exact']"),
		wcElement('xpath', "//select[@name='doc_crit']/option[@value='b' and text()='Begins With']"),
		wcElement('name', 'docid', size='10'),
	], reason='Verify Document ID Fields')
	u.verifyElements([
		wcElement('name', 'partition'),
		wcElement('xpath', "//select[@name='partition']/option[@value='all' and text()='All']"),
	], reason='Verify Partition Fields')
	u.verifyElements([
		wcElement('name', 'chart_online'),
		wcElement('xpath', "//select[@name='chart_online']/option[@value='' and text()='All']"),
		wcElement('xpath', "//select[@name='chart_online']/option[@value='0' and text()='No']"),
		wcElement('xpath', "//select[@name='chart_online']/option[@value='1' and text()='Full']"),
		wcElement('xpath', "//select[@name='chart_online']/option[@value='2' and text()='Partial']"),
	], reason='Verify Chart Online Fields')
	u.verifyElements([
		wcElement('name', 'result_limit'),
		wcElement('xpath', "//select[@name='result_limit']/option[@value='10' and text()='10']"),
		wcElement('xpath', "//select[@name='result_limit']/option[@value='20' and text()='20']"),
		wcElement('xpath', "//select[@name='result_limit']/option[@value='40' and text()='40']"),
		wcElement('xpath', "//select[@name='result_limit']/option[@value='60' and text()='60']"),
		wcElement('xpath', "//select[@name='result_limit']/option[@value='80' and text()='80']"),
		wcElement('xpath', "//select[@name='result_limit']/option[@value='100' and text()='100']"),
	], reason='Verify Result Limit Options')
	u.verifyElements([
		wcElement('value', 'Search'),
		wcElement('value', 'Clear All'),
	], reason='Look for Search buttons')
	u.test()


	d.startSection('Simple Patient/Chart Search')

	t = d.getWCUnitTest('Simple Patient Search by MR')
	systyp = d.getUserData('systemType')
	if systyp == 'EH':
		t.setup(navSimple)
		t.setup(lambda d: d.clickElement(xpath='//label[contains(.,"EMP #")]/input[@type="radio"]'))
		t.setup(lambda d: d.enterFormData('10006', name='sstring'))
	else:
		t.setup(navSimple)
		t.setup(lambda d: d.clickElement(xpath='//label[contains(.,"MR #")]/input[@type="radio"]'))
		t.setup(lambda d: d.enterFormData('10006', name='sstring'))
	t.verifyElements([jdoe], reason='Verify Jane Doe was found by MR #')
	t.test(clickSearch)

	t = d.getWCUnitTest('Simple Patient Search by Name')
	t.setup(navSimple)
	t.setup(lambda d: d.clickElement(xpath='//label[contains(.,"Name")]/input[@type="radio"]'))
	t.setup(lambda d: d.enterFormData('roger', name='sstring'))
	t.verifyElements([crogers], reason='Verify Cory Rogers was found by Name')
	t.test(clickSearch)

	t = d.getWCUnitTest('Simple Patient Search by D.O.B')
	t.setup(navSimple)
	t.setup(lambda d: d.clickElement(xpath='//label[contains(.,"D.O.B")]/input[@type="radio"]'))
	t.setup(lambda d: d.enterFormData('07-02-1990', name='sstring'))
	t.verifyElements([crogers], reason='Verify Cory Rogers was found by D.O.B')
	t.test(clickSearch)

	t = d.getWCUnitTest('Simple Patient Search by Mobile Phone')
	t.setup(navSimple)
	t.setup(lambda d: d.clickElement(xpath='//label[contains(.,"Mobile Phone")]/input[@type="radio"]'))
	t.setup(lambda d: d.enterFormData('(617) 555-1234 ', name='sstring'))
	t.verifyElements([jpregnant], reason='Verify Jennifer Pregnant was found by Mobile Phone')
	t.test(clickSearch)

	t = d.getWCUnitTest('Simple Patient Search by Doc ID')
	t.setup(navSimple)
	t.setup(lambda d: d.clickElement(xpath='//label[contains(.,"Doc ID")]/input[@type="radio"]'))
	t.setup(lambda d: d.enterFormData('0000458', name='sstring'))
	t.verifyElements([jgrowing], reason='Verify Joseph Growing was found by Doc ID')
	t.test(clickSearch)
	d.endSection()


	d.startSection('Detailed Patient/Chart Search')

	t = d.getWCUnitTest('Detailed Patient Search by MR')
	t.setup(navDetailed)
	t.setup(lambda d: d.enterFormData('10006', name='mr_sstring'))
	t.verifyElements([jdoe], reason='Verify Jane Doe was found by MR #')
	t.test(clickSearch)

	t = d.getWCUnitTest('Detailed Patient Search by Name')
	t.setup(navDetailed)
	t.setup(lambda d: d.enterFormData('roger', name='last_name'))
	t.verifyElements([crogers], reason='Verify Cory Rogers was found by Name')
	t.test(clickSearch)
	
	t = d.getWCUnitTest('Detailed Patient Search by D.O.B')
	t.setup(navDetailed)
	t.setup(lambda d: d.enterFormData('07-02-1990', name='start_bdate'))
	t.verifyElements([crogers], reason='Verify Cory Rogers was found by D.O.B')
	t.test(clickSearch)

	t = d.getWCUnitTest('Detailed Patient Search by Home Phone')
	t.setup(navDetailed)
	t.setup(lambda d: d.enterFormData('(650) 326-2530', name='phone'))
	t.verifyElements([cmorrison], reason='Verify Catherine Morrison was found by Home Phone')
	t.test(clickSearch)

	t = d.getWCUnitTest('Detailed Patient Search by Doc ID')
	t.setup(navDetailed)
	t.setup(lambda d: d.enterFormData('0000458', name='docid'))
	t.verifyElements([jgrowing], reason='Verify Joseph Growing was found by Doc ID')
	t.test(clickSearch)
	d.endSection()






















