"""
            DO NOT USE THE SCREENSHOT METHOD OF MIEDRIVER, USE THE PROVIDED SCREENSHOT() METHOD HERE
    @owners: dcarlson
"""

cobrands = {
    'NMC':          {'id': 0, 'name': 'NoMoreClipboard'},
    'OAKCREEKDEMO': {'id': 68425, 'name': 'NoMoreClipboard - Oak Creek Standard Demo'},
    'OCCARDIO':     {'id': 51027, 'name': 'NoMoreClipboard - Oak Creek Cardiology'},
    }

DEFAULT_COBRAND = 'NMC'

def screenshot(d):
    d.screenshot('cobrand_%s' %DEFAULT_COBRAND)

def main(d, WCURL):
    d.setUserData('systemType', 'NMC')
    cobrand = cobrands.get(DEFAULT_COBRAND, cobrands['NMC'])
    user = buildUserData(None,cobrand['id'])

    d.navigate(WCURL.LOGOUT, report=False)
    d.navigate('?f=nmc&svar_cobrand_patid=%d' %cobrand['id'])
    
    if runSection(d, createAccount, user, 'Account Creation'):
        runSection(d, regAccount, user, 'Account Registration')
        if cobrand['id']:
            runSection(d, preRegisterAppt, user, 'Pre Register for an Upcoming Appointment')

        runSection(d, memberReview, user, 'Member Review Progress')

        if cobrand['id']:
            runSection(d, AskANurse, user, 'Ask A Nurse')
            runSection(d, requestAppt, user, 'Request An Appointment')
            runSection(d, requestMedRefill, user, 'Request a Medication Refill')
            runSection(d, billing, user, 'Billing Department')
            runSection(d, viewMessages, user, 'View Messages')
            runSection(d, proceedPHR, user, 'Proceed to Your Personal Health Record')

        runSection(d, memberAccessCenter, user, 'Member Access Center [Edit]')
        runSection(d, registerInformation, user, 'Registration Information [Edit]')
        runSection(d, ccme, user, 'cc:Me')
        runSection(d, insurance, user, 'Insurance [Edit]')
        runSection(d, medicalProviders, user, 'Medical Providers [Edit]')
        runSection(d, documents, user, 'Documents')

        if cobrand['id'] == 68425:
            runSection(d, oakCreekStandardDemo, user, 'Send Updated Medical History')
        elif cobrand['id'] == 51027:
            runSection(d, oakCreekCardiology, user, 'Send Updated Medical History')

        runSection(d, currentMeds, user, 'Current Medications [Edit]')
        runSection(d, currentIllness, user, 'Current Illnesses [Edit] [Conditions Review]')
        runSection(d, pastIllness, user, 'Past Illnesses [Edit]')
        runSection(d, surgeries, user, 'Surgeries/Procedures [Edit]')
        runSection(d, immunizations, user, 'Immunizations [Edit]')
        runSection(d, allergies, user, 'Allergies [Edit]')
        runSection(d, familyHistory, user, 'Family Medical History [Edit]')
        runSection(d, socialHistory, user, 'Social History [Edit]')
        runSection(d, dataTracking, user, 'Data Tracking [Edit]')
        runSection(d, hipaa, user, 'HIPAA Access Information [Edit]')
        runSection(d, download, user, 'Download NoMoreClipboard Health Information')
        runSection(d, addMembers, user, 'Add Additional Member - New')
        runSection(d, ccMeNew, user, 'ccMe - View Entry')
        runSection(d, testDocumentSecureSend, user, 'Test document secure send')
        runSection(d, accountSummary, user, 'Account Summary Page')
        runSection(d, testNoPats, user, 'Test no pat_id pages')
        runSection(d, testflayout, user, 'Test f=layout')

def accountSummary(d, user):
    d.clickElement(text='Account Summary')
    #screenshot(d)
    d.clickElement(text='Tell A Friend')
    d.enterFormData('Bob Smith',id='sendername', clear=True)
    d.enterFormData('no-reply@nomoreclipboard.com',id='senderemail', clear=True)
    d.enterFormData('Barb Smith',id='name1', clear=True)
    d.enterFormData('no-reply@nomoreclipboard.com',id='email1', clear=True)
    #screenshot(d)
    d.clickElement(text='Submit')
    d.clickElement(text='Account Summary')
    d.clickElement(text='Subscription Center')
    screenshot(d)
    d.clickElement(text='Account Summary')
    d.clickElement(text='Update Account')
    screenshot(d)
    d.clickElement(text=u'NEXT \u25ba')
    screenshot(d)

def createAccount(d, user):
    d.enterFormData(user['username'], id='reg_user')
    d.enterFormData(user['password'], id='reg_passwd')
    d.enterFormData(user['password'], id='password')
    d.enterFormData(user['email'], id='email')
    if user['cobrand']:
        d.enterFormData('From another website', id='heardabout')
    d.clickElement(id='termschecked')
    screenshot(d)

    d.clickElement(value='Create Account')
    d.verifyElementPresent(xpath="//div[@id='header_table']//span[normalize-space(text())='Logged in as:']")
    
