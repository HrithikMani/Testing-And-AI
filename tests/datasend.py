import os
import time
import imp
import fnmatch
from wcunittest import wcDBRecord

from wcunithelpers import wcRemoteFile

RTS_ID = 'WCUnit'
OUTFILE = 'wcunit.msg'
LOGFILE = 'wcunit.log'

SYSTEM_NAME = 'wctest'
DSD_CONF = '../datasend/dsdbinary.conf'

TESTROOT = os.path.join(os.path.dirname(__file__), '..', 'testlib')

""" This is the list of datasend tests by group.
    Each group is a dictionary of the following keys:
    {
        'name': 'The name of the group (for display purposes)',
        'description': 'A short description (for display purposes)',
        'src': 'The filename that contains all of the tests to run for this group (relative to 'testlib')',
        'partition': 'The partition to be used for the system_partition value when building the refer_to_systems entry',
        'method': 'A numeric value representing the method for the datasend_route entry',
    }
"""
TESTGROUPS = [
    {
        'name': 'Injections Export',
        'description': 'Testing injection export messages',
        'src': 'datasend_inject_export.py',
        'partition': 'MIE',
        'method': 23
    },
    {
        'name': 'Outbound Orders',
        'description': 'Orders HL7 messages (ORM^O01)',
        'src': 'datasend_orders.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Outbound Orders with Flowsheets',
        'description': 'Orders HL7 messages (ORM^O01) with and without flowsheets',
        'src': 'datasend_orders_flowsheets.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Outbound DFT',
        'description': 'Billing HL7 messages (DFT^P03)',
        'src': 'datasend_dft.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Outbound Documents via cc_hl7',
        'description': 'Outbound Documents via cc_hl7',
        'src': 'datasend_documents_cc_hl7.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Incidents -- incident.so',
        'description': 'Incidents -- incident.so',
        'src': 'datasend_incidents.py',
        'partition': 'MIE',
        'method': 25
    },
    {
        'name': 'Appointments via cc_hl7',
        'description': 'Appointments via cc_hl7',
        'src': 'datasend_appointments_cc_hl7.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Patients via cc_hl7',
        'description': 'Patients via cc_hl7',
        'src': 'datasend_patients_cc_hl7.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Lab Results via oru_hl7',
        'description': 'Lab Results via oru_hl7',
        'src': 'datasend_oru_hl7.py',
        'partition': 'MIE',
        'method': 13
    },
    {
        'name': 'Syndromic Surveillance',
        'description': 'Syndromic Surveillance',
        'src': 'datasend_syndromic_surveillance.py',
        'partition': 'MIE',
        'method': 27
    },
    {
        'name': 'Encounters',
        'description': 'Encounters including Radiology Orders',
        'src': 'datasend_encounters.py',
        'partition': 'MIE',
        'method': 4
    },
    {
        'name': 'Documents via mdm_hl7.so',
        'description': 'Documents via mdm_hl7.so',
        'src': 'datasend_mdm_hl7.py',
        'partition': 'MIE',
        'method': 22
    },
    {
        'name': 'Incidents via sap_osha.so',
        'description': 'Incidents via sap_osha.so',
        'src': 'datasend_sap_osha.py',
        'partition': 'MIE',
        'method': 14
    }
]

def setupDBExec(d, query):
    # All setup dbExecs need to be executed within the context of the given TIMESTAMP
    d.miedb.dbExec(query, presql=f"SET TIMESTAMP=UNIX_TIMESTAMP('{d.getUserData('run_datetime')}')")

