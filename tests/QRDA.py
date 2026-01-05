import os
import time
import shutil

MEASURES = ['CMS138v6', 'CMS165v6', 'CMS68v6', 'CMS69v6', 'CMS156v6', 'CMS50v7',
    'CMS164v6', 'CMS139v6', 'CMS147v7', 'CMS130v6', 'CMS125v6', 'CMS122v6', 'CMS159v6',
    'CMS52v6', 'CMS127v6', 'CMS22v6', 'CMS145v6', 'CMS144v6', 'CMS135v6', 'CMS2v7',
    'CMS131v6', 'CMS90v7', 'CMS154v6', 'CMS146v6', 'CMS124v6', 'CMS136v7', 'CMS117v6',
    'CMS153v6', 'CMS75v6', 'CMS155v6', 'CMS134v6', 'CMS149v6', 'CMS157v6', 'CMS160v6',
    'CMS166v7', 'CMS65v7', 'CMS74v7', 'CMS82v5', 'CMS123v6', 'CMS137v6', 'CMS347v1',
    'CMS56v6', 'CMS66v6', 'CMS128v6', 'CMS129v7', 'CMS132v6', 'CMS133v6', 'CMS142v6',
    'CMS143v6', 'CMS161v6', 'CMS177v6', 'CMS349v1', 'CMS645v1', ]

RXDB = 'rxdb_utf8'
MEASURE_YEAR = 2018
CYPRESS_ROOT = '/usr/local/webchart/Cypress'
CYPRESS_DATA_PATH = os.path.join(CYPRESS_ROOT, 'Cypress_Test_Deck')
UPLOAD_SCRIPT = os.path.join(CYPRESS_ROOT, 'uploadCDAs.py')

DOWNLOADS_DIR = os.path.expanduser(os.path.join('~', 'Downloads'))
SELENIUM_USER_ID = 8

CYPRESS_LOGIN_URL = 'https://ec2-34-205-10-37.compute-1.amazonaws.com/users/sign_in'
CYPRESS_WC_URL = 'https://ec2-34-205-10-37.compute-1.amazonaws.com/vendors/5a313e313e0df603e51f871a/products/5ade2c493e0df629b9cf116a'
CYPRESS_QRDA1_URL = 'https://ec2-34-205-10-37.compute-1.amazonaws.com/vendors/5a313e313e0df603e51f871a/products/5ade2c493e0df629b9cf116a#c1___c3__qrda_i_'
CYPRESS_QRDA3_URL = 'https://ec2-34-205-10-37.compute-1.amazonaws.com/vendors/5a313e313e0df603e51f871a/products/5ade2c493e0df629b9cf116a#c2___c3__qrda_iii_'
CYPRESS_USERNAME = 'selenium@mieweb.com'
CYPRESS_PASSWORD = '@suppx123'
CYPRESS_TIMEOUT = 300   # Seconds to wait for tests to process
WEBCHART_TIMEOUT = 60   # Seconds to wait for webchart to download xml files
CYPRESS_C1_COLUMN = 3
CYPRESS_C2_COLUMN = 3
CYPRESS_C3_COLUMN = 4

def runUploadScript(d, measure):
    ws = d.getWebServer()
    # Find the data path for this measure
    ret = ws.system('ls {0}'.format(CYPRESS_DATA_PATH))
    paths = sorted(ret.stdout(True))
    data_path = None
    for p in paths:
        if p.strip().startswith(measure):
            data_path = os.path.join(CYPRESS_DATA_PATH, p.strip())
            d.reportCommandStatus('Using data source', data_path, True, '', '')
            break
    if data_path:
        ret = ws.system('{0} -m 100 -u {username} -p {password} '\
            '-U "https://zeus-web.med-web.com/webchart/{handle}/webchart.cgi" '\
            '-D {data_path} -P {partition}'.format(UPLOAD_SCRIPT, **{
                'username': d.getUserData('selenium_username'),
                'password': d.getUserData('selenium_password'),
                'handle':   d.getUserData('handle'),
                'data_path': data_path,
                'partition': measure.split('v')[0]
            }))
        if not ret.returnCode():
            return True
        else:
            d.reportCommandStatus('Upload Script Failed', '', False, ret.stdout(), ret.stderr())
    else:
        d.reportCommandStatus('Failed to find upload data for measure', measure, False, '', paths)

