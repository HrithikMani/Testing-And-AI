"""
@owners: pepperson
"""

def main (d, WCURL):
    """
    Verifies that the IDS correctly flags bad requests
    """
    
    t = d.getWCUnitTest('Verify Email for a known bad value')
    d.wcErrorLog.ignore('Intrusion Detection Triggered - Pattern (/../) found in (f=/../)')
    t.test(lambda d: d.navigate('?f=/../'), reason='Trigger the error email')

    t = d.getWCUnitTest('Verify Email for a known bad varname')
    d.wcErrorLog.ignore('Intrusion Detection Triggered - Pattern (/../) found in (/../=)')
    t.test(lambda d: d.navigate('?/../='), reason='Trigger the error email')

    t = d.getWCUnitTest('Verify Email for a known bad var/value pair')
    d.wcErrorLog.ignore('Intrusion Detection Triggered - Pattern (php) found in (f=php)')
    t.test(lambda d: d.navigate('?f=php'), reason='Trigger the error email')

    t = d.getWCUnitTest('Verify Email for a configured bad varname')
    d.wcErrorLog.ignore('Intrusion Detection Triggered - Pattern (md5() found in (md5(abc)=admin)')
    t.test(lambda d: d.navigate('?md5(abc)=admin'), reason='Trigger the error email')

    t = d.getWCUnitTest('Verify Email for a configured bad value')
    d.wcErrorLog.ignore('Intrusion Detection Triggered - Pattern (md5() found in (f=md5(abc))')
    t.test(lambda d: d.navigate('?f=md5(abc)'), reason='Trigger the error email')

    t = d.getWCUnitTest('Verify No Email for a known bad value in a whitelisted varname')
    t.test(lambda d: d.navigate('?f=admin&file=/../'), reason='Trigger the error email')

    t = d.getWCUnitTest('Verify No Email for a configured bad value in a whitelisted varname')
    t.test(lambda d: d.navigate('?f=admin&file=md5(abc)'), reason='Trigger the error email')
