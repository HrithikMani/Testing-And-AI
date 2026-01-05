import os
import re
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
import json
import collections
import base64
import functools


JSON_HEADERS = {'Content-Type': 'application/json'}


def jsonUrlCB(url):
    try:
        return 'webchart.cgi/json/' + base64.b64encode(urlparse.unquote(url))
    except TypeError:
        return 'webchart.cgi/json/' + base64.b64encode(urlparse.unquote(url).encode('utf8')).decode('utf8')


def fhirUrlCB(url):
    return 'webchart.cgi/fhir/' + url


def jsonDataCB(data):
    return json.dumps(json.loads(data))


def jsonResponseCB(data, parsed=None):
    ignored_keys = ['edit_date', 'create_date', 'login_lastfailure', 'email',
        'last_login', 'login_count']
    d = parsed if parsed is not None else json.loads(data, object_pairs_hook=collections.OrderedDict)
    if isinstance(d, list):
        for key in d:
            jsonResponseCB(None, key)
    elif isinstance(d, dict):
        for key in d.keys():
            if key in ignored_keys:
                d[key] = 'Dynamic Value Removed For Testing'
            else:
                jsonResponseCB(None, d[key])
    return json.dumps(d, indent=4)


class CurlTest():
    """
    Tests are defined by theses parameters:
        * Title (displayed in the results as a section)
        * Filename containing list of urls and associated names
            a) These files must be located at webchart/selenium/wccurl
            b) These files are parsed by the wccurl selenium extension using these rules:
                i) Lines beginning with a SUPPORTED_HTTP verb are parsed as urls
                    >) Url is considered the last continuous string
                    >) Header fields may be set by using the syntax HEADER^VALUE before
                        the url string
                ii) Lines beginning with a supported COMMAND are executed
                iii) Blank lines or commented lines are skipped
                iv) All other lines are interpreted as filenames to name the following urls
        * Indicate using a WCTCOOKIE to login
        * Credentials object if not using a WCTCOOKIE
        * Regex to use for diffing
        * Log errors to ignore

    Note that the MIEDriver instance will have all available regexes populated
    into various userData fields. So if you need to use a non-standard regex
    you can either build one yourself or see what else is available in
    webchart/selenium/extensions/wccurl_regex_rules.py

    """
    url_callback = None
    response_callback = None
    headers = None

    def __init__(self, title, filename, cookies=None, credentials=None, regex=None, errors_ignored=None):
        self.title = title
        self.filename = filename
        self.cookies = cookies
        self.credentials = credentials
        self.regex = regex
        self.errors_ignored = errors_ignored

    def run(self, d, baseurl, selenium_login):
        d.startSection(self.title)
        if self.cookies:
            d.wcutils.insertWCTSession(selenium_login['login_user'])
        with d.getWCCurl(baseurl, self.cookies, self.credentials, self.regex) as curl:
            if self.url_callback:
                curl.setUrlCB(self.url_callback)
            if self.response_callback:
                curl.setResponseCB(self.response_callback)
            if self.headers:
                curl.setHeaders(self.headers)
            curl.runFile(os.path.join(os.path.dirname(__file__), '..', 'wccurl', self.filename))
            if self.errors_ignored:
                for ei in self.errors_ignored:
                    d.wcErrorLog.ignore(ei)
        d.endSection()


class JsonTest(CurlTest):
    url_callback = functools.partial(jsonUrlCB) # prevent "self" from being passed to jsonUrlCB
    response_callback = functools.partial(jsonResponseCB)
    headers = JSON_HEADERS


class FHIRTest(CurlTest):
    url_callback = functools.partial(fhirUrlCB)
    response_callback = functools.partial(jsonResponseCB)
    headers = JSON_HEADERS


