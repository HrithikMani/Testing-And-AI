"""
    Unit test for miepub pub/sub API
    @owners: sgrider
    @filedeps: jsbin/miepub.js, src/miepub.c, include/miepub.h
"""

from wcunittest import wcJSCode

"""
This is now setup as part of the deploy process
def setupAPI(d):
    d.miedb.dbExec("REPLACE INTO refer_to_systems (system_id, system_name, system_address, system_pass) "\
        "VALUES ('MIEPUB_API', 'MIEPUB Server API', "\
        "(SELECT SUBSTRING_INDEX(value, '/', 3) FROM system_settings "\
            "WHERE module='System' AND section='WebChart' AND item='MIEPub Server'), "\
        "'remote03')")
"""

def deleteAPI(d):
    d.miedb.dbExec("REPLACE INTO refer_to_systems (system_id, system_name, system_address, system_pass) VALUES ('MIEPUB_API', 'MIEPUB Server API',  '', '')")

def publishAPI(d):
    d.pause(5)
    res = d.miedb.dbQuery("SELECT system_address, system_pass FROM refer_to_systems WHERE system_id='MIEPUB_API'")
    if not res or not res.getRow(0):
        d.reportCommandStatus('Failed to find MIEPub API Url', '', False, '', res.dbError())
    else:
        wccurl = d.getWCCurl('{0}/put'.format(res.getRow(0)['system_address']))
        wccurl.setIgnoreSSLErrors(True)
        ret = wccurl.get('?apikey={0}&channel={1}/seleniumTest&message=I%20came%20from%20the%20API'.format(
            res.getRow(0)['system_pass'], d.getUserData('handle')))
        d.reportCommandStatus('Publish API', ret, None, '', '')

def subscribe(d):
    d.pause(5)
    d.runJS("miepub.subscribe('seleniumTest', {"\
        "onMessage:function(msg) { wcnotify.message('MIEPUB Test', msg, {fixed: true}) },"\
        "echo: true})")

def unsubscribe(d):
    d.pause(5)
    d.runJS("miepub.unsubscribe('seleniumTest')")

def publish(d, msg):
    d.pause(5)
    d.runJS("miepub.publish('seleniumTest', '{0}')".format(msg))

def closeAll(d):
    d.pause(5)
    unsubscribe(d)
    d.runJS("wcnotify.closeAll()")

def main(d, wcurl):
    u = d.getWCUnitTest('Verify no message when not subscribed', coreCheck=False)
    u.setup(publish, 'Message for me', reason='Publish a message')
    u.verifyJS([
        wcJSCode("wcnotify.getMessages().length", 0),
    ])
    u.teardown(closeAll)
    u.test()

    u = d.getWCUnitTest('Verify 1 message is delivered when subscribed', coreCheck=False)
    u.setup(subscribe)
    u.setup(publish, 'Message for me', reason='Publish a message')
    u.verifyJS([
        wcJSCode("wcnotify.getMessages().length", 1),
        wcJSCode("wcnotify.getMessages()[0].title", 'MIEPUB Test'),
        wcJSCode("wcnotify.getMessages()[0].message", 'Message for me')
    ])
    u.teardown(closeAll)
    u.test()

    u = d.getWCUnitTest('Verify multiple messages are delivered when subscribed', coreCheck=False)
    u.setup(subscribe)
    u.setup(publish, 'Message for me1', reason='Publish a message1')
    u.setup(publish, 'Message for me2', reason='Publish a message2')
    u.setup(publish, 'Message for me3', reason='Publish a message3')
    u.verifyJS([
        wcJSCode("wcnotify.getMessages().length", 3),
        wcJSCode("wcnotify.getMessages()[0].title", 'MIEPUB Test'),
        wcJSCode("wcnotify.getMessages()[0].message", 'Message for me1'),
        wcJSCode("wcnotify.getMessages()[1].title", 'MIEPUB Test'),
        wcJSCode("wcnotify.getMessages()[1].message", 'Message for me2'),
        wcJSCode("wcnotify.getMessages()[2].title", 'MIEPUB Test'),
        wcJSCode("wcnotify.getMessages()[2].message", 'Message for me3'),
    ])
    u.teardown(closeAll)
    u.test()

    u = d.getWCUnitTest('Verify subscription.cancel will prevent subsequent local callbacks')
    u.setup(lambda d: d.runJS('''miepub.subscribe('seleniumTest', function() { window.sub2.cancel() })'''),
        reason='Subscribe to the channel and cancel the second subscription onMessage')
    u.setup(lambda d: d.runJS('''window.sub2 = miepub.subscribe('seleniumTest', function() { wcnotify.message('MIEPUB Test', 'Hello', {fixed: true})})'''),
        reason='Add a second subscription to the same channel that shows a notification')
    u.setup(lambda d: d.runJS('''miepub.publish('seleniumTest', 'Hello')'''),
        reason='Publish a message on the channel')
    u.verifyJS([
        wcJSCode('wcnotify.getMessages().length', 0),
    ], reason='Since the first subscription handler cancels the second, we should not get any notifications')
    u.test()

    u = d.getWCUnitTest('Verify miepub JS API')
    u.setup(subscribe)
    u.verifyJS([
        wcJSCode("miepub.getUsers('seleniumTest').length", 1),
        wcJSCode("miepub.getUsers('seleniumTest')[0].username", 'selenium'),
        wcJSCode("miepub.getUserNames('seleniumTest').length", 1),
        wcJSCode("miepub.getUserNames('seleniumTest')", ['selenium']), 
    ])
    u.teardown(closeAll)
    u.test()

    u = d.getWCUnitTest('Verify the backend API is working correctly', coreCheck=False)
#    u.setup(setupAPI, reason='Setup the RTS entry for the API')
    u.setup(subscribe, reason='Subscribe to the channel')
    u.verifyJS([
        wcJSCode('wcnotify.getMessages().length', 1),
        wcJSCode('wcnotify.getMessages()[0].title', 'MIEPUB Test'),
        wcJSCode('wcnotify.getMessages()[0].message', 'I came from the API')
    ], reason='Verify we got the message from the API')
    u.teardown(deleteAPI, reason='Don\'t leave the API active')
    u.teardown(closeAll)
    u.test(publishAPI, reason='Publish a message to the API (not via JS)')

