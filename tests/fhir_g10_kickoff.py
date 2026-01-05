"""
 Test for FHIR G10 validation
 @owners: dcarlson nrichardson
"""

from wcunittest import wcElement, wcDBRecord
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = 'http://nvme-test.med-web.com/'

def main(d, WCURL):
    webdriver = driver.getWebDriver()
    d.startSection('Set Handle')
    res = d.miedb.dbQuery("SELECT value FROM system_info WHERE name='HANDLE' LIMIT 1")
    if res:
        res = res.getRes()
    d.setUserData('handle', res[0]['value'])
    d.endSection()

    d.startSection('Connect William Hart to Selenium')
    d.miedb.dbExec("INSERT INTO user_patients SET id=8,id_type='user',pat_id=18,role_id=1")
    d.endSection()

    d.startSection('Create a new G10 Test')
    d.setBaseURL('')
    d.navigate(LOGIN_URL)
    d.clickElement(xpath='//span[contains(., "ONC Certification (g)(10) Standardized API")]')
    d.clickElement(xpath='//button[contains(., "Start Testing")]')
    d.clickElement(xpath='//button[contains(., "Run All Tests")]')
    d.enterFormData('https://zeus.med-web.com/webchart/'+d.getUserData('handle')+'/webchart.cgi/fhir/', id='requirement0_input')
    d.enterFormData('MIE-Inferno', id='requirement1_input')
    d.enterFormData('ABC123DEF456GHI789J0', id='requirement2_input')
    d.enterFormData('MIE-Inferno', id='requirement8_input')
    d.enterFormData('ABC123DEF456GHI789J0', id='requirement9_input')
    d.enterFormData('https://zeus.med-web.com/webchart/'+d.getUserData('handle')+'/webchart.cgi/fhir/', id='requirement13_input')
    d.enterFormData('https://zeus.med-web.com/webchart/'+d.getUserData('handle')+'/webchart.cgi/oauth/token/', id='requirement14_input')
    d.enterFormData('MIE-Inferno-Bulk', id='requirement15_input')
    d.enterFormData('23', id='requirement18_input')
    d.enterFormData('18,49', id='requirement19_input')
    d.clickElement(xpath='//input[@type="radio" and @value="RS384"]/parent::span')
    d.enterFormData('https://zeus.med-web.com/webchart/'+d.getUserData('handle')+'/webchart.cgi/fhir/', id='requirement23_input')

    d.screenshot('After entry')
    d.clickElement(xpath='//button[contains(., "Submit")]')
    d.endSection()

    d.startSection('Testing Starting')

    d.startSection('First authorization')
    d.waitFor(d, lambda d: d.getElement(xpath="//a[contains(., 'Follow this link to authorize with the SMART server')]"), timeout=15)
    d.screenshot('First auth')
    d.clickElement(xpath='//a[contains(., "Follow this link to authorize with the SMART server")]')
    d.screenshot('Outside page 1')
    d.clickElement(id='pat_scope')
    d.screenshot('Auth page 1')
    d.clickElement(name='allow_access')

    d.screenshot('Inferno back')

    d.endSection() 

    d.startSection('Second authorization')

    d.waitFor(d, lambda d: d.getElement(xpath="//h3[contains(., 'Standalone Patient App - Limited Access')]"), timeout=75)

    d.screenshot('2nd auth')

    d.clickElement(xpath='//a[contains(., "Follow this link to authorize with the SMART server")]')

    d.screenshot('Outside page 2')
    d.clickElement(id='pat_scope')
    d.screenshot('Auth page 1')
    d.clickElement(xpath='//li[contains(., "patient/AllergyIntolerance.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Binary.read")]')
    d.clickElement(xpath='//li[contains(., "patient/CapabilityStatement.read")]')
    d.clickElement(xpath='//li[contains(., "patient/CarePlan.read")]')
    d.clickElement(xpath='//li[contains(., "patient/CareTeam.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Device.read")]')
    d.clickElement(xpath='//li[contains(., "patient/DiagnosticReport.read")]')
    d.clickElement(xpath='//li[contains(., "patient/DocumentReference.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Encounter.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Endpoint.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Goal.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Group.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Immunization.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Location.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Medication.read")]')
    d.clickElement(xpath='//li[contains(., "patient/MedicationRequest.read")]')
    d.clickElement(xpath='//li[contains(., "patient/OperationOutcome.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Organization.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Person.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Practitioner.read")]')
    d.clickElement(xpath='//li[contains(., "patient/PractitionerRole.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Procedure.read")]')
    d.clickElement(xpath='//li[contains(., "patient/Provenance.read")]')

    d.screenshot('Auth Clicked')
    d.clickElement(name='allow_access')
    d.screenshot('Inferno back')

    d.endSection() 

    d.startSection('Third authorization')

    d.waitFor(d, lambda d: d.getElement(xpath="//h3[contains(., 'EHR Practitioner App')]"), timeout=75)

    d.screenshot('3rd auth')

    d.navigate('https://zeus.med-web.com/webchart/'+format(d.getUserData('handle'))+'/webchart.cgi?func=omniscope')

    d.clickElement(xpath='//span[contains(., "Select Portlets")]')
    d.clickElement(xpath='.//input[@type="checkbox" and @value="FHIR Launch"]')    
    d.clickElement(xpath='.//input[@type="checkbox" and @value="Checkin"]')    
    d.clickElement(xpath='.//input[@type="checkbox" and @value="Tasks"]')    

    d.screenshot('FHIR Launch clicked')

    d.clickElement(value='Save')

    d.pause(3)
    
    d.waitFor(d, lambda d: d.getElement(xpath="id='moveable_shade_AdministratorPortlet_Welcome'"), timeout=15)
    d.clickElement(id='moveable_shade_AdministratorPortlet_Welcome')

    d.clickElement(xpath='//a[contains(., "Launch Inferno EHR Launch")]')

    d.pause(2)

    d.switchToPopup()

    d.waitFor(d, lambda d: d.getElement(xpath='//a[contains(., "Follow this link to authorize with the SMART server")]'), timeout=15)

    d.screenshot('Back to Inferno')

    d.clickElement(xpath='//a[contains(., "Follow this link to authorize with the SMART server")]')
    d.screenshot('Outside page 3')

    d.clickElement(id='pat_scope')

    d.screenshot('Auth page 3')
    d.screenshot('Auth Clicked')
    d.clickElement(name='allow_access')
    d.screenshot('Inferno back')

    d.endSection()     

    d.startSection('4, 5, then 6 authorization')

    d.waitFor(d, lambda d: d.getElement(xpath="//h3[contains(., 'Additional Tests')]"), timeout=500)

    wcElement('xpath', '//h3[contains(., "Additional Tests")]', exists=True)

    d.pause(3)

    d.screenshot('6th auth')

    d.clickElement(xpath='//a[contains(., "Follow this link to authorize with the SMART server")]')    
    d.pause(3)
    d.screenshot('Outside page 1')
    d.clickElement(id='pat_scope')
    d.screenshot('Auth page 1')
    d.clickElement(name='allow_access')

    d.screenshot('Inferno back')

    d.waitFor(d, lambda d: d.getElement(xpath="//h3[contains(., 'User Action Required')]"), timeout=500)
    d.clickElement(xpath='//a[contains(., "Perform Invalid Launch")]')
    d.pause(3)
    webdriver.back()
    d.pause(3)
    d.clickElement(xpath='//a[contains(., "Attest launch failed")]') 

    d.pause(10)
    d.clickElement(xpath='//a[contains(., "Follow this link to authorize with the SMART server")]')    
    d.pause(3)
    d.screenshot('Outside page 1')
    d.clickElement(id='pat_scope')
    d.screenshot('Auth page 1')
    d.clickElement(name='allow_access')

    d.waitFor(d, lambda d: d.getElement(xpath="//h3[contains(., 'Visual Inspection and Attestation')]"), timeout=500)
    d.clickElement(xpath='//button[contains(., "Submit")]')

    d.endSection()     

    d.endSection()

    d.startSection('Final Result SS')

    d.clickElement(id='mui-8-g10_certification/report')
    d.screenshot('Final Report')

    d.endSection()

    d.setBaseURL('https://zeus.med-web.com/webchart/{0}/webchart.cgi'.format(d.getUserData('handle')))
