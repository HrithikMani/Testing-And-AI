"""
    SystemSettings Unit Tests
    @owners: sgrider
"""
import urllib.parse as urllib_parse
try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request
try:
    from io import StringIO
except ImportError:
    from io import BytesIO as StringIO
from xml.dom import minidom

from wcunittest import wcElement, wcDBRecord

MODIFY_VALUE = '{module:.3s}|{section:.3s}|{item:.3s}|UNITTEST'

# Don't touch any settings for these items, it might screw something up
RESTRICTED_ITEMS = ['PORT', 'HOST', 'DATABASE', 'SERVER', 'HOSTNAME', 'DBPORT']

# Don't touch any settings for this section, it will definitely cause hours of debugging
RESTRICTED_SECTIONS = ['LOGIN','DB']

def dumpMemcache(d, module, section, item):
    d.wcutils.insertWCTSession(d.getUserData('selenium_username'))
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.setWCCookie('WCTESTSESSION')
    res = wccurl.get('?f=ajaxget&s=memcache&module={0}&section={1}&item={2}'.format(
        urllib_parse.quote(module),
        urllib_parse.quote(section),
        urllib_parse.quote(item)))
    d.reportHTML('pre', res, 'Memcache Value for {0}:{1}:{2}'.format(module, section, item))

def getSettings(d, query):
    d.wcutils.insertWCTSession(d.getUserData('selenium_username'))
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.setWCCookie('WCTESTSESSION')
    source = wccurl.get('?f=ajaxget&s=settings_query&querystring={0}'.format(urllib_parse.quote(query)))
    settings = []
    if not len(source):
        d.reportCommandStatus('GetXMLSource', '', False, '', 'No Source Returned')
    else:
        try:
            dom = minidom.parse(StringIO(source))
        except Exception as e:
            d.reportCommandStatus('Parse XML', '', False, source, e)
        else:
            settings = [dict(x.attributes.items()) for x in dom.getElementsByTagName('SETTINGS_AC') \
                if not x.attributes['item'].value.upper() in RESTRICTED_ITEMS and \
                not x.attributes['section'].value.upper() in RESTRICTED_SECTIONS]
    d.startSection('AJAX SETTINGS')
    for s in settings:
        d.reportCommandStatus('{module} | {section} | {item}'.format(**s), 'Default: {def_val}'.format(**s),
            None, 'Current: {curr_val}'.format(**s), '')
    d.endSection()
    return settings

def checkSettings(d, settings, xmlfield='curr_val'):
    for s in settings:
        d.startSection('Checking setting: {module} | {section} | {item} | actual db value against xmlfield: {0}'.format(xmlfield, **s))
        res = d.miedb.dbQuery("SELECT value FROM system_settings WHERE module='{module}' and section='{section}' AND item='{item}'".format(**s))
        row = res.getRow(0)
        if not row:
            d.reportCommandStatus('Setting Does Not Exist in DB', '', False, '', s)
        elif row['value'] != s[xmlfield]:
            d.reportCommandStatus('Setting db value does not match ajax response', 'DB Value: {0}'.format(row['value']), False, 'Ajax Value: {0}'.format(s[xmlfield]), '')
        else:
            d.reportCommandStatus('OK', 'DB Value: {0}'.format(row['value']), True, 'Ajax Value: {0}'.format(s[xmlfield]), '')
        d.endSection()

def modifySettings(d, settings):
    d.startSection('DBExec')
    for s in settings:
        d.miedb.dbExec("UPDATE system_settings SET value='{0}' WHERE module='{module}' AND section='{section}' AND item='{item}'".format(MODIFY_VALUE.format(**s), **s))
    d.endSection()

