"""
    @owner: sgrider
    @filedeps: src/ec_patemail.c
"""
from wcunittest import wcElement, wcDBRecord

EMAIL_NAME = 'Pat UnitTest Email'

def preview(d):
    d.clickElement(text='Preview')
    d.wcutils.waitForEle(xpath='//div[@class="wc_win_title"]', timeout=60)

def createLayout(d, data):
    if not d.miedb.dbExec("INSERT INTO layout (name, module, layout_html, active) VALUES "\
        "('{0}', '{1}', '{2}', 1)".format(data.get('name'), data.get('module'),
        data.get('html'))):
        d.reportCommandStatus('DB Statement Failed', d.miedb.dbError(), False, '', '')

def enterComment(d, val):
    d.enterFormData(val, name='add_comment')

def enterSubject(d, val):
    d.enterFormData(val, name='subject')

def cleanup(d):
    d.miedb.dbExec("DELETE FROM layout WHERE module='email' AND name='{0}'".format(EMAIL_NAME))

def goToEmailPage(d):
    d.navigate('?f=chart&s=pat&pat_id=18&opp=email')

def selectLayout(d, layout):
    d.enterFormData(layout, name='layout_name')

def main(d, WCURL):
    wcunit = d.getWCUnitTest('Email Patient Screen')
    wcunit.setup(goToEmailPage)
    wcunit.verifyElements([
        wcElement('name', 'layout_name'),
        wcElement('name', 'subject', size=30),
        wcElement('name', 'dont_email_patient', type='checkbox', value='1'),
        wcElement('name', 'toemail_ac_txt'),
        wcElement('name', 'ccemail_ac_txt'),
        wcElement('name', 'add_comment', rows=4, cols=60),
        wcElement('value', 'Send'),
        wcElement('value', 'Cancel')
    ], reason='Validate standard form inputs')
    wcunit.test()
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Preview Comments Only')
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, 'Comments Only')
    wcunit.setup(enterComment, '*This is a test comment*')
    wcunit.verifyElements([
        wcElement('xpath', "//body[contains(., 'Subject: Patient Email')]")
    ], reason='Expect Default Subject Field')
    wcunit.teardown(cleanup)
    wcunit.test(preview)
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Preview Comments Only w/Subject')
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, 'Comments Only')
    wcunit.setup(enterComment, '*This is a test comment*')
    wcunit.setup(enterSubject, 'This is the email subject')
    wcunit.verifyElements([
        wcElement('xpath', "//div[@class='wc_win' and contains(., '*This is a test comment*')]"),
        wcElement('xpath', "//div[@class='wc_win' and contains(., 'Subject: This is the email subject')]")
    ], reason='Expect Given Fields')
    wcunit.teardown(cleanup)
    wcunit.test(preview)
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Preview An Email From a Layout')
    wcunit.setup(createLayout, {
        'name': EMAIL_NAME,
        'module': 'Email',
        'html': 'This is an email being rendered from a layout'
    }, reason='Insert a layout to be used')
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, EMAIL_NAME)
    wcunit.verifyElements([
        wcElement('xpath', "//div[@class='wc_win' and contains(., 'This is an email being rendered from a layout')]"),
        wcElement('xpath', "//div[@class='wc_win' and contains(., 'Subject: Patient Email')]")
    ], reason='Expect Given Fields')
    wcunit.teardown(cleanup)
    wcunit.test(preview)
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Send an email')
    wcunit.setup(goToEmailPage)
    wcunit.setup(enterComment, 'This is a comment from a selenium unittest')
    wcunit.verifyElements([
        wcElement('xpath', "//h3[text()='Successfully sent email']"),
    ], reason='Check for success message')
    wcunit.verifyDB([
        wcDBRecord("FROM documents d INNER JOIN documents_txt dt USING(doc_id) "\
            "WHERE d.doc_type='EMAIL' AND d.pat_id=18 ORDER BY d.doc_id DESC LIMIT 1", {
                'dt.txt_value': lambda x: 'This is a comment from a selenium unittest' in x,
                'dt.subject': 'Patient Email'
            }),
    ], reason='Ensure a document was created for this email')
    wcunit.test(lambda d: d.clickElement(value='Send'), reason='Click the Send button')
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Preview an email using the WCSYSFILE tag')
    wcunit.setup(createLayout, {
        'name': EMAIL_NAME,
        'module': 'Email',
        'html': """This is the letterhead: <WCSYSFILE FILEALIAS="System Letterhead" INLINE_DATA="0" ALT="sysletterhead_alt">"""
    })
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, EMAIL_NAME)
    wcunit.verifyElements([
        wcElement('xpath', "//div[@class='wc_win' and contains(., 'This is the letterhead:')]"),
        wcElement('xpath', "//img[contains(@src, 'sysfile=System%20Letterhead')]", title='sysletterhead_alt', alt='sysletterhead_alt'),
    ], reason='Ensure preview data shows correctly')
    wcunit.teardown(cleanup)
    wcunit.test(preview)
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Send an email using the WCSYSFILE tag')
    wcunit.setup(createLayout, {
        'name': EMAIL_NAME,
        'module': 'Email',
        'html': """This is the letterhead: <WCSYSFILE FILEALIAS="System Letterhead" INLINE_DATA="0" ALT="sysletterhead_alt">"""
    })
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, EMAIL_NAME)
    wcunit.verifyElements([
        wcElement('xpath', "//h3[text()='Successfully sent email']"),
    ], reason='Check for success message')
    wcunit.verifyDB([
        wcDBRecord("FROM documents d INNER JOIN documents_txt dt USING(doc_id) "\
            "WHERE d.doc_type='EMAIL' AND d.pat_id=18 ORDER BY d.doc_id DESC LIMIT 1", {
                'dt.txt_value': lambda x: 'sysfile=System%20Letterhead' in x,
                'dt.subject': 'Patient Email'
            }),
    ], reason='Ensure a document with an img tag was created for this email')
    wcunit.teardown(cleanup)
    wcunit.test(lambda d: d.clickElement(value='Send'), reason='Click the Send button')
    d.wcErrorLog.ignore('Error caused by sending blank email*')
    
    wcunit = d.getWCUnitTest('Preview an email using the WCSYSFILE tag and inline data')
    wcunit.setup(createLayout, {
        'name': EMAIL_NAME,
        'module': 'Email',
        'html': """This is the letterhead: <WCSYSFILE FILEALIAS="System Letterhead" INLINE_DATA="1" ALT="sysletterhead_alt">"""
    })
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, EMAIL_NAME)
    wcunit.verifyElements([
        wcElement('xpath', "//div[@class='wc_win' and contains(., 'This is the letterhead:')]"),
        wcElement('xpath', "//img[contains(@src, 'data:image')]", title='sysletterhead_alt', alt='sysletterhead_alt'),
    ], reason='Ensure preview data shows correctly')
    wcunit.teardown(cleanup)
    wcunit.test(preview)
    d.wcErrorLog.ignore('Error caused by sending blank email*')

    wcunit = d.getWCUnitTest('Send an email using the WCSYSFILE tag and inline data')
    wcunit.setup(createLayout, {
        'name': EMAIL_NAME,
        'module': 'Email',
        'html': """This is the letterhead: <WCSYSFILE FILEALIAS="System Letterhead" INLINE_DATA="1" ALT="sysletterhead_alt">"""
    })
    wcunit.setup(goToEmailPage)
    wcunit.setup(selectLayout, EMAIL_NAME)
    wcunit.verifyElements([
        wcElement('xpath', "//h3[text()='Successfully sent email']"),
    ], reason='Check for success message')
    wcunit.verifyDB([
        wcDBRecord("FROM documents d INNER JOIN documents_txt dt USING(doc_id) "\
            "WHERE d.doc_type='EMAIL' AND d.pat_id=18 ORDER BY d.doc_id DESC LIMIT 1", {
                'dt.txt_value': lambda x: 'src="data:image' in x,
                'dt.subject': 'Patient Email'
            }),
    ], reason='Ensure a document with an img tag with inline data was created for this email')
    wcunit.teardown(cleanup)
    wcunit.test(lambda d: d.clickElement(value='Send'), reason='Click the Send button')
    d.wcErrorLog.ignore('Error caused by sending blank email*')

