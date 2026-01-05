def main(d, _):
    ws = d.getWebServer()
    ret = ws.system('mycores {0}'.format(d.getUserData('handle')))
    cores = []
    if not ret.returnCode():
        cores = [x for x in ret.stdout(True) if 'apache' in x]
    if ret.returnCode():
        d.reportCommandStatus('mycores', 'command failed', False,
            ret.stdout(), ret.stderr())
    else:
        for core in cores:
            cf = core.split(' ').pop()
            d.reportCommandStatus('Core Dump', cf, False, '', '')
            d.startSection('Backtrace {0}'.format(cf))
            ret = ws.system('sudo gdb -q -batch -ex "bt" cgibin/webchart.cgi "{0}" 2>&1'.format(cf))
            if not ret.returnCode():
                d.reportHTML('pre', ret.stdout())
            else:
                d.reportCommandStatus('Backtrace Failed', ret.stdout(), False, '', '')
            d.endSection()