def main(d, WCURL):
    # This test cannot run in a time-altered state because memcache relies on timestamps
    d.wcutils.SetSystemSetting('WebChart', 'Demo', 'Demo Date', '0', False)
    d.miedb.dbExec("UPDATE users SET pwd_expire=DATE_ADD(CURDATE(), INTERVAL 1 YEAR) WHERE username='selenium'")

    queries = ['E-Chart', 'System', 'Admin']
    d.setScreenShotOnError(False)
    modify = []

    d.startSection('Verify that the setting values from the autocomplete match the DB values')
    for q in queries:
        d.startSection('Checking Original {0}'.format(q))
        s = getSettings(d, q)
        if s:
            checkSettings(d, s)
            modify.extend(s)
        d.endSection()
    d.endSection()

    d.startSection('Modifying all setting values in the DB')
    # Now go modify all the settings in the DB
    modifySettings(d, modify)
    d.endSection()

    d.startSection('Verify that the autocomplete properly returns the modified values from the DB')
    for q in queries:
        d.startSection('Checking Modified {0}'.format(q))
        s = getSettings(d, q)
        if s:
            checkSettings(d, s)
        d.endSection()
    d.endSection()

    # TODO: bring this back to work with memcache
    # Now we're going to test the deletion of some settings to ensure:
    # 1) That when we query for them and they come from the cache, the don't go back into the DB
    # 2) After flushing the cache when we query for them, they do go back into the db with the expected defaults
    #d.startSection('Verify that caching is working by deleting some settings and ensuring they still show up via the cache')
    # First we have to ensure that the values we're checking for are actually cached
    #d.miedb.dbExec("DELETE FROM system_settings WHERE module='System' AND section='Cron'")
    #settings = getSettings(d, "Cron")
    #if not settings:
    #    d.reportCommandStatus('Setting Retrieval Broken', 'Items deleted in the DB should still show up in responses from the cache', False, '', '')
    #else:
    #    res = d.miedb.dbQuery("SELECT value FROM system_settings WHERE module='System' AND section='Cron'")
    #    if res.numRows():
    #        d.reportCommandStatus('Something is broken', 'Cron settings were deleted from the db, but now they are back in the db', False, '', 'Found {0} records'.format(res.numRows()))
    #    else:
    #        d.reportCommandStatus('Caching OK', '', True, '', 'No DB Records found')
    #d.endSection()

    d.startSection('Verify that default values get populated correctly')
    d.miedb.dbExec("DELETE FROM system_settings WHERE module='System' AND section='Cron'")
    settings = getSettings(d, "Cron")
    if settings:
        checkSettings(d, settings, 'def_val')
    d.endSection()

    d.startSection('Verify an update without a reason does not revision the setting',
        comments='This most likely should be fixed in the future to not allow revision-less updates via the UI')
    res = d.miedb.dbQuery("SELECT * FROM system_settings WHERE section='Cron' AND item='Max Threads'")
    if res:
        if not res.numRows():
            d.reportCommandStatus('Query returned no rows', '', False, '', '')
            return
        d.navigate('?f=admin&s=system_settings&opp=edit&value=NOREASON&module=System&section=Cron&item=Max+Threads&sysset_submit=Change')
        ares = d.miedb.dbQuery("SELECT * FROM system_settings WHERE section='Cron' AND item='Max Threads'")
        if ares:
            if not ares.numRows():
                d.reportCommandStatus('Query returned no rows', '', False, '', '')
                return
            arow = ares.getRow(0)
            brow = res.getRow(0)
            if arow['value'] != 'NOREASON':
                d.reportCommandStatus('Setting value did not save', '', False, brow['value'], arow['value'])
            elif int(arow['revision_number']) != int(brow['revision_number']):
                d.reportCommandStatus('Revision number changed without a reason', '', False,
                    brow['revision_number'], arow['revision_number'])
            else:
                d.reportCommandStatus('Revision number is stable', arow['value'], True,
                    brow['revision_number'], arow['revision_number'])
    d.endSection()

    d.startSection('Verify an update with a reason revisions properly')
    res = d.miedb.dbQuery("SELECT * FROM system_settings WHERE module='System' AND section='Cron' AND item='Max Threads'")
    if res:
        if not res.numRows():
            d.reportCommandStatus('Query returned no rows', '', False, '', '')
            return
        d.navigate('?f=admin&s=system_settings&opp=edit&value=WITHREASON&module=System&section=Cron&item=Max+Threads&sysset_submit=Change&reason=BECAUSETESTING')
        ares = d.miedb.dbQuery("SELECT * FROM system_settings WHERE section='Cron' AND item='Max Threads'")
        if ares:
            if not ares.numRows():
                d.reportCommandStatus('Query returned no rows', '', False, '', '')
                return
            arow = ares.getRow(0)
            brow = res.getRow(0)
            if arow['value'] != 'WITHREASON':
                d.reportCommandStatus('Setting value did not save', '', False, brow['value'], arow['value'])
            elif int(arow['revision_number']) != int(brow['revision_number']) + 1:
                d.reportCommandStatus('Revision number is not old revision + 1', '', False,
                    brow['revision_number'], arow['revision_number'])
            else:
                d.reportCommandStatus('Revision incremented by 1', arow['value'], True,
                    brow['revision_number'], arow['revision_number'])
    d.endSection()

    d.startSection('Verify deletes')
    rres = d.miedb.dbQuery("SELECT * FROM system_setting_revisions WHERE module='System' AND section='Cron' AND item='Max Threads' ORDER BY revision_number DESC LIMIT 1")
    d.navigate('?f=admin&s=system_settings&opp=delete&reason=Delete&module=System&section=Cron&item=Max+Threads&sysset_submit=Delete')
    res = d.miedb.dbQuery("SELECT * FROM system_settings WHERE module='System' AND section='Cron' AND item='Max Threads'")
    if res and rres:
        if res.numRows():
            d.reportCommandStatus('Setting did not delete', '', False, '', '')
            return
        d.reportCommandStatus('Setting deleted', '', True, '', '')
    ares = d.miedb.dbQuery("SELECT * FROM system_setting_revisions WHERE module='System' AND section='Cron' AND item='Max Threads' ORDER BY revision_number DESC LIMIT 1")
    if ares:
        bnum = int(rres.getRow(0)['revision_number'])
        anum = int(ares.getRow(0)['revision_number'])
        if anum != bnum + 1:
            d.reportCommandStatus('Revision number did not increment by 1', '', False, bnum, anum)
        else:
            d.reportCommandStatus('Setting deleted and revision incremented', '', True, bnum, anum)
    d.endSection()

    d.startSection('Verify an addition inserts with the correct revision_number')
    rres = d.miedb.dbQuery("SELECT * FROM system_setting_revisions WHERE module='System' AND section='Cron' AND item='Max Threads' ORDER BY revision_number DESC LIMIT 1")
    if rres:
        # Get the setting to get the default value inserted
        getSettings(d, 'Max Threads')
        res = d.miedb.dbQuery("SELECT * FROM system_settings WHERE module='System' AND section='Cron' AND item='Max Threads'")
        if res:
            rnum = int(rres.getRow(0)['revision_number'])
            anum = int(res.getRow(0)['revision_number'])
            if anum != rnum + 1:
                d.reportCommandStatus('Default insert did not insert as revision + 1', '', False, rnum, anum)
            else:
                d.reportCommandStatus('Default insert used the correct revision number for a previously deleted setting', '', True, rnum, anum)
        else:
            d.reportCommandStatus('Query returned no results', '', False, '', '')
    d.endSection()

    d.setScreenShotOnError(True)

    u = d.getWCUnitTest('Ensure editing an untracked setting displays the edit page')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO system_settings (module, section, item, value) VALUES ('zTest', 'zTest', 'zTest', 'zValue')"),
        reason='Insert an untracked setting directly into the db')
    u.verifyElements([
        wcElement('id', 'value'),
        wcElement('name', 'reason')
    ], reason='Check for value/reason inputs')
    u.test(lambda d: d.navigate('?f=admin&s=system_settings&opp=edit&module=zTest&section=zTest&item=zTest'),
        reason='Go to the edit page and ensure it displays')

    u = d.getWCUnitTest('Ensure editing an untracked setting saves the value')
    u.setup(lambda d: d.navigate('?f=admin&s=system_settings&opp=edit&module=zTest&section=zTest&item=zTest'),
        reason='Go to the edit page')
    u.setup(lambda d: d.enterFormData('IT WORKED', id='value', clear=True), reason='Type in a new value')
    u.setup(lambda d: d.enterFormData('FOR TESTING', name='reason'), reason='Give a reason')
    u.verifyElements(wcElement('xpath', "//span[contains(., 'Successfully modified system setting with module')]"),
        reason='Look for the success message')
    u.verifyDB(wcDBRecord("FROM system_settings WHERE module='zTest'", {
        'module': 'zTest',
        'section': 'zTest',
        'item': 'zTest',
        'value': 'IT WORKED'
    }), reason='Ensure the db shows the new saved value')
    u.test(lambda d: d.clickElement(value='Change'), reason='Click the Change button')

