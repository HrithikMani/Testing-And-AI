"""
 Test for FHIR US Core validation
 @owners: dcarlson
"""

from wcunittest import wcElement

LOGIN_URL = 'http://nvme-test.med-web.com/'

def main(d, WCURL):
    d.startSection('Get the session_id and system handle from the system')
    res = d.miedb.dbQuery("SELECT session_id FROM logins ORDER BY id DESC LIMIT 1")
    if res:
        res = res.getRes()
    d.setUserData('session_id', res[0]['session_id'])
    # d.miedb.dbExec("INSERT INTO session_extended_values SET session_id='{0}', name='fhir_resource_*', value='cruds'".format(res[0]['session_id']))
    res = d.miedb.dbQuery("SELECT value FROM system_info WHERE name='HANDLE' LIMIT 1")
    if res:
        res = res.getRes()
    d.setUserData('handle', res[0]['value'])
    d.endSection()

    d.startSection('Create a new US Core Test')
    d.setBaseURL('')
    d.navigate(LOGIN_URL)
    d.clickElement(xpath='//span[contains(., "US Core v3.1.1")]')
    d.clickElement(xpath='//button[contains(., "Start Testing")]')
    d.clickElement(xpath='//button[contains(., "Run All Tests")]')
    d.enterFormData('https://zeus.med-web.com/webchart/'+d.getUserData('handle')+'/webchart.cgi/fhir/', id='requirement0_input')
    d.enterFormData(d.getUserData('session_id'), id='requirement1_access_token')
    d.enterFormData('18', id='requirement2_input')
    d.screenshot('After entry')
    d.clickElement(xpath='//button[contains(., "Submit")]')
    d.endSection()

    d.startSection('Testing Starting')
    d.waitFor(d, lambda d: d.getElement(xpath="//p[contains(., '274')]"), timeout=10)
    d.screenshot('Tests starting')
    d.waitFor(d, lambda d: d.getElement(xpath="//button[@aria-label='cancel']"), expected_return=False, timeout=600)
    d.endSection() 

    d.startSection('Test Completed')
    d.screenshot('Tests completed')
    d.endSection()

    d.startSection('Check for main level sections passing')

    d.startSection('Capability Statement')
    if d.getElement(xpath='//a[contains(.,"Capability Statement")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Capability Statement")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Capability Statement', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Capability Statement', 'Failed')
        d.screenshot('Capability Statement Failure Message')
    d.endSection()

    d.startSection('Patient Tests')
    if d.getElement(xpath='//a[contains(.,"Patient Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Patient Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Patient Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Patient Tests', 'Failed')
        d.screenshot('Patient Tests Failure Message')
    d.endSection()

    d.startSection('AllergyIntolerance Tests')
    if d.getElement(xpath='//a[contains(.,"AllergyIntolerance Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"AllergyIntolerance Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'AllergyIntolerance Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'AllergyIntolerance Tests', 'Failed')
        d.screenshot('AllergyIntolerance Tests Failure Message')
    d.endSection()

    d.startSection('CarePlan Tests')
    if d.getElement(xpath='//a[contains(.,"CarePlan Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"CarePlan Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'CarePlan Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'CarePlan Tests', 'Failed')
        d.screenshot('CarePlan Tests Failure Message')
    d.endSection()

    d.startSection('CareTeam Tests')
    if d.getElement(xpath='//a[contains(.,"CareTeam Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"CareTeam Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'CareTeam Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'CareTeam Tests', 'Failed')
        d.screenshot('CareTeam Tests Failure Message')
    d.endSection()

    d.startSection('Condition Tests')
    if d.getElement(xpath='//a[contains(.,"Condition Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Condition Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Condition Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Condition Tests', 'Failed')
        d.screenshot('Condition Tests Failure Message')
    d.endSection()

    d.startSection('Implantable Device Tests')
    if d.getElement(xpath='//a[contains(.,"Implantable Device Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Implantable Device Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Implantable Device Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Implantable Device Tests', 'Failed')
        d.screenshot('Implantable Device Tests Failure Message')
    d.endSection()

    d.startSection('DiagnosticReport for Report and Note exchange Tests')
    if d.getElement(xpath='//a[contains(.,"DiagnosticReport for Report and Note exchange Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"DiagnosticReport for Report and Note exchange Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'DiagnosticReport for Report and Note exchange Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'DiagnosticReport for Report and Note exchange Tests', 'Failed')
        d.screenshot('DiagnosticReport for Report and Note exchange Tests Failure Message')
    d.endSection()

    d.startSection('DiagnosticReport for Laboratory Results Reporting Tests')
    if d.getElement(xpath='//a[contains(.,"DiagnosticReport for Laboratory Results Reporting Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"DiagnosticReport for Laboratory Results Reporting Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'DiagnosticReport for Laboratory Results Reporting Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'DiagnosticReport for Laboratory Results Reporting Tests', 'Failed')
        d.screenshot('DiagnosticReport for Laboratory Results Reporting Tests Failure Message')    

    d.endSection()

    d.startSection('DocumentReference Tests (Not Tested Yet)')
    # if d.getElement(xpath='//a[contains(.,"DocumentReference Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
	  #     d.verifyElementPresent(xpath='//a[contains(.,"DocumentReference Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
    #     d.reportCommandStatus('FHIR', 'Inferno', True, 'DocumentReference Tests', 'Passed')
    # else:
    #     d.reportCommandStatus('FHIR', 'Inferno', False, 'DocumentReference Tests', 'Failed')
    #     d.screenshot('DocumentReference Tests')
    d.endSection()

    d.startSection('Goal Tests')
    if d.getElement(xpath='//a[contains(.,"Goal Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Goal Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Goal Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Goal Tests', 'Failed')
        d.screenshot('Goal Tests Failure Message')
    d.endSection()

    d.startSection('Immunization Tests')
    if d.getElement(xpath='//a[contains(.,"Immunization Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Immunization Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Immunization Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Immunization Tests', 'Failed')
        d.screenshot('Immunization Tests Failure Message')
    d.endSection()

    d.startSection('MedicationRequest Tests')
    if d.getElement(xpath='//a[contains(.,"MedicationRequest Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"MedicationRequest Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'MedicationRequest Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'MedicationRequest Tests', 'Failed')
        d.screenshot('MedicationRequest Tests')
    d.endSection()

    d.startSection('Smoking Status Observation Tests')
    if d.getElement(xpath='//a[contains(.,"Smoking Status Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Smoking Status Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Smoking Status Observation Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Smoking Status Observation Tests', 'Failed')
        d.screenshot('Smoking Status Observation Tests Failure Message')
    d.endSection()

    d.startSection('Pediatric Weight for Height Observation Tests')
    if d.getElement(xpath='//a[contains(.,"Pediatric Weight for Height Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Pediatric Weight for Height Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Pediatric Weight for Height Observation Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Pediatric Weight for Height Observation Tests', 'Failed')
        d.screenshot('Pediatric Weight for Height Observation Tests')
    d.endSection()

    d.startSection('Laboratory Result Observation Tests')
    if d.getElement(xpath='//a[contains(.,"Laboratory Result Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Laboratory Result Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Laboratory Result Observation Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Laboratory Result Observation Tests', 'Failed')
        d.screenshot('Laboratory Result Observation Tests')
    d.endSection()

    d.startSection('Pediatric BMI for Age Observation Tests')
    if d.getElement(xpath='//a[contains(.,"Pediatric BMI for Age Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Pediatric BMI for Age Observation Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Pediatric BMI for Age Observation Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Pediatric BMI for Age Observation Tests', 'Failed')
        d.screenshot('Pediatric BMI for Age Observation Tests')
    d.endSection()

    d.startSection('Pulse Oximetry Tests')
    if d.getElement(xpath='//a[contains(.,"Pulse Oximetry Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Pulse Oximetry Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Pulse Oximetry Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Pulse Oximetry Tests', 'Failed')
        d.screenshot('Pulse Oximetry Tests')
    d.endSection()

    d.startSection('Pediatric Head Occipital-frontal Circumference Percentile Tests')
    if d.getElement(xpath='//a[contains(.,"Pediatric Head Occipital-frontal Circumference Percentile Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Pediatric Head Occipital-frontal Circumference Percentile Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Pediatric Head Occipital-frontal Circumference Percentile Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Pediatric Head Occipital-frontal Circumference Percentile Tests', 'Failed')
        d.screenshot('Pediatric Head Occipital-frontal Circumference Percentile Tests')
    d.endSection()

    d.startSection('Observation Body Height Tests')
    if d.getElement(xpath='//a[contains(.,"Observation Body Height Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Observation Body Height Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Observation Body Height Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Observation Body Height Tests', 'Failed')
        d.screenshot('Observation Body Height Tests')
    d.endSection()

    d.startSection('Observation Body Temperature Tests')
    if d.getElement(xpath='//a[contains(.,"Observation Body Temperature Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Observation Body Temperature Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Observation Body Temperature Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Observation Body Temperature Tests', 'Failed')
        d.screenshot('Observation Body Temperature Tests')
    d.endSection()

    d.startSection('Observation Blood Pressure Tests')
    if d.getElement(xpath='//a[contains(.,"Observation Blood Pressure Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Observation Blood Pressure Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Observation Blood Pressure Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Observation Blood Pressure Tests', 'Failed')
        d.screenshot('Observation Blood Pressure Tests')
    d.endSection()

    d.startSection('Observation Body Weight Tests')
    if d.getElement(xpath='//a[contains(.,"Observation Body Weight Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Observation Body Weight Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Observation Body Weight Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Observation Body Weight Tests', 'Failed')
        d.screenshot('Observation Body Weight Tests')
    d.endSection()

    d.startSection('Observation Heart Rate Tests')
    if d.getElement(xpath='//a[contains(.,"Observation Heart Rate Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Observation Heart Rate Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Observation Heart Rate Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Observation Heart Rate Tests', 'Failed')
        d.screenshot('Observation Heart Rate Tests')
    d.endSection()

    d.startSection('Observation Respiratory Rate Tests')
    if d.getElement(xpath='//a[contains(.,"Observation Respiratory Rate Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Observation Respiratory Rate Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Observation Respiratory Rate Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Observation Respiratory Rate Tests', 'Failed')
        d.screenshot('Observation Respiratory Rate Tests')
    d.endSection()

    d.startSection('Procedure Tests')
    if d.getElement(xpath='//a[contains(.,"Procedure Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Procedure Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Procedure Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Procedure Tests', 'Failed')
        d.screenshot('Procedure Tests Failure Message')
    d.endSection()
    
    d.startSection('Encounter Tests')
    if d.getElement(xpath='//a[contains(.,"Encounter Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
     d.verifyElementPresent(xpath='//a[contains(.,"Encounter Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
     d.reportCommandStatus('FHIR', 'Inferno', True, 'Encounter Tests', 'Passed')
    else:
     d.reportCommandStatus('FHIR', 'Inferno', False, 'Encounter Tests', 'Failed')
     d.screenshot('Encounter Tests')
    d.endSection()

    d.startSection('Organization Tests')
    if d.getElement(xpath='//a[contains(.,"Organization Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Organization Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Organization Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Organization Tests', 'Failed')
        d.screenshot('Organization Tests Failure Message')
    d.endSection()

    d.startSection('Practitioner Tests')
    if d.getElement(xpath='//a[contains(.,"Practitioner Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Practitioner Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Practitioner Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Practitioner Tests', 'Failed')
        d.screenshot('Practitioner Tests')
    d.endSection()

    d.startSection('Provenance Tests')
    if d.getElement(xpath='//a[contains(.,"Provenance Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Provenance Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Provenance Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Provenance Tests', 'Failed')
        d.screenshot('Provenance Tests')
    d.endSection()

    d.startSection('Clinical Notes Guidance (Not Tested Yet)')
# if d.getElement(xpath='//a[contains(.,"Clinical Notes Guidance")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
#     d.verifyElementPresent(xpath='//a[contains(.,"Clinical Notes Guidance")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
#     d.reportCommandStatus('FHIR', 'Inferno', True, 'Clinical Notes Guidance', 'Passed')
# else:
#     d.reportCommandStatus('FHIR', 'Inferno', False, 'Clinical Notes Guidance', 'Failed')
#     d.screenshot('Clinical Notes Guidance')
    d.endSection()

    d.startSection('Missing Data Tests')
    if d.getElement(xpath='//a[contains(.,"Missing Data Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]'):
        d.verifyElementPresent(xpath='//a[contains(.,"Missing Data Tests")]/ancestor::ul/preceding-sibling::div/*[local-name()="svg" and contains(@aria-label, "passed")]', present=True)
        d.reportCommandStatus('FHIR', 'Inferno', True, 'Missing Data Tests', 'Passed')
    else:
        d.reportCommandStatus('FHIR', 'Inferno', False, 'Missing Data Tests', 'Failed')
        d.screenshot('Missing Data Tests Failure Message')
    d.endSection()
    
    d.endSection()

    d.startSection('Check for optional options passing')

    d.endSection()

    d.setBaseURL('https://zeus.med-web.com/webchart/{0}/webchart.cgi'.format(d.getUserData('handle')))
