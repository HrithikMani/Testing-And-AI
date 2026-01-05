"""
    Javascript unit tests
    @owner: sgrider
"""

from wcunittest import wcJSCode

def main(d, WCURL):
    # Just go anyway to ensure we're not in the frameset
    d.navigate(WCURL.OMNISCOPE)
    d.startSection('miestring')

    u = d.getWCUnitTest('EncodePV (i)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.encodePV('This is an invalid id', 'i')", 'This_20is_20an_20invalid_20id'),
        wcJSCode("miestring.encodePV('$$ This id is a hot mess!','i')", 'z_24_24_20This_20id_20is_20a_20hot_20mess_21'),
        wcJSCode("miestring.encodePV('Thisidshouldnotneedanyescaping','i')", 'Thisidshouldnotneedanyescaping'),
    ])
    u.test()

    u = d.getWCUnitTest('DecodePV (i)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.decodePV(miestring.encodePV('This is an invalid id','i'),'i');",
            'This is an invalid id'),
        wcJSCode("miestring.decodePV(miestring.encodePV('$$ This id is a hot mess!','i'),'i');",
            '$$ This id is a hot mess!'),
        wcJSCode("miestring.decodePV(miestring.encodePV('Thisidshouldnotneedanyescaping','i'),'i');",
            'Thisidshouldnotneedanyescaping'),
    ])
    u.test()

    u = d.getWCUnitTest('EncodePV (I)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.encodePV('$$ This is an invalid id','I');", '_24_24_20This_20is_20an_20invalid_20id'),
        wcJSCode("miestring.encodePV('!@#$','I');", '_21_40_23_24'),
        wcJSCode("miestring.encodePV('_-:.','I');", '__-:.'),
    ])
    u.test()

    u = d.getWCUnitTest('DecodePV (I)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.decodePV(miestring.encodePV('$$ This is an invalid id','I'),'I');",
            '$$ This is an invalid id'),
        wcJSCode("miestring.decodePV(miestring.encodePV('!@#$','I'),'I');", '!@#$'),
        wcJSCode("miestring.decodePV(miestring.encodePV('_-:.','I'),'I');", '_-:.'),
    ])
    u.test()

    u = d.getWCUnitTest('EncodePV (j)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.encodePV('Thisisavalidvarname', 'j')", 'Thisisavalidvarname'),
    ])
    u.test()

    u = d.getWCUnitTest('DecodePV (j)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.decodePV('Thisisavalidvarname', 'j')", 'Thisisavalidvarname'),
    ])
    u.test()

    u = d.getWCUnitTest('EncodePV (j)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.encodePV('This is an invalid varname', 'j')", 'This_20is_20an_20invalid_20varname'),
    ])
    u.test()

    u = d.getWCUnitTest('DecodePV (j)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.decodePV('This_20is_20an_20invalid_20varname', 'j')", 'This is an invalid varname'),
    ])
    u.test()

    u = d.getWCUnitTest('EncodePV (J)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.encodePV('Thisisavalidvarname', 'J')", 'Thisisavalidvarname'),
    ])
    u.test()

    u = d.getWCUnitTest('DecodePV (J)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.decodePV('Thisisavalidvarname', 'J')", 'Thisisavalidvarname'),
    ])
    u.test()
    u = d.getWCUnitTest('EncodePV (J)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.encodePV('This is an invalid varname', 'J')", 'This_20is_20an_20invalid_20varname'),
    ])
    u.test()

    u = d.getWCUnitTest('DecodePV (J)', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.decodePV('This_20is_20an_20invalid_20varname', 'J')", 'This is an invalid varname'),
    ])
    u.test()

    u = d.getWCUnitTest('startsWith', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.startsWith('Text', 'Text');", True),
        wcJSCode("miestring.startsWith('Text_At_Start', 'Text');", True),
        wcJSCode("miestring.startsWith('Text_That_Begins_With_And_Ends_With_Text', 'Text');", True),
        wcJSCode("miestring.startsWith('Text_That_Begins_With_Contains_Text_And_Ends_With_Text', 'Text');", True),
        wcJSCode("miestring.startsWith('Contains_Text_But_Does_Not_Start_With_It', 'Text');", False),
        wcJSCode("miestring.startsWith('Missing', 'Text');", False),
        wcJSCode("miestring.startsWith('Ends_With_Text', 'Text');", False)
    ])
    u.test()

    u = d.getWCUnitTest('endsWith', coreCheck=False)
    u.verifyJS([
        wcJSCode("miestring.endsWith('Text', 'Text');", True),
        wcJSCode("miestring.endsWith('Ends_With_Text', 'Text');", True),
        wcJSCode("miestring.endsWith('Text_That_Begins_With_And_Ends_With_Text', 'Text');", True),
        wcJSCode("miestring.endsWith('Contains_Text_And_Ends_With_Text', 'Text');", True),
        wcJSCode("miestring.endsWith('Contains_Text_And_Does_Not_End_With_It', 'Text');", False),
        wcJSCode("miestring.endsWith('Missing', 'Text');", False),
        wcJSCode("miestring.endsWith('Text_At_Beginning_Only', 'Text');", False)
    ])
    u.test()

    d.endSection()

    d.startSection('miebrowser')
    u = d.getWCUnitTest('miebrowser.getAgent', coreCheck=False)
    # Different tests, depening on our current browser
    if d.browser == 'Firefox':
        enum = 'AGENT_MOZILLA'
    elif d.browser == 'Chrome':
        enum = 'AGENT_CHROME'
    elif d.browser == 'Ie':
        enum = 'AGENT_MSIE'
    elif d.browser == 'Opera':
        enum = 'AGENT_OPERA'
    elif d.browser == 'Safari':
        enum = 'AGENT_SAFARI'
    else:
        enum = 'UNKNOWN'
    u.verifyJS([
        wcJSCode("miebrowser.browserName()", d.browser),
        wcJSCode("miebrowser.getAgent() == wcenum('{0}')".format(enum), True),
    ])
    u.test()
    d.endSection()

    d.startSection('miearray')
    u = d.getWCUnitTest('inSet', coreCheck=False)
    u.verifyJS([
        wcJSCode("miearray.inSet(1, [1,2,3,4,5])", True),
        wcJSCode("miearray.inSet(3, [1,2,3,4,5])", True),
        wcJSCode("miearray.inSet(5, [1,2,3,4,5])", True),
        wcJSCode("miearray.inSet(0, [1,2,3,4,5])", False),
        wcJSCode("miearray.inSet(-1, [1,2,3,4,5])", False),
        wcJSCode("miearray.inSet(6, [1,2,3,4,5])", False),
    ])
    u.test()

    u = d.getWCUnitTest('each', coreCheck=False)
    u.verifyJS([
        wcJSCode("function() {var x=[]; miearray.each([1,2,3], function(val) {x.push(val + 1)}); return x}()", [2,3,4]),
        wcJSCode("function() {var x=[]; miearray.each([1,2,3], function(val) {x.push(val * val)}); return x}()", [1, 4, 9]),
    ])
    u.test()
    d.endSection()

    d.startSection('miedate')
    u = d.getWCUnitTest('Native Date Methods', coreCheck=False)
    u.verifyJS([
        wcJSCode("function() {var x = new window.Date(2000,0,1);"\
            "return {'year':x.getYear(),'month':x.getMonth(),'date':x.getDate()}}();",
            {'year':100,'date':1,'month':0}),
    ])
    u.test()

    u = d.getWCUnitTest('toSQLMethods', coreCheck=False)
    u.verifyJS([
        wcJSCode("function() {var x = new window.Date(2000,0,1); return x.toSQLDate()}()", '2000-01-01'),
        wcJSCode("function() {var x = new window.Date(2000,0,1); return x.toSQLDateTime()}()", '2000-01-01 00:00:00'),
        wcJSCode("function() {var x = new window.Date(2000,0,1,13,30,30); return x.toSQLTime()}();", '13:30:30'),
    ])
    u.test()
    d.endSection()

    d.startSection('mieobject')
    u = d.getWCUnitTest('getLength', coreCheck=False)
    u.verifyJS([
        wcJSCode("mieobject.getLength({'name': 'selenium', 'type': 'test', 'func': function() {}})", 3),
    ])
    u.test()
    d.endSection()

    d.startSection('miecgi')
    u = d.getWCUnitTest('parseURI', coreCheck=False)
    u.verifyJS([
        wcJSCode("miecgi.parseURI(window.location.href).domain", ("zeus.med-web.com", "zeus-test.med-web.com")),
        wcJSCode("miecgi.parseURI(window.location.href).directoryPath", '/{0}/{1}/'.format('webchart', d.getUserData('handle'))),
        wcJSCode("miecgi.parseURI(window.location.href).protocol", "https"),
        wcJSCode("miecgi.parseURI(window.location.href).authority", ('zeus.med-web.com', 'zeus.med-web.com:8888', 'zeus-test.med-web.com', 'zeus-test.med-web.com:8888')),
    ])
    u.test()

    u = d.getWCUnitTest('cgiObject', coreCheck=False)
    u.verifyJS([
        wcJSCode("miecgi.cgiObject({f: 'chart', pat_id: 18}).toCGIString()", 'f=chart&pat_id=18'),
        wcJSCode("miecgi.cgiObject({f: 'chart', pat_id: 18}).toCGIString('?')", '?f=chart&pat_id=18'),
		wcJSCode("miecgi.cgiObject({f: 'blankentries', blank: '', pat_id: 20}).toCGIString()",  'f=blankentries&blank&pat_id=20'),
        wcJSCode("function() {var c=miecgi.cgiObject({f: 'chart', pat_id: 18}); c.add('test', 'this'); return c.toCGIString()}()", 'f=chart&pat_id=18&test=this'),
        wcJSCode("function() {var c=miecgi.cgiObject({f: 'chart', pat_id: 18}); c.add('test', 'this has space'); return c.toCGIString()}()", 'f=chart&pat_id=18&test=this%20has%20space'),
        wcJSCode("function() {var c=miecgi.cgiObject({f: 'chart', pat_id: 18}); c.addString('  & &&a=b&  & '); return c.toCGIString()}()", 'f=chart&pat_id=18&a=b'),
        wcJSCode("function() {var c=miecgi.cgiObject({f: 'chart', pat_id: 18}); c.addString('  & &&a=b&  & ', true); return c.toCGIString()}()", 'f=chart&pat_id=18&a=b'),
        wcJSCode("function() {var c=miecgi.cgiObject({f: 'chart', pat_id: 18}); c.addString('&thishas space=1'); return c.toCGIString()}()", 'f=chart&pat_id=18&thishas space=1'),
        wcJSCode("function() {var c=miecgi.cgiObject({f: 'chart', pat_id: 18}); c.addString('&thishas space=1', true); return c.toCGIString()}()", 'f=chart&pat_id=18&thishas%20space=1'),
        wcJSCode("function() {var c=miecgi.cgiObject(); c.addString('&this is alone=1', true); return c.toCGIString()}()", 'this%20is%20alone=1'),
		wcJSCode("function() {var c=miecgi.cgiObject(); c.addString('&=invalidKey', true); return c.toCGIString()}()", '')
    ])
    u.test()
    d.endSection()

    d.startSection('mieel')
    u = d.getWCUnitTest('Lookup By ID ($)', coreCheck=False)
    u.verifyJS([
        wcJSCode("mieel.$('wc_footer_container') ? true : false", True),
    ])
    u.test()

    u = d.getWCUnitTest('Lookup By Class Name', coreCheck=False)
    u.verifyJS([
        wcJSCode("x.length ? true : false", True, "var x = mieel.getElementsByClassName('wc_tab')"),
    ])
    u.test()

    u = d.getWCUnitTest('getInnerText', coreCheck=False)
    u.verifyJS([
        wcJSCode("mieel.innerText(document.getElementsByClassName('wc_tab')[0])", 'Quick View'),
    ])
    u.test()
    d.endSection()

    d.startSection('miehttp')
    # We need a way to unit test async functions in miedriver, we may have to implement
    # d.execute_script_async
    u = d.getWCUnitTest('Synchronous Response Checking', coreCheck=False)
    u.verifyJS([
        wcJSCode("miehttp.get({async: false, url: '?f=ajaxget&system_report'}) instanceof XMLHttpRequest", True),
    ])
    u.test()

    u = d.getWCUnitTest('Synchronous Response Checking (Using miehttp object style)', coreCheck=False)
    u.verifyJS([
        wcJSCode("h.get('?f=ajaxget&system_report') instanceof XMLHttpRequest", True,
            "var h = miehttp.http({async: false});"),
    ])
    u.test()

    u = d.getWCUnitTest('Synchronous Response Checking (jsHTTP)', coreCheck=False)
    u.verifyJS([
        wcJSCode("h.get('?f=ajaxget&system_report') instanceof XMLHttpRequest", True,
            "var h = new jsHTTP(); h.SetAsync(false)"),
    ])
    u.test()

    u = d.getWCUnitTest('Synchronous Response Checking (jsHTTP New Instantiation Style)', coreCheck=False)
    u.verifyJS([
        wcJSCode("h.get() instanceof XMLHttpRequest", True,
            "var h = new jsHTTP({'async': false, 'url': '?f=ajaxget&system_report'})"),
        wcJSCode("h.get().responseXML instanceof XMLDocument", True,
            "var h = new jsHTTP({'async': false, 'url': '?f=ajaxget&system_report'})"),
    ])
    u.test()

    u = d.getWCUnitTest

    u = d.getWCUnitTest('Synchronous Response Checking Using Custom MIE ResponseType', coreCheck=False)
    # These won't work yet because the MIE custom response only applies the argument
    # passed to the callback function, NOT the direct return of the GET function in
    # synchronous mode. These can only be tested in async mode or with convoluted sync testing
    """
    wcJSCode("Boolean(h.get().getResponse())", True,,
        "var h = new jsHTTP({'async': false, 'url': '?f=ajaxget&system_report'})"\
    wcJSCode("Boolean(h.get().getResponse().getXML())", True,,
        "var h = new jsHTTP({'async': false, 'url': '?f=ajaxget&system_report'})"\
    wcJSCode("Boolean(h.get().getResponse().getJSON())", True,,
        "var h = new jsHTTP({'async': false, 'url': '?f=ajaxget&system_report'})"\
    u.test()
    """
    d.endSection()

    d.startSection('miedomseek')
    d.endSection()