def regAccount(d, user):
    screenshot(d)
    # Click NO for Member Activation?
    d.clickElement(text='NO')

    #d.enterFormData(user['activation_code'],id='NMC_pickup_code')
    d.enterFormData(user['first'],id='DUI_first_name')
    #d.enterFormData(user['middle'],id='DUI_middle_name')
    d.enterFormData(user['last'],id='DUI_last_name')
    #d.enterFormData(user['address1'],id='DUI_address1')
    #d.enterFormData(user['address2'],id='DUI_address2')
    #d.enterFormData(user['city'],id='DUI_city')
    #d.enterFormData(user['state'],id='DUI_state')
    d.enterFormData(user['zip'],id='DUI_zip')
    d.enterFormData(user['timezone'],id='time_zone')
    #d.enterFormData(user['email'],id='DUI_email',clear=True)
    #d.enterFormData(user['phone'],id='DUI_home_phone')
    #d.enterFormData(user['cell'],id='DUI_cell_phone')
    #d.enterFormData(user['carrier'],id='DUI_cellco_id')
    d.enterFormData(user['alert'],id='DUI_preferred_alert_method')
    #d.enterFormData(user['language'],id='DUI_preferred_language')
    d.enterFormData(user['security_question'],id='securitydrop')
    d.enterFormData(user['security_answer'],id='DUI_securityanswer')

    d.verifyElementPresent(id='DPI_country');

    screenshot(d)

    d.clickElement(text=u'NEXT \u25ba')

    # This got removed since we do not ask for ccMe anymore
    #screenshot(d)
    #d.clickElement(text='COMPLETE YOUR NMC REGISTRATION')

    screenshot(d)
    d.clickElement(xpath=u"//a[contains(text(),'Get Started!')]")

def addMembers(d, user):
    d.clickElement(text='Account Summary')
    screenshot(d)
    d.clickElement(text='Add Member')
    screenshot(d)
    d.clickElement(text='Add a New Member')
    screenshot(d)
    d.startSection('Demographics')

    d.enterFormData('Mercuria',id='DPI_first_name')
    d.enterFormData('NMC',id='DPI_middle_name')
    d.enterFormData('Seltest',id='DPI_last_name', clear=True)
    d.enterFormData('123 Main St.',id='DPI_address1', clear=True)
    d.enterFormData('Apt 2A',id='DPI_address2', clear=True)
    d.enterFormData('Boise',id='DPI_city', clear=True)
    d.enterFormData('ID',id='DPI_state', clear=True)
    d.enterFormData('46804',id='DPI_zip_code', clear=True)
    d.enterFormData('UNITED STATES',id='DPI_country', clear=True)
    d.enterFormData('F',id='DPI_sex')
    d.enterFormData('123456777',id='DPI_ssn', clear=True)
    d.enterMIEDate('DPD_birth_date',1,3,1970)
    d.enterFormData('Married',id='DPI_marital_status', clear=True)
    d.enterFormData('5556667777',id='DPI_home_phone', clear=True)
    d.enterFormData('5556667778',id='DPI_cell_phone', clear=True)
    d.enterFormData('no-reply@nomoreclipboard.com',id='DPI_email', clear=True)
    d.enterFormData('English',id='language', clear=True)
    d.enterFormData('Asian',id='DPI_race', clear=True)
    d.enterFormData('Hispanic or Latino',id='ethnicity', clear=True)
    d.enterFormData('70',id='height', clear=True)
    d.enterFormData('166',id='weight', clear=True)
    d.enterFormData('A pos',id='DPI_blood_type', clear=True)
    d.enterFormData('Ed Wood',id='DPI_spouse_name', clear=True)
    d.enterMIEDate('DPD_spouse_birthdate',1,3,1965)
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')

    screenshot(d)

    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Demographics - Page 2')

    d.enterFormData(True,xpath="//input[@type='radio' and @id='DPI_employment_status_P' and @value='P']")
    d.enterFormData('Dog Catcher',id='DPI_occupation')
    d.enterFormData("Mary's Dog Catching Service",id='DPI_employer_name')
    d.enterFormData('5556668888',id='DPI_work_phone', clear=True)
    d.enterFormData('5645 Main St.',id='DPI_employer_addr1', clear=True)
    d.enterFormData('Suite 12',id='DPI_employer_addr2', clear=True)
    d.enterFormData('Molassas',id='DPI_employer_city', clear=True)
    d.enterFormData('ID',id='DPI_employer_state', clear=True)
    d.enterFormData('46807',id='DPI_employer_zipcode', clear=True)
    d.enterFormData('Billy Jones',id='DPI_emergency_contact', clear=True)
    d.enterFormData('Brother',id='DPI_emergency_relation', clear=True)
    d.enterFormData('4442223333',id='DPI_emergency_phone', clear=True)
    d.enterFormData('4442556666',id='DPI_emergency_phone_2', clear=True)
    d.enterFormData('5633 1st Ave.',id='DPI_emergency_addr1', clear=True)
    d.enterFormData('Apt 22',id='DPI_emergency_addr2', clear=True)
    d.enterFormData('Boise',id='DPI_emergency_city', clear=True)
    d.enterFormData('ID',id='DPI_emergency_state', clear=True)
    d.enterFormData('47466',id='DPI_emergency_zip_code', clear=True)
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Health Care Proxy' and @value='No']")
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Living Will' and @value='No']")
    d.enterFormData(True,xpath="//input[@type='radio' and @name='DNR' and @value='Yes']")
    d.enterFormData(True,xpath="//input[@type='radio' and @name='DNH' and @value='No']")
    d.enterFormData(True,xpath="//input[@type='radio' and @name='POLST' and @value='No']")

    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')

    screenshot(d)

    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Click Member Summary to Exit')
    d.clickElement(text='Member Summary')

    screenshot(d)

    d.endSection()

