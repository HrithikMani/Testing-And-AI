def main (d, WCURL):
    """
    Adds a Pregnancy to patient Jennifer Pregnant and tracks
    the condition through all of its stages.
    """
    #$ begin by adding a pregnancy condition
    d.navigate(WCURL.CHART_PREGNANT_JENNIFER + "v=cond&t=Medical+Record%3APatient%2FFamily+Conditions")
    d.clickElement(text='Add Condition')
    
    d.verifyElementPresent(value='Submit and Conclude')
    
    d.wcutils.setNeverConfirm(True)
    
    d.enterAutocomplete('js_cond_ac','pregnancy',0,'Pregnancy (V22, Normal Pregnancy) (Z33.1, Pregnant state, incidental)')
    
    if not d.verifyAttribute('value','3140',id='autocode'):
        d.addErrorMessage('The conditions autocomplete did not select the right code for pregnancy (3140)')
        return

    d.verifyAttribute('checked',True,id='autocode')
    
    d.enterMIEDateAdd('onset_date',-9,'month')
    
    d.clickElement(value='Submit')
    
    d.verifyElementPresent(text='Pregnancy (V22 Z33.1)')
    
    d.navigate(WCURL.CHART_PREGNANT_JENNIFER + "v=dashboard&t=Visits%3AOB+Flow", auto_screenshot=False)
    
    d.verifyElementPresent(xpath="//font[text()='Obstetrical Record']")
    
    d.enterFormData('O pos',id='DPI_blood_type_rh')
    d.clickElement(value='Set')
    
    # navigate to top row input page
    #d.clickElement(xpath="//form[@id='preginput']/table[3]//fieldset/table[0]//table[0]//tr[1]/td[1]/a")