def main(d, wcurl):
    OID = getOID(d)
    for group in TESTGROUPS:
        name = group.get('name')
        desc = group.get('description')
        filename = group.get('src')
        d.startSection('{0} | {1}'.format(name, filename), comments=desc)
        try:
            src = imp.load_source('DS_SOURCE', os.path.join(TESTROOT, filename))
        except Exception as e:
            d.reportCommandStatus('Failed to load tests from {0}'.format(filename), str(e), False, '', '')
        else:
            if not hasattr(src, 'TESTS'):
                d.reportCommandStatus('The source file does not contain a TESTS variable', filename,
                    False, '', '')
            elif not isinstance(src.TESTS, list):
                d.reportCommandStatus('Source file TESTS variable is not a list object', filename,
                    False, '', '')
            elif len(src.TESTS):
                setupData = {'OID':OID}
                if hasattr(src, 'setup') and callable(src.setup):
                    d.startSection('Test Group Setup')
                    try:
                        src.setup(d, setupData)
                    except Exception as e:
                        d.reportCommandStatus('Exception raised in setup', '', False,
                            str(e), e)
                    finally:
                        d.reportCommandStatus('Setup Data', str(setupData), True, '', '')
                        d.endSection()
                for test in src.TESTS:
                    if not test.get('name') or \
                        (not test.get('doc_id') and not test.get('enc_id') and not test.get('inc_id') and not test.get('apt_id') and not test.get('pat_id') ) or \
                        (not test.get('message') and not test.get('log') and not test.get('logparts')):
                        d.reportCommandStatus('Test objects require name, item_id '\
                            'and either a message or log properties in order to run',
                            '', False, '', '')
                    else:
                        runTest(d, test, {
                            'OID': OID,
                            'group': group,
                            'setupData': setupData
                        })
                if hasattr(src, 'teardown') and callable(src.teardown):
                    d.startSection('Test Group Teardown')
                    try:
                        src.teardown(d, setupData)
                    except Exception as e:
                        d.reportCommandStatus('Exception raised in teardown', '', False,
                            str(e), e)
                    finally:
                        d.endSection()
        d.endSection()

def getOID(d):
    d.startSection('Query System OID')
    res = d.miedb.dbQuery("SELECT value FROM system_info WHERE name='OID'")
    if res:
        if res.numRows():
            OID = res.getRes()[0]['value']
        else:
            d.reportCommandStatus('OID query returned no rows', '', False, '', '')
    else:
        d.reportCommandStatus('Failed to query system OID', d.miedb.dbError(), False,
            '', '')
    d.endSection()
    return OID

def insertRTSEntry(d, udata):
    d.startSection('Insert RTS Entry')
    group = udata.get('group', {})
    systemAddress = 'file|./{0}'.format(OUTFILE)
    systemUser = ''
    systemPass = ''
    partition = group.get('partition')
    rts = udata.get('rts', {})
    if rts:
        systemAddress = rts.get('system_address', systemAddress)
        systemUser = rts.get('system_user', '')
        systemPass = rts.get('system_pass', '')
        partition = rts.get('partition', partition)
    systemAddress = systemAddress.format(BE_CAREFUL_HOSTNAME=d.getUserData('BE_CAREFUL_HOSTNAME'))
    d.miedb.dbExec("INSERT INTO refer_to_systems (system_id, system_name, system_user, system_pass, "\
        "system_address, system_partition, system_options, active, system_address2) "\
        "VALUES ('{0}', 'WC Unit Test', '{1}', '{2}', '{3}', '{4}', 4, 1, '') ON DUPLICATE KEY UPDATE  system_name = "\
                    "VALUES(system_name), system_address = VALUES(system_address), system_partition = "\
                    "VALUES(system_partition), system_options = VALUES(system_options), active = VALUES(active),"\
                    " system_address2 = VALUES(system_address2);".format(
            udata['system_id'], systemUser, systemPass, systemAddress, partition))
    d.endSection()

