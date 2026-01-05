def main(d, _):
    d.wcErrorLog.read()
    d.startSection('Error Logs', comments='{0} Errors {1} Ignored'.format(
        d.wcErrorLog.numLogs(), d.wcErrorLog.numIgnored()))
    failures = d.wcErrorLog.numFailures()
    d.reportCommandStatus('{0}Error Logs Detected'.format(
        '' if failures > 0 else 'No '), '', failures == 0, '', '')
    # Hack to get around reportHTML not allowing attributes or css
    d.reportHTML('style', '''
        logError {
            background-color: #E000003D;
            display: block;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            margin: 10px;
            padding: 10px;
        }
        logIgnored {
            background-color: #ccc;
            display: block;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            margin: 10px;
            padding: 10px;
        }''')
    for log in d.wcErrorLog:
        d.reportHTML('logIgnored' if log.isIgnored() else 'logError',
            log.read())
    d.endSection()

