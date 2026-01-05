def main(d, WCURL):
    """
    This Clinical Test Scenario involves a routine well-child
    visit to his Primary Care Physician for immunization, 
    examination and prescription creation.
    """
    d.navigate(WCURL.LOGOUT)
    reception = 'reception'
    nurse = 'nurse'
    nurse_p = 'ethompson'
    password = 'paper'
    # Remove the password expiration on users (reception, nurse)
    d.miedb.dbExec("UPDATE users SET pwd_expire='' WHERE username IN ('%s','%s')" %(reception, nurse))
    
    #$ Receptionist
    d.enterFormData(reception,id='login_user')
    d.enterFormData(password,'login_passwd')
    d.clickElement(value='Log On')
    d.verifyTitle('(WebChart Testing System) - User: (Reception)')
    d.navigate(WCURL.ECHART)
    d.clickElement(text='Patient Registration')
    last = 'Gardner'
    first = 'Joe'
    ssn = '111-11-1111'
    mrn = '12345678'
    d.enterFormData(last,id='patient_last_name')
    d.enterFormData(first,id='patient_first_name')
    d.enterMIEDate('patient_birth_date',07,01,1998)
    d.enterFormData(ssn,id='patient_ssn')
    d.clickElement(value='Search')

    d.enterFormData(mrn,xpath="//input[@name='mrnumber_CCHIT' and @type='HIDDEN']/following-sibling::input")
    d.clickElement(value='Save')

    d.navigate(WCURL.ECHART)
    d.enterFormData('Smith',name='sstring')
    d.clickElement(value='Search')
    if not d.verifyElementPresent(text='CCHIT-41205323'):
        d.addErrorMessage('Joe Smith - CCHIT-41205323 Did not show in the listview when searching by Smith')
    if not d.verifyElementPresent(text='CCHIT-00000222'):
        d.addErrorMessage('Ted Smith - CCHIT-00000222 Did not show in the listview when searching by Smith')
    d.addErrorMessage('Still missing a second Joe Smith in the database, I do not know why he isnt there')

    d.enterFormData('CCHIT-41205323',name='sstring')
    d.clickElement(xpath="//input[@type='radio' and @name='by' and @value='m']")
    d.clickElement(value='Search')
    if not d.verifyElementPresent(value='Preview Merge'):
        d.addErrorMessage('Couldnt find the Preview Merge button, did we get to Joe Smiths chart?')
    d.navigate(WCURL.ECHART)

    d.enterFormData('Gardner',name='sstring')
    d.clickElement(xpath="//input[@type='radio' and @name='by' and @value='n']")
    d.clickElement(value='Search')
    d.clickElement(text='Manual Search')
    d.clickElement(xpath="//input[@type='radio' and @name='by' and @value='m']")
    d.enterFormData('CCHIT-41205323',name='sstring')
    d.clickElement(value='Search')
    d.clickElement(text='CCHIT-41205323')
    d.clickElement(xpath="//input[@type='radio' and @name='merge_opts_9' and @value='2']")
    d.clickElement(value='Merge Using Selected Options')
    if not d.clickElement(value='Go To Patient'):
        d.addErrorMessage('Could not find the Go To Patient button after a successful patient merge')

    d.navigate(WCURL.ECHART)
    d.addErrorMessage('Still need to verify Age expressed in years and months')

    d.clickElement(text='CCHIT-12345678')
    d.clickElement(text='Edit Demo')
    d.addErrorMessage('There are no female Smiths in the system. Need to have one listed as Joe Smiths mother')

    d.addErrorMessage('Cant check historical data without having someone to edit as Joe Smiths mother')

    d.addErrorMessage('There is no patient available to be listed as Joe Gardners/Joe Smiths grandmother')

    d.navigate(WCURL.LOGOUT)

    #$ Nurse
    d.enterFormData(nurse,id='login_user')
    d.enterFormData(password,id='login_passwd')
    d.clickElement(value='Log On')
    d.verifyTitle('(WebChart Testing System) - User: (Nurse, RN)')
    d.navigate(WCURL.ECHART)
    d.enterFormData('Gardner',name='sstring')
    d.clickElement(value='Search')

    d.clickElement(xpath="//label[text()='Family Medical History']/following-sibling::div/div/a[@title='Manage Information']")
    d.clickElement(text='Add Family Condition')
    d.enterAutocomplete('le_cond_ac','js_cond_ac_span_choices','Heart Disea',0)
    d.clickElement(xpath="//input[@id='relation_type_id' and @value='10']")
    d.enterFormData('Died of heart attack at age 34',name='cond_notes')
    d.clickElement(value='Submit')

    d.addErrorMessage('I do not know how to view immunizations that are due')

    d.navigate(WCURL.ECHART)
    d.clickElement(text='CCHIT-12345678')
    if not d.verifyElementPresent(xpath="//label[text()='Allergies']/parent::div/parent::div//li[contains(text(),'PENICILLINS')]"):
        d.addErrorMessage('Could not find the PENICILLIN allergy in the patient Allergies portlet')

    d.clickElement(xpath="//label[text()='Allergies']/following-sibling::div/div/a[@title='Manage Information']")
    d.clickElement(xpath="//a/font[text()='PENICILLINS']/parent::a/parent::font/parent::td/parent::tr/td[last()]//a/font[text()='Discontinue']")
    d.clickElement(id='end_dateTODAY')
    d.enterFormData('Overbearing mother gave false information',id='reason')
    d.clickElement(value='Submit')

    d.clickElement(text='Quick Allergy')
    d.enterAutocomplete('qagy_allergy_name0','qagyagyac0_span_choices','Peanut',1)
    # if we don't blur the AC, it won't POST correctly, so click the allergy radio
    d.clickElement(xpath="//input[@type='radio' and @name='qagy_intolerance0']")
    d.clickElement(name='qagy_submit')

    d.clickElement(text='Peanuts')
    d.enterAutocomplete('agydetails_reaction','reactac_span_choices','Hiv',0,'hives')
    d.clickElement(value='Submit')

    d.clickElement(text='Show Discontinued')
    if not d.verifyElementPresent(xpath="//b[text()='Discontinued']/parent::font/parent::font/parent::td/parent::tr//nobr[text()='N']"):
        d.addErrorMessage('Discontinued the penicillin allergy, but now either cannot find it or its not listing who discontinued it')

    d.clickElement(text='Patient Summary')
    d.clickElement(xpath="//label[text()='Vitals']/following-sibling::div/div/a[@title='Manage Information']")
    d.enterFormData('130',id='bpsys')
    d.enterFormData('90',id='bpdia')
    d.closeAlert(False)
    d.enterFormData('58',id='height')
    d.enterFormData('in',id='height_units')
    d.enterFormData('80',id='weight')
    d.enterFormData('lbs',id='weight_units')
    d.enterFormData('98.6',id='temperature')
    d.enterFormData('F',id='temp_units')
    d.enterFormData('124',id='pulse')
    d.closeAlert(False)
    d.enterFormData('30',id='resp')
    d.closeAlert(False)
    d.clickElement(value='Submit')

    if not d.verifyAttribute('text','16.72',xpath="//td/font[text()='Nurse']/parent::td/parent::tr/td[4]/font/a"):
        d.addErrorMessage('Could not find the valid BMI of 16.72')

    if not d.verifyAttribute('text',' ',xpath="//td/font[text()='Nurse']/parent::td/parent::tr/td[last()-1]/font"):
        d.addErrorMessage('Could not verify the pain level of 0')

    #???

    # ???? Flowsheets - MIEPLOT.cgi is missing

    d.navigate(WCURL.LOGOUT)

    #$ Nurse Practitioner
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! This should be Nurse Practitioner instead
    d.enterFormData(nurse_p,id='login_user')
    d.enterFormData(password,id='login_passwd')
    d.verifyTitle('(WebChart Testing System) - User: (Reception)')
    
    d.enterFormData('Gardner',name='sstring')
    d.clickElement(xpath="//label[text()='Allergies']/following-sibling::div/div/a[@title='Manage Information']")





    #$ Nurse












    #$ Nurse Practitioner












    #$ Doctor Alexander















    d.navigate(WCURL.LOGOUT)