def main(d, WCURL):
    """
    This test is a replacement for legacy wctest.pl
    It essentially hits webchart urls with various parameters and logs the
    output, diffing them to a baseline as it goes.
    In the event that the generated output differs from the baseline someone
    will either need to figure out what brought about the change and fix it or
    if the change is desired, they will need to update the baseline file by
    committing the generated output as the new baseline.

    """

    WCTCOOKIE = {
        '{0}_session_id'.format(d.getUserData('_submissionData')['dbConf']['dbname']): 'WCTESTSESSION'
    }
    selenium_login = {
        'login_user': d.getUserData('selenium_username'),
        'login_passwd': d.getUserData('selenium_password')
    }
    regexg = [
        [r'zeus(.+)?\.med-web\.com(:[0-9]+)?','WEBSERVER_REMOVED',0,0],
        ['email=".*?"', 'email="EMAIL_REMOVED"', 0, 0],
        [d.getUserData('handle'), 'HANDLE_REMOVED', 0, 0],
    ]
    # We want to ignore everything except for the UNSUPPORTED BROWSER message
    browser_regex = [
        ['<html.*(<a.*UNSUPPORTED BROWSER.*?</a>)', '\\1', 0, re.DOTALL|re.IGNORECASE],
        ['(</a>).*', '\\1', 0, re.DOTALL|re.IGNORECASE],
    ]
    # Strip the "create_datetime" and "revision_datetime" properties.
    json_regex = [
        # ['"((create|revision|modified)_datetime)": "\\d{{4}}-\\d{{2}}-\\d{{2}} \\d{{2}}:\\d{{2}}:\\d{{2}}"', '"\\1": "REMOVED"', 0, 0],
        [r'"((create|revision|modified)_datetime)": "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"', '"\\1": "REMOVED"', 0, 0],
    ]
    # Strip the start and end dates from FHIR
    fhir_regex = d.getUserData('wcHtmlRegex').copy()
    fhir_regex.append([r'"start": "\d\d\d\d-\d\d-\d\d"', '"start": "REMOVED"', 0, 0])
    fhir_regex.append([r'"end": "\d\d\d\d-\d\d-\d\d"', '"end": "REMOVED"', 0, 0])
    baseurl = d._base_urls[-1]

    tests = [
        CurlTest('AJAX XML Responses', 'ajax_urls', WCTCOOKIE, regex=regexg),
        CurlTest('Unsupported Browser Check', 'browser_urls', regex=browser_regex),
        CurlTest('Layout streams', 'layout_urls', WCTCOOKIE, regex=d.getUserData('wcHtmlRegex')),
        CurlTest('Audit Event Log', 'aelog_urls', WCTCOOKIE, regex=d.getUserData('wcHtmlRegex')),
        CurlTest('CDA Generation', 'cda_urls', WCTCOOKIE),
        CurlTest('WebChart Inventory urls', 'inventory_urls', WCTCOOKIE, regex=d.getUserData('wcHtmlRegex')),
        CurlTest('System', 'system_tests', WCTCOOKIE, regex=d.getUserData('wcHtmlRegex')),
#       CurlTest('Chart HTML', 'chart_urls', credentials=selenium_login, regex=d.getUserData('wcHtmlRegex')),
#       CurlTest('WebChart Growth Charts', 'growth_charts', WCTCOOKIE, regex=d.getUserData('wcHtmlRegex')),
        JsonTest('JSON Get requests', 'json_urls_get', WCTCOOKIE, regex=json_regex),
        JsonTest('JSON Post requests', 'json_urls_post', WCTCOOKIE),
        JsonTest('JSON Get without Golden Ticket', 'json_urls_ticket_get', credentials=selenium_login),
        JsonTest('JSON Get with Golden Ticket', 'json_urls_ticket_get', WCTCOOKIE),
        JsonTest('JSON Post without Golden Ticket', 'json_urls_ticket_post', credentials=selenium_login),
        JsonTest('JSON Post with Golden Ticket', 'json_urls_ticket_post', WCTCOOKIE),
        JsonTest('Scishield POST requests', 'scishield_json_urls_post', WCTCOOKIE),
        JsonTest('OAuth Authorization Codes Cooked Handler GET', 'oauth_authorization_codes_get', WCTCOOKIE),
        JsonTest('OAuth Authorization Codes Cooked Handler POST', 'oauth_authorization_codes_post', WCTCOOKIE),
        FHIRTest('FHIR Get requests', 'fhir_url_get', WCTCOOKIE, regex=fhir_regex),
        FHIRTest('FHIR Post requests', 'fhir_url_post', WCTCOOKIE),
        CurlTest('WebChart Unittests', 'webchart_unit', WCTCOOKIE, regex=d.getUserData('wcHtmlRegex'),
                 errors_ignored = [
                     'Attempt to run query with insufficient permissions: SELECT 1+1 AS sum',
                     'WCJS Log: Testing WCJS console.log',
                     'WCJS Error: Testing WCJS console.error',
                 ]),
    ]

    for test in tests:
        # setup for tests that need it
        if test.filename == 'webchart_unit':
            # OzwellPatientReferrer
            d.wcutils.SetSystemSetting(
                'AI', 'Agent', 'URL',
                "https://ai.bluehive.com",
                False
            )

        test.run(d, baseurl, selenium_login)

        # teardown
        if test.filename == 'webchart_unit':
            # OzwellPatientReferrer
            d.wcutils.SetSystemSetting(
                'AI', 'Agent', 'URL',
                "",
                False
            )