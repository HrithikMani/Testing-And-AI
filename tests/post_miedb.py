def main(d, _):
    s = d.miedb._stats['queries']
    d.reportCommandStatus('DB Queries',
        '{0} queries, totaling {1:.03f}(s), with an average of: {2:.03f}(s)'.format(s['count'], s['duration'],
             s['duration'] / s['count']), True, '', '')
    s = d.miedb._stats['execs']
    d.reportCommandStatus('DB Execs',
        '{0} statements, totaling {1:.03f}(s), with an average of: {2:.03f}(s)'.format(s['count'], s['duration'],
             s['duration'] / s['count']), True, '', '')

