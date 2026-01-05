#
# Webchart ICE UnitTest
#
from wcunittest import wcElement
import wcutils
from datetime import date

def createChart(unit, data):
    sql = "INSERT INTO patients (%s) VALUES (%s)" %(','.join(data['patients'].keys()),
        ','.join(['%s'] * len(data['patients'])))
    d = unit.getDriver()
    res = d.miedb.dbExec(sql, *data['patients'].values())
    data['patient_mrns']['pat_id'] = str(res.lastrowid)

    sql = "INSERT INTO patient_mrns (%s) VALUES (%s)" %(','.join(data['patient_mrns'].keys()),
        ','.join(['%s'] * len(data['patient_mrns'])))
    res = d.miedb.dbExec(sql, *data['patient_mrns'].values())
    return data['patient_mrns']['pat_id']

def createInjectDocument(unit, data):
    document = {
        'service_date': data['document']['service_date'],
        'storage_type': '12',
        'pat_id': unit.getSetupData()[0],
        'doc_type': 'INJECT',
        'user_id': '8'
    }
    sql = "INSERT INTO documents (%s) VALUES (%s)" %(','.join(document.keys()),
        ','.join(['%s'] * len(document)))
    d = unit.getDriver()
    res = d.miedb.dbExec(sql, *document.values())

    data['injection']['doc_id'] = str(res.lastrowid)

    sql = "INSERT INTO injections (%s) VALUES (%s)" %(','.join(data['injection'].keys()),
        ','.join(['%s'] * len(data['injection'])))
    res = d.miedb.dbExec(sql, *data['injection'].values())
    return data['injection']['doc_id']

