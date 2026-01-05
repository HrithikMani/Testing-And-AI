from xml.dom import minidom
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
try:
    import StringIO
except ImportError:
    import io as StringIO
import json
import os.path
import urllib
try:
    import urllib2
except ImportError:
    import urllib.parse
import os
import time
import subprocess

from wcunittest import wcElement
from wcunittest import wcDBRecord

TESTGROUPS = [
    {
        'name': 'Sample Tests',
        'description': 'Sample Tests',
        'src': 'file_validator_tests.json'
    }
]

def uploadData(d, udata):
    try:
        test = udata['test']
        cgi = { 'f' : 'filevalidator', 
                'verb' : test['verb'].encode('utf-8'), 
                'line_delim' : test['line_delim'].encode('utf-8'), 
                'col_delim' : test['col_delim'].encode('utf-8'),
                'line_regex' : test['line_regex'].encode('utf-8'),
                'test_data' : test['tests'].encode('utf-8') }

        fileData = {}
        d.reportHTML('pre', '', section='Test Variables')
        d.initSubComment("Verbosity: '{0}'".format(test['verb']))
        d.initSubComment("Line Delimiter: '{0}'".format(test['line_delim']))
        d.initSubComment("Line Regex: '{0}'".format(test['line_regex']))
        d.initSubComment("Column Delimiter: '{0}'".format(test['col_delim']))
        d.initSubComment("Test Layout: '{0}'".format(test['tests']))

        script_dir = os.path.dirname(__file__)
        rel_path = '../upload/{0}'.format(test['file'])
        abs_file_path = os.path.join(script_dir, rel_path)

        if os.path.exists(abs_file_path):
            try:
                d.reportHTML('pre', '', section='File Data')
                d.initSubComment("File Path: '{0}'".format(abs_file_path))
                fileData['process_file'] = open(abs_file_path, 'r')
                d.initSubComment("<a target='_blank' href='{0}'>View Test File Data</a>".format(rel_path))

                udata['res'] = udata['wccurl'].multiPartPost(data=cgi, files=fileData)
                    
                if test['baseline'] in udata['res'].decode():
                    d.reportCommandStatus('File Passed Validation', '', True, '', '')
                else:
                    d.reportCommandStatus('File Failed Validation', '', False, '', '')

                d.reportHTML('pre', udata['res'].decode(), section='WC Ouput')
                d.reportHTML('pre', test['baseline'], section='Baseline')

                fileData['process_file'].close()
            except Exception as e:
                d.reportCommandStatus('Failed to open data file: {0}'.format(abs_file_path.decode()), e, False, '', '')   
        else:
            d.reportCommandStatus('File Could Not Be Found: {0}'.format(abs_file_path.decode()), '', False, '', '')
    except Exception as e:
        d.reportCommandStatus(repr(e), e, False, '', '')

def runTestGroup(d, tests, udata):
    wccurl = udata['wccurl']
    res = udata['res']

    for test in tests:
        if test['file'] == "":
            d.reportCommandStatus('Skipping test without any file data', '', False, '', '')
        else:
            unit = d.getWCUnitTest(test['name'])                
            unit.test(uploadData, { 'wccurl' : wccurl, 'res' : res, 'test' : test })

def main(d, _):
    base = d._base_urls[-1]
    if not base.endswith('webchart.cgi'):
        base = '{0}{1}webchart.cgi'.format(base, '' if base[-1] == '/' else '/')
    wccurl = d.getWCCurl(base)
    wccurl.setWCCookie('WCTESTSESSION')
    res = ""

    for group in TESTGROUPS:
        name = group.get('name')
        desc = group.get('description')
        filename = group.get('src')
        
        d.startSection('{0} | {1}'.format(name, filename), comments=desc)

        try:
            file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testlib', filename)
            if (os.path.isfile(file)):
                try:
                    with open(file, 'r') as src:
                        tests = json.load(src)
                        runTestGroup(d, tests, { 'wccurl' : wccurl, 'res' : res })
                except Exception as e:
                    d.reportCommandStatus('Failed to open file: ' + file, e, False, '', '')
            else:
                d.reportCommandStatus('Failed to open test file: ' + file, '', False, '', '')
        except Exception as e:
            d.reportCommandStatus('Failed to import test list', e, False, '', '')
        d.endSection()
