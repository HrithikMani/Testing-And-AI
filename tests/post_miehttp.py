def main(d, progressClass=None):
    requests = d.getUserData('_miehttp_requests')
    if requests:
        d.startSection('AJAX Metrics')
        incomplete = [r for r in requests if not r['complete']]
        d.startSection('Incomplete requests', comments=len(incomplete))
        for i in incomplete:
            dump_miehttp_request(d, i)
        d.endSection()
        d.startSection('Requests by duration', comments=len(requests))
        for v in sorted(requests, reverse=True, key=lambda x: x['duration']):
            dump_miehttp_request(d, v)
        d.endSection()
        grouped = {}
        for v in requests:
            if not v['url'] in grouped:
                grouped[v['url']] = {
                    'url': v['url'],
                    'count': 0,
                    'duration': 0.0
                }
            grouped[v['url']]['count'] += 1
            grouped[v['url']]['duration'] += v['duration']
        sorts = [
            ('Requests by total duration', lambda x: x[1]['duration']),
            ('Requests by count', lambda x: x[1]['count']),
        ]
        for sect, sorter in sorts:
            d.startSection(sect, comments=len(grouped))
            for v in sorted(grouped.items(), reverse=True, key=sorter):
                d.reportHTML('pre', 'Tracked Url: {url}\n'\
                    'Count: {count}\n'\
                    'Total Duration: {duration:.3f}s\n'\
                    'Average Duration: {avg:.3f}s'.format(**{
                        'url': v[1]['url'],
                        'count': v[1]['count'],
                        'duration': v[1]['duration'] / float(1000),
                        'avg': v[1]['duration'] / float(1000) / v[1]['count'],
                    }))
            d.endSection()
        d.endSection()

