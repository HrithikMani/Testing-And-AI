
from wcunittest import wcElement

MODULE = 'wcunit'
NAME = 'CountryCodes'
LAYOUT = """
<WCPATDATAENTRY field="country" type="country" />
<WCPATDATAENTRY field="state" type="state" />
<WCPATDATAENTRY field="zip_code" type="zip" />
"""

def gotoLayout(d, pat_id):
    d.navigate('?f=layout&module={0}&name={1}{2}'.format(
        MODULE, NAME, '&pat_id={0}'.format(pat_id) if pat_id else ''))

def selectCountry(d, country):
    d.wcutils.waitForAJAX(timeout=60, quiet=30)
    d.enterFormData(country, id='DPI_country')
    d.wcutils.waitForAJAX(timeout=60, quiet=30)

def selectState(d, state):
    d.wcutils.waitForAJAX(timeout=60, quiet=30)
    d.enterFormData(state, id='DPI_state')
    d.wcutils.waitForAJAX(timeout=60, quiet=30)

def enterZip(d, zip):
    d.wcutils.waitForAJAX(timeout=60, quiet=30)
    d.enterFormData(zip, id='DPI_zip_code')
    d.wcutils.waitForAJAX(timeout=60, quiet=30)

def insertLayout(d, layout):
    d.wcutils.insertLayout(layout)

def main(d, wcurl):
    u = d.getWCUnitTest('Verify state has nothing when no country selected')
    u.setup(insertLayout, {
        'module': MODULE,
        'name': NAME,
        'layout_html': LAYOUT
    })
    u.setup(gotoLayout)
    u.verifyElements(wcElement('xpath', "//option[text()='No provinces available']"), reason='Check for no results')
    u.test(selectCountry, '', reason='Select no country')

    u = d.getWCUnitTest('Verify state results for known country')
    u.setup(gotoLayout)
    u.verifyElements(wcElement('xpath', "//option[text()='Indiana']"), reason='Verify indiana shows up')
    u.test(selectCountry, 'United States', reason='Select USA baby')

    u = d.getWCUnitTest('Verify state results for known country')
    u.setup(gotoLayout)
    u.verifyElements(wcElement('xpath', "//option[text()='Nordurland vestra']"), reason='Check for iceland state')
    u.test(selectCountry, 'Iceland', reason='Ice Ice Baby')

    u = d.getWCUnitTest('Verify nothing shows for a country with no provinces')
    u.setup(gotoLayout)
    u.verifyElements(wcElement('xpath', "//option[text()='No provinces available']"), reason='Check for no results')
    u.test(selectCountry, 'Aruba')

    u = d.getWCUnitTest('Verify zip code auto-completion works')
    u.setup(gotoLayout)
    u.setup(selectCountry, 'United States', reason='Ensure we already have the US')
    u.verifyElements(wcElement('xpath', "//option[text()='Indiana']"), reason='Ensure Indiana auto-populates for state')
    u.test(enterZip, '46815')

