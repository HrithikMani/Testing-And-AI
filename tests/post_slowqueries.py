import re

def main(d, _):
    slowQueryThreshold = d.getUserData('slow_query_threshold') or 2.0
    d.startSection('Slow Queries',
        comments='>= {0}s [not run by root]'.format(slowQueryThreshold))
    dbConf = d.getUserData('_submissionData')['dbConf']
    # instead of managing another ssh key, i'm going to use the webserver
    # extension to connect to zeus-web and then run an ssh command on zeus-db
    # This assumes that the key exists from zeus-web to zeus-db and the logfile
    # is group readable
    ws = d.getWebServer()
    ret = ws.system("ssh {dbHost} \"pt-query-digest "\
        "--filter '\$event->{{db}} && \$event->{{db}} =~ /{dbName}/ && "\
        "\$event->{{Query_time}} >= {slowQueryThreshold} && "\
        "\$event->{{user}} !~ /root/' {slowQueryLog}\"".format(**{
            'dbHost': dbConf['host'],
            'dbName': dbConf['dbname'],
            'slowQueryThreshold': slowQueryThreshold,
            'slowQueryLog': '/storage/db/mysql/zeus-db-slow.log'
        }))
    if ret.returnCode():
        d.reportCommandStatus('Slow Query Analysis', '', False,
            ret.stdout(), ret.stderr())
    else:
        IGNORED_PT_LINES = (
            '# A software update is available:',
            '# No events processed.'
        )
        # List any expected slow queries here if they cannot be fixed or optimized
        # Enter enough of the query to make it unique.
        #
        # NOTE: The 'USESTANDARD' query, it is slow in testing, can't replicate in live, need to figure out 'reasons'
        ACKD_SLOW_QUERIES = [
            "UPDATE order_list",
            "(SELECT cs.condsearch_id AS condsearch_id, cs.code AS code,'USESTANDARD',",
            "UPDATE users SET",
            "INSERT INTO"
        ]
        lines = [x for x in ret.stdout(True) if x not in IGNORED_PT_LINES]
        out = '\n'.join(lines).strip()
        slowlist = [x for x in lines if not any(a in x for a in ACKD_SLOW_QUERIES)]
        whitelist = [x for x in lines if any(a in x for a in ACKD_SLOW_QUERIES)]
        slowlistout = '\n'.join(slowlist).strip()
        if slowlist:
            skip = 0
            slowqueries = []
            for line in slowlist:
                if not skip:
                    slowquery = re.findall('^[^#\s].+', line, re.MULTILINE)
                    if slowquery:
                        slowqueries.append(slowquery)
                else:
                    skip = 0
                if "EXPLAIN" in line:
                    skip = 1
            if slowqueries:
                d.startSection('Slow Queries Detected', comments=len(slowqueries))
                for q in slowqueries:
                    d.reportCommandStatus(q, '', False, '', '')
                d.reportHTML('pre', slowlistout, 'Slow Query Report')
                d.endSection()
        if whitelist:
            d.startSection('Whitelisted Slow Queries')
            for query in whitelist:
                d.reportCommandStatus(query.strip(), '', True, '', '')
            d.endSection()
        if not slowlist:
            d.reportCommandStatus('No Slow Queries Detected', '', True, '', out)
    d.endSection()
