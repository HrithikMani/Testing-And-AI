from wcunittest import wcElement, wcJSCode

def growlWait(d, data):
    d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="growl-title"]'), expected_return=True, timeout=30)

def main(d, WCURL):
    u = d.getWCUnitTest('Verify default notification behavior', coreCheck=False)
    u.setup(growlWait)
    u.verifyElements([
        wcElement('xpath', "//div[@class='growl-title']", text='UnitTest Title'),
        wcElement('xpath', "//div[@class='growl-message']", text='UnitTest Message')
    ], reason='Ensure the notification appears')
    u.verifyElements([
        wcElement('xpath', "//div[@class='growl-title']", exists=False),
        wcElement('xpath', "//div[@class='growl-message']", exists=False)
    ], reason='Ensure the notification automatically removes within 6 seconds', timeout=6)
    u.test(lambda d: d.runJS("wcnotify.info('UnitTest Title', 'UnitTest Message')"),
        reason='Show the notification')

    u = d.getWCUnitTest('Ensure notifications respect the static/fixed option', coreCheck=False)
    u.setup(lambda d: d.pause(6), reason='Wait for 6 seconds')
    u.verifyElements([
        wcElement('xpath', "//div[@class='growl-title']", text='UnitTest Title'),
        wcElement('xpath', "//div[@class='growl-message']", text='UnitTest Message')
    ], reason='Ensure the notifications are still present')
    u.teardown(lambda d: d.runJS("wcnotify.closeAll()"), reason='Close any notifications')
    u.test(lambda d: d.runJS("wcnotify.info('UnitTest Title', 'UnitTest Message', {static: true, fixed: true})"),
        reason='Show a static notification')

    u = d.getWCUnitTest('Ensure the wcnotify API can close all notifications', coreCheck=False)
    u.setup(lambda d: d.runJS("wcnotify.info('UnitTest Title', 'UnitTest Message', {static: true, fixed: true})"),
        reason='Show a static notification')
    u.verifyElements([
        wcElement('xpath', "//div[@class='growl-title']", exists=False),
        wcElement('xpath', "//div[@class='growl-message']", exists=False)
    ], reason='Ensure the notifications are not present')
    u.test(lambda d: d.runJS("wcnotify.closeAll()"), reason='Clear all notifications')

    u = d.getWCUnitTest('Ensure the wcnotify API can query the notifications', coreCheck=False)
    u.setup(lambda d: d.runJS("wcnotify.info('UnitTest Title', 'UnitTest Message', {static: true, fixed: true})"),
        reason='Show a static notification')
    u.setup(lambda d: d.runJS("wcnotify.info('UnitTest Title', 'UnitTest Message', {static: true, fixed: true})"),
        reason='Show a static notification')
    u.setup(lambda d: d.runJS("wcnotify.info('UnitTest Title', 'UnitTest Message', {static: true, fixed: true})"),
        reason='Show a static notification')
    u.verifyElements([
        wcElement('xpath', "(//div[@class='growl-title'])[1]"),
        wcElement('xpath', "(//div[@class='growl-message'])[1]"),
        wcElement('xpath', "(//div[@class='growl-title'])[2]"),
        wcElement('xpath', "(//div[@class='growl-message'])[2]"),
        wcElement('xpath', "(//div[@class='growl-title'])[3]"),
        wcElement('xpath', "(//div[@class='growl-message'])[3]")
    ], reason='Ensure multiple notifications are present')
    u.verifyJS([
        wcJSCode("wcnotify.getAll().length", 3)
    ], reason='Expect 3 notification objects')
    u.teardown(lambda d: d.runJS("wcnotify.closeAll()"), reason='Clear all notifications')
    u.test()

    u = d.getWCUnitTest('Verify invocation of a notification without a message', coreCheck=False)
    u.verifyElements([
        wcElement('xpath', "//div[@class='growl-title']", text=''),
        wcElement('xpath', "//div[@class='growl-message']", text='UnitTest Title')
    ], reason='Ensure the notification appears')
    u.teardown(lambda d: d.runJS("wcnotify.closeAll()"), reason='Close any notifications')
    u.test(lambda d: d.runJS("wcnotify.info('UnitTest Title')"), reason='Show the notification')

    u = d.getWCUnitTest('Verify invocation of a notification with an undefined message works the same',
        coreCheck=False)
    u.verifyElements([
        wcElement('xpath', "//div[@class='growl-title']", text=''),
        wcElement('xpath', "//div[@class='growl-message']", text='UnitTest Title')
    ], reason='Ensure the notification appears')
    u.teardown(lambda d: d.runJS("wcnotify.closeAll()"), reason='Close any notifications')
    u.test(lambda d: d.runJS("wcnotify.info('UnitTest Title', undefined, {})"), reason='Show the notification')

    sizes = ['small', 'medium', 'large']
    attrs = [
        {
            'method': 'info',
            'class': 'notice'
        },
        {
            'method': 'message',
            'class': 'default'
        },
        {
            'method': 'warning',
            'class': 'warning'
        },
        {
            'method': 'error',
            'class': 'error'
        }
    ]
    for a in attrs:
        for size in sizes:
            u = d.getWCUnitTest('Ensure expected html structure for [ {0} {1} ] notifications'.format(size, a['method']),
                coreCheck=False)
            u.verifyElements([
                wcElement('xpath',
                    '//div[contains(@class, "growl") and contains(@class, "growl-{class}") and contains(@class, "growl-{size}")]'.format(**{
                    'class': a['class'],
                    'size': size
                })),
                wcElement('xpath', '//div[@class="growl-title"]', text='UnitTest Title'),
                wcElement('xpath', '//div[@class="growl-message"]', text='UnitTest Message')
            ], reason='Expect html structure to be present on the page')
            u.teardown(lambda d: d.runJS('wcnotify.closeAll()'), reason='Close all notifications')
            u.test(lambda d: d.runJS("wcnotify.{0}('UnitTest Title', 'UnitTest Message', {{size: '{1}'}})".format(a['method'], size)))
