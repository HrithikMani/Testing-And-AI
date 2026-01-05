import urllib.parse
from xml.dom import minidom
from io import StringIO

from wcunittest import wcElement

IGNORED_MODULES = ['PHP', 'DymoXML']

def execLayout(unit, data):
    url = {
        'f': 'layout',
    }
    url.update(data)
    unit.getDriver().navigate('?{0}'.format(urllib.parse.urlencode(url)))

def main(d, WCURL):
    d.wcutils.insertWCTSession(d.getUserData('selenium_username'))
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.setWCCookie('WCTESTSESSION')
    source = wccurl.get('?f=ajaxget&s=layout&hide_html=1')
    if not len(source):
        d.reportCommandStatus('GetXMLSource', '', False, '', 'No Source Returned')
        return
    try:
        dom = minidom.parse(StringIO(source))
    except Exception as e:
        d.reportCommandStatus('Parse XML', '', False, source, e)
        return
    allLayouts = [x for x in dom.getElementsByTagName('LAYOUT') if \
                  'name' in x.attributes.keys() and 'module' in x.attributes.keys()]
    validLayouts = [x for x in allLayouts if x.getAttribute('module') not in IGNORED_MODULES]
    d.reportCommandStatus('Committed Layouts', 'Ignored Modules: {0}'.format(IGNORED_MODULES),
                          None, '', 'Validating {0} layouts out of {1} total'.format(
                          len(validLayouts), len(allLayouts))
    )
    validLayouts.sort(key=lambda x: (x.attributes['module'].value, x.attributes['name'].value))
    d.setUserData('skip_logging_functions', True)
    for layout in validLayouts:
        data = {
            'name': layout.attributes['name'].value,
            'module': layout.attributes['module'].value,
        }
        with d.getWCUnitTest('Validate Committed Layout {module}:{name}'.format(**data)) as u:
            u.verifyElements([
                wcElement('xpath', "//*[contains(., 'ERROR: UNKNOWN WC CODE')]",
                          exists=False),
                wcElement('xpath', "//*[contains(., 'ERROR on SELECT layout query:')]",
                          exists=False),
                wcElement('xpath', "//h3[contains(., 'ERROR: ')]", exists=False),
            ], reason='Check for possible error messages')
            u.test(execLayout, data, reason='Render the layout')