def main (driver, WCURL):
    """
    Verifies that the ICE integration works and displays data
    """
    d = driver

    # Get the system demo date
    res = d.miedb.dbQuery("SELECT value FROM system_settings WHERE module='WebChart' AND section='Demo' AND item='Demo Date'");
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['value']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    demo_date = res.getRow(0)['value']
    # Check the birthdate on Joseph Growing
    res = d.miedb.dbQuery("SELECT UNIX_TIMESTAMP(birth_date) AS 'birth_date' FROM patients WHERE pat_id=27");
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['birth_date']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    birth_date = res.getRow(0)['birth_date']
    # Get the injections document date range for Joseph Growing
    res = d.miedb.dbQuery("SELECT UNIX_TIMESTAMP(min(service_date)) AS 'start_date',UNIX_TIMESTAMP(MAX(service_date)) AS 'end_date' FROM documents WHERE pat_id=27 AND storage_type=12");
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['start_date']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    low_date = res.getRow(0)['start_date']
    high_date = res.getRow(0)['end_date']
    ld = date.fromtimestamp(low_date);
    hd = date.fromtimestamp(high_date);
    bd = date.fromtimestamp(birth_date);

    with d.getWCUnitTest('ICE Query') as u:
        u.verifyElements([
        wcElement('xpath',"//span/label[contains(., 'Created Document')]"),
        wcElement('xpath',"//span/label[contains(., 'Queue ID')]")
        ])
        # d.reportCommandStatus('Information','',False,'bd: {0} vs ld: {1}'.format(bd,ld),'')
        if ld and bd > ld:
            # adjust Joseph Growing's birthdate to coincide with his injection documents (This way, if they're ever fixed in the snapshot I don't have to fix this test too.)
            u.setup(lambda u: u.getDriver().miedb.dbExec("UPDATE patients SET birth_date=DATE_SUB(birth_date, INTERVAL (YEAR(birth_date)-YEAR(FROM_UNIXTIME({0}))) year) WHERE pat_id=27".format(low_date)),reason='Fix DOB to match Injection Documents')

        u.setup(lambda u: u.getDriver().pause(7), reason='Let the query respond')
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=queryimport&pat_id=27&qry_module=Immunizations&qry_name=ForecastICEQuery&xslt_module=Immunizations&xslt_name=ICEXMLtoSQL&system_id=ICE'),reason='Process the Query operation')

    # Get the id of the queue entry we just created
    res = d.miedb.dbQuery("SELECT MAX(queue_id) as `queue_id` FROM injection_queue WHERE pat_id=27 AND queue_type='frc' AND status='C'");
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['queue_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    queue_id = res.getRow(0)['queue_id']

    # Get the id of the document we just uploaded
    res = d.miedb.dbQuery("SELECT MAX(doc_id) as `doc_id` FROM documents WHERE storage_type=34");
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['doc_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    doc_id = res.getRow(0)['doc_id']

    with d.getWCUnitTest('ICE Results Display') as u:
        u.verifyElements([
        # ensure the immunization groups are well represented
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Hep B Vaccine Group')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Hib Vaccine Group')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'MMR Vaccine Group')]"),
        # ensure that an immunization group contains the age at immunization, the recommendation and the time-frame for the immunization.
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Hib Vaccine Group')]/following-sibling::td[contains(.,'4M 5D')]"),
        # uncomment once we figure out testing issue wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'DTP Vaccine Group')]/following-sibling::td[contains(.,'Between:')]")
        # ensure that it's the Polio Vaccine Group showing the Between message since that is the injection from ICE that has a note
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Polio Vaccine Group')]/following-sibling::td[contains(.,'Due Now.')]")
        ])
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=pat&pat_id=27&v=inject&injopp=forecast&queue_id={0}'.format(queue_id)),reason='View the output layout')

    with d.getWCUnitTest('ICE Document Display') as u:
        u.verifyElements([
        # ensure the immunization groups are well represented
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Hep B Vaccine Group')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Hib Vaccine Group')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'MMR Vaccine Group')]"),
        # ensure that an immunization group contains the age at immunization, the recommendation and the time-frame for the immunization.
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Hib Vaccine Group')]/following-sibling::td[contains(.,'4M 5D')]"),
        # uncomment once we figure out testing issue wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'DTP Vaccine Group')]/following-sibling::td[contains(.,'Between:')]")
        # ensure that it's the Polio Vaccine Group showing the Between message since that is the injection from ICE that has a note
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Polio Vaccine Group')]/following-sibling::td[contains(.,'Due Now.')]")
        ])
        if ld and bd > ld:
            u.teardown(lambda u: u.getDriver().miedb.dbExec("UPDATE patients SET birth_date=FROM_UNIXTIME({0}) WHERE pat_id=27".format(birth_date)))

        u.test(lambda u: u.getDriver().navigate('?f=chart&s=doc&doc_id={0}'.format(doc_id)),reason='View the ICE Results as a Document')

    with d.getWCUnitTest('Realistic History - Patient Setup') as u:
        u.setup(createChart, {
            'patients': {
                'last_name': 'Smith',
                'first_name': 'John',
                'birth_date': '2004-06-16',
                'sex': 'M'
            },
            'patient_mrns': {
                'wc_partition': 'MIE',
                'mrnumber': '111999000'
            }
        }, reason='Create Test Patient')

        ipv_injection = {
            'inject_code': '10',
            'description': 'IPV'
        }
        dtap_injection = {
            'inject_code': '20',
            'description': 'DTaP'
        }
        mmr_injection = {
            'inject_code': '03',
            'description': 'MMR'
        }
        mmr_injection = {
            'inject_code': '03',
            'description': 'MMR'
        }
        varicella_injection = {
            'inject_code': '21',
            'description': 'Varicella'
        }
        hepb_injection = {
            'inject_code': '08',
            'description': 'Hep-B'
        }
        hepa_injection = {
            'inject_code': '31',
            'description': 'Hep-A'
        }
        prevnar_injection = {
            'inject_code': '100',
            'description': 'Prevnar-7'
        }
        # IPV
        u.setup(createInjectDocument, {'document': {'service_date': '2004-09-22'}, 'injection': ipv_injection}, reason='IPV Injection')
        # DTaP
        u.setup(createInjectDocument, {'document': {'service_date': '2004-10-21'}, 'injection': dtap_injection}, reason='DTaP Injection')
        # DTaP
        u.setup(createInjectDocument, {'document': {'service_date': '2004-11-11'}, 'injection': dtap_injection}, reason='DTaP Injection')
        # DTaP
        u.setup(createInjectDocument, {'document': {'service_date': '2004-12-02'}, 'injection': dtap_injection}, reason='DTaP Injection')
        # IPV
        u.setup(createInjectDocument, {'document': {'service_date': '2005-03-22'}, 'injection': ipv_injection}, reason='IPV Injection')
        # MMR
        u.setup(createInjectDocument, {'document': {'service_date': '2005-06-17'}, 'injection': mmr_injection}, reason='MMR Injection')
        # DTaP
        u.setup(createInjectDocument, {'document': {'service_date': '2006-03-13'}, 'injection': dtap_injection}, reason='DTaP Injection')
        # Varicella #1
        u.setup(createInjectDocument, {'document': {'service_date': '2006-03-20'}, 'injection': varicella_injection}, reason='Varicella Injection')
        # Hep-B
        u.setup(createInjectDocument, {'document': {'service_date': '2006-05-22'}, 'injection': hepb_injection}, reason='Hep-B Injection')
        # Hep-B
        u.setup(createInjectDocument, {'document': {'service_date': '2006-06-19'}, 'injection': hepb_injection}, reason='Hep-B Injection')
        # Hep-B
        u.setup(createInjectDocument, {'document': {'service_date': '2006-12-09'}, 'injection': hepb_injection}, reason='Hep-B Injection')
        # Prevnar
        u.setup(createInjectDocument, {'document': {'service_date': '2007-08-08'}, 'injection': prevnar_injection}, reason='Prevnar Injection')
        # IPV
        u.setup(createInjectDocument, {'document': {'service_date': '2007-08-08'}, 'injection': ipv_injection}, reason='IPV Injection')
        # Hep-A
        u.setup(createInjectDocument, {'document': {'service_date': '2007-08-08'}, 'injection': hepa_injection}, reason='Hep-A Injection')
        # MMR
        u.setup(createInjectDocument, {'document': {'service_date': '2009-08-01'}, 'injection': mmr_injection}, reason='MMR Injection')
        # DTaP
        u.setup(createInjectDocument, {'document': {'service_date': '2009-09-03'}, 'injection': dtap_injection}, reason='DTaP Injection')
        # IPV
        u.setup(createInjectDocument,  {'document': {'service_date': '2009-09-03'}, 'injection': ipv_injection}, reason='IPV Injection')
        # Varicella #2
        u.setup(createInjectDocument, {'document': {'service_date': '2009-09-03'}, 'injection': varicella_injection}, reason='Varicella Injection')

        u.verifyElements([
        # make sure the patient was created and shows up in a search
        wcElement('xpath',"//span[@id='wc_pat_bar_mrns' and contains(text(),'111999000')]")
        ])
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=search&search_method=simple&by=n&phone_list=Mobile+Phone&sstring=smith%2Cjohn&pat_search=Search'))

    # Get the pat_id of the chart just created
    res = d.miedb.dbQuery("SELECT MAX(pat_id) as `pat_id` FROM patients");
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['pat_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    pat_id = res.getRow(0)['pat_id']

    with d.getWCUnitTest('ICE Varicella MultiDose - Query') as u:
        u.verifyElements([
        wcElement('xpath',"//span/label[contains(., 'Created Document')]"),
        wcElement('xpath',"//span/label[contains(., 'Queue ID')]")
        ])
        u.setup(lambda u: u.getDriver().pause(7), reason='Let the query respond')
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=queryimport&pat_id={0}&qry_module=Immunizations&qry_name=ForecastICEQuery&xslt_module=Immunizations&xslt_name=ICEXMLtoSQL&system_id=ICE'.format(pat_id)),reason='Process the Query operation')

    # Get the id of the queue entry we just created
    res = d.miedb.dbQuery("SELECT MAX(queue_id) as `queue_id` FROM injection_queue WHERE pat_id={0} AND queue_type='frc' AND status='C'".format(pat_id));
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['queue_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    queue_id = res.getRow(0)['queue_id']

    with d.getWCUnitTest('Realistic History - ICE Results Display') as u:
        u.verifyElements([
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'21M 5D')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'5')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'Invalid Dose')]", exists=False),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'Due Now.')]", exists=False),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'Completed vaccine series')]"),
        ])
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=pat&pat_id={0}&v=inject&injopp=forecast&queue_id={1}'.format(pat_id,queue_id)),reason='View the output layout')

    with d.getWCUnitTest('Invalid Varicella Dose - Query') as u:
        u.verifyElements([
        wcElement('xpath',"//span/label[contains(., 'Created Document')]"),
        wcElement('xpath',"//span/label[contains(., 'Queue ID')]")
        ])
        u.setup(lambda u: u.getDriver().miedb.dbExec("UPDATE documents SET service_date='2009-08-07' WHERE service_date='2009-08-01' AND pat_id={0} AND doc_type='INJECT' and storage_type=12".format(pat_id)), reason='Invalidate the 2nd Varicella Injection')
        u.setup(lambda u: u.getDriver().pause(7), reason='Let the query respond')
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=queryimport&pat_id={0}&qry_module=Immunizations&qry_name=ForecastICEQuery&xslt_module=Immunizations&xslt_name=ICEXMLtoSQL&system_id=ICE'.format(pat_id)),reason='Process the Query operation')

    # Get the id of the queue entry we just created
    res = d.miedb.dbQuery("SELECT MAX(queue_id) as `queue_id` FROM injection_queue WHERE pat_id={0} AND queue_type='frc' AND status='C'".format(pat_id));
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['queue_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    queue_id = res.getRow(0)['queue_id']

    with d.getWCUnitTest('ICE Varicella MultiDose - ICE Results Display') as u:
        u.verifyElements([
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'21M 5D')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'5')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'Invalid Dose')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'Due Now.')]"),
        wcElement('xpath',"//td[contains(@class,'table-secondary') and contains(., 'Varicella Vaccine Group')]/following-sibling::td[contains(.,'Completed vaccine series')]", exists=False),
        ])
        u.test(lambda u: u.getDriver().navigate('?f=chart&s=pat&pat_id={0}&v=inject&injopp=forecast&queue_id={1}'.format(pat_id,queue_id)),reason='View the output layout')
