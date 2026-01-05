from wcunittest import wcElement, wcJSCode

def insertLayout(d, html):
    d.miedb.dbExec("REPLACE INTO layout (active, module, name, layout_html) VALUES (1, 'UnitTest', 'UnitTest', %s)", html)

def visitLayout(d):
    d.navigate('?f=layout&module=UnitTest&name=UnitTest')

def clickPicker(d):
    d.clickElement(id='start_link')

def main(d, WCURL):
    u = d.getWCUnitTest('Ensure an miedate control shows up with the expected input/defaults')
    u.setup(insertLayout, """<WCINPUT type="date" name="start">""")
    u.verifyElements([
        wcElement('id', 'startMONTH', name='startMONTH', autocomplete='off', placeholder='MM'),
        wcElement('id', 'startDAY', name='startDAY', autocomplete='off', placeholder='DD'),
        wcElement('id', 'startYEAR', name='startYEAR', autocomplete='off', placeholder='YYYY'),
    ], reason='Ensure the three inputs show up')
    u.verifyElements([
        wcElement('id', 'start_link', title='Calendar'),
    ], reason='Ensure we get a datepicker by default')
    u.verifyElements([
        wcElement('id', 'startNOW', exists=False),
        wcElement('id', 'startCLEAR', exists=False),
        wcElement('id', 'startTIME', exists=False),
    ], reason='Ensure today, clear and time inputs are not present since we did not put them in the tag')
    u.test(visitLayout)

    u = d.getWCUnitTest('Ensure an miedatetime control shows up with the expected input/defaults')
    u.setup(insertLayout, """<WCINPUT type="datetime" name="start">""")
    u.verifyElements([
        wcElement('id', 'startMONTH', name='startMONTH', autocomplete='off', placeholder='MM'),
        wcElement('id', 'startDAY', name='startDAY', autocomplete='off', placeholder='DD'),
        wcElement('id', 'startYEAR', name='startYEAR', autocomplete='off', placeholder='YYYY'),
        wcElement('id', 'startTIME', name='startTIME', autocomplete='off', title='Time'),
    ], reason='Ensure the four inputs show up')
    u.verifyElements([
        wcElement('id', 'start_link', title='Calendar'),
    ], reason='Ensure we get a datepicker by default')
    u.verifyElements([
        wcElement('id', 'startNOW', exists=False),
        wcElement('id', 'startCLEAR', exists=False),
    ], reason='Ensure today and clear inputs are not present since we did not put them in the tag')
    u.test(visitLayout)

    u = d.getWCUnitTest('Ensure an miedatetime control shows the now and clear inputs')
    u.setup(insertLayout, """<WCINPUT type="datetime" name="start" shownow="1" showclear="1">""")
    u.verifyElements([
        wcElement('id', 'startMONTH', name='startMONTH', autocomplete='off', placeholder='MM'),
        wcElement('id', 'startDAY', name='startDAY', autocomplete='off', placeholder='DD'),
        wcElement('id', 'startYEAR', name='startYEAR', autocomplete='off', placeholder='YYYY'),
        wcElement('id', 'startTIME', name='startTIME', autocomplete='off', title='Time'),
    ], reason='Ensure the four inputs show up')
    u.verifyElements([
        wcElement('id', 'start_link', title='Calendar'),
    ], reason='Ensure we get a datepicker by default')
    u.verifyElements([
        wcElement('id', 'startNOW', title='Now', type='button'),
        wcElement('id', 'startCLEAR', title='Clear', type='button'),
    ], reason='Ensure today and and clear are there')
    u.test(visitLayout)

    u = d.getWCUnitTest('Ensure the datepicker shows a calendar')
    u.setup(visitLayout)
    u.verifyElements([
        wcElement('id', 'start_cal'),
    ])
    u.test(clickPicker)

    u = d.getWCUnitTest('Ensure the datepicker closes when clicking anything outside of the calendar')
    u.setup(visitLayout)
    u.setup(clickPicker)
    u.verifyElements([
        wcElement('id', 'start_cal', exists=False),
    ])
    u.test(lambda x: x.clickElement(id='startMONTH'), reason='Just click on the month input')

    u = d.getWCUnitTest('Ensure clicking the "Today" button populates the correct values')
    u.setup(visitLayout)
    u.verifyElements([
        wcElement('id', 'startMONTH', value='02'),
        wcElement('id', 'startDAY', value='02'),
        wcElement('id', 'startYEAR', value='{}'.format(d.getUserData("run_year"))),
        wcElement('id', 'startTIME', value='09:15'),
    ], reason='Since our demo date is set, these values should be known for all time')
    u.test(lambda x: x.clickElement(id='startNOW'), reason='Click the today button')

    u = d.getWCUnitTest('Ensure clicking the "Clear" button clears everything')
    u.setup(visitLayout)
    u.verifyElements([
        wcElement('id', 'startMONTH', value=''),
        wcElement('id', 'startDAY', value=''),
        wcElement('id', 'startYEAR', value=''),
        wcElement('id', 'startTIME', value=''),
    ])
    u.test(lambda x: x.clickElement(id='startCLEAR'), reason='Click the clear button')

    u = d.getWCUnitTest('Ensure clicking a date from the datepicker populates the correct fields')
    u.setup(visitLayout)
    u.setup(clickPicker, reason='Open the calendar')
    u.verifyElements([
        wcElement('id', 'start_cal', exists=False),
    ], reason='Calendar should go away after selection')
    u.verifyElements([
        wcElement('id', 'startMONTH', value='02'),
        wcElement('id', 'startDAY', value='13'),
        wcElement('id', 'startYEAR', value='{}'.format(d.getUserData("run_year"))),
        wcElement('id', 'startTIME', value=''),
    ], reason=f'Picked the 13th, should be Feb 13, {d.getUserData("run_year")} without a time value')
    u.test(lambda x: x.clickElement(xpath="//div[@id='start_cal']//button[text()='13']"), reason='Click on the 13th')
