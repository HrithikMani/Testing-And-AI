import json
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

def main(d, _):
    res = d.miedb.dbQuery("SELECT act_id, session_id, user_id, username, pat_id, "\
        "patfname, ip_address, event_dt, func, subfunc, opp, cgi_method, cgi_data "\
        "FROM logins_activity_log WHERE subfunc='jserror' ORDER BY act_id ASC")
    if not res:
        return
    errors = res.getRes()
    d.startSection('JS Errors', comments='{} Errors'.format(len(errors)))
    if len(errors):
        d.reportCommandStatus('Javascript Errors Detected', '', False, '', '')
    for row in errors:
        try:
            err = json.loads(urlparse.parse_qs(row['cgi_data'])['data'][0])
        except Exception as e:
            d.reportCommandStatus('Failed to parse cgi_data', e, None, '',
                'act_id: {0}'.format(row['act_id']))
            continue
        d.reportHTML('pre', '==================================\n'\
            'ID: {id}\n'\
            'Session ID: {session}\n'\
            'IP Address: {ip}\n'\
            'Error Details: {error}\n'\
            '=================================='\
            ''.format(**{
                'id': row['act_id'],
                'session': row['session_id'],
                'ip': row['ip_address'],
                'error': json.dumps(err, indent=2)
            }), 'Javascript Error: {0}'.format(err['msg']))
    d.endSection()

