def main(d, _):
    res = d.miedb.dbQuery('''SELECT m.type, m.func, ll.username, m.session_id,
        COUNT(id) AS count, SUM(duration) AS duration, AVG(duration) AS average
        FROM ajax_metrics m
        LEFT JOIN logins_log ll USING(session_id)
        GROUP BY m.session_id, m.type, m.func ORDER BY average DESC''')
    # I can't wait until Newt is ready and I could just write out a table
    rows = []
    delim = ' '
    headers = ['Type', 'Function', 'Username', 'SessionID', 'Count', 'Duration', 'Average']
    maxlens = [len(x) for x in headers]
    fields = ['type', 'func', 'username', 'session_id', 'count', 'duration', 'average']
    rows.append(headers)
    for row in res.getRes():
        rows.append(['{{{0}}}'.format(f).format(**row) for f in fields])
        maxlens = [max(p, len(v)) for p, v in zip(maxlens, rows[-1])]
    s = []
    for row in rows:
        for r, l in zip(row, maxlens):
            s.append(r)
            s.append(delim * (l + 4 - len(r)))
        s.append('\n')
    d.reportHTML('pre', ''.join(s))