def getDownloadedFilename(d, ext):
    duration = WEBCHART_TIMEOUT
    count = 0
    while count < duration:
        if os.path.exists(DOWNLOADS_DIR):
            files = os.listdir(DOWNLOADS_DIR)
            if files:
                return [x for x in files if x.endswith(ext)][0]
        count = count + 5
        time.sleep(5)

def downloadXMLFile(d, measure, url, extension):
    d.setBaseURL('https://zeus-web.med-web.com/webchart/{0}/webchart.cgi'.format(
        d.getUserData('handle')))
    d.navigate(url + '&RunMe=Run+Report&year={year}&performing_user_id={user_id}&'\
        'wc_partition={partition}&begin_dateDAY=01&begin_dateMONTH=01&'\
        'begin_dateYEAR={year}&end_dateDAY=31&end_dateMONTH=12&'\
        'end_dateYEAR={year}'.format(**{
        'user_id': SELENIUM_USER_ID,
        'year': MEASURE_YEAR,
        'partition': measure.split('v')[0]
        }))
    if not d.getElement(id='download_all_{0}'.format(measure)):
        d.reportCommandStatus('Download button not present', '', False, '', '')
        return None
    d.clickElement(id='download_all_{0}'.format(measure))
    return getDownloadedFilename(d, extension)

def validateFile(d, measure, filename, version):
    d.setBaseURL('')
    if version == 1:
        d.navigate(CYPRESS_QRDA1_URL)
    else:
        d.clickElement(text='C2 + C3 (QRDA-III)')
    # Upload the file for this measure
    row = d.getElement(xpath="(//td[text()='{0}']/parent::tr)[{1}]".format(
        measure, '1' if version == 1 else '2'))
    if not row:
        d.reportCommandStatus('Failed to find measure row', '', False, '', '')
        return
    d.scrollTo(0, row.location['y'])
    d.startSection('Upload File')
    ele = d.getElement(xpath=".//input[contains(@id, 'multi-upload-field')]", ele=row)
    d.reportCommandStatus('Uploading File', os.path.join(DOWNLOADS_DIR, filename), None, '', '')
    ele.send_keys(os.path.join(DOWNLOADS_DIR, filename))
    d.endSection()
    d.startSection('Wait for processing to begin')
    if not d.waitFor(d, lambda d: d.getElement(xpath=".//span[text()='testing...']", ele=row), timeout=30):
        d.reportCommandStatus('Test Processing Never Started', '', False, '', '')
        d.endSection()
        return
    d.endSection()
    d.startSection('Wait For Results')
    if not d.waitFor(d, lambda d: d.getElement(xpath=".//span[text()='testing...']", ele=row), timeout=CYPRESS_TIMEOUT, expected_return=False):
        d.reportCommandStatus('Processing Did Not Complete', '', False, '', '')
        d.endSection()
        return
    # Add a retry loop for stale elements
    tries = 0
    while tries < 2:
        try:
            c1 = d.getElement(xpath=".//td[{0}]//strong".format(CYPRESS_C1_COLUMN if version == 1 else CYPRESS_C2_COLUMN), ele=row)
            c3 = d.getElement(xpath=".//td[{0}]//strong".format(CYPRESS_C3_COLUMN), ele=row)
            d.reportCommandStatus('C1 Results' if version == 1 else 'C2 Results', c1.text, c1.text.lower() == 'passed', '', '')
            d.reportCommandStatus('C3 Results', c3.text, c3.text.lower() == 'passed', '', '')
            break
        except Exception as e:
            d.reportCommandStatus('Exception caught, trying again?', e, None, '', '')
        tries += 1
    d.screenshot()
    d.endSection()

def loginToCypress(d):
    d.startSection('Login To Cypress')
    d.setBaseURL('')
    d.navigate(CYPRESS_LOGIN_URL)
    d.enterFormData(CYPRESS_USERNAME, id='user_email')
    d.enterFormData(CYPRESS_PASSWORD, id='user_password')
    d.clickElement(value='Sign in')
    d.endSection()

