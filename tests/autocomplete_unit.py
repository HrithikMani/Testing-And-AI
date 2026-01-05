from wcunittest import wcElement, wcJSCode, wcDBRecord

def insertLayout(unit, html):
    res = unit.getDriver().miedb.dbExec("REPLACE INTO layout (active, module, name, layout_html) VALUES (1, 'UnitTest', 'UnitTest', %s)", html)
    return {
        'layout': ('lay_id', res.lastrowid)
    }

def insertPatient(unit, pat):
    d = unit.getDriver()
    ret = {
        'patients': None,
        'patient_partitions': None,
        'patient_mrns': None
    }
    sql = "REPLACE INTO patients (%s) VALUES (%s)" %(','.join(pat.keys()),
        ','.join(['%s'] * len(pat)))
    res = d.miedb.dbExec(sql, *pat.values())
    ret['patients'] = ('pat_id', res.lastrowid)
    d.miedb.dbExec("REPLACE INTO patient_partitions (wc_partition, name, active) VALUES "\
        "('UnitTest', 'UnitTest', 1)")
    ret['patient_partitions'] = ('id', res.lastrowid)
    d.miedb.dbExec("REPLACE INTO patient_mrns (wc_partition, mrnumber, pat_id) VALUES "\
        "('UnitTest', %s, (SELECT pat_id FROM patients WHERE last_name=%s AND first_name=%s))",
        pat['first_name'][-1], pat['last_name'], pat['first_name'])
    ret['patient_mrns'] = ('id', res.lastrowid)
    return ret

def dbDeletes(unit, udata):
    data = unit.getSetupData()
    for d in data:
        for table, idx in d.items():
            unit.getDriver().miedb.dbExec("DELETE FROM {table} WHERE {column}={id}".format(**{
                'table': table,
                'column': idx[0],
                'id': idx[1]
            }))

def visitLayout(unit):
    unit.getDriver().navigate('?f=layout&module=UnitTest&name=UnitTest')

def enterText(unit, text):
    unit.getDriver().enterFormData(text, id='pat_id_patac_input', blur=False)

def selectPat(unit, idx):
    unit.getDriver().clickElement(id='pat_id_patac_span_choices_%d' %idx)

def insertTestingPatients(u):
    u.setup(insertPatient, {
        'last_name': 'UnitTester',
        'first_name': 'Tester1',
    }, reason='Insert a patient to search for')
    u.setup(insertPatient, {
        'last_name': 'UnitTester',
        'first_name': 'Tester2',
    }, reason='Insert a patient to search for')
    u.setup(insertPatient, {
        'last_name': 'UnitTester',
        'first_name': 'Tester3',
    }, reason='Insert a patient to search for')
    u.setup(insertPatient, {
        'last_name': 'UnitTester',
        'first_name': 'Tester4',
    }, reason='Insert a patient to search for')

def main(d, WCURL):
    with d.getWCUnitTest('Ensure that WCSEARCHPATAC tag generates a patient autocomplete') as u:
        u.setup(insertLayout, """<WCSEARCHPATAC norecent="1" patvar="pat_id">""")
        u.verifyElements([
            wcElement('id', 'pat_id_patac_input'),
            wcElement('id', 'pat_id_patac_span'),
        ], reason='Ensure the required elements appear')
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test(visitLayout)

    with d.getWCUnitTest('Ensure that the autocomplete returns results for expected patients',
        timeout=30) as u:
        u.setup(insertLayout, """<WCSEARCHPATAC norecent="1" patvar="pat_id">""")
        insertTestingPatients(u)
        u.setup(visitLayout)
        u.verifyElements([
            wcElement('id', 'pat_id_patac_span_choices'),
            wcElement('id', 'pat_id_patac_span_choices_0', text='UnitTester, Tester1*'),
            wcElement('id', 'pat_id_patac_span_choices_1', text='UnitTester, Tester2*'),
            wcElement('id', 'pat_id_patac_span_choices_2', text='UnitTester, Tester3*'),
            wcElement('id', 'pat_id_patac_span_choices_3', text='UnitTester, Tester4*'),
        ], reason='Look for the patients we just inserted')
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test(enterText, 'UnitTe', reason='Enter this text without blurring the input')

    with d.getWCUnitTest('Selecting a choice should populate a hidden input and make the choices go away',
        timeout=30) as u:
        u.setup(insertLayout, """<WCSEARCHPATAC norecent="1" patvar="pat_id">""")
        insertTestingPatients(u)
        u.setup(visitLayout)
        u.setup(enterText, 'UnitTe', reason='Getting the results to show up')
        # MIEDriver needs to support lambdas in verifyAttribute
    #    u.verifyElements([
    #        wcElement('id', 'pat_id', value=lambda x: x>0),
    #    ], reason='pat_id input should be populated')
        u.verifyJS([
            wcJSCode("pat_id_patac.GetData('pat_id')", lambda x: x > 0),
            wcJSCode("pat_id_patac.GetData('first_name')", 'Tester1'),
        ], reason='Verify the pat_id and displayed values are correct')
        u.verifyJS([
            wcJSCode('pat_id_patac.IsBoxOpen()', False),
        ], reason='Ensure the choices box is closed and no longer showing')
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test(selectPat, 0, reason='Select the first entry for Tester1')

    with d.getWCUnitTest('Ensure the autocomplete fires an onblur handler',
        timeout=30) as u:
        u.setup(insertLayout, """<WCSEARCHPATAC norecent="1" patvar="pat_id"
            onblur="var ele = document.createElement('input'); ele.id = 'UnitTest_dynamic_ele';
            ele.value = 'This was generated from the blur event'; document.body.appendChild(ele);
            window['UnitTest_dynamic_js'] = 'I am a global variable generated from the blur event';">""")
        insertTestingPatients(u)
        u.setup(visitLayout)
        u.setup(enterText, 'UnitTe', reason='Getting the results to show up')
        u.verifyElements([
            wcElement('id', 'UnitTest_dynamic_ele', value='This was generated from the blur event')
        ])
        u.verifyJS([
            wcJSCode('UnitTest_dynamic_js', 'I am a global variable generated from the blur event')
        ])
        u.teardown(dbDeletes, reason='DB Cleanup')
        u.test(selectPat, 0, reason='Select the first entry for Tester1')
