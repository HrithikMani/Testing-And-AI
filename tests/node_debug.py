"""
Test used to generate some stats on the running VM node

"""
import subprocess
import os

def network(d):
    oldbase = d._base_urls[-1]
    d.setBaseURL('')
    d.navigate('https://fast.com')
    d.waitFor(d, lambda d: d.getElement(xpath="//span[contains('oc-icon-refresh')]"), timeout=120)
    d.screenshot('Speedtest')
    d.setBaseURL(oldbase)

def disk(d):
    of = os.path.join(os.path.dirname(__file__), '_nodetest_.dat')
    for x in range(1, 4):
        p = subprocess.Popen('dd if=/dev/zero of={0} bs=1G count=1 oflag=sync && rm {0}'.format(of),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        d.reportHTML('pre', 'Writing to file: {0}\n'.format(of) + err)

def main(d, _):
    tests = (
        ['Network Speed Test', network],
        ['Disk Speed Test', disk],
    )
    for name, func in tests:
        try:
            d.startSection(name)
            func(d)            
        except Exception as e:
            d.reportCommandStatus('Exception in test', '', False, '', str(e))
        finally:
            d.endSection()