def ccMeNew (d, user):
    d.clickElement(id='ccme_sw_imglink')
    screenshot(d)
    d.clickElement(text='Member Summary')

def preRegisterAppt(d, user):
    d.clickElement(xpath="//img[@alt='Pre-Register for an Upcoming Appointment']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    screenshot(d)

def testNoPats(d,user):
	d.navigate('?f=nmc&page=NMC+Summary')
	screenshot(d)

	# test going to f=layout, should go back to home page
def testflayout(d,user):
	d.navigate('?f=layout&module=NMC+Admin&name=BACKOFFICE&tabmodule=admin')
	screenshot(d)

def memberReview(d, user):
    screenshot(d)
    if not user['cobrand']:
        d.clickElement(xpath="//b[text()='Member Review']/parent::td/parent::tr//a")
        #d.clickElement(xpath="//td/font/a/font[text()='%s, %s']/parent::a/parent::font/parent::td/following-sibling::td/\
        #               following-sibling::td/following-sibling::td/font/a[text()='Begin Review']" %(user['last'], user['first']))

    d.startSection('Demographics')
    d.startSection('Demographic Registration Info')
	 
    d.enterFormData('M',id='DPI_sex')
    d.enterFormData(user['ssn'], id='DPI_ssn')
    d.enterMIEDate('DPD_birth_date', 1,1,1960)
    d.enterFormData(user['marriage'], id='DPI_marital_status')

    d.enterFormData(user['spouse_name'], id='DPI_spouse_name')
    d.enterMIEDate('DPD_spouse_birthdate',1,1,1960)
    d.enterFormData(user['race'], id='DPI_race')
    d.enterFormData(user['ethnicity'], id='ethnicity')
    d.enterFormData(user['language'], id='language')
    d.enterFormData(user['height'], id='height')
    d.enterFormData(user['weight'], id='weight')
    d.enterFormData(user['blood'], id='DPI_blood_type')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    screenshot(d)
    d.startSection('Employment Info')
    d.clickElement(id='DPI_employment_status_F')
    d.enterFormData(user['occupation']['title'], id='DPI_occupation')
    d.enterFormData(user['occupation']['employer'], id='DPI_employer_name')
    d.enterFormData(user['occupation']['phone'], id='DPI_work_phone')
    d.enterFormData(user['occupation']['address1'], id='DPI_employer_addr1')
    d.enterFormData(user['occupation']['address2'], id='DPI_employer_addr2')
    d.enterFormData(user['occupation']['city'], id='DPI_employer_city')
    d.enterFormData(user['occupation']['state'], id='DPI_employer_state')
    d.enterFormData(user['occupation']['zip'], id='DPI_employer_zipcode')
    d.endSection()

    d.startSection('Emergency Contact Info')
    d.enterFormData(user['contact']['name'], id='DPI_emergency_contact')
    d.enterFormData(user['contact']['relation'], id='DPI_emergency_relation')
    d.enterFormData(user['contact']['phone1'], id='DPI_emergency_phone')
    d.enterFormData(user['contact']['phone2'], id='DPI_emergency_phone_2')
    d.enterFormData(user['contact']['address1'], id='DPI_emergency_addr1')
    d.enterFormData(user['contact']['address2'], id='DPI_emergency_addr2')
    d.enterFormData(user['contact']['city'], id='DPI_emergency_city')
    d.enterFormData(user['contact']['state'], id='DPI_emergency_state')
    d.enterFormData(user['contact']['zip'], id='DPI_emergency_zip_code')
    d.endSection()

    d.startSection('Advance Care Documents')
    d.enterFormData(True,name='Health Care Proxy')
    d.enterFormData(True,name='Living Will')
    d.enterFormData(True,name='DNR')
    d.enterFormData(True,name='DNH')
    d.enterFormData(True,name='POLST')
    d.endSection()

    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()
    
    d.startSection('Physicians/Other Medical Providers/Facilities')

    d.enterFormData('Don', id='le_UserPatientsuser__name__display', clear=True, blur=False)
    if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
        d.clickElement(xpath='//span[@id="le_UserPatientsuser_up_id_value_input_span"]//span')
    else:
         d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')
    d.enterFormData('Art Therapy', id='le_UserPatientsuser_up_role_id_value')
    d.clickElement(id='le_UserPatientsuser_button')

    d.enterFormData('NEWZIP',id='le_UserPatientsuser__name__display_zip_input',clear=True)
    d.enterFormData('Don', id='le_UserPatientsuser__name__display', clear=True, blur=False)
    if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
        d.clickElement(xpath='//span[@id="le_UserPatientsuser_up_id_value_input_span"]//span')
    else:
         d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')
    d.enterFormData('Optician', id='le_UserPatientsuser_up_role_id_value')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(id='le_UserPatientsuser_button')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')

    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Insurance')
    d.enterFormData(user['insurance']['company'], id='le_insedit_ac', clear=True, blur=False)
    if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
        d.clickElement(xpath='//span[@id="js_insedit_ac_span"]')
    else:
         d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')
    d.enterFormData(user['insurance']['policy_holder'], id='policy_holder')
    d.enterFormData(user['insurance']['relationship'], id='le_insedit_relation_insured_value')
    d.enterFormData(user['insurance']['group'],id='le_insedit_group_number_value')
    d.enterFormData(user['insurance']['policy'],id='le_insedit_policy_number_value')
    d.enterFormData(user['insurance']['priority'],id='le_insedit_priority_value')
    d.enterMIEDateString('le_insedit_start_datetime_value_var',user['insurance']['start'])
    d.enterMIEDateString('le_insedit_end_datetime_value_var',user['insurance']['end'])
    d.enterFormData(user['insurance']['comment'],id='le_insedit_comments_value')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(id='le_insedit_button')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Medications')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')    
    screenshot(d)
    d.enterFormData(False,id='XRXUP_NOMEDS_check')
    for m in user['meds']:
        #d.enterAutocomplete('js_patmed_ac',m['name'],0)
        d.enterFormData(m['name'], id='le_patmed_ac', clear=True, blur=False)
        if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
             d.clickElement(xpath='//span[@id="js_patmed_ac_span"]')
        else:
             d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')
        #d.enterAutocomplete('dosageac',m['form'],0)
        d.enterFormData(m['form'], id='le_patmed_dosage_value', clear=True, blur=False)
        if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
             d.clickElement(xpath='//span[@id="dosageac_span"]')
        else:
             d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')
        d.enterFormData(m['directions'],id='le_patmed_sig_value')
        d.enterFormData(m['start'],id='le_patmed_start_date_fuzzy_value')
        # Don't enter stopped taking otherwise we get an MIEWindow
        #d.enterFormData(m['end'],id='le_patmed_end_date_fuzzy_value')
        d.enterFormData(m['comment'],id='le_patmed_comments_value')
        d.clickElement(id='le_patmed_button')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Allergies')
    d.enterFormData(True,id='DSA_NKDA')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Illnesses')
    for ill in user['illnesses']:
        current = ill['current']['name'].replace(' ','_')
        past = ill['past']['name'].replace(' ','_')
        no = ill['no'].replace(' ','_')
        d.startSection('Patient Screening %d/3' %(user['illnesses'].index(ill)+1))        
        d.enterFormData(True,xpath="(//input[@type='checkbox' and @id='DS_%s'])[1]" %current)
        d.enterFormData(ill['current']['comment'],id='DSCOMM_%s' %current)
        d.enterFormData(ill['current']['start'],id='DSODATE_%s' %current)

        d.enterFormData(True,xpath="(//input[@type='checkbox' and @id='DS_%s'])[2]" %past)
        d.enterFormData(ill['past']['comment'],id='DSCOMM_%s' %past)
        d.enterFormData(ill['past']['start'],id='DSODATE_%s' %past)
        d.enterFormData(ill['past']['end'],id='DSCDATE_%s' %past)
        
        d.enterFormData(True,xpath="(//input[@type='checkbox' and @id='DS_%s'])[3]" %no)
        d.clickElement(id='helpbuttonorig')
        d.clickElement(id='helpbutton')
        screenshot(d)
        d.clickElement(id='btn3')
        d.clickElement(id='helpbuttonorig')
        d.clickElement(id='helpbutton')
        screenshot(d)
        d.clickElement(xpath="//div[text()='Submit and Proceed']")
        d.endSection()

    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Procedures')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.enterFormData(False,id='DPS_No Known Past Procedures')
    for p in user['procedures']:
        #d.enterAutocomplete('js__ac',p['name'],0)
        d.enterFormData(p['name'],id='le__ac', clear=True, blur=False)
        if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
             d.clickElement(xpath='//span[@id="js__ac_span"]')
        else:
             d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')        
        d.enterFormData(p['physician'],id='le__performing_physician_value')
        d.enterFormData(p['date'],id='le__service_date_fuzzy_value')
        d.enterFormData(p['comment'],id='le__notes_value')
        d.clickElement(id='le__button')
    d.clickElement(id='anesthesia_No')
    d.enterFormData(user['screening']['eye_exam'],id='DPSODATE_Eye Exam')
    d.enterFormData(user['screening']['blood_glucose'],id='DPSODATE_Blood Glucose Screening')
    d.enterFormData(user['screening']['blood_pressure'],id='DPSODATE_Blood Pressure Screening')
    d.enterFormData(user['screening']['flu_vaccine'],id='DPSODATE_flu vaccine')
    d.enterFormData(user['screening']['pneumovax_vaccine'],id='DPSODATE_pneumovax vaccine')
    d.enterFormData(user['screening']['wellness_visit'],id='DPSODATE_wellness visit')
    d.enterFormData(user['screening']['bone_density'],id='DPSODATE_bone density study')
    d.enterFormData(user['screening']['psa'],id='DPSODATE_PSA screening')
    d.enterFormData(user['screening']['colonoscopy'],id='DPSODATE_colonoscopy screening')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')

    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Immunizations')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)

    for imm in user['immunizations']:
        #d.enterAutocomplete('injac',imm['name'],0)
        d.enterFormData(imm['name'],id='le_immunizations_i_description_value', clear=True, blur=False)
        if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
             d.clickElement(xpath='//span[@id="injac_span"]')
        else:
             d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')        
        d.enterMIEDateString('le_immunizations_d_service_date_value_var',imm['date'])
        d.enterFormData(imm['comment'],id='le_immunizations_i_reaction_value')
        d.clickElement(id='le_immunizations_button')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')

    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Family History')
    for hist in user['fam_history']:
        #d.enterAutocomplete('js_famconditions_ac',hist['problem'],0)
        d.enterFormData(hist['problem'], id='le_famconditions_ac', clear=True, blur=False)
        if d.waitFor(d, lambda d: d.getElement(xpath='//div[@class="defaultacdiv"]//div'), expected_return=True, timeout=15):
             d.clickElement(xpath='//span[@id="js_famconditions_ac_span"]')
        else:
             d.reportCommandStatus('nmc.py', '', False, 'autocomplete failure', 'failed to locate the autocomplete choices')  
        d.enterFormData(hist['relationship'],id='le_famconditions_pc_relation_type_id_value')
        d.enterFormData(hist['age'], id='le_famconditions_notes_value')
        d.clickElement(id='le_famconditions_button')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Social History')
    screenshot(d)
    s = user['soc_history']['smoking']
    d.clickElement(xpath="//input[@type='radio' and @value='%s']" %s['value'])
    d.enterFormData(s['started'], id='Smoking Started Age')
    d.enterFormData(s['quit'], id='Smoking Quit Age')
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Smoking Cigarettes' and @value='%s']" %s['cigarettes'])
    d.enterFormData(True, xpath="//input[@type='radio' and @name='Smoking Cigars' and @value='%s']" %s['cigars'])
    d.enterFormData(True, xpath="//input[@type='radio' and @name='Smoking Pipe' and @value='%s']" %s['pipe'])
    d.enterFormData(True, xpath="//input[@type='radio' and @name='Smoking Smokeless' and @value='%s']" %s['smokeless tobacco'])
    a = user['soc_history']['alcohol']
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Alcohol Use' and @value='%s']" %a['value'])
    d.enterFormData(a['drinks'],id='Alcohol Use - Drinks')
    d.enterFormData(a['per'], id='alc_units')
    c = user['soc_history']['caffeine']
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Caffeine Use' and @value='%s']" %c['value'])
    d.enterFormData(c['cups'],id='Caffeine Use - Cups')
    d.enterFormData(c['per'], id='caff_units')
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Drug Use' and @value='%s']" %user['soc_history']['drugs'])
    d.enterFormData(True,xpath="//input[@type='radio' and @name='Exercise' and @value='%s']" %user['soc_history']['exercise'])
    d.enterFormData(user['soc_history']['diet'], id='Diet')
    d.enterFormData(user['soc_history']['comment'], id='Social History - Misc')
    screenshot(d)
    d.clickElement(xpath="//div[text()='Submit and Proceed']")
    d.endSection()

    d.startSection('Finish')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.endSection()

