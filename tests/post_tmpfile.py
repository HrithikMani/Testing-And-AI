import os

def main(d, _):
    if hasattr(d, 'getWebServer'):
        ws = d.getWebServer()
        ret = ws.system('[ -d /mnt/tmpfs/{0} ] && DIR=/mnt/tmpfs/{0} || '\
            'DIR=/dev/shm/{0}; find $DIR -type f'.format(d.getUserData('handle')))
        if ret.returnCode():
            d.reportCommandStatus('Find command failed', '', True, ret.stdout(), ret.stderr())
        elif ret.stdout(True):
            ret = ws.system('du -hc {0}/*'.format(os.path.dirname(ret.stdout(True)[0])))
            if ret.returnCode():
                d.reportCommandStatus('du', 'Command failed', False, ret.stdout(), ret.stderr())
            else:
                out = ret.stdout(True)
                total = out.pop()
                d.reportCommandStatus('Tmp Files',
                    '{0} Leftover files'.format(len(out)), len(out) == 0, total.split()[0], '')
                d.reportHTML('pre', '\n'.join(out))
        else:
            d.reportCommandStatus('Tmp File Check', 'No tmp files left behind', True, '', '')