def main(d, WCURL):
    loginToCypress(d)
    started = False

    # Turn off demo date so we get the real years in the dropdowns
    d.setBaseURL('https://zeus-web.med-web.com/webchart/{0}/webchart.cgi'.format(
        d.getUserData('handle')))
    d.miedb.dbExec("DELETE FROM system_settings WHERE module='WebChart' AND "\
        "section='Demo' AND item='Demo Date'")
    d.miedb.dbExec("UPDATE users SET pwd_expire=DATE_ADD(CURDATE(), INTERVAL 1 YEAR) "\
        "WHERE user_id={0}".format(SELENIUM_USER_ID))
    d.wcutils.flushMemcache()

#    for measure in MEASURES[0:2]:
    for measure in MEASURES:
        try:
            if os.path.exists(DOWNLOADS_DIR):
                shutil.rmtree(DOWNLOADS_DIR)
            if started:
                d.endSection()
            started = True
            d.startSection('Measure {0}'.format(measure))
            d.setBaseURL('https://zeus-web.med-web.com/webchart/{0}/webchart.cgi'.format(
                d.getUserData('handle')))
            # Enroll in this measure
            res = d.miedb.dbQuery("SELECT report_name FROM {0}.Measures WHERE program='quality' "
                "AND measure_year=%s AND eMeasureId=%s".format(RXDB), MEASURE_YEAR, measure)
            if not res.numRows():
                d.reportCommandStatus('Query RXDB returned no rows', measure, False, '', '')
                continue
            d.miedb.dbExec("TRUNCATE measure_enrollment")
            d.miedb.dbExec("TRUNCATE measure_calc")
            for report in res.getRows(): 
                d.miedb.dbExec("INSERT INTO measure_enrollment "
                    "(report_name, provider_id, start_date, end_date, status) VALUES "
                    "('{1}', '{2}', '{0}-01-01', LAST_DAY('{0}-12-01'), 1)".format(
                    MEASURE_YEAR, report['report_name'], SELENIUM_USER_ID))
            res = d.miedb.dbQuery("SELECT enrollment_id FROM measure_enrollment ORDER BY enrollment_id ASC")
            if not res:
                d.reportCommandStatus('Failed to query the measures we just inserted', '', False, '', '')
                continue

            # Upload the sample data
            d.startSection('Upload Sample Data')
            if not runUploadScript(d, measure):
                d.endSection()
                continue
            d.endSection()

            # Recalculate measures
            d.startSection('Recalculate Measures')
            for row in res.getRows():
                d.navigate('?f=ajaxpost&s=quality_eval&enrollment_id={0}'.format(row['enrollment_id']))
            d.endSection()

            d.startSection('Download QRDAI File')
            zipfile = downloadXMLFile(d, measure,
                '?f=layout&s=pat&module=SystemReport&name=QRDA+I+Report', '.zip')
            if not zipfile:
                d.reportCommandStatus('Failed to download QRDAI measure xml file', measure, False, '', '')
                d.endSection()
                continue
            else:
                d.reportCommandStatus('Downloaded Zip File', zipfile, True, '', '')
            d.endSection()

            d.startSection('Download QRDAIII File')
            d.navigate('?f=layout&module=StructDocTypes&name=QRDA-III&XML&filename=qrda_iii.xml&'\
                'content_type=text/plain&my_user_id={user_id}&partition={partition}&measure_id={measure_id}&'\
                'begin_dateDAY=01&begin_dateMONTH=01&'\
                'begin_dateYEAR={year}&end_dateDAY=31&end_dateMONTH=12&'\
                'end_dateYEAR={year}&year={year}'.format(**{
                    'user_id': SELENIUM_USER_ID,
                    'partition': measure.split('v')[0],
                    'measure_id': measure,
                    'year': MEASURE_YEAR,
                }))
            xmlfile = getDownloadedFilename(d, '.xml')
            if not xmlfile:
                d.reportCommandStatus('Failed to download QRDAIII measure xml file', measure, False, '', '')
                d.endSection()
                continue
            else:
                d.reportCommandStatus('Downloaded XML File', xmlfile, True, '', '')
            d.endSection()

            d.startSection('Validate QRDAI')
            validateFile(d, measure, zipfile, 1)
            d.endSection()

            d.startSection('Validate QRDAIII')
            validateFile(d, measure, xmlfile, 3)
            d.endSection()
        except Exception as e:
            d.reportCommandStatus('Exception thrown during measure test', measure, False, e, str(e))

