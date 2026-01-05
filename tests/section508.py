import re
"""
    This test runs pa11y on WebChart logged in GET urls to check for Section508 compliance.
    This third party tool: pa11y is documented here: https://github.com/pa11y/pa11y
    @owners: jswing, sgrider
"""

TOOLNAME = 'pa11y'
OPTIONS = ['--standard Section508']

# Don't validate these cgi funcs
IGNORED = ['script', 'style', 'ajaxget', 'ajaxpost', 'fsstream', 'stream', 'stgstream']
IGNORED = []

def main(d, WCURL):
    urldata = d.getUserData('ActivityLogUrls')
    baseurl = d._base_urls[-1]

    if urldata:
        ws = d.getWebServer()
        ret = ws.system('which {0}'.format(TOOLNAME))
        if ret.returnCode():
            d.reportCommandStatus('Requested System Tool Not Installed', TOOLNAME, False,
                ret.stdout(), ret.stderr())
            return
        try:
            for session in urldata['GETS'].itervalues():
                creds = session['credentials']
                # Only validate logged-in sessions
                if len(creds['session_id']) and creds['session_id'] != 'No Session Activity':
                    d.miedb.dbExec("REPLACE INTO logins SET session_id='{session_id}', "\
                        "username='{username}', user_id={user_id}, ip_address='127.0.0.1', "\
                        "userfname='Nunya', login_dt=NOW()".format(**creds))
                else:
                    continue
                for row in session['data']:
                    # Don't care about path related invocations
                    if not row['cgi_data'].startswith('/') and row['func'] not in IGNORED:
                        d.startSection('Validate URL {0}:{1}'.format(creds['username'], row['cgi_data']))
                        ret = ws.system('{0} {1} "{2}?{3}&session_id={4}"'.format(
                                TOOLNAME, ' '.join(OPTIONS), baseurl, row['cgi_data'],
                                creds['session_id']), validExitCodes=[0,2])
                        """
                        0: Pa11y ran successfully, and there are no errors
                        1: Pa11y failed run due to a technical fault
                        2: Pa11y ran successfully but there are errors in the page
                        """
                        if ret.returnCode() == 1:
                            d.reportCommandStatus('Validation Command Failed', '', False,
                                ret.stdout(), ret.stderr())
                        else:
                            if ret.returnCode() == 0:
                                d.reportCommandStatus('0 Errors Detected', '', True, '', '')
                            else:
                                match = re.search('([\d]+) Errors', ' '.join(ret.stdout(True)[-5:]))
                                errors = int(match.group(1)) if match else 'Some'
                                d.reportCommandStatus('{0} Errors Detected'.format(errors), '',
                                    False, '', '')
                            d.reportHTML('pre', ret.stdout(), 'Report Summary')
                        d.endSection()
        except AttributeError:
            for session in urldata['GETS'].values():
                creds = session['credentials']
                # Only validate logged-in sessions
                if len(creds['session_id']) and creds['session_id'] != 'No Session Activity':
                    d.miedb.dbExec("REPLACE INTO logins SET session_id='{session_id}', "\
                        "username='{username}', user_id={user_id}, ip_address='127.0.0.1', "\
                        "userfname='Nunya', login_dt=NOW()".format(**creds))
                else:
                    continue
                for row in session['data']:
                    # Don't care about path related invocations
                    if not row['cgi_data'].startswith('/') and row['func'] not in IGNORED:
                        d.startSection('Validate URL {0}:{1}'.format(creds['username'], row['cgi_data']))
                        ret = ws.system('{0} {1} "{2}?{3}&session_id={4}"'.format(
                                TOOLNAME, ' '.join(OPTIONS), baseurl, row['cgi_data'],
                                creds['session_id']), validExitCodes=[0,2])
                        """
                        0: Pa11y ran successfully, and there are no errors
                        1: Pa11y failed run due to a technical fault
                        2: Pa11y ran successfully but there are errors in the page
                        """
                        if ret.returnCode() == 1:
                            d.reportCommandStatus('Validation Command Failed', '', False,
                                ret.stdout(), ret.stderr())
                        else:
                            if ret.returnCode() == 0:
                                d.reportCommandStatus('0 Errors Detected', '', True, '', '')
                            else:
                                match = re.search('([\d]+) Errors', ' '.join(ret.stdout(True)[-5:]))
                                errors = int(match.group(1)) if match else 'Some'
                                d.reportCommandStatus('{0} Errors Detected'.format(errors), '',
                                    False, '', '')
                            d.reportHTML('pre', ret.stdout(), 'Report Summary')
                        d.endSection()
    else:
        d.reportCommandStatus('ActivityLogUrls', 'No url data has been collected', None,
            '', 'Either there was no data in the system or the urlCollector test did not '\
            'run')
