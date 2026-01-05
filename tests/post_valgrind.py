"""
    Runs a full valgrind leak check against each unique url seen by the system
    @owner: sgrider
"""

import cgi
from multiprocessing.pool import ThreadPool
from datetime import datetime
import json

noSession = 'No Session Activity'

def valgrind(d, row, res):
    ws = None
    try:
        start = datetime.now()
        url = row['cgi_data']
        path = None
        data = None
        creds = {}
        if url.startswith('/'):
            spl = row['cgi_data'].split('?')
            path = spl[0]
            url = spl[1] if len(url) else ''
            if row['cgi_method'] == 'POST':
                data = url
                url = ''
        elif row['cgi_method'] == 'POST':
            data = row['cgi_data']
        if row['session_id'] and row['session_id'] != noSession:
            creds = {
                'session_id': row['session_id']
            }
        ws = d.getWebServer()
        ret = ws.valgrind(url, **{
            'path': path,
            'data': data,
            'credentials': creds,
            'flags': ['--leak-check=full', '--track-fds=yes', '--track-origins=yes']
        })
    except Exception as e:
        ret = {
            'error': ('valgrind extension raised an exception', str(e))
        }
    finally:
        if ws:
            ws.close()
    try:
        ret['displayUrl'] = '&'.join(['{0}={1}'.format(k, cgi.escape(v)) for k, v in \
            cgi.parse_qsl(url, keep_blank_values=True)]) or url
    except AttributeError:
        import html
        ret['displayUrl'] = '&'.join(['{0}={1}'.format(k, html.escape(v)) for k, v in \
            html.parse_qsl(url, keep_blank_values=True)]) or url
    ret['displayUser'] = row['username'] if row['session_id'] != noSession else 'No Session'
    ret['row'] = row
    ret['duration'] = (datetime.now() - start)
    res.append(ret)

def main(d, WCURL):
    urlData = d.wcutils.collectUrls()
    if urlData:
        pool = ThreadPool(processes=4)
        res = []
        sessions = set()
        d.startSection('Re-initialize login sessions and submit valgrind tests')
        for method in urlData.keys():
            for url, rows in urlData[method].items():
                for row in rows:
                    creds = {}
                    if row['session_id'] and row['session_id'] != noSession:
                        # Ensure we are still logged in
                        if not row['session_id'] in sessions:
                            d.miedb.dbExec("REPLACE INTO logins SET session_id='{session_id}',"\
                                "username='{username}', user_id={user_id},"\
                                "ip_address='127.0.0.1', userfname='valgrind', "\
                                "login_dt=NOW()".format(**row))
                        sessions.add(row['session_id'])
                    pool.apply_async(valgrind, (d, row, res))
        d.endSection()
        pool.close()
        pool.join()
        summary = {
            'definitelyLost': 0,
            'indirectlyLost': 0,
            'possiblyLost': 0,
            'fileDescriptors': 0,
        }
        for r in res:
            for k in summary.keys():
                if k in r:
                    summary[k] += r[k] - 3 if k == 'fileDescriptors' else r[k]
        d.startSection('{0} Valgrind Results'.format(len(res)),
            comments='{lost:,} bytes lost | {fd:,} open file handles'.format(**{
            'lost': summary['definitelyLost'],
            'fd': summary['fileDescriptors'],
        }))
        d.reportHTML('style', 'valgrindPre { white-space: pre-wrap; font-family: monospace }')
        for r in sorted(res, key=lambda x: x['row']['event_dt']):
            d.startSection('Valgrind: {0}'.format(r['displayUrl']), comments=r['displayUser'])
            d.reportHTML('valgrindPre', json.dumps(r['row'], indent=2,
                default=lambda x: str(x)), 'Activity Log Record')
            if r['error']:
                d.reportCommandStatus(r['error'][0],
                    r['error'][1] if len(r['error']) > 1 else '',
                    False,
                    r['error'][2] if len(r['error']) > 2 else '',
                    r['error'][3] if len(r['error']) > 3 else '')
            elif r['warning']:
                d.reportCommandStatus(r['warning'][0],
                    r['warning'][1] if len(r['warning']) > 1 else '',
                    None,
                    r['warning'][2] if len(r['warning']) > 2 else '',
                    r['warning'][3] if len(r['warning']) > 3 else '')
            else:
                d.reportHTML('valgrindPre', r['command'], 'Valgrind Command')
                d.reportHTML('valgrindPre', r['output'], 'Standard Output')
                d.reportHTML('valgrindPre', r['report'], 'Valgrind Raw Report')
                if r['fileDescriptors'] > 3:
                    d.reportCommandStatus('fileDescriptors', r['fileDescriptors'], False, '', '')
                for k in ('definitelyLost', 'indirectlyLost', 'possiblyLost'):
                    if r[k]:
                        d.reportCommandStatus(k, '{0} bytes'.format(r[k]), False, '', '')
            d.endSection()
        d.endSection()
    else:
        d.reportCommandStatus('Valgrind', 'No Url Data Found', None, '', '')
