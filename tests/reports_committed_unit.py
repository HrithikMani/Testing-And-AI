import json
from xml.dom import minidom
try:
    from urllib.request import quote, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib import quote
    from urllib2 import urlopen, URLError
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from wcunittest import wcElement

IGNORED_CATEGORIES = ('WCINCLUDE', 'Model', 'Compendium')
IGNORED_REPORTS = ('Portal Supervisor Message Notification Email','RandomDrugScreenGenerator', 'MIE Test Metrics')

def getResponse(d, url):
    ret = None
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.setWCCookie('WCTESTSESSION')
    try:
        ret = wccurl.get(url)
    except URLError as e:
        ret = None
    if not ret:
        d.reportCommandStatus('getResponse', '', False, '', 'Server returned no response')
    return ret

def execReport(unit, name):
    d = unit.getDriver()
    try:
        src = getResponse(d, '?f=ajaxget&s=run_system_report&report_name={0}&response_format=json'.format(
            quote(name)))
    except AttributeError:
        src = getResponse(d, '?f=ajaxget&s=run_system_report&report_name={0}&response_format=json'.format(
            quote(name)))
    js = None
    if src:
        try:
            js = json.loads(src)
            if 'results' in js.keys():
                if 'error' in js['results'].keys():
                    d.reportCommandStatus('Error in report', name, False, js['results']['error'], '')
                else:
                    d.reportCommandStatus('Report OK', name, True, '', '')
            else:
                d.reportCommandStatus('Response is missing "results" key', name, False, '', '')
        except Exception as e:
            d.reportCommandStatus('Failed to parse response as json', name, False, e, '')
        finally:
            d.reportHTML('pre', src if js is None else json.dumps(js, indent=2), 'Server Response')

def execLV(d, name):
    try:
        d.navigate('?f=admin&s=system_report&opp=query&report_name={0}'.format(
                   urllib.quote(name)))
    except AttributeError:
        import urllib.parse
        d.navigate('?f=admin&s=system_report&opp=query&report_name={0}'.format(
                   urllib.parse.quote(name)))

def checkForErrors(d, udata):
    eles = d.getElements(xpath="//span[@class='mielistview_error']")
    if not eles:
        d.reportCommandStatus('No Errors Present', '', True, '', '')
    for e in eles:
        children = d.getElements(xpath="./span", ele=e)
        d.reportCommandStatus(children[0].text, e.get_attribute('name'), False,
            children[2].text, '')
        d.reportHTML('div', children[1].text, 'Listview SQL')

def main(d, WCURL):
    d.wcutils.insertWCTSession(d.getUserData('selenium_username'))
    d.miedb.dbExec("UPDATE security_role_acl SET security_value=%s "\
    "WHERE module_name='Control' AND category_name='Manage System Reports' "\
    "AND security_role_id=(SELECT security_role_id FROM users WHERE "\
    "username=%s)", 2, d.getUserData('selenium_username'))
    xml = getResponse(d, '?f=ajaxget&s=system_report')
    if not xml:
        return
    try:
        dom = minidom.parse(StringIO.StringIO(xml))
    except AttributeError:
        dom = minidom.parseString(xml)
    except Exception as e:
        d.reportCommandStatus('XML Parsing Failed', '', False, f'DataType: {type(xml)} | xml: {vars(xml)}', '')
        d.reportHTML('pre', xml, 'Response')
        return

    allReports = [x for x in dom.getElementsByTagName('SYSTEM_REPORT') if \
                  'name' in x.attributes.keys()]

    validReports = [x for x in allReports if x.attributes['category'].value not in IGNORED_CATEGORIES \
					and x.attributes['name'].value not in IGNORED_REPORTS \
					and '@TIMER_TS' not in x.attributes['sql_query'].value \
                    and 'webchart_nmc.' not in x.attributes['sql_query'].value]
    d.reportCommandStatus('Committed Reports', 'Ignored Categories: {0}, Ignored Reports: {1}'.format(IGNORED_CATEGORIES, IGNORED_REPORTS),
                          None, '', 'Validating {0} reports out of {1} total'.format(
                          len(validReports), len(allReports)))
    validReports.sort(key=lambda x: x.attributes['name'].value)
    for report in validReports:
        name = report.attributes['name'].value
        with d.getWCUnitTest('Validate Committed Report: {0}'.format(name), coreCheck=False) as u:
            u.test(execReport, name, reason='Execute report SQL')
#            u.verifyElements([
#                wcElement('xpath', "//table[@class='lv_root']"),
#            ], reason='Verify a listview is present')
#            u.verifyFunc(checkForErrors, None, reason='Check for SQL Errors')
#            u.test(execLV, name, reason='Execute the report')
