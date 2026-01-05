# 
# Webchart Injection Extended Add UnitTest

def main (driver, WCURL):
    """
    Add an injection record with immunization registry options enabled
    """

    d = driver

    # enable chirp options
    d.wcutils.SetSystemSetting("E-Chart","CHIRP","Use Chirp","1",False)

    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT,auto_screenshot='VXQ_link_present')

    d.clickElement(text='Add Inj/Imm')
    d.pause(2)
    d.screenshot('adddialog')
    
    value = """
SELECT p.last_name as 'Patient Last Name',
p.first_name AS 'Patient First Name',
p.address1 AS 'Patient\\'s Address',
p.city AS 'Patient\\'s City',
p.zip_code AS 'Patient\\'s Zip Code',
p.sex AS 'Patient\\'s Gender',
p.race AS 'Patient\\'s Race',
o.obs_result AS 'Patient\\'s Ethnicity',
pvfc.value AS 'Patient\\'s VFC Code',
IF(opt.obs_result IS NULL OR opt.obs_result='I','.','') AS 'Patient is Currently Opted Out. This record will not be submitted to the Wyoming Immunization Registry. Opt In'
FROM patients p
LEFT JOIN observations o ON o.pat_id=p.pat_id AND o.obs_code=(SELECT obs_code FROM observation_codes WHERE obs_name='Ethnicity' AND interface='WEBCHART')
LEFT JOIN observations opt ON opt.pat_id=p.pat_id AND opt.obs_name='WCWYOPTSTATUS'
LEFT JOIN patient_extended_values pvfc ON pvfc.pat_id=p.pat_id AND pvfc.ext_id=(SELECT ext_id FROM patient_extended_index WHERE name='vfc_code')
LEFT JOIN patient_extended_values pm ON pm.pat_id=p.pat_id AND pm.ext_id=(SELECT ext_id FROM patient_extended_index WHERE name='mother_maiden_name')
LEFT JOIN patient_extended_values plg ON plg.pat_id=p.pat_id AND plg.ext_id=(SELECT ext_id FROM patient_extended_index WHERE name='LegalGuardian')
LEFT JOIN (
SELECT * FROM patients WHERE pat_id=(SELECT gurantor_id FROM patients WHERE pat_id=@pat_id)
UNION
SELECT * FROM patients WHERE pat_id=(SELECT related_pat_id FROM pat_pat_relations WHERE pat_id=@pat_id AND relation_type_id=9)
UNION
SELECT * FROM patients WHERE pat_id=(SELECT related_pat_id FROM pat_pat_relations WHERE pat_id=@pat_id AND relation_type_id=10)
UNION
SELECT * FROM patients WHERE pat_id=(SELECT related_pat_id FROM pat_pat_relations WHERE pat_id=@pat_id AND relation_type_id=3)
) as g ON 1"""
    d.wcutils.SetSystemSetting("E-Chart","Injections","Patient Required Fields",value,False)
    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT,auto_screenshot=False)
    d.clickElement(text='Add Inj/Imm')
    d.pause(2)
#    d.screenshot('patient_warning')
    d.verifyAlert('Required Fields: * not present.*',accept=True)
    d.pause(2)
    d.screenshot('pat_stay_on_page')
    
    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT,auto_screenshot=False)
    d.clickElement(text='Add Inj/Imm')
    d.pause(2)
    d.verifyAlert('Required Fields: * not present.*',accept=False)
    d.pause(2)
    d.screenshot('redirect_to_demo')

    # lazy - don't fix the problem, just remove the prompt
    d.wcutils.SetSystemSetting("E-Chart","Injections","Patient Required Fields","",False)
    
    value = """
{
  'route': {
    'text':'Immunization Route',
    'req':true,
    'fields': [$('route')]
  },
  'site': {
    'text':'Immunization Site',
    'req':true,
    'fields': [$('site')]
  },
  'vacc_date': {
    'text':'Vaccination Date',
    'req':true,
    'fields':  [$('service_dateMONTH'),
                $('service_dateDAY'),
                $('service_dateYEAR')]
  },
  'service_location': {
     'text':'Service Location',
     'req':true,
     'fields': [$('service_location')]
  },
  'vfc_code': {
     'text':'VFC Code',
     'req':true,
     'fields': [$('vfc_code')]
  }
}"""
#    d.wcutils.SetSystemSetting("E-Chart","Injections","Additional Warning Fields",value,False)
#    d.wcutils.SetSystemSetting("E-Chart","Injections","Additional Warning Message","Other fields are required",False)
#    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT + "&injopp=add",auto_screenshot=False)
#    d.clickElement(value='Submit')
#    d.verifyAlert('Other fields are required*',accept=False)
#    d.pause(2)
#    d.screenshot('inj_stay_on_page')
#
#    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT + "&injopp=add",auto_screenshot=False)
#    d.clickElement(value='Submit')
#    d.verifyAlert('Other fields are required*',accept=True)
#    d.pause(2)
#    d.screenshot('inj_submit_empty')
    
    d.navigate(WCURL.CHART_HART_WILLIAM + WCURL.INJECT + "&injopp=add",auto_screenshot=False)
    d.enterAutocomplete('description_ac','Hep B',2,'Hep B, adult')
    d.enterFormData('Office',id='service_location')
    #d.enterMIEDate('service_date',5,1,2013,1600)
    d.enterFormData('IM',id='route')
    d.enterFormData('RA',id='site')
    d.enterAutocomplete('doseac','10',-1,'10')
    d.enterAutocomplete('strengthac','1',-1,'1')
    d.enterAutocomplete('manufacturer_ac_inject_manufact','SKB',-1)
    d.enterFormData('ABC1239',id='vial')
    d.enterMIEDate('expiration_date',5,1,2015)

    d.enterFormData('I am a comment!',id='reaction')
    d.enterFormData('V01',id='vfc_code')
    
    d.clickElement(value='Submit')
    d.pause(2)
    d.screenshot('injection_added')
