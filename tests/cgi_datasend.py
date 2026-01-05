import os
import time
import imp
import fnmatch
import re
from wcunittest import wcDBRecord

from wcunithelpers import wcRemoteFile

RTS_ID = 'WCUnit'
OUTFILE = 'wcunit.msg'
LOGFILE = 'wcunit.log'

SYSTEM_NAME = 'wctest'

CGIDATASENDLOGPATH = '/usr/local/webchart/wc_basedir/logs/'

TESTROOT = os.path.join(os.path.dirname(__file__), '..', 'testlib')

TESTGROUPS = [
    {
        'name': 'Printing',
        'description': 'Printing with cgi_datasend',
        'src': 'cgi_datasend_print.py',
        'partition': 'MIE',
        'method': '1'
    },
    {
        'name': 'Faxing',
        'description': 'Faxing with cgi_datasend',
        'src': 'cgi_datasend_fax.py',
        'partition': 'MIE',
        'method': '2'
    }
]

def initSystemSettings(d):
    d.startSection('Initialize System Settings')
    d.miedb.dbExec("INSERT IGNORE INTO system_settings (module, section, item, value) VALUES "\
                   "('CGI DataSend', 'Config', 'Enable Print', '0')")
    d.miedb.dbExec("INSERT IGNORE INTO system_settings (module, section, item, value) VALUES "\
                     "('CGI DataSend', 'Config', 'Enable Fax', '0')")
    d.miedb.dbExec("INSERT IGNORE INTO system_settings (module, section, item, value) VALUES "\
                        "('CGI DataSend', 'Child Control', 'Max Children', '1')")
    d.endSection()

def setupDBExec(d, query):
    # All setup dbExecs need to be executed within the context of the given TIMESTAMP
    d.miedb.dbExec(query, presql='''SET TIMESTAMP=UNIX_TIMESTAMP('2023-02-02 09:15:00')''')

def main(d, wcurl):
    OID = getOID(d)
    initSystemSettings(d)
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
                setupData = {}
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
    partition = group.get('partition')
    rts = udata.get('rts', {})
    if rts:
        systemAddress = rts.get('system_address', systemAddress)
        partition = rts.get('partition', partition)
    d.miedb.dbExec("INSERT INTO refer_to_systems (system_id, system_name, "\
        "system_address, system_partition, system_options, active, system_address2) "\
        "VALUES ('{0}', 'WC Unit Test', '{1}', '{2}', 4, 1, '')".format(
            udata['system_id'], systemAddress, partition))
    d.endSection()

def insertRTSSCPEntry(d, udata):
    d.startSection('Insert RTS Entry')
    group = udata.get('group', {})
    systemAddress = 'scp|{0}|22|/tmp/|scp|/home/selenium/.ssh/id_rsa.pub'.format(d.getUserData('webserver_hostname'))
    partition = group.get('partition')
    rts = udata.get('rts', {})
    if rts:
        systemAddress = rts.get('system_address', systemAddress)
        partition = rts.get('partition', partition)
    d.miedb.dbExec("INSERT INTO refer_to_systems (system_id, system_name, "\
        "system_address, system_partition, system_options, active, system_address2, system_user) "\
        "VALUES ('{0}', 'WC Unit Test SCP', '{1}', '{2}', 4, 1, '','selenium')".format(
            udata['system_id'], systemAddress, partition))
    d.endSection()

def dropRTSEntry(d, data):
    d.startSection('Drop RTS Entry')
    d.miedb.dbExec("DELETE FROM refer_to_systems WHERE system_id='{0}'".format(data['system_id']))
    d.endSection()

def insertDataSendRoute(d, data):

    recipient_id = 0
    recipient_name = data.get('recipient_name')
    if not recipient_name:
        recipient_name = 'Johnny Test'
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
            "method_detail, status, active, ar_id, no_auto_resend, route_option, recipient_id, recipient_name) VALUES ("\
            "'{0}', {1}, {2}, '{3}', 'W', 1, 0, 0, '{4}',{5},'{6}')".format(item_type, item_id, method, data['system_id'],data_route_option, recipient_id, recipient_name))
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
    ws = d.getWebServer()
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.get('?f=datasend')
    log = ws.getFiles('../wc_basedir/logs/{0}/cgi_datasend.log'.format(d.getUserData('handle')))
    if log:
        filename = '{0}.log'.format(time.time())
        log = '\n'.join(log)
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
    ws = d.getWebServer()
    ws.system('rm -f ../wc_basedir/logs/{0}/cgi_datasend.log {1}'.format(d.getUserData('handle'), OUTFILE))

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
        if (isinstance(s, str)):
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
    log = re.sub(r'\bPID\s+is\s+\d+\b', 'PID is *', log)
    log = re.sub(r'\d+\.\d+', '*', log)
    testfile = test['logoutput']
    testfile = "\n".join(line.split(":: ", 1)[-1] for line in testfile.splitlines())
    testfile = re.sub(r'\bPID\s+is\s+\d+\b', 'PID is *', testfile)
    testfile = re.sub(r'\d+\.\d+', '*', testfile)
    if log:
        u.verifyFile(log,testfile,reason='Validate generated log file',contains=contains)

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
    system_id = formatStr(d, test.get('system_id'), data) or RTS_ID
    data['system_id'] = system_id
    data['doc_id'] = formatStr(d, test.get('doc_id'), data)
    data['item_type'] = test.get('item_type')
    data['enc_id'] = formatStr(d, test.get('enc_id'), data)
    data['route_option'] = test.get('route_option')
    data['inc_id'] = test.get('inc_id')
    data['apt_id'] = test.get('apt_id')
    data['pat_id'] = test.get('pat_id')
    ignores = []
    for ignore in test.get('ignores', []):
        ignores.append(ignore)

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

    for ignore in ignores:
        d.wcErrorLog.ignore(ignore)