def insertRTSSCPEntry(d, udata):
    d.startSection('Insert RTS Entry')
    group = udata.get('group', {})
    systemAddress = 'scp|{0}|22|/tmp/|scp|/home/selenium/.ssh/id_rsa.pub'
    partition = group.get('partition')
    rts = udata.get('rts', {})
    if rts:
        systemAddress = rts.get('system_address', systemAddress)
        partition = rts.get('partition', partition)
    systemAddress = systemAddress.format(d.getUserData('BE_CAREFUL_HOSTNAME'))
    d.miedb.dbExec("INSERT INTO refer_to_systems (system_id, system_name, system_address, system_partition, "\
                   "system_options, active, system_address2, system_user) VALUES ('{0}', 'WC Unit Test SCP', "\
                    "'{1}', '{2}', 4, 1, '','selenium') ON DUPLICATE KEY UPDATE system_name = "\
                    "VALUES(system_name), system_address = VALUES(system_address), system_partition = "\
                    "VALUES(system_partition), system_options = VALUES(system_options), active = VALUES(active),"\
                    " system_address2 = VALUES(system_address2);".format(udata['system_id'], systemAddress, partition))
    d.endSection()

def dropRTSEntry(d, data):
    d.startSection('Drop RTS Entry')
    d.miedb.dbExec("DELETE FROM refer_to_systems WHERE system_id='{0}'".format(data['system_id']))
    d.endSection()

def insertDataSendRoute(d, data):

    recipient_id = 0
    item_type = data.get('item_type')
    if not item_type:  #default is document
        item_id = data.get('doc_id')
        item_type = 'doc'
    elif item_type == 'procedure':
        item_id = data.get('enc_id')
    elif item_type == 'enc':
        item_id = data.get('enc_id')
    elif item_type == 'pat_enc':
        item_id = data.get('enc_id')
        recipient_id = item_id
    elif item_type == 'patEncClos':
        item_id = data.get('enc_id')
    elif item_type == 'incident':
        item_id = data.get('inc_id')
    elif item_type == 'apt':
        item_id = data.get('apt_id')
    elif item_type == 'pat':
        item_id = data.get('pat_id')
    elif item_type == 'doc':  # if someone forgets and sets item_type = doc, let's handle that appropriately.
        item_id = data.get('doc_id')

    method = data.get('group', {}).get('method')
    data_route_option = data.get('route_option')

    if not data_route_option:
        route_option = ''
    else:
        route_option = data_route_option
    if item_id:
        d.startSection('Create DataSend Route for Item/Method: {0}/{1}'.format(item_id, method))
        ret = d.miedb.dbExec("INSERT INTO datasend_route (item_type, item_id, method, "\
            "method_detail, status, active, ar_id, no_auto_resend, route_option, recipient_id) VALUES ("\
            "'{0}', {1}, {2}, '{3}', 'P', 1, 0, 0, '{4}',{5})".format(item_type, item_id, method, data['system_id'],data_route_option, recipient_id))
        d.endSection()
        data['route_id'] = ret.lastrowid

def dropDataSendRoute(d, data):
    route_id = data.get('route_id')
    del data['route_id']
    d.startSection('Drop DataSend Route', comments=route_id)
    d.miedb.dbExec("DELETE FROM datasend_route WHERE route_id={0}".format(route_id))
    d.miedb.dbExec("DELETE FROM datasend_route_revisions WHERE route_id={0}".format(route_id))
    d.endSection()

def datasend(d, udata):
    data = udata['data']
    test = udata['test']
    route_id = data.get('route_id')
    ws = d.getWebServer(os.path.join(d.getUserData('webserver_defaultPath'), 'cgibin'))
    escaped_baseurl = "{}".format(d.driverOptions.baseurl).replace('/', '\/')
    ret = ws.system("sudo sed -i 's/SYSTEM_HANDLE/{0}/g' ../datasend/dsdclient.conf".format(escaped_baseurl))
    d.reportHTML('pre', ret.stderr(), 'sed Output')
    ret = ws.system("./wcdata_sendd -n -r '{0}|{1}' {2}".format(SYSTEM_NAME, route_id, DSD_CONF))
    d.reportHTML('pre', ret.stderr(), 'Datasend Output')
    log = ws.getFiles(LOGFILE)[0]
    if log:
        filename = '{0}.log'.format(time.time())
        with open(os.path.join(d.driverOptions.uploadDir, '..', filename), 'wb') as fp:
            try:
                fp.write(log)
            except TypeError:
                fp.write(bytes(log, 'utf-8'))
        # store locally
        test['logoutput'] = log
        test['logfilename'] = filename
        d.initSubComment("<a target='_blank' href='../{0}'>View LogFile</a>".format(filename))
    else:
        d.reportCommandStatus('Failed to acquire logfile', LOGFILE, None, '', '')