#    eles = d.getElements(xpath="//form[@id='preginput']//a/font[contains(text(),'Add')]/parent::a")
#    i=0
#    while i < len(eles):
#        href = eles[i].get_attribute('href')
#        if href:
#            idx = href.find('Preg1')
#            if idx > -1:
#                eles[i].click()
#                break
#        i = i + 1
    d.clickElement(xpath="//a[contains(@href,'Preg1')]")
    
    d.verifyElementPresent(xpath="//span[contains(text(),'Add Pregnancy Observations')]")
    d.verifyElementPresent(xpath="//td[text()='HGB']")

    d.enterMIEDateAdd('observed_datetime',-14,'day')
    
    d.enterFormData('15',id='hgb')
    d.enterFormData('25',id='hct')
    d.enterFormData('35',id='plt')
    d.enterFormData('nonreactive',id='rpr')
    d.enterFormData('immune',id='rubella')
    d.enterFormData('neg',id='antibody')
    d.enterFormData('neg',id='hbsag')
    d.enterFormData('ok',id='pap')
    d.enterFormData('neg',id='ua')
    d.enterFormData('declined',id='hiv')
    d.enterFormData('neg',id='triple')
    
    d.clickElement(value='Submit')
    
    d.verifyElementPresent(xpath="//font[text()='Obstetrical Record']")
    d.verifyElementPresent(text='declined')
    
    d.clickElement(xpath="//a[contains(@href,'Preg2')]")
    
    d.verifyElementPresent(xpath="//span[contains(text(),'Add Pregnancy Observations')]")
    d.verifyElementPresent(xpath="//td[text()='28 wk Titer']")

    d.miedb.dbExec("insert into autocomplete_field set module='observations',field=40,use_count=2,data='abc123'")

    d.enterMIEDateAdd('observed_datetime',-14,'day')
    
    d.enterFormData('pos',id='wktiter')
    d.enterFormData('20',id='wkhgb')
    d.enterFormData('30',id='1hrglu')
    d.enterFormData('0',id='2hrpp')
    d.enterFormData('0',id='fbs')
    d.enterFormData('1',id='1hr')
    d.enterFormData('2',id='2hr')
    d.enterFormData('3',id='3hr')
    d.enterAutocomplete('betastrac','a',0,'abc123')
    d.enterFormData('neg',id='cfscreen')
    d.enterFormData('0',id='amnio')
    
    d.clickElement(value='Submit')
    
    d.verifyElementPresent(xpath="//font[text()='Obstetrical Record']")
    d.verifyElementPresent(text='abc123')
    
    d.clickElement(text='Edit')
    
    d.verifyElementPresent(xpath="//span[contains(text(),'Pregnancy Details')]")
    
    d.enterFormData('3',id='Total Pregnancies')
    d.enterFormData('2',id='Full Term Pregnancies')
    d.enterFormData('1',id='Pre Term Pregnancies')
    d.enterFormData('0',id='Abortions and Miscarriages')
    d.enterFormData('3',id='Living Children')
    d.enterAutocomplete('preghosp0_ac','r',0)
    d.enterAutocomplete('preghosp1_ac','m',0)
    d.enterFormData('Dr Shnots',id='DPREGI_pediatrician')
    d.enterFormData('Raul',id='DPREGI_father')
    d.enterMIEDateAdd('DPREGD_onset_date',-9,'month')
    d.clickElement(value='Calculate')
    d.enterFormData('LMP',id='DPREGI_date_change_reason')
    
    d.clickElement(value='Submit')
    
    d.verifyElementPresent(xpath="//font[text()='Obstetrical Record']")
    d.verifyElementPresent(xpath="//td[contains(text(),'Raul')]")

    d.clickElement(xpath="//a[contains(@href,'Flow')]/font[text()='Add']/parent::a")
    
    d.miedb.dbExec("insert into autocomplete_field (module, field, use_count, data) VALUES \
                 ('observations',8,2,'2'),('observations',9,2,'7'),('observations',11,2,'12'), \
                 ('observations',12,2,'17'),('observations',44,2,'breach'),('observations',48,2,'Likes to bite');")
    
    d.enterMIEDateAdd('observed_datetime',-1,'month')
    
    d.enterFormData('180',id='weight')
    d.enterAutocomplete('uralbac','2',0)
    #d.enterFormData('2',id='uralb')
    #ele = d.getElement(id='uralbac_span_choices_0')
    #if ele:
    #    ele.click()
    d.enterAutocomplete('urgluac','7',0)
    d.enterFormData('180/90',id='bp')
    d.enterAutocomplete('mvmntac','1',0)
    d.enterAutocomplete('edemaac','1',0)
    d.enterFormData('23',id='fheight')
    d.enterFormData('190',id='fhr')
    d.enterAutocomplete('fpositionac','b',0)
    d.enterAutocomplete('quickremac','L',0)
    d.enterFormData('A Remarkable Lady',id='remarks')
    d.enterFormData('9',id='RTO',clear=True)
    d.enterFormData('mie',id='initials')    
    
    d.clickElement(value='Submit')
    
    d.verifyElementPresent(xpath="//font[text()='Obstetrical Record']")
    d.verifyElementPresent(text='180/90')

    d.clickElement(text='Conclude Pregnancy')
    
    d.verifyElementPresent(xpath="//span[contains(text(),'Conclude Pregnancy')]")
    
    d.miedb.dbExec("insert into autocomplete_field (module, field, use_count, data) VALUES \
                 ('preg','diag',2,'Live Birth'),('preg','anesth',2,'Epidural'),\
                 ('preg','sterile',2,'None'),('preg','method',2,'Vaginal'),\
                 ('preg','epis',2,'+1');")
    
    d.enterMIEDateAdd('admitdate',-1,'day')
    d.enterFormData('9',id='preg_deliveringDr_pick')
    d.enterFormData('16',id='preg_recordDr_pick')
    d.enterAutocomplete('diagac','l',0)
    d.enterAutocomplete('anesthac','e',0)
    d.enterAutocomplete('sterac','n',0)
    d.enterAutocomplete('delMethac','v',0)
    d.enterAutocomplete('episac','+',0)
    #d.enterFormData('',id='gestAge')
    # simulate tabbing through gestAge
    d.runJS("conclusion_dateOnChange($('gestAge'))")
    d.enterFormData('One Happy Bundle of Joy',id='pregNotes')
    
    d.clickElement(value='Enter Child Information (Step 1 of 2)')
    
    d.verifyElementPresent(xpath="//td[text()='Infant Information']")
    
    d.miedb.dbExec("insert into autocomplete_field (module,field,use_count,data) VALUES \
                 ('preg','apgar',2,'8'),('preg','apgar',2,'9');")
    
    d.enterAutocomplete('preg_delMeth0ac','v',0)
    d.enterFormData('0',id='preg_isLive0')
    d.enterFormData('Male',id='preg_sex0')
    d.enterAutocomplete('preg_apgar10ac','8',0)
    d.enterAutocomplete('preg_apgar50ac','9',0)
    d.enterFormData('7',id='preg_lbs0')
    d.enterFormData('8',id='preg_oz0')
    d.enterFormData('19',id='preg_infLength0')
    d.enterFormData('15',id='preg_infHead0')
    d.enterFormData('John',id='preg_infFName0')
    d.enterFormData('Michael',id='preg_infMName0')
    d.enterFormData('Bluth',id='preg_infLName0')
    
    d.clickElement(value='Conclude Pregnancy')

    d.navigate(WCURL.CHART_PREGNANT_JENNIFER + "v=list&t=Document+Summary", auto_screenshot=False)

    d.verifyElementPresent(text='OB Flow - Archived')
    
    d.clickElement(text='OB Flow - Archived')
    
    d.verifyElementPresent(xpath="//td[text()='3402 g']")
    d.verifyElementPresent(xpath="//td[text()='One Happy Bundle of Joy']")
    d.verifyElementPresent(xpath="//a[text()='immune']")
    d.verifyElementPresent(xpath="//td[text()='A Remarkable Lady']")

    #$ now we can edit the pregnancy condition
    d.navigate(WCURL.CHART_PREGNANT_JENNIFER + "t=Current%3APast+Medical+History&v=dashboard")
    d.screenshot('Past_medical_history_before')
    d.clickElement(id='preglist_RecordList_Edit0')
    d.enterFormData('Cesarean',id='le_preglist_birth_method_value', clear=True)
    #This is throwing a JS error
    #d.enterMIEDateAdd('le_preglist_birth_time_value_var',-2,'day')
    d.enterFormData('8',id='le_preglist_wt_lbs_value', clear=True)
    d.enterFormData('9',id='le_preglist_wt_oz_value', clear=True)
    d.enterFormData('F',id='le_preglist_sex_value', clear=True)
    d.enterFormData('Michael',id='le_preglist_name_first_value', clear=True)
    d.enterFormData("Cries a lot",id='le_preglist_complications_value', clear=True)
    d.enterFormData('Dr Feelgood',id='le_preglist_delivering_dr_string_value', clear=True)
    d.clickElement(xpath="//span[@id='preglist_RecordList_edit_span']/span[1]/input")
    d.clickElement(value='Submit')
    d.screenshot('Past_medical_history_after')