def AskANurse(d, user):
    d.clickElement(text='Click here to return to the portal menu.')
    d.clickElement(xpath="//img[@alt='Ask a Nurse']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    d.enterAutocomplete('datasend_userid_ac_ac','Web',0)
    d.enterFormData('Patient Question', name='doc_subject', clear=True)
    d.enterFormData('Test Question',id='file')
    d.enterFormData(True,id='agree')
    screenshot(d)
    d.clickElement(text='Submit')
    d.clickElement(text='Return to Home Page')

def requestAppt(d, user):
    d.clickElement(xpath="//img[@alt='Request an Appointment']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    d.enterAutocomplete('datasend_userid_ac_ac', 'Web', 0)
    d.enterFormData(True, id='Monday')
    d.enterFormData(True, id='Morning')
    d.clickElement(id='urgency_1')
    d.enterFormData('Testing', id='reason')
    d.enterFormData('This is just a test', id='file')
    screenshot(d)
    d.clickElement(text='Submit')
    d.clickElement(text='Return to Home Page')

def requestMedRefill(d, user):
    d.clickElement(xpath="//img[@alt='Request a Medication Refill']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    d.enterAutocomplete('js_patmed_ac',user['meds'][2]['name'],0)
    d.enterAutocomplete('dosageac',user['meds'][2]['form'],0)
    screenshot(d)
    d.clickElement(text='Submit')

    d.enterAutocomplete('datasend_userid_ac_ac','Web',0)
    d.clickElement(xpath="//b[text()='%s']" %user['meds'][2]['name'])
    d.enterAutocomplete('datasend_pharmid_ac_ac','WalMart',0)
    d.clickElement(id='supply_30')
    d.enterFormData('This is a test',id='file')
    screenshot(d)
    d.clickElement(text='Submit')
    d.clickElement(text='Return to Home Page')

def billing(d, user):
    screenshot(d)
    d.startSection('Make A Payment')
    d.clickElement(xpath="//img[@alt='bill pay']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    d.clickElement(xpath="//img[@alt='Make a Payment']/parent::a")
    screenshot(d)
    d.clickElement(text='Cancel')
    d.endSection()

    d.startSection('Send a question or message')
    d.clickElement(xpath="//img[@alt='bill pay']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    d.clickElement(xpath="//img[@alt='Send a Billing Message']/parent::a")
    d.enterFormData('Test Question', name='doc_subject')
    d.enterFormData('This is just a test', id='file')
    screenshot(d)
    d.clickElement(text='Submit')
    d.clickElement(text='Return to Home Page')
    d.endSection()

    d.startSection('View Receipts')
    d.clickElement(xpath="//img[@alt='bill pay']/parent::a")
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    d.clickElement(xpath="//img[@alt='View Receipts']/parent::a")
    screenshot(d)
    d.clickElement(text='Return To Menu')
    d.endSection()

def viewMessages(d, user):
    d.clickElement(xpath="//img[@alt='View Mailbox']/parent::a")
    screenshot(d)
    d.clickElement(text='View Member Documents')
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))
    screenshot(d)
    d.clickElement(text='Return to Home Page')

def proceedPHR(d, user):
    d.clickElement(xpath="//img[@alt='Proceed to Your Personal Health Record']/parent::a")
    d.enterFormData(True,id='DUCB_dea_number')
    screenshot(d)
    d.clickElement(text='Continue to Personal Health Record')
    screenshot(d)
    d.clickElement(xpath="//font[text()='%s, %s']/parent::a" %(user['last'], user['first']))

def memberAccessCenter(d, user):
    d.startSection('Member Summary Layout')
    d.clickElement(xpath="//b[text()='Edit Member Summary Layout']/parent::td/preceding-sibling::td/a")
    #d.enterFormData(True,id='DPCB_nmc_widget_mshealthvaultdev')
    #d.enterFormData(True,id='DPCB_nmc_widget_nchica')
    #d.enterFormData(True,id='DPCB_nmc_widget_mdmouse')
    screenshot(d)
    d.clickElement(text='Submit')
    d.endSection()

    d.startSection('Access Privileges')
    d.clickElement(xpath="//b[text()='Access Privileges']/parent::td/preceding-sibling::td/a")
    screenshot(d)
    d.clickElement(id='menu1')
    screenshot(d)
    d.clickElement(id='menu2')
    screenshot(d)
    d.clickElement(id='menu3')
    d.enterFormData(user['email'], id='nmc_adminaccess_emailaddress')
    d.enterFormData('Full Access', id='nmc_adminaccess_level')
    #d.clickElement(text='Send Access Email')
    screenshot(d)
    d.clickElement(id='menu4')
    # Ids are supposed to be unique people!
    d.enterFormData(user['email'], xpath="(//input[@id='nmc_adminaccess_emailaddress'])[2]")
    #d.clickElement(text='Send Emancipation Email')
    screenshot(d)
    d.clickElement(id='menu5')
    d.enterFormData('1234',id='DPI_extern_id1')
    d.clickElement(text='Submit PIN')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Print NMC911.com Card (Pops into new window)')
    d.switchToPopup()
    # This popup has an auto-inc mr number, we wont screenshot it
    screenshot(d)
    d.closePopup()
    d.clickElement(text='Member Summary')
    d.endSection()

    d.startSection('Print Summary')
    d.clickElement(xpath="//b[text()='Print Summary']/parent::td/preceding-sibling::td/a")
    d.switchToPopup()
    screenshot(d)
    d.closePopup()
    d.endSection()

    d.startSection('Share my PHR Information with others')
    d.clickElement(xpath="//b[text()='Share my PHR information with others']/parent::td/preceding-sibling::td/a")
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Send Forms')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')
    d.endSection()

    d.startSection('Print NMC911 Card')
    d.clickElement(xpath="//b[text()='Print NMC911 Card']/parent::td/preceding-sibling::td/a")
    d.switchToPopup()
    # This popup has an auto-inc mr number, we wont screenshot it
    #screenshot(d)
    d.closePopup()
    d.endSection()

    #d.startSection('Import Data from pickup code')
    #d.clickElement(xpath="//span[text()='Import data from pickup code']/parent::form/preceding-sibling::a")
    #d.enterFormData('1234', name='PROMO_MERGE', clear=True, blur=False)
    #screenshot(d)
    # Close the MIEWindow (no title)
    #d.clickElement(xpath="//div[text()='Get Documents']/parent::div/parent::button")
    #screenshot(d)
    #d.clickElement(xpath='//div[@class="wc_win noTitle noStatus"]/input[@class="xclose"]')
    #screenshot(d)
    #d.endSection()

def registerInformation(d, user):
    d.clickElement(id='reg_sw_textlink')
    screenshot(d)
    d.clickElement(text='Submit and Edit Employer and Emergency Info')
    screenshot(d)
    d.clickElement(text='Member Summary')
    #d.clickElement(text='Cancel')

    d.clickElement(xpath="//img[@alt='Add Photo']/parent::a")
    screenshot(d)
    d.clickElement(text='Member Summary')

def ccme(d, user):
    d.clickElement(id='ccme_sw_textlink')
    screenshot(d)
    d.clickElement(xpath="//span[text()='How it works']")
    screenshot(d)
    d.clickElement(xpath="//span[text()='FAQ']")
    screenshot(d)
    d.clickElement(xpath="//span[text()='App Tools']")
    screenshot(d)
    d.clickElement(text='Member Summary')

def insurance(d, user):    
    d.clickElement(id='ins_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def medicalProviders(d, user):
    d.clickElement(id='prov_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def documents(d, user):
    d.miedb.dbExec("UPDATE user_extended_fields uef LEFT JOIN users on users.user_id=uef.user_id SET nmc_premium_expire='2030-01-01',nmc_concierge=1 WHERE username='seleniumtest'");
    d.wcutils.waitForAJAX(timeout=60, quiet=5)
    d.clickElement(id='docs_sw_imglink')
    screenshot(d)
    d.clickElement(text='Member Summary')
    d.clickElement(xpath="//img[@alt='Scan Upload Documents']/parent::a")
    d.enterFormData('Test Document', name='subject')
    d.enterFormData('CDA Document', name='doc_type')
    d.enterMIEDate('service_date',4,1,2014)
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.enterFormData('CDAtest.xml',name='file')
    d.clickElement(text='Upload Document')    
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def oakCreekStandardDemo(d, user):
    # What? These things are all covered be previous sections in this test?
    screenshot(d)

def oakCreekCardiology(d, user):
    # What? These things are all covered be previous sections in this test?
    screenshot(d)

def painManagement(d, user):
    d.clickElement(id='ris_sw_textlink')
    # This displays a calendar based on the current day, can't take a screenshot
    d.clickElement(text='Member Summary')

def msHealthVault(d, user):
    d.clickElement(id='hv_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def currentMeds(d, user):
    d.clickElement(id='meds_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def currentIllness(d, user):
    d.clickElement(id='illness_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    
    screenshot(d)
    d.clickElement(text='Member Summary')

    d.startSection('Conditions Review')
    d.clickElement(id='review_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(xpath="//a[@title='Submit and Proceed']")
    screenshot(d)
    d.clickElement(text='Member Summary')
    d.endSection()

def pastIllness(d, user):
    d.clickElement(id='pastill_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def surgeries(d, user):
    d.clickElement(id='surg_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def immunizations(d, user):
    d.clickElement(id='immu_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')    
    screenshot(d)
    d.clickElement(text='Member Summary')

def allergies(d, user):
    d.clickElement(id='agy_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def familyHistory(d, user):
    d.clickElement(id='famhist_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def socialHistory(d, user):
    d.clickElement(id='sochist_sw_textlink')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.clickElement(text='Member Summary')

def dataTracking(d, user):
    d.clickElement(id='datatrack_sw_textlink')
    d.enterFormData(True,id='DPCB_datatrack_bloodpressure')
    d.enterFormData(True,id='DPCB_datatrack_calories')
    d.enterFormData(True,id='DPCB_datatrack_carbs')
    d.enterFormData(True,id='DPCB_datatrack_creatine')
    d.enterFormData(True,id='DPCB_datatrack_glucose')
    d.enterFormData(True,id='DPCB_datatrack_bmi')
    d.enterFormData(True,id='DPCB_datatrack_steps')
    d.enterFormData(True,id='DPCB_datatrack_triglycerides')
    d.enterFormData(True,id='DPCB_datatrack_cholesterol')
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    #d.clickElement(text='Submit')
    #screenshot(d)
    # Jesus, all these links

    d.wcutils.setNeverConfirm(True)

    d.clickElement(text='Member Summary')

def hipaa(d, user):
    d.clickElement(id='hipaa_sw_textlink')
    for h in user['hipaa']:
        idx = user['hipaa'].index(h) + 1
        d.enterFormData(h['name'], id='DPI_HIPAA_person_%d' %idx)
        d.enterFormData(h['relationship'], id='DPI_HIPAA_relationship_%d' %idx)
        d.enterMIEDateString('DPD_HIPAA_dob_%d' %idx, h['dob'])
        d.enterFormData(h['ssn'], id='DPI_HIPAA_id_%d' %idx)
    d.clickElement(id='helpbuttonorig')
    d.clickElement(id='helpbutton')
    screenshot(d)
    d.wcutils.setNeverConfirm(True)
    d.clickElement(text='Member Summary')

def testDocumentSecureSend(d, user):
    d.miedb.dbExec("insert into user_patients SET id=(select user_id FROM users WHERE username='seleniumtest'),pat_id=60580,id_type='user',role_id=1,entered_date=NOW()")
    d.clickElement(id='buttonlink-email');
    d.clickElement(text='0074894')
    d.clickElement(id='email_button');
    screenshot(d)
    d.navigate("?f=chart&s=print&pat_id=60580&page=Mailbox&wizard=2&doc_id=74894&&print_email_recipient=testacct@ccme.com&email_subject=SeleniumTest&email_from_direct_address=testacct@ccme.com&email_body=Testing&print_send_method=8&print_submit_email=Send+Email", report=False)
    screenshot(d)

def download(d, user):
    d.clickElement(xpath="//a[text()='Plain Text/ASCII Format (\"Blue Button\")']")
    d.switchToPopup()
    screenshot(d)
    d.closePopup()
    # These other links are external, not support by webdriver

def runSection(d, func, udata, title):
    d.startSection(title)
    func(d, udata)
    d.endSection()
    return d.getSectionResults()

def buildUserData(username, cobrand):
    u = {
        'activation_code': '',
        'username': username if username else 'seleniumtest',
        'password': 'paper123',
        'first': 'Selenium',
        'middle': 'NMC',
        'last': 'Seltest',
        'address1': '123 Testing Rd',
        'address2': 'Apt 45',
        'city': 'Fort Wayne',
        'state': 'IN',
        'zip': '46835',
        'timezone': 'US/Eastern',
        'email': 'selenium@nomoreclipboard.com',
        'phone': '2605555555',
        'cell': '2605551234',
        'carrier': 'Verizon',
        'alert': 'Email',
        'language': 'English',
        'ssn': '123121234',
        'security_question': 'What is your mothers maiden name?',
        'security_answer': 'Selenium',
        'marriage': 'Married',
        'spouse_name': 'Kate Beckinsale',
        'race': 'White',
        'ethnicity': 'Not Hispanic or Latino',
        'height': '68',
        'weight': '170',
        'blood': 'O pos',
        }
    contact = {
        'name': 'Liam Neeson',
        'relation': 'Professional Ass Kicker',
        'phone1': '2605551010',
        'phone2': '2605552020',
        'address1': 'Unknown',
        'address2': '',
        'city': 'Unknown',
        'state': 'IN',
        'zip': '12345', 
        }
    occupation = {
        'title': 'Software Tester',
        'employer': 'MIE',
        'phone': '2604596270',
        'address1': '6302 Consitution Dr',
        'address2': '',
        'city': 'Fort Wayne',
        'state': 'IN',
        'zip': '46804'
        }
    meds = [
        {'name': 'Levsin',
         'form': 'tablet 0.125mg',
         'directions': 'Three times daily',
         'start': '1-1-2000',
         'end': '1-1-3000',
         'comment': 'Sub-lingual',
         },
        {'name': 'nortriptyline',
         'form': 'capsule 25mg',
         'directions': 'Once daily',
         'start': '1-1-2000',
         'end': '1-1-3000',
         'comment': 'crazy crazy',
         },
        {'name': 'Zetia',
         'form': 'tablet 10mg',
         'directions': 'As needed',
         'start': '1-1-2000',
         'end': '1-1-3000',
         'comment': 'This drug only has one form option so we overcome a bug here',
         }
        ]
    screening = {
        'eye_exam': '1-1-2000',
        'blood_glucose': '1-2-2000',
        'blood_pressure': '1-3-2000',
        'flu_vaccine': '1-4-2000',
        'pneumovax_vaccine': '1-5-2000',
        'wellness_visit': '1-6-2000',
        'bone_density': '1-7-2000',
        'psa': '1-8-2000',
        'colonoscopy': '1-9-2000',
        }
    insurance = {
        'company': 'SAUDER WELFARE TRUST',
        'policy_holder': '%s %s %s' %(u['first'], u['middle'], u['last']),
        'relationship': 'Self',
        'group': '12345',
        'policy': '54321',
        'priority': 'Primary',
        'start': '1-1-2000',
        'end': '1-1-3000',
        'comment': 'An entire century of coverage',
        }
    illnesses = [
        {'current': {
                'name': 'Alzheimers Disease',
                'start': '1-1-2000',
                'comment': 'I dont remember having this',
                },
         'past': {
                'name': 'Difficulty Swallowing',
                'start': '1-1-2000',
                'end': '1-2-2000',
                'comment': 'Just working the turkey through',
                },
         'no': 'Heart Murmur',
         },
        {'current': {
                'name': 'Cirrhosis',
                'start': '1-3-2000',
                'comment': 'I can quit anytime I want',
                },
         'past': {
                'name': 'Liver Failure',
                'start': '1-4-2000',
                'end': '1-5-2000',
                'comment': 'Now is a good time to quit',
                },
         'no': 'Irritable Bowel Syndrome',
         },
        {'current': {
                'name': 'Chlamydia',
                'start': '1-6-2000',
                'comment': 'Curse that foul wench',
                },
         'past': {
                'name': 'Undescended Testicle',
                'start': '1-7-2000',
                'end': '1-8-2000',
                'comment': 'The Descent, now a major motion picture',
                },
         'no': 'Alcoholism',
         },
        ]
    procedures = [
        {'name':'CT scan - whole body',
         'physician': 'Kebert, Xela',
         'date': '1-1-2000',
         'comment': 'This sounds very painful',
         },
        {'name':'Full GIT examination',
         'physician': 'Torvalds, Linus',
         'date': '3-1-2000',
         'comment': 'Git status',
         },
        {'name':'VRA - Visual reinforcement audiometry',
         'physician': 'Rivera, Nick',
         'date': '6-1-2000',
         'comment': 'Hi everybody!',
         },
        ]
    immunizations = [
        {
            'name': 'Eggs',
            'date': '3-3-2000',
            'comment': 'It was eggstravagant!',
        },
        {
            'name': 'Japanese encephalitis',
            'date': '2-14-2000',
            'comment': 'Thank you Mr Roboto',
        },
        {
            'name': 'Latex',
            'date': '1-29-2000',
            'comment': 'This would really suck',
        },
        ]
    fam_history = [
        {
            'problem': 'T cell subsets',
            'relationship': 'Cousin',
            'age': '25',
        },
        {
            'problem': 'B virus infection',
            'relationship': 'Sibling',
            'age': '13',
        },
        {
            'problem': 'K overload',
            'relationship': 'Parent',
            'age': '50',
        },
        ]
    soc_history = {
        'smoking': {
            'value': 'Former smoker',
            'started': '10',
            'quit': '20',
            'cigarettes': 'No',
            'cigars': 'No',
            'pipe': 'No',
            'smokeless tobacco': 'No',
            },
        'alcohol': {
            'value': 'Yes',
            'drinks': '4',
            'per': 'Week',
            },
        'caffeine': {
            'value': 'Yes',
            'cups': '1',
            'per': 'Day',
            },
        'drugs': 'No',
        'exercise': 'Yes',
        'diet': 'Everything I eat turns into poop!',
        'comment': "Here's to alcohol, the cause of and solution to all of life's problems",
        }
    hipaa = [
        {
            'name': 'Darth Vader',
            'relationship': 'Father',
            'dob': '1-1-1960',
            'ssn': '1231212345',
        },
        {
            'name': 'Ellen Ripley',
            'relationship': 'Sister',
            'dob': '1-1-1970',
            'ssn': '111223333',
        },
        {
            'name': 'Weyland-Yutani',
            'relationship': 'Employer',
            'dob': '1-1-1930',
            'ssn': '999887878',
        },
        {
            'name': 'Carl Sagan',
            'relationship': 'Life Coach',
            'dob': '1-1-1940',
            'ssn': '987226548',
        },
        ]
    
    u['meds'] = meds
    u['screening'] = screening
    u['contact'] = contact
    u['occupation'] = occupation
    u['insurance'] = insurance
    u['illnesses'] = illnesses
    u['procedures'] = procedures
    u['immunizations'] = immunizations
    u['fam_history'] = fam_history
    u['soc_history'] = soc_history
    u['hipaa'] = hipaa
    u['cobrand'] = cobrand

    return u