def dbExec(d, query):
    d.miedb.dbExec(query)

def deleteFiles(d):
    ws = d.getWebServer(os.path.join(d.getUserData('webserver_defaultPath'), 'cgibin'))
    ws.system('rm -f {0} {1}'.format(LOGFILE, OUTFILE))

def addTrans(d, trans):
    d.miedb.dbExec("INSERT INTO translate (name, trans_from, trans_to) VALUES ("\
        "'{name}', '{trans_from}', '{trans_to}')".format(**trans))

def deleteTrans(d, trans):
    d.miedb.dbExec("DELETE FROM translate WHERE name='{name}' AND trans_from='{trans_from}'"\
        "AND trans_to='{trans_to}'".format(**trans))

def setupUrl(d, url):
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.setWCCookie('WCTESTSESSION')
    d.reportCommandStatus('Hit Url', url, True, '', '')
    wccurl.get(url)

def formatStr(d, s, data):
    repl = {
        'SYSTEM_OID': data.get('OID'),
        'ROUTE_ID': data.get('route_id'),
        'SELENIUM_USERNAME': d.getUserData('selenium_username')
    }
    repl.update(data.get('setupData', {}))
    try:
        if (isinstance(s, str) and 'hl7rules' not in s): #don't format setup queries inserting hl7 msgrules or segdefs
            s = s.format(**repl)
    except KeyError as e:
        d.reportCommandStatus('Failed to format test source', s, False, str(e), '')
    finally:
        return s

def compareLogFile(d, udata):
    test = udata['test']
    data = udata['data']
    if test['logoutput']:
        expected = formatStr(d, test['log'], data)
        match = fnmatch.fnmatch(test['logoutput'], expected)
        d.reportCommandStatus('Match string against log file', expected, match,
            '', '' if match else 'Match not found')
        if not match:
            d.initSubComment("<a target='_blank' href='../{0}'>View LogFile</a>".format(
                test['logfilename']))
    else:
        d.reportCommandStatus('Log file contents not available', '', False, '', '')

def verifyLogFile(d, udata):
    """
    Wrapper for u.verifyFile so that route_id is in scope during execution for formatStr
    """
    u = udata['u']
    test = udata['test']
    data = udata['data']
    contains = udata['contains']
    log = formatStr(d, test.get('log',''), data)
    if log:
        u.verifyFile(log,wcRemoteFile(LOGFILE,relativePath='cgibin'),reason='Validate generated log file',contains=contains)

def verifyDBData(d, udata):
    """
    Wrapper for u.verifyDB so that route_id is in scope during execute for formatStr
    """
    u = udata['u']
    test = udata['test']
    data = udata['data']
    for k,v in test.get('conditions', {}).items():
        whr = formatStr(d,k,data)
        if whr:
            d.startSection('Post-Condition: '+whr)
            cols=""
            sep=""
            for c,a in v.items():
                cols = cols + sep + c
                sep = ","
            if len(cols) > 0:
                res = d.miedb.dbQuery("SELECT " + cols + ' ' + whr)
                if not res:
                    d.reportCommandStatus('dbQuery Failed','',False,'','')
                    return
                if not res.getRow(0):
                    d.reportCommandStatus('dbQuery returned no results','',False,'','')
                    return
                for c,a in v.items():
                    cval = res.getRow(0)[c]
                    if cval and str(cval) == str(a):
                        d.reportCommandStatus(c,'['+str(a)+']',True,'','')
                    else:
                        d.reportCommandStatus(c,'Value ['+str(cval)+'] does not match',False,'Expected ['+str(a)+']','')
            else:
                d.reportCommandStatus('Post-Condition','No Columns available',False,'','')
            d.endSection()
        else:
            d.reportCommandStatus('Unable to format query: '+k,'',False,'','')

