"""
    Unit test for WebChart Preference Manager
    @owners: sgrider
"""
import os
import json
from wcunittest import wcElement, wcDBRecord

# Give a dbquery that must return numRows == 0 if you want to ignore a preference
CONDITIONAL_PREFS = {
    'WebChart': {
        'User Interface': {
            'Enable Messenger': "SELECT value FROM system_settings WHERE module='System' "\
                "AND section='MIEMessenger' AND item='Enable Messenger' AND value>0",
        },
    },
    'E-Chart': {
        'Injections': {
            'Confirm Route Status On Add': "SELECT value FROM system_settings WHERE "\
                "module='E-Chart' AND section='Injections' AND "\
                "item='Wait For Route Completion' AND value>0",
        },
    }
}

# Give a dbquery that must return numRows == 0 if you want to ignore a preference option
CONDITIONAL_OPTIONS = {
    'E-Chart': {
        'Patient Search Criteria': {
            'Search By': {
                'Account': "SELECT value FROM system_settings WHERE module='E-Chart' "\
                    "AND section='Defaults' AND item='Search for Account' AND value>0",
            }
        },
    },
}

def prefIsIgnored(opts, d, mod, cat, name, opt=None):
    if opt:
        condQuery = opts.get(mod, {}).get(cat, {}).get(name, {}).get(opt, '')
    else:
        condQuery = opts.get(mod, {}).get(cat, {}).get(name, '')
    if condQuery:
        res = d.miedb.dbQuery(condQuery)
        if not res or res.numRows() == 0:
            return True
    return False

def setPref(d, udata):
    d.wcutils.SetPreference(udata.get('module'), udata.get('category'), udata.get('name'),
        udata.get('value'))

def main(d, WCURL):
    prefParsed = {}
    parsedFile = 'preferences_parsed.py'
    # First try to read the auto-generated preferences file
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', parsedFile)) as fp:
            prefParsed = json.load(fp)
    except Exception as e:
        d.reportCommandStatus('Load Parsed Preferences', 'Failed to load auto-generated file',
            False, parsedFile, e)
        return
    # Now we use this auto-gen data to verify the UI looks like we expect it to
    d.startSection('UI Verification')
    d.navigate('?f=admin')
    for module in sorted(prefParsed.keys()):
        for category in sorted(prefParsed[module].keys()):
            u = d.getWCUnitTest('Verify UI Elements for {0} | {1}'.format(module, category),
                coreCheck=False)
            for name, pref in sorted(prefParsed[module][category].items()):
                if prefIsIgnored(CONDITIONAL_PREFS, d, module, category, name):
                    continue
                if pref['type'] == 'INPUT_TYPE_DBQUERY' and pref['query']:
                    res = d.miedb.dbQuery(pref['query'])
                    if res and res.numRows():
                        u.verifyElements(wcElement('xpath', '//label[text()="{0}"]'.format(name)),
                            reason='Display label exists for {0}'.format(name))
                        u.verifyElements([wcElement('xpath',
                            '//select[@name="{0}{1}{2}"]//option[contains(., "{3}") and @value="{4}"]'.format(
                            module, category, name, row[1] if res.numFields() > 1 else row[0], row[0])) \
                            for row in res.rows],
                            reason='Verify display/code option for {0}'.format(name))
                elif pref['type'] == 'INPUT_TYPE_PERMLIST':
                    u.verifyElements(wcElement('xpath', '//label[text()="{0}"]'.format(name)),
                        reason='Display label exists for {0}'.format(name))
                    if len(pref['codes']) == len(pref['display']):
                        # Verify codes/display exist and correlate to each other based on
                        # the given orders in each list
                        eles = []
                        for s, c in zip(pref['display'], pref['codes']):
                            if not prefIsIgnored(CONDITIONAL_OPTIONS, d, module, category, name, s):
                                eles.append(wcElement('xpath',
                                    '//select[@name="{0}{1}{2}"]'\
                                    '//option[contains(., "{3}") and @value="{4}"]'.format(
                                    module, category, name, s, c)))
                        u.verifyElements(eles, reason='Verify code/display exists for {0}'.format(name))
                    else:
                        # Since the number of codes/display do not match each other
                        # we can't assume any relationship between them and we can't ignore
                        # specific codes since they're dependendent on knowing the corresponding
                        # display option. So all we can do here is verify the display options
                        eles = []
                        for s in pref['display']:
                            if not prefIsIgnored(CONDITIONAL_OPTIONS, d, module, category, name, s):
                                eles.append(wcElement('xpath',
                                    '//select[@name="{0}{1}{2}"]//option[contains(., "{3}")]'.format(
                                    module, category, name, s)))
                        u.verifyElements(eles, reason='Verify display option exist for {0}'.format(name))
                elif pref['type'] == 'INPUT_TYPE_AUTOCOMPLETE':
                    u.verifyElements(wcElement('xpath', '//label[text()="{0}"]'.format(name)),
                        reason='Display label exists for {0}'.format(name))
                    u.verifyElements(wcElement('xpath',
                        '//input[@name="{0}" and @class="autocomplete"]'.format(
                        '{0}_{1}_{2}_ac_txt'.format(module, category, name).translate(None, ' /-'))),
                        reason='Verify autocomplete input')
            u.test()
    d.endSection()

    # Now we want to load up the preferences_data that developers have set so that we 
    # can verify that the preferences options behave as expected
    try:
        import preferences_data
    except ImportError as e:
        d.reportCommandStatus('Import preferences_data', 'Failed to import preferences_data',
            False, '', '')
        return
    prefData = preferences_data.preferences
    def sortCodes(c):
        try:
            return int(c[0])
        except:
            return c[0]

    d.startSection('Functionality Verification')
    for module in sorted(prefData.keys()):
        for category in sorted(prefData[module].keys()):
            for name, pref in sorted(prefData[module][category].items()):
                for code, tests in sorted(pref.items(), key=sortCodes):
                    for t in tests:
                        if not t['elements']:
                            continue
                        u = d.getWCUnitTest('{0} | {1} | {2} [Verify code: {3}]'.format(
                            module, category, name, code), coreCheck=False)
                        u.setup(setPref, {
                            'module': module,
                            'category': category,
                            'name': name,
                            'value': code
                        }, reason='Set the preference value in the db')
                        u.verifyElements(t['elements'], reason=t.get('reason') or 'Reason not given')
                        u.test(lambda x: x.navigate(t['url']),
                            reason='Visit url: {0}'.format(t['url']))
    d.endSection()

