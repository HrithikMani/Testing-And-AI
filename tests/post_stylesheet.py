import time
import re
import miessh
import os

def main(d, _):
    baseurl = d._base_urls[-1]
    urls = [
        '?f=style&mode=stylesheet',
    ]
    # This will run on the local testing node
    node = miessh.localClient()
    for url in urls:
        d.startSection('Validating stylesheet using csstidy', comments=url)
        filename = time.time()
        ret = node.execute('''wget --no-check-certificate -O ~/{0} "{1}{2}"'''.format(filename, baseurl, url))
        if not ret.code:
            ret = node.execute('''csstidy ~/{0} --silent'''.format(filename))
            if not ret.code:
                lines = ret.stdout(True)
                data = {
                    'errors': [],
                    'optimizations': [],
                    'fixes': [],
                }
                d.reportCommandStatus(lines[0], '', True, '', '')
                d.reportCommandStatus(lines[1], '', True, '', '')
                for line in lines[3:]:
                    if re.match('^\d+:', line):
                        spl = line.split(':')
                        lineno = spl[0]
                        msg = ':'.join(spl[1:]).strip()
                        if msg.startswith('Optimised'):
                            data['optimizations'].append(line)
                        elif msg.startswith('Fixed'):
                            data['fixes'].append(line)
                        else:
                            data['errors'].append(line)
                d.reportHTML('pre', '\n'.join(data['fixes']), 'Automatic fixes applied [ {0} ]'.format(len(data['fixes'])))
                d.reportHTML('pre', '\n'.join(data['optimizations']), 'Optimizations applied [ {0} ]'.format(len(data['optimizations'])))
                d.reportHTML('pre', '\n'.join(data['errors']), 'Issues found [ {0} ]'.format(len(data['errors'])))
            else:
                d.reportCommandStatus('CSSTidy failed', '', False, ret.stdout(), ret.stderr())
        else:
            d.reportCommandStatus('Failed to retrieve stylesheet', '', False, ret.stdout(), ret.stderr())
        if os.path.exists(str(filename)):
            os.remove(filename)
        d.endSection()