def runTest(d, test, data):
    u = d.getWCUnitTest(test['name'], coreCheck=False, errorScreens=False)
    urls = test.get('setupUrl')
    system_id = test.get('system_id') or RTS_ID
    data['system_id'] = system_id
    data['doc_id'] = formatStr(d, test.get('doc_id'), data)
    data['item_type'] = test.get('item_type')
    data['enc_id'] = formatStr(d, test.get('enc_id'), data)
    data['route_option'] = test.get('route_option')
    data['inc_id'] = test.get('inc_id')
    data['apt_id'] = test.get('apt_id')
    data['pat_id'] = test.get('pat_id')
    data['contains'] = test.get('contains', False)

    if urls:
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            u.setup(setupUrl, url, 'Navigate setupUrl')
    rts = test.get('rts', {})
    if system_id.lower().startswith('scp_'):
        u.setup(insertRTSSCPEntry, {
            'group': data['group'],
            'rts': rts,
            'system_id':system_id
        })
    else:
        u.setup(insertRTSEntry, {
            'group': data['group'],
            'rts': rts,
            'system_id':system_id
        })
    u.teardown(dropRTSEntry, data)
    u.setup(insertDataSendRoute, data)
    u.teardown(dropDataSendRoute, data)
#    if test.get('setupQueries'):
#        u.setup(lambda d: d.miedb.dbExec('''SET TIMESTAMP=UNIX_TIMESTAMP('2007-02-02 09:15:00')'''), reason='Configure timestamp for Demo Date')
    for query in test.get('setupQueries', []):
        u.setup(setupDBExec, formatStr(d, query, data), reason='Run custom setup query')
    for query in test.get('teardownQueries', []):
       u.teardown(dbExec, formatStr(d, query, data), reason='Run custom teardown query')
    for trans in test.get('translations', []):
        for k, v in trans.items():
            trans[k] = formatStr(d, v, data)
        u.setup(addTrans, trans,
            reason='Add custom translation: {name}:{trans_from}=>{trans_to}'.format(**trans))
        u.teardown(deleteTrans, trans, reason='Delete custom translation')
    rtse = []
    for key, value in test.get('rtsExtended', {}).items():
        rtse.append((key, formatStr(d, value, data)))
    if rtse:
        u.setup(lambda d: d.wcutils.addRTSE(system_id, rtse), reason='Insert custom RTS extended values')
    if test.get('rtsExtended', {}):
       u.teardown(lambda d: d.wcutils.deleteRTSE(system_id), reason='Delete any custom RTS extended values')
    msg = formatStr(d, test.get('message', ''), data)
    if msg:
        if test.get('contains', False):
            u.verifyFile(msg, wcRemoteFile(OUTFILE, relativePath='cgibin'),
                reason='Validate generated message file', contains=True)
        else:
            u.verifyFile(msg, wcRemoteFile(OUTFILE, relativePath='cgibin'),
                reason='Validate generated message file')

    if test.get('conditions',None):
        u.verifyFunc(verifyDBData, {
            'u': u,
            'test': test,
            'data': data
        },'Verify DB post-Conditions')

    if test.get('log', None):
        u.verifyFunc(verifyLogFile, {
            'u': u,
            'test': test,
            'data': data,
            'contains': False
        }, 'Generate log file baseline')

    if test.get('logparts', None):
        for part in test.get('logparts', []):
            u.verifyFunc(verifyLogFile, {
                'u': u,
                'test': test,
                'data': data,
                'contains': True
            }, 'Generate log file part baseline')

    u.teardown(deleteFiles)

    u.test(datasend, {
        'test': test,
        'data': data
    }, reason='Execute datasend')

