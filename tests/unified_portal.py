from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import Select
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
import sys
import math
import cgi

CGIVars = {}
roundCeil = 200
roundDiffFactor = 20
resumeClinician = 'Request Leave of Absence'
calculation = 'Intimate Partner Violence Screening (IPV)'
questionnaires = ['Lead Questionnaire', 'Travel Questionnaire']
patient = {'questionnaire': 'Incident Report', 'questionnaire_doc_type': 'Report Injury or Illness', 'file_upload': 'Upload Case Supporting Documentation'}
supervQuestion = 'Animal Exposure Questionnaire (Supervisor Notification)'
conditional = 'Influenza Vaccination Authorization Form'
uploadFile = 'Upload Medical Certification Form Supporting Documentation'
mmiModules = ['Allergies', 'Immunizations', 'Medications']
attrs = ['id', 'name', 'title', 'class', 'placeholder']
patFirst = 'Fredrick'
patLast = 'Anderson'

def main(d, WCURL):
    default_resolution = d.driverOptions.resolution
    wd = d.getWebDriver()
    wait = WebDriverWait(wd, 10)
    longWait = WebDriverWait(wd, 60)
    isEHSystem = int( # querying db is much faster than breaking frameset and checking JS var
        d.miedb.dbQuery(
            '''
                SELECT value
                FROM system_settings
                WHERE item='Enterprise Health'
            '''
        ).getRes()[0]['value']
    )

    pat_id = d.miedb.dbQuery(
        '''
            SELECT pat_id
            FROM patients
            WHERE last_name='Hart'
            AND chart_online='1'
        '''
    ).getRes()[0]['pat_id']

    harris_id = d.miedb.dbQuery(
        '''
            SELECT pat_id
            FROM patients
            WHERE last_name='Harris'
            AND chart_online='1'
            LIMIT 1
        '''
    ).getRes()[0]['pat_id']

    anderson_id = d.miedb.dbQuery(
        '''
            SELECT pat_id
            FROM patients
            WHERE last_name='Anderson'
            LIMIT 1
        '''
    ).getRes()[0]['pat_id']

    user_id = d.miedb.dbQuery(
        '''
            SELECT user_id
            FROM users
            WHERE last_name = 'Selenium'
        '''
    ).getRes()[0]['user_id']

    class MMI:
        def immunizations(self, modName):
            immuneMod = eleFound('css_selector', '.active .' + modName)

            if immuneMod:
                d.startSection('MMI - Immunizations')
                # add an immunization
                d.startSection('Adding an immunization')
                d.clickElement(xpath='//button[text()="Add an immunization"]')
                d.enterAutocomplete('injac_jsname', 'Hep B,', 0, 'Hep B, adolescent or pediatric')
                d.clickElement(id='MMI_date_of_immunization_link')
                d.clickElement(xpath='//div[@id="MMI_date_of_immunization_cal"]//button[text()="1"]')
                d.enterFormData('Adding an immunization. This is a comment field.', name='MMI_comment')
                d.clickElement(xpath='//button[text()="Add an immunization"]/..//button[contains(@class, "portal-save-btn")]')

                wait.until(
                    EC.invisibility_of_element_located(
                        (By.XPATH, '//button[text()="Add an immunization"]/..//button[contains(@class, "portal-save-btn")]')
                    )
                )

                d.endSection() # END adding an immunization

                d.startSection('Editing an immunization')
                d.clickElement(xpath='//span[contains(text(), "influenza")]/../../../following-sibling::div//button')
                d.clickElement(id='immunization_date_edit_link')
                waitClick('xpath', '//div[@id="immunization_date_edit_cal"]//button[text()="1"]')
                d.enterFormData('Editing an Immunization. This is a reaction field.', name='reaction')
                findClick('css_selector', '.' + modName + ' .mmi-editTemplate .portal-save-btn')

                wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, '.' + modName + ' .mmi-editTemplate .portal-save-btn')
                    )
                )

                d.endSection() # END adding an immunization

                d.startSection('Verify Immunization')
                d.verifyElementPresent(xpath='//span[text()="Adding an immunization. This is a comment field."]')
                d.verifyElementPresent(xpath='//span[text()="Editing an Immunization. This is a reaction field."]')
                d.endSection() # END adding an immunization

                d.endSection() # END MMI - Immunizations

        def medications(self, modName):
            medMod = eleFound('css_selector', '.active .' + modName)

            if medMod:
                # add a med
                echo('Adding a medication')
                try:
                    clickEle(medMod.find_element_by_xpath('//button[text()="Add a medication"]'))
                    d.enterAutocomplete('medlistAdd_jsname', 'Amb', 0, 'Ambien')
                    resizeWin()
                    d.clickElement(id='dosageAdd')
                    waitClick('id', 'MMI_start_date_link')
                    d.clickElement(xpath='//div[@id="MMI_start_date_cal"]//button[text()="2"]')
                    addDir = medMod.find_element_by_name('MMI_directions')
                    addDir.clear()
                    addDir.send_keys('Adding a directive. These are your directions.')
                    addDoc = medMod.find_element_by_name('MMI_physician')
                    addDoc.clear()
                    addDoc.send_keys('Adding a physician. This is the physician field.')
                    clickEle(medMod.find_element_by_class_name('portal-save-btn'))

                    # edit a med
                    echo('Editing a medication')
                    # Ibuprofen is a unique med, may prevent issues by choosing a unique row
                    waitClick('xpath', '//span[contains(text(), "Ibuprofen")]/../../../following-sibling::div//button', expect=('id', 'mmiMedsEdit'))

                    # get edit container
                    medEdit = medMod.find_element_by_id('mmiMedsEdit')

                    waitClick('id', 'MMI_stopped_link')
                    d.clickElement(xpath='//div[@id="MMI_stopped_cal"]//button[text()="2"]')
                    editDir = medEdit.find_element_by_name('MMI_directions')
                    editDir.clear()
                    editDir.send_keys('Editing a directive. These are your directions.')
                    editDoc = medEdit.find_element_by_name('MMI_physician')
                    editDoc.clear()
                    editDoc.send_keys('Editing a physician. This is the physician field.')
                    clickEle(medEdit.find_element_by_class_name('mmi-save-btn'))
                except AttributeError:
                    from selenium.webdriver.common.by import By
                    clickEle(medMod.find_element(By.XPATH, '//button[text()="Add a medication"]'))
                    d.enterAutocomplete('medlistAdd_jsname', 'Amb', 0, 'Ambien')
                    resizeWin()
                    d.clickElement(id='dosageAdd')
                    waitClick('id', 'MMI_start_date_link')
                    d.clickElement(xpath='//div[@id="MMI_start_date_cal"]//button[text()="2"]')
                    addDir = medMod.find_element(By.NAME, 'MMI_directions')
                    addDir.clear()
                    addDir.send_keys('Adding a directive. These are your directions.')
                    addDoc = medMod.find_element(By.NAME, 'MMI_physician')
                    addDoc.clear()
                    addDoc.send_keys('Adding a physician. This is the physician field.')
                    clickEle(medMod.find_element(By.CLASS_NAME, 'portal-save-btn'))
    
                    # edit a med
                    echo('Editing a medication')
                    # Ibuprofen is a unique med, may prevent issues by choosing a unique row
                    waitClick('xpath', '//span[contains(text(), "Ibuprofen")]/../../../following-sibling::div//button', expect=('id', 'mmiMedsEdit'))
    
                    # get edit container
                    medEdit = medMod.find_element(By.ID, 'mmiMedsEdit')
    
                    waitClick('id', 'MMI_stopped_link')
                    d.clickElement(xpath='//div[@id="MMI_stopped_cal"]//button[text()="2"]')
                    editDir = medEdit.find_element(By.NAME, 'MMI_directions')
                    editDir.clear()
                    editDir.send_keys('Editing a directive. These are your directions.')
                    editDoc = medEdit.find_element(By.NAME, 'MMI_physician')
                    editDoc.clear()
                    editDoc.send_keys('Editing a physician. This is the physician field.')
                    clickEle(medEdit.find_element(By.CLASS_NAME, 'mmi-save-btn'))
                wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, modName + ' .mmi-editTemplate .portal-save-btn')
                    )
                )

                d.verifyElementPresent(xpath='//span[text()="Adding a directive. These are your directions."]')
                d.verifyElementPresent(xpath='//span[text()="Adding a physician. This is the physician field."]')
                d.verifyElementPresent(xpath='//span[text()="Editing a directive. These are your directions."]')
                d.verifyElementPresent(xpath='//span[text()="Editing a physician. This is the physician field."]')

        def allergies(self, modName):
            agyMod = eleFound('css_selector', '.active .' + modName)

            if agyMod:
                # add a allergy
                echo('Adding an allergy')
                try:
                    clickEle(agyMod.find_element_by_xpath('//button[text()="Add an allergy"]'))
                    d.enterAutocomplete('addagy_medacf_jsname', 'Pean', 0, 'PEANUT (manually screen)')
                    addReaction = agyMod.find_element_by_name('MMI_reaction')
                    addReaction.clear()
                    addReaction.send_keys('Adding a reaction. This is a reaction.')
                    addAllergy = agyMod.find_element_by_name('MMI_comment')
                    addAllergy.clear()
                    addAllergy.send_keys('Adding an allergy comment. This is a comment.')
                    clickEle(agyMod.find_element_by_class_name('portal-save-btn'))

                    # edit a allergy
                    echo('Editing an allergy')
                    waitClick('css_selector', '.active .' + modName + ' .mmi-list-last .mmi-img-wrap')

                    # get edit container
                    agyEdit = agyMod.find_element_by_id('mmiAllergiesEdit')

                    editReaction = agyEdit.find_element_by_name('reaction')
                    wait.until(EC.element_to_be_clickable((By.XPATH, getEleXPATH(editReaction))))
                    editReaction.clear()
                    editReaction.send_keys('Editing an allergy reaction. This is a reaction.')
                    editComment = agyEdit.find_element_by_name('comments')
                    editComment.clear()
                    editComment.send_keys('Editing an allergy comment. This is a comment.')
                    clickEle(agyEdit.find_element_by_class_name('mmi-save-btn'))
                except AttributeError:
                    from selenium.webdriver.common.by import By
                    clickEle(agyMod.find_element(By.XPATH, '//button[text()="Add an allergy"]'))
                    d.enterAutocomplete('addagy_medacf_jsname', 'Pean', 0, 'PEANUT (manually screen)')
                    addReaction = agyMod.find_element(By.NAME, 'MMI_reaction')
                    addReaction.clear()
                    addReaction.send_keys('Adding a reaction. This is a reaction.')
                    addAllergy = agyMod.find_element_b(By.NAME, 'MMI_comment')
                    addAllergy.clear()
                    addAllergy.send_keys('Adding an allergy comment. This is a comment.')
                    clickEle(agyMod.find_element(By.CLASS_NAME, 'portal-save-btn'))

                    # edit a allergy
                    echo('Editing an allergy')
                    waitClick('css_selector', '.active .' + modName + ' .mmi-list-last .mmi-img-wrap')

                    # get edit container
                    agyEdit = agyMod.find_element(By.ID, 'mmiAllergiesEdit')

                    editReaction = agyEdit.find_element(By.NAME, 'reaction')
                    wait.until(EC.element_to_be_clickable((By.XPATH, getEleXPATH(editReaction))))
                    editReaction.clear()
                    editReaction.send_keys('Editing an allergy reaction. This is a reaction.')
                    editComment = agyEdit.find_element(By.NAME, 'comments')
                    editComment.clear()
                    editComment.send_keys('Editing an allergy comment. This is a comment.')
                    clickEle(agyEdit.find_element(By.CLASS_NAME, 'mmi-save-btn'))

                wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, modName + ' .mmi-editTemplate .portal-save-btn')
                    )
                )

                d.verifyElementPresent(xpath='//span[text()="Adding a reaction. This is a reaction."]')
                d.verifyElementPresent(xpath='//span[text()="Adding an allergy comment. This is a comment."]')
                d.verifyElementPresent(xpath='//span[text()="Editing an allergy reaction. This is a reaction."]')
                d.verifyElementPresent(xpath='//span[text()="Editing an allergy comment. This is a comment."]')

    """
    Performs a standard workflow for using the unified patient portal:
    ****
    """

    # Generic functions
    def escapeHTML(html):
        try:
            return cgi.escape(str(html))
        except AttributeError:
            import html
            return html.escape(str(html))

    def echo(msg, val='', comment='', status=''):
        # reportCommandStatus(
            #'getElementByID',
            #'id=%s' %id,
            #None,
            #'',
            #'Found [%d] elements with the given id [%s]. According to the HTML specification, ids MUST be unique' %(l, id)
        #)
        d.reportCommandStatus(escapeHTML(msg),val,True,comment,status)

    def fail(msg, val='', comment='', status=''):
        d.reportCommandStatus(escapeHTML(msg),val,False,comment,status)
        screen(escapeHTML(msg).replace('\n','')[0:20])

    def roundUp(num, multiplier):
        return int(math.ceil(num / float(multiplier))) * int(multiplier)

    def blurBox():
        d.scrollTo() # reset scroll position after win resize
        jQuery = wd.execute_script('return +Boolean(window.jQuery)')

        if int(jQuery):
            wd.execute_async_script( # inject element useful for blurring focused element
                '''
                    var blurBox = jQuery(
                    '<div id="blurBox" style="position:fixed;width:10px;height:10px;z-index:9999;bottom:0;left:0;">'
                    ).insertBefore('body');
                '''
            )

            # use webdriver to click blurBox, avoid using mie click methods which output messages to the results page
            d.getElement(id='blurBox').click()
            wd.execute_script('blurBox.remove()')

            wd.execute_script( # inject element useful for blurring focused element
                '''
                    return jQuery(document.activeElement).blur()
                '''
            )

    # def blurBox():
    #     d.scrollTo() # reset scroll position after win resize
    #     jQuery = wd.execute_script('return +Boolean(window.jQuery)')

    #     if int(jQuery):
    #         wd.execute_async_script( # inject element useful for blurring focused element
    #             '''
    #                 var blurBox = jQuery(
    #                 '<div id="blurBox" style="position:fixed;width:10px;height:10px;z-index:9999;bottom:0;left:0;">'
    #                 ).insertBefore('body');
    #                 arguments[0]()
    #             ''',
    #             lambda: _finishBlurBox()
    #         )
    # def _finishBlurBox():
    #         # use webdriver to click blurBox, avoid using mie click methods which output messages to the results page
    #         d.getElement(id='blurBox').click()
    #         wd.execute_script('blurBox.remove()')

    #         wd.execute_script( # inject element useful for blurring focused element
    #             '''
    #                 return jQuery(document.activeElement).blur()
    #             '''
    #         )

    def screen(title='', width=default_resolution[0], widgetWait=False):
        defaultHeight = default_resolution[1]

        if width != default_resolution[0]:
            echo('Breakpoint width: ' + str(width) + 'px')

        if widgetWait:
            d.pause(10)

        # prepare for screenshot. resize window to full length of body. scroll window to top of page
        resetWinSize(width, defaultHeight) # set the new resolution
        wd.set_window_size(width, defaultHeight) # resize the window to the new resolution
        # set the new window height to the calculated height of the page body
        # round up to the nearest ceiling for consistent screenshots
        bodyHeight = wd.execute_script('return (window.jQuery ? jQuery(document).height() : document.documentElement.getBoundingClientRect().height)') # the calculated height can be slightly different from run to run -- hence the need for rounding
        roundedHeight = roundUp(bodyHeight, roundCeil)

        # some screenshots will be slightly less tall from run to run despite consistent body content. The logic below normalizes screenshot heights
        if (roundedHeight - bodyHeight) <= roundDiffFactor: # if body height is slightly less than the rounding ceiling, force it up to the next ceiling
            roundedHeight = roundUp((bodyHeight + roundDiffFactor), roundCeil)

        resetWinSize(width, roundedHeight)

        if title:
            # take screenshot and reset window size
            d.pause(1)
            blurBox()
            d.screenshot(title)

        resetWinSize()

    def resizeWin():
        screen()

    def isList(dataObj):
        return type(dataObj) == list

    def employeeHome():
        if 'employeeHome' not in CGIVars:
            d.navigate(WCURL.OMNISCOPE + '&use_portal=0')
            CGIVars['employeeHome'] = d.getElement(xpath='//div[@id="access-wrapper"]//a[contains(text(), "Provider Portal")]').get_attribute('href')

        wd.get(CGIVars['employeeHome'])

    def eleFound(method=False, selector=False, anc=False, wait=False):
        try:
            if method and type(method) == str:
                byAttr = getattr(By, method.upper())

                if wait:
                    longWait.until(EC.element_to_be_clickable((byAttr, selector)))

                return (anc if anc else wd).find_element(byAttr, selector)
            else:
                return False
        except Exception as err:
            return False

    def elesFound(method=False, selector=False, anc=False, wait=False):
        try:
            if method and type(method) == str:
                byAttr = getattr(By, method.upper())

                if wait:
                    longWait.until(EC.element_to_be_clickable((byAttr, selector)))

                return (anc if anc else wd).find_elements(byAttr, selector)
            else:
                return False
        except Exception as err:
            return False

    def clickEle(ele=False, anc=False, hideMsg=False):
        # this is a web element
        eleXPATH = getEleXPATH(ele)
        msgVal = ''

        for attr in attrs:
            getAttr = ele.get_attribute(attr)

            if getAttr:
                msgVal += (attr + '=\'' + getAttr + '\' ')

        if ele.text:
            msgVal += 'text=\'' + ele.text + '\''

        msgVal = (msgVal if msgVal else 'xpath=\'' + eleXPATH + '\'')

        try:
            ele.click()

            if not hideMsg:
                echo('clickElement', msgVal)
        except Exception as e:
            try:
                waitEle = eleFound('xpath', eleXPATH, anc)

                if waitEle:
                    waitEle.click()

                    if not hideMsg:
                        echo('clickElement', msgVal)

                    return waitEle

            except Exception as w:
                fail('clickElement', msgVal)
                fail(str(w))

                return False

    def getEle(method=False, selector=False, anc=False):
        return eleFound(method=method, selector=selector, anc=anc)

    def findClick(method=False, selector=False, anc=False):
        found = eleFound(method, selector, anc)
        echo('clickElement', selector)
        found.click()

        return found

    def wordLib(senLen=0, startIdx=0, page=''):
        wordLib = ''
        sentance = ''

        if page:
            d.navigate(page)
        # create a word library
        try:
            for rows in wd.find_elements_by_css_selector('label,p,h2'):
                wordLib += rows.text + ' '
        except AttributeError:
            from selenium.webdriver.common.by import By
            for rows in wd.find_elements_by(By.CSS_SELECTOR, 'label,p,h2'):
                wordLib += rows.text + ' '


        wordLib = wordLib.split() # split on space

        for word in range(startIdx, senLen):
            sentance += wordLib[word] + ' '

        if senLen > 0:
            return sentance
        else:
            return wordLib

    def getEleXPATH(ele):
        xpath = wd.execute_script('''
            function getElementXPath(element) {
            if (element && element.id)
            return '//*[@id="' + element.id + '"]';
            else
            return getElementTreeXPath(element);
            }

            function getElementTreeXPath(element) {
            var paths = [];

            // Use nodeName (instead of localName) so namespace prefix is included (if any).
            for (; element && element.nodeType == 1; element = element.parentNode) {
            var index = 0;
            for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
            // Ignore document type declaration.
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
            continue;

            if (sibling.nodeName == element.nodeName)
            ++index;
            }

            var tagName = element.nodeName.toLowerCase();
            var pathIndex = (index ? "[" + (index+1) + "]" : "");
            paths.splice(0, 0, tagName + pathIndex);
            }

            return paths.length ? "/" + paths.join("/") : null;
            }

            return getElementTreeXPath(arguments[0]);
        ''', ele)

        return xpath

    def css2xpath(css):
        return getEleXPATH(getEle('css_selector', css))

    def centerClick(ele):
        eleSize = ele.size

        # click middle and center of element
        ActionChains(wd).move_to_element_with_offset(ele, int(eleSize['height'] / 2), int(eleSize['width'] / 2)).click().perform()

        return ele

    def waitClick(method, selector, anc='', expect='', invisible='', refresh=False):
        try:
            def doClick():
                mattr = getattr(By, method.upper()) # method (selection) attribute
                longWait.until(EC.element_to_be_clickable((mattr, selector)))
                found = (anc if anc else wd).find_element(mattr, selector)
                page = d.getElement(xpath='//body')

                try:
                    clickEle(found)
                except Exception as e:
                    centerClick(found)

                if refresh:
                    wait.until(
                        staleness_of(page)
                    )

                if invisible:
                    wait.until(
                        EC.invisibility_of_element_located(
                            invisible
                        )
                    )

            if expect:
                for itr in range(0, 10):
                    expectFound = eleFound(getattr(By, expect[0].upper()), expect[1])

                    if not expectFound or not expectFound.is_displayed():
                        doClick()
            else:
                doClick()
        except Exception as err:
            if not expect:
                fail('waitClick function caught an exception: ' + escapeHTML(err))
                screen('Fullscreen error capture')

    def eleByIdx(idx, eles):
        for ele in eles:
            if eles.index(ele) == idx:
                return ele

    def dismissAppTimeout():
        d.pause(3)
        if eleFound('id', 'log-extend-btn') and eleFound('id', 'log-extend-btn').is_displayed():
            d.clickElement(id='log-extend-btn')

    def mmiEval(modules):
        dismissAppTimeout()
        def evalMod(mod):
            dismissAppTimeout()
            modAttr = mod.lower()

            if hasattr(MMI, modAttr):
                modInst = MMI()
                modFunc = getattr(modInst, modAttr)
                dismissAppTimeout()

                if callable(modFunc):
                    dismissAppTimeout()
                    modFunc(mod)
                    dismissAppTimeout()

        if modules:
            dismissAppTimeout()
            if isList(modules):
                dismissAppTimeout()
                for mod in modules:
                    dismissAppTimeout()
                    evalMod(mod)
                    dismissAppTimeout()
            else:
                dismissAppTimeout()
                evalMod(modules)
                dismissAppTimeout()

    def getClasses(ele):
        return ele.get_attribute('class').split(' ')

    def hasClass(ele, classNames):
        allClasses = getClasses(ele)

        if type(classNames) == str:
            classNames = [classNames]

        for cssClass in classNames:
            if cssClass in allClasses:
                return True

    def answerQuestions(responsiveBreakpoint=True, mmi=True, fromPage='', dismissAppPopup=False):
        dismissAppTimeout()
        d.screenshot('pre_wait_until_ec_visibility_of_element_located_by_id_questionnair_wrapper_in_answerquestions')
        wait.until(
            EC.visibility_of_element_located(
                (By.ID,'questionnaire_wrapper')
            )
        )

        d.screenshot('pre_pagecount_in_answerquestions')
        pageCount = 1
        d.screenshot('pre_questName_getElement_main-heading_text_in_answerquestions')
        questName = d.getElement(id='main-heading').text
        d.screenshot('pre_pages_wd_find_elements_by_css_selector_page_wrapper_in_answerquestions')
        try:
            pages = wd.find_elements_by_css_selector('.page_wrapper')
        except AttributeError:
            from selenium.webdriver.common.by import By
            pages = wd.find_elements_by(By.CSS_SELECTOR, '.page_wrapper')

        def itrHandler(itr, lst):
            lstLen = (lst if type(lst) == int else len(lst)) - 1

            return itr if itr <= lstLen else 0

        def answerPage(required=False):
            yesNoItr = radioItr = textItr = listMultiply = 0
            dateItr = 0
            timeItr = 0
            library = wordLib() # word library from text in questionnaire
            tokenReq = False

            # yes/no rows
            try:
                for questRow in wd.find_elements_by_css_selector('.active .portal-row-container'):
                    if dismissAppPopup:
#                        d.screenshot('pre_if_dismissAppPopup')
                        dismissAppTimeout()
#                        d.screenshot('post_if_dismissAppPopup')

                    if questRow.is_displayed():
                        if hasClass(questRow, 'required'):
                            if not tokenReq and not required:
                                # skip required row
#                                d.screenshot('pre_if_not_tokenReq')
                                tokenReq = True
#                                d.screenshot('post_if_not_tokenReq')
                                continue

                        # Skip non-required fields if we're need to answer a required question
                        elif required:
                            continue

                        # Yes/No Question
                        if hasClass(questRow, 'yes_no_list'):
                            if yesNoItr % 2 == 0:
#                                d.screenshot('pre_if_yesNoItr_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                clickEle(questRow.find_element_by_css_selector('input[value="Yes"]')) # verify 508 accessability
#                                d.screenshot('post_if_yesNoItr_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                dismissAppTimeout()
                            else:
#                                d.screenshot('pre_else_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                clickEle(questRow.find_element_by_css_selector('input[value="No"]')) # verify 508 accessability
#                                d.screenshot('post_else_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                dismissAppTimeout()

                            yesNoItr += 1

                        # Radio Question
                        elif hasClass(questRow, ['radio_list', 'radio_horiz_list']):
                            if eleFound('css_selector', 'input', questRow):
                                radioFields = questRow.find_elements_by_css_selector('input')
                                radioItr = itrHandler(radioItr, radioFields)
#                                d.screenshot('pre_if_eleFound_css_selector_input_clickEle_eleByIdx_radioItr__radioFields__')
                                clickEle(eleByIdx(radioItr, radioFields))
#                                d.screenshot('post_if_eleFound_css_selector_input_clickEle_eleByIdx_radioItr__radioFields__')
                                dismissAppTimeout()

                                radioItr += 1

                            if eleFound('css_selector', 'select', questRow):
                                # click select box then choose option
                                opts = centerClick(questRow.find_element_by_css_selector('select')).find_elements_by_css_selector('option')
                                radioItr = itrHandler(radioItr, opts)
#                                d.screenshot('pre_if_eleFound_css_selector_select_clickEle_eleByIdx_radioItr__opts__')
                                clickEle(eleByIdx(radioItr, opts))
#                                d.screenshot('post_if_eleFound_css_selector_select_clickEle_eleByIdx_radioItr__opts__')
                                dismissAppTimeout()

                                radioItr += 1

                        # Text question
                        elif hasClass(questRow, ['text_type', 'textarea_type']):
                            libLen = len(library) - 1
                            fieldTxt = ''

                            for wordIdx in range(listMultiply, listMultiply + 5):
                                if not wordIdx in range(0, libLen):
#                                    d.screenshot('pre_if_not_wordIdx_in_range_0__libLen_')
                                    library.append(library[wordIdx - libLen])
#                                    d.screenshot('post_if_not_wordIdx_in_range_0__libLen_')

                                fieldTxt += library[wordIdx] + ' '

#                            d.screenshot('pre_questRow_find_element_by_css_selector__input_type__text____textarea___send_keys_fieldTxt_')
                            questRow.find_element_by_css_selector('input[type="text"], textarea').send_keys(fieldTxt)
#                            d.screenshot('post_questRow_find_element_by_css_selector__input_type__text____textarea___send_keys_fieldTxt_')
                            listMultiply = textItr * 5
                            dismissAppTimeout()
                            textItr += 1

                        elif hasClass(questRow, 'file_type'):
                            fileEle = questRow.find_element_by_css_selector('input[type="file"]')

                            # Make file input visible so that MIE Driver can perform file upload
                            dismissAppTimeout()
#                            d.screenshot('pre_d_runJS__return_jQuery_arguments_0___css__opacity____1______fileEle_')
                            d.runJS('return jQuery(arguments[0]).css("opacity", "1");', fileEle)
#                            d.screenshot('post_d_runJS__return_jQuery_arguments_0___css__opacity____1______fileEle_')
                            d.enterFormData( '7600A.pdf', id=fileEle.get_attribute('id') )
#                            d.screenshot('post_d_enterFormData___7600A_pdf___id_fileEle_get_attribute__id____')
                            dismissAppTimeout()

                            # Reset file input styling
#                            d.screenshot('pre_d_runJS__return_jQuery_arguments_0___css__opacity__________fileEle_')
                            d.runJS('return jQuery(arguments[0]).css("opacity", "");', fileEle)
#                            d.screenshot('post_d_runJS__return_jQuery_arguments_0___css__opacity__________fileEle_')
                            dismissAppTimeout()

                        elif hasClass(questRow, ['date_type', 'datetime_type']):
                            dateField = questRow.find_element_by_css_selector('input[type="date"]')
                            timeField = eleFound('css_selector', '.datetime_type input.time-input', questRow)

                            dismissAppTimeout()
                            if dateItr % 2 == 0:
#                                d.screenshot('pre_if_dateItr___2____0__dateField_send_keys__09252013__')
                                dateField.send_keys('09252013')
#                                d.screenshot('post_if_dateItr___2____0__dateField_send_keys__09252013__')

                                if timeField:
#                                    d.screenshot('pre_if_timeField_timeField_send_keys__03_16AM__')
                                    timeField.send_keys('03:16AM')
#                                    d.screenshot('post_if_timeField_timeField_send_keys__03_16AM__')
                            else:
#                                d.screenshot('pre_else_dateField_send_keys__03142015__')
                                dateField.send_keys('03142015')
#                                d.screenshot('post_else_dateField_send_keys__03142015__')

                                if timeField:
#                                    d.screenshot('pre_else_if_timeField__timeField_send_keys__10_15PM__')
                                    timeField.send_keys('10:15PM')
#                                    d.screenshot('post_else_if_timeField__timeField_send_keys__10_15PM__')
                                    d.screenshot()
                            dismissAppTimeout()

                            dateItr += 1

                        elif hasClass(questRow, 'time_type'):
                            dismissAppTimeout()
#                            d.screenshot('pre_elif_hasClass_questRow___time_type____timeField___questRow_find_element_by_css_selector__input__')
                            timeField = questRow.find_element_by_css_selector('input')
#                            d.screenshot('post_elif_hasClass_questRow___time_type____timeField___questRow_find_element_by_css_selector__input__')
                            dismissAppTimeout()

                            if timeItr % 2 == 0:
#                                d.screenshot('pre_if_timeItr___2____0__timeField_send_keys__11_16AM__')
                                timeField.send_keys('11:16AM')
#                                d.screenshot('post_if_timeItr___2____0__timeField_send_keys__11_16AM__')
                            else:
#                                d.screenshot('pre_else_timeField_send_keys__07_47PM__')
                                timeField.send_keys('07:47PM')
#                                d.screenshot('post_else_timeField_send_keys__07_47PM__')

                            timeItr += 1
                            dismissAppTimeout()

                        # Required questions have been answered
                        if hasClass(questRow, 'required') and required:
                            break
            except AttributeError:
                from selenium.webdriver.common.by import By
                for questRow in wd.find_elements_by(By.CSS_SELECTOR, '.active .portal-row-container'):
                    if dismissAppPopup:
#                        d.screenshot('pre_if_dismissAppPopup')
                        dismissAppTimeout()
#                        d.screenshot('post_if_dismissAppPopup')

                    if questRow.is_displayed():
                        if hasClass(questRow, 'required'):
                            if not tokenReq and not required:
                                # skip required row
#                                d.screenshot('pre_if_not_tokenReq')
                                tokenReq = True
#                                d.screenshot('post_if_not_tokenReq')
                                continue

                        # Skip non-required fields if we're need to answer a required question
                        elif required:
                            continue

                        # Yes/No Question
                        if hasClass(questRow, 'yes_no_list'):
                            if yesNoItr % 2 == 0:
#                                d.screenshot('pre_if_yesNoItr_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                clickEle(questRow.find_element(By.CSS_SELECTOR, 'input[value="Yes"]')) # verify 508 accessability
#                                d.screenshot('post_if_yesNoItr_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                dismissAppTimeout()
                            else:
#                                d.screenshot('pre_else_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                clickEle(questRow.find_element(By.CSS_SELECTOR, 'input[value="No"]')) # verify 508 accessability
#                                d.screenshot('post_else_clickEle_questRow_find_element_by_css_selector__input_value__Yes_______verify_508_accessability')
                                dismissAppTimeout()

                            yesNoItr += 1

                        # Radio Question
                        elif hasClass(questRow, ['radio_list', 'radio_horiz_list']):
                            if eleFound('css_selector', 'input', questRow):
                                radioFields = questRow.find_elements_by(By.CSS_SELECTOR, 'input')
                                radioItr = itrHandler(radioItr, radioFields)
#                                d.screenshot('pre_if_eleFound_css_selector_input_clickEle_eleByIdx_radioItr__radioFields__')
                                clickEle(eleByIdx(radioItr, radioFields))
#                                d.screenshot('post_if_eleFound_css_selector_input_clickEle_eleByIdx_radioItr__radioFields__')
                                dismissAppTimeout()

                                radioItr += 1

                            if eleFound('css_selector', 'select', questRow):
                                # click select box then choose option
                                opts = centerClick(questRow.find_element(By.CSS_SELECTOR, 'select')).find_elements_by(By.CSS_SELECTOR, 'option')
                                radioItr = itrHandler(radioItr, opts)
#                                d.screenshot('pre_if_eleFound_css_selector_select_clickEle_eleByIdx_radioItr__opts__')
                                clickEle(eleByIdx(radioItr, opts))
#                                d.screenshot('post_if_eleFound_css_selector_select_clickEle_eleByIdx_radioItr__opts__')
                                dismissAppTimeout()

                                radioItr += 1

                        # Text question
                        elif hasClass(questRow, ['text_type', 'textarea_type']):
                            libLen = len(library) - 1
                            fieldTxt = ''

                            for wordIdx in range(listMultiply, listMultiply + 5):
                                if not wordIdx in range(0, libLen):
#                                    d.screenshot('pre_if_not_wordIdx_in_range_0__libLen_')
                                    library.append(library[wordIdx - libLen])
#                                    d.screenshot('post_if_not_wordIdx_in_range_0__libLen_')

                                fieldTxt += library[wordIdx] + ' '

#                            d.screenshot('pre_questRow_find_element_by_css_selector__input_type__text____textarea___send_keys_fieldTxt_')
                            questRow.find_element(By.CSS_SELECTOR, 'input[type="text"], textarea').send_keys(fieldTxt)
#                            d.screenshot('post_questRow_find_element_by_css_selector__input_type__text____textarea___send_keys_fieldTxt_')
                            listMultiply = textItr * 5
                            dismissAppTimeout()
                            textItr += 1

                        elif hasClass(questRow, 'file_type'):
                            fileEle = questRow.find_element(By.CSS_SELECTOR, 'input[type="file"]')

                            # Make file input visible so that MIE Driver can perform file upload
                            dismissAppTimeout()
#                            d.screenshot('pre_d_runJS__return_jQuery_arguments_0___css__opacity____1______fileEle_')
                            d.runJS('return jQuery(arguments[0]).css("opacity", "1");', fileEle)
#                            d.screenshot('post_d_runJS__return_jQuery_arguments_0___css__opacity____1______fileEle_')
                            d.enterFormData( '7600A.pdf', id=fileEle.get_attribute('id') )
#                            d.screenshot('post_d_enterFormData___7600A_pdf___id_fileEle_get_attribute__id____')
                            dismissAppTimeout()

                            # Reset file input styling
#                            d.screenshot('pre_d_runJS__return_jQuery_arguments_0___css__opacity__________fileEle_')
                            d.runJS('return jQuery(arguments[0]).css("opacity", "");', fileEle)
#                            d.screenshot('post_d_runJS__return_jQuery_arguments_0___css__opacity__________fileEle_')
                            dismissAppTimeout()

                        elif hasClass(questRow, ['date_type', 'datetime_type']):
                            dateField = questRow.find_element(By.CSS_SELECTOR, 'input[type="date"]')
                            timeField = eleFound('css_selector', '.datetime_type input.time-input', questRow)

                            dismissAppTimeout()
                            if dateItr % 2 == 0:
#                                d.screenshot('pre_if_dateItr___2____0__dateField_send_keys__09252013__')
                                dateField.send_keys('09252013')
#                                d.screenshot('post_if_dateItr___2____0__dateField_send_keys__09252013__')

                                if timeField:
#                                    d.screenshot('pre_if_timeField_timeField_send_keys__03_16AM__')
                                    timeField.send_keys('03:16AM')
#                                    d.screenshot('post_if_timeField_timeField_send_keys__03_16AM__')
                            else:
#                                d.screenshot('pre_else_dateField_send_keys__03142015__')
                                dateField.send_keys('03142015')
#                                d.screenshot('post_else_dateField_send_keys__03142015__')

                                if timeField:
#                                    d.screenshot('pre_else_if_timeField__timeField_send_keys__10_15PM__')
                                    timeField.send_keys('10:15PM')
#                                    d.screenshot('post_else_if_timeField__timeField_send_keys__10_15PM__')
                                    d.screenshot()
                            dismissAppTimeout()

                            dateItr += 1

                        elif hasClass(questRow, 'time_type'):
                            dismissAppTimeout()
#                            d.screenshot('pre_elif_hasClass_questRow___time_type____timeField___questRow_find_element_by_css_selector__input__')
                            timeField = questRow.find_element(By.CSS_SELECTOR, 'input')
#                            d.screenshot('post_elif_hasClass_questRow___time_type____timeField___questRow_find_element_by_css_selector__input__')
                            dismissAppTimeout()

                            if timeItr % 2 == 0:
#                                d.screenshot('pre_if_timeItr___2____0__timeField_send_keys__11_16AM__')
                                timeField.send_keys('11:16AM')
#                                d.screenshot('post_if_timeItr___2____0__timeField_send_keys__11_16AM__')
                            else:
#                                d.screenshot('pre_else_timeField_send_keys__07_47PM__')
                                timeField.send_keys('07:47PM')
#                                d.screenshot('post_else_timeField_send_keys__07_47PM__')

                            timeItr += 1
                            dismissAppTimeout()

                        # Required questions have been answered
                        if hasClass(questRow, 'required') and required:
                            break
        for page in pages:
            answerPage()

            if mmi:
                dismissAppTimeout()
#                d.screenshot('pre_if_mmi__mmiEval_mmiModules___check_for_MMI_modules')
                mmiEval(mmiModules) # check for MMI modules
#                d.screenshot('post_if_mmi__mmiEval_mmiModules___check_for_MMI_modules')
                dismissAppTimeout()

            if pageCount == 1:
                dismissAppTimeout()
#                d.screenshot('pre_if_pageCount____1__ssName___questName_______str_pageCount_')
                ssName = questName + '_' + str(pageCount)
#                d.screenshot('post_if_pageCount____1__ssName___questName_______str_pageCount_')
                dismissAppTimeout()

                if dismissAppPopup:
#                    d.screenshot('pre_if_pageCount____1__if_dismissAppPopup__dismissAppTimeout__')
                    dismissAppTimeout()
#                    d.screenshot('post_if_pageCount____1__if_dismissAppPopup__dismissAppTimeout__')

                if responsiveBreakpoint:
#                    d.screenshot('pre_if_pageCount____1__if_responsiveBreakpoint__multiScreen_ssName_')
                    dismissAppTimeout()
                    multiScreen(ssName)
                    dismissAppTimeout()
#                    d.screenshot('post_if_pageCount____1__if_responsiveBreakpoint__multiScreen_ssName_')
                else:
#                    d.screenshot('pre_if_pageCount____1__else_screen_ssName_')
                    dismissAppTimeout()
                    screen(ssName)
#                    d.screenshot('post_if_pageCount____1__else_screen_ssName_')
                dismissAppTimeout()


#            d.screenshot('pre_d_clickElement_xpath____button_contains__class___form-save___and__value__SUBMIT____')
#            if d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]'), expected_return=True, timeout=90):
#                d.clickElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]')
#            elif d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]'), expected_return=True, timeout=90):
#            d.clickElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]')
            d.clickElement(xpath='//button[contains(@class, "form-save") or contains(@id, "form-save")]')

            d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=True, timeout=90)
            d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=False, timeout=90)
#            waitClick('css_selector', '.form-save')
#            waitClick('css_selector', '.active .form-save')
#            longWait.until(wd.find_elements_by_css_selector('.active .form-save'))
#            d.screenshot('post_d_clickElement_xpath____button_contains__class___form-save___and__value__SUBMIT____')

            dismissAppTimeout()
#            d.screenshot('pre_reqModal___eleFound__id____required-questions___wait_True_')
            reqModal = eleFound('id', 'required-questions', wait=True)
#            d.screenshot('post_reqModal___eleFound__id____required-questions___wait_True_')
            dismissAppTimeout()

            dismissAppTimeout()
            if reqModal and reqModal.is_displayed(): # form submitted with unanswered questions
                if eleFound('id', 'invalid-label').is_displayed():
#                    d.screenshot('pre_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____partialScreen__invalid_modal___reqModal_')
                    partialScreen('invalid modal', reqModal)
#                    d.screenshot('post_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____partialScreen__invalid_modal___reqModal_')
                    # Wait until the portal mask is closed before answering required questions
#                    d.screenshot('pre_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____waitClick__id____invalid-btn___invisible__By_CSS_SELECTOR___body_>__portal-mask___')
                    waitClick('id', 'invalid-btn', invisible=(By.CSS_SELECTOR, 'body > .portal-mask'))
#                    d.screenshot('post_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____waitClick__id____invalid-btn___invisible__By_CSS_SELECTOR___body_>__portal-mask___')
#                    d.screenshot('pre_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____answerPage_required_True_')
                    answerPage(required=True)
#                    d.screenshot('post_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____answerPage_required_True_')
#                    d.screenshot('pre_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____waitClick__css_selector_____active__form-save__')
#                    waitClick('css_selector', '.active .form-save')
                    if d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]'), expected_return=True, timeout=90):
                        d.clickElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]')
                    elif d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]'), expected_return=True, timeout=90):
                        d.clickElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]')

                    d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=True, timeout=90)
                    d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=False, timeout=90)
#                    d.screenshot('post_if_reqModal_and_reqModal_is_displayed____if_eleFound__id____invalid-label___is_displayed____waitClick__css_selector_____active__form-save__')
                elif eleFound('id', 'unanswered-label').is_displayed():
#                    d.screenshot('pre_if_reqModal_and_reqModal_is_displayed____elif_eleFound__id____unanswered-label___is_displayed____partialScreen__unanswered_modal___reqModal_')
                    partialScreen('unanswered modal', reqModal)
#                    d.screenshot('post_if_reqModal_and_reqModal_is_displayed____elif_eleFound__id____unanswered-label___is_displayed____partialScreen__unanswered_modal___reqModal_')
#                    d.screenshot('pre_if_reqModal_and_reqModal_is_displayed____elif_eleFound__id____unanswered-label___is_displayed____waitClick__css_selector_____required-questions__portal-save-btn__')
                    waitClick('css_selector', '#required-questions .portal-save-btn')
#                    d.screenshot('post_if_reqModal_and_reqModal_is_displayed____elif_eleFound__id____unanswered-label___is_displayed____waitClick__css_selector_____required-questions__portal-save-btn__')
            dismissAppTimeout()

            if pageCount == len(pages):
                dismissAppTimeout()
                try:
                    # submitting page and waiting on confirmation page redirect
                    longWait.until(
                        staleness_of(page)
                    )
                except:
                    echo('Staleness of page failed')

                dismissAppTimeout()
                confirmPage = eleFound('id', 'request-continue')

                dismissAppTimeout()
                if confirmPage:
                    confirmHeaderMsg = getEle('css_selector', '#portal-content-wrapper > h1.portal-title').text
                    echo('Confimation page loaded.')

                    # <div id="portal-content-wrapper">
                    #     <h1 class="portal-title">

                    if fromPage in ['questionnaire']:
                        if 'Thank You!' in confirmHeaderMsg:
                            echo('Confirmation message found')
                        else:
                            fail('Confirmation message not found')

                    try:
                        wait.until(
                            staleness_of(confirmPage)
                        )
                    except:
                        echo('Confim page did not stale')
            else:
                try:
                    wait.until(
                        EC.invisibility_of_element_located(
                            (By.CSS_SELECTOR, 'body > .portal-mask')
                        )
                    )
                except:
                    echo('Portal mask did not become invisible')

            dismissAppTimeout()
            pageCount += 1

    def submitQuestions():
        dismissAppTimeout()
        pageBody = d.getElement(xpath='//body')

#        waitClick('css_selector', '.active .form-save')
        if d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]'), expected_return=True, timeout=90):
            d.clickElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]')
        elif d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]'), expected_return=True, timeout=90):
            d.clickElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]')

        d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=True, timeout=90)
        d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=False, timeout=90)

        wait.until(
            staleness_of(pageBody)
        )
        dismissAppTimeout()

    def docSummary(setPatID=None):
        d.navigate('?f=chart&s=pat&t=Documents&v=list&pat_id=' + str(setPatID or pat_id) + '&lv_lv_wc_order=%60Doc+ID%60&lv_lv_wc_dir=DESC&lv_lv_wc_dir2=ASC&lv_lv_wc_dir3=ASC&lv_lv_wc_limit=0&use_portal=0') # ?f=chart&s=pat&t=Document+Summary&v=list&pat_id=18&lv_lv_wc_order=%60Doc+ID%60&lv_lv_wc_dir=DESC&lv_lv_wc_dir2=ASC&lv_lv_wc_dir3=ASC

    def resetWinSize(width=default_resolution[0], height=default_resolution[1]):
        d.driverOptions.resolution = (width, height)

    def multiScreen(title):
        dismissAppTimeout()
        d.startSection('Responsive breakpoints')
        dismissAppTimeout()
        screen(title + '_desktop', 992) # desktop
        dismissAppTimeout()
        screen(title + '_tablet', 768) # tablet
        dismissAppTimeout()
        screen(title + '_mobile', 480) # mobile
        dismissAppTimeout()
        d.endSection()

    def partialScreen(title, scrollPos=None):
        if scrollPos:
            # Could either be an offset INT value or a WebElement. Using jQuery to get an accurate offsetTop value
            vertical = (scrollPos if type(scrollPos) == int else int(d.runJS('return jQuery(arguments[0]).offset().top;', scrollPos)))
            d.scrollTo(x=0, y=vertical)

        d.pause(1)
        blurBox()
        d.screenshot(title)
        d.scrollTo()

    def getFlowsheetID(flowsheetName):
        return d.miedb.dbQuery(
            '''
                SELECT obs_form_id
                FROM obs_forms
                WHERE form_item_desc = '%s'
                AND form_item_type = 'form'
            ''' % (flowsheetName)
        ).getRes()[0]['obs_form_id']

    def addVisitOrders(orders, skip_required=0):
        for order in orders:
            orderID = d.miedb.dbQuery(
                '''
                    SELECT order_id
                    FROM order_list
                    WHERE name = '%s'
                ''' % (order)
            ).getRes()[0]['order_id']

            obsFormID = getFlowsheetID(order)

            # add questionnaires to pat chart
            d.miedb.dbQuery(
                '''
                    INSERT INTO encounter_orders (pat_id, user_id, type, order_name, order_id)
                    VALUES ('%s', '%s', 'QUESTIONNAIRE', '%s', '%s')
                ''' % (pat_id, user_id, order, orderID)
            )

            if not skip_required:
                # mark first obs as required
                d.miedb.dbQuery(
                    '''
                        UPDATE obs_forms
                        SET required = 1
                        WHERE form_item_type = 'item'
                        AND obs_form_id = %d
                        AND conditional = ''
                        AND required = ''
                        LIMIT 1
                    ''' % (obsFormID)
                )

            d.miedb.dbQuery(
                '''
                    UPDATE
                        obs_forms
                    SET
                        stage_prev_value = 3
                    WHERE
                        form_item_type = 'item' AND
                        obs_form_id = %d AND
                        obs_code > 0
                    LIMIT 5
                ''' % (obsFormID)
            )

            # disable Better Corp redirect
            d.miedb.dbQuery(
                '''
                    UPDATE
                        patient_extended_values
                    SET
                        value = ''
                    WHERE
                        value = 'https://www.enterprisehealth.com'
                '''
            )

            # update patient_extended_values set value = '' where value = 'https://www.enterprisehealth.com'

    def linkPat(user, role):
        d.enterAutocomplete('le_UPatsuser_up_pat_id_value_patac',user.split(',')[0],0,user) # 'Hart, William S. (MIE-10019) DOB: 11-30-1954 SSN: 111-11-1111'
        d.enterFormData(role, id='le_UPatsuser_up_role_id_value')
        d.clickElement(id="le_UPatsuser_button")
        d.clickElement(value='Submit')

    def linkPortal(patName, mrn='', portalName='Provider Portal (PO-1) IN, US'):
        d.navigate(WCURL.ECHART)
        d.enterFormData(patName, xpath='//input[@name="sstring"]')
        d.clickElement(xpath='//input[@type="submit"]')
        d.clickElement(xpath='//a[contains(text(), "' + (mrn if mrn else patName) + '")]')
        d.navigate('?f=chart&s=pat&pat_id=' + str(pat_id) + '&v=dashboard&t=Relationships')
        d.enterAutocomplete('le_pat_parent_relations_pr_related_pat_id_as_name_value_patac', portalName.split(' ')[0], 0, portalName)
        Select(d.getElement(id='le_pat_parent_relations_rt_relation_type_value')).select_by_visible_text('Cousin')
        d.clickElement(id='le_pat_parent_relations_button')
        d.clickElement(xpath='//input[@type="submit"]')

    def verifyDocHeaders(verifySig=False):
        d.verifyElementPresent(xpath='//div[@class="document_wrapper"]/div[@class="document_header"]') # element found
        d.verifyElementPresent(xpath='//div[@class="document_wrapper"]/div[@class="document"]') # element found

        if verifySig:
            d.verifyElementPresent(xpath='//strong[contains(text(), "Signed")]/span[contains(text(), "(Final)")]') # doc sign successful

    def verifyDocAnswers(answers):
        for idx, item in enumerate(answers):
            strIdx = str(idx + 1)
            rowXpath = '//table[@class="newui zebra flowsheet_procedure"]/tbody[' + strIdx + ']'

            # Verify question column
            d.verifyElementPresent(xpath=rowXpath + '//*[contains(text(), "' + item[0] + '")]')

            # Verify answer column, selenium doesn't handle pre tags correctly

            if item[1]:
                rowAnsw = d.getElement(xpath=rowXpath + '//td[2]').text

                if item[1] in rowAnsw:
                    echo('verifyElementPresent', "xpath='" + rowXpath + "//td[2]'", '%s Answer Found' % rowAnsw)
                else:
                    fail('verifyElementPresent', "xpath='" + rowXpath + "//td[2]'", '%s Answer NOT Found' % rowAnsw)

    def resolveURL(url):
        return ('/webchart.cgi' + url if url[0] == '?' else url)

    def login(username, passw, portal='', env='', dirLink=''):
        d.navigate(resolveURL('?f=logout'))

        if dirLink:
            d.navigate(resolveURL(dirLink))

        d.enterFormData(username, id='login_user')
        d.enterFormData(passw, id='login_passwd')
        d.clickElement(name='login_submit')

        if portal:
            d.clickElement(xpath='//a[contains(text(), "' + portal + '")]')

        if env and env == 'Employer':
            d.clickElement(id='portal-user-menu-top')
            d.clickElement(xpath='//div[@id="portal-user-menu-exp"]//a[contains(text(), "Supervisor Portal")]')

    def homepageBtn(name):
        d.clickElement(xpath='//div[@id="btn-container"]//span[contains(text(), "' + name + '")]')

    def clickBell():
        try:
            d.clickElement(id='portal-header-notify')
        except Exception as e:
            echo(e)

            longWait.until(
                EC.element_to_be_clickable(
                    (By.ID, 'portal-header-notify')
                )
            )

            d.clickElement(id='portal-header-notify')

    def getScrollTop():
        return d.runJS('return jQuery(window).scrollTop();')

    def scrollFinished():
        scrollPos = getScrollTop()

        for opt in range(0, 10):
            d.pause(1)
            newPos = getScrollTop()

            if newPos == scrollPos:
                return True
            else:
                scrollPos = newPos

    def revealToolbar():
        d.runJS('topmenu.openTabDrawer()')
        lastTab = eleFound('xpath', '(//ul[@id="wc_tabwrapper"]//a)[last()]')

        if lastTab and not lastTab.is_displayed():
            ActionChains(wd).move_to_element(eleFound('xpath', '(//ul[@id="wc_tabwrapper"]//a)[1]')).perform()

        if lastTab and not lastTab.is_displayed():
            return False

        return True

    try:
        if not isEHSystem:
            fail('Not currently supporting portals in non-EH systems. Use "./wctest.py --queue=webchart -s \'EH Standard Portal\'" in /webchart/selenium/ directory.')
            return False

        d.startSection('Grant portal access')


        # +--------------------+------------------+------+-----+---------------------+----------------+
        # | Field              | Type             | Null | Key | Default             | Extra          |
        # +--------------------+------------------+------+-----+---------------------+----------------+
        # | sign_id            | int(10) unsigned | NO   | PRI | NULL                | auto_increment |
        # | wc_uuid            | binary(16)       | NO   | UNI | NULL                |                |
        # | user_id            | int(10) unsigned | NO   |     | 0                   |                |
        # | where_clause       | mediumtext       | NO   |     | NULL                |                |
        # | start_date         | datetime         | NO   | MUL | 0000-00-00 00:00:00 |                |
        # | display_forsign    | int(10) unsigned | NO   |     | 0                   |                |
        # | priority           | int(10) unsigned | NO   |     | 0                   |                |
        # | signature_priority | int(10) unsigned | NO   |     | 0                   |                |
        # +--------------------+------------------+------+-----+---------------------+----------------+

        # insert into datebegin_esigning (where_clause) values("d.doc_type IN('REPIIQ', 'LEADQ')");
        # ADD esign rule which affects document signing

        d.miedb.dbQuery(
            '''
                INSERT INTO
                    task_template (name, description, doc_type)
                VALUES
                    ('Signal Superv Response', 'Supervisor Response', 'ALLERQ')
            '''
        )

        # update supervisor questionnaire to have "Prefill From Context"
        d.miedb.dbQuery(
            '''
                UPDATE
                    obs_forms
                SET
                    stage_prev_value = 3
                WHERE
                    form_item_type = 'item' AND
                    obs_form_id = %d AND
                    obs_code > 0
                LIMIT 5
            ''' % (getFlowsheetID(supervQuestion))
        )

        d.miedb.dbQuery(
            '''
                UPDATE
                    obs_forms
                SET
                    section = '{"active": 1, "hide_save_for_later": 1}'
                WHERE
                    form_item_type = 'form' AND
                    obs_form_id = %d
            ''' % (getFlowsheetID('Lead Questionnaire'))
        )

        # ADD tasks for supervisor response workflow
        d.miedb.dbQuery(
            '''
                INSERT INTO
                    tasklist_events (evt_type, template_name, where_clause, priority)
                VALUES
                    ("on_doc_add", "Signal Superv Response", "d.doc_type IN('LEADQ','TRAVQ','REPIIQ')", 1)
            '''
        )

        d.miedb.dbQuery(
            '''
                INSERT INTO
                    datebegin_esigning (where_clause, display_forsign, signature_priority)
                VALUES
                    ("d.doc_type IN('TRAVQ', 'SANIMALQ')", 1, 5)
            '''
        )

        d.miedb.dbQuery(
            '''
                CREATE TEMPORARY TABLE PortalQuestionnaireNames (
                    obs_form_id int(10) unsigned,
                    order_id int(10) unsigned,
                    INDEX (obs_form_id)
                )
            '''
        )

        d.miedb.dbQuery(
            '''
                INSERT INTO
                    PortalQuestionnaireNames (obs_form_id)
                SELECT
                    obs_form_id
                FROM
                    obs_forms
                WHERE
                    form_item_type = "form" AND
                    form_item_desc IN(
                        "%s",
                        "%s",
                        "%s",
                        "%s"
                    )
            ''' % (questionnaires[1], questionnaires[0], patient['questionnaire'], supervQuestion)
        )

        d.miedb.dbQuery(
            '''
                UPDATE
                    obs_forms of
                INNER JOIN
                    PortalQuestionnaireNames pqn ON pqn.obs_form_id = of.obs_form_id
                SET
                    of.section =
                    CASE
                        WHEN LENGTH(of.conditional) THEN "conditional"
                        WHEN of.obs_code = 0 THEN "break_type"
                    END
                WHERE
                    (LENGTH(of.conditional) OR of.obs_code = 0) AND
                    of.form_item_type != 'form'
            '''
        )

        d.miedb.dbQuery(
            '''
                INSERT INTO
                    order_pick_list (set_name, order_id, column_index)
                VALUES
                    ("Supervisor Response", (SELECT order_id FROM order_list WHERE name = "%s"), 1),
                    ("Supervisor Response", (SELECT order_id FROM order_list WHERE name = "Lead Questionnaire"), 1),
                    ("Supervisor Response", (SELECT order_id FROM order_list WHERE name = "Travel Questionnaire"), 1),
                    ("Supervisor Response", (SELECT order_id FROM order_list WHERE name = "Request An Appointment"), 1)
            ''' % (patient['questionnaire'])
        )

        # Hard code date because test system's dates are set to 12-02-2017
        d.miedb.dbQuery(
            '''
                UPDATE
                    charttabs
                SET
                    where_clause = "DATE(service_date) < '2019-02-19'"
                WHERE
                    tabname = 'Supervisor Documents'
            '''
        )

        d.miedb.dbQuery(
            '''
                INSERT INTO
                    security_exception (user_id, module_name, category_name, security_value, admin_user_id, comment)
                VALUES
                    (%d, 'Control', 'Manage System Reports', 2, %d, 'Add edit sys reports')
            ''' % (user_id, user_id)
        )

        # INSERT INTO order_pick_list (set_name, order_id) VALUES();
        d.miedb.dbQuery(
            '''
                INSERT INTO
                    order_pick_list (set_name, order_id, order_by)
                VALUES
                    ('Applicant Portal', 2789, 0)
            '''
        )

        # Add layout to test custom layout module functionality
        d.miedb.dbQuery(
            '''
                INSERT INTO
                    layout (active, module, name, layout_html)
                VALUES
                    (1, 'UPortal Custom Layouts', 'Portal Custom Layout', '<h1>Portal Custom Layout Test!</h1>')
            '''
        )

        # Borrowed from wc_systemreports.py
        d.navigate(WCURL.SYSTEM_REPORTS)

        # Set up our values to use for a new system report
        report_name = 'Simple Patients Report'
        report_desc = 'Selenium Report Desc'
        report_cat = 'Employer Portal Report'
        report_notes = 'Selenium Report Notes'
        report_sql = "SELECT CONCAT(p.last_name,', ',p.first_name) AS full_name FROM patients p"

        # Now let's click the 'Add Report' link
        d.clickElement(text='Add Report')

        # Fill out a bunch of system report stuff
        # d.enterFormData(report_name,id='report_name')
        # d.enterFormData(report_desc,id='report_description')
        # d.enterFormData(report_notes,id='report_notes')
        d.enterFormData(report_name,id='name')
        d.enterFormData(report_desc,id='description')
        d.enterFormData(report_notes,id='notes')

        # This will open a jsWindow but our API should wait for our form inputs to appear
        # so we should be ok without explicitly waiting for a jswindow to appear
        # d.enterFormData('Add New Category',id='report_category')
        # d.enterFormData(report_cat,id='new_cat_name')
        # d.clickElement(value='Add Category')
        d.enterFormData('Add New Category',id='category')
        d.enterFormData(report_cat,id='newCategory')
        d.clickElement(value='Add')

        d.enterFormData(report_sql,id='report_sql_query')

        d.clickElement(id='submit_add_explain')

        d.navigate('?f=layout&module=Unified+Portal')
        screen('Portal access restricted')
        d.navigate(WCURL.LAYOUT + 'module=MIE&name=UserPatientsLELayout&tabmodule=admin&t=Access+Control&use_portal=0')
        d.clickElement(xpath='//font[text()="Portal User"]/../following-sibling::td//input')

        # Link relationships Selenium
        linkPat('Hart, William S. (MIE-10019) DOB: 11-30-1954 SSN: 111-11-1111 selenium@mieweb.com', 'Portal User') #Harris, Christine M. (MIE-10008) DOB: 03-11-1975 SSN: 879-44-3777 selenium@mieweb.com
        linkPat('Harris, Christine M. (MIE-10008) DOB: 03-11-1975 SSN: 879-44-3777 selenium@mieweb.com', 'Portal User') #Anderson, Frederick (MIE-10025) DOB: 02-08-1983 SSN: 401-65-9987 selenium@mieweb.com
        linkPat('Harris, Christine M. (MIE-10008) DOB: 03-11-1975 SSN: 879-44-3777 selenium@mieweb.com', 'Supervisor') #Anderson, Frederick (MIE-10025) DOB: 02-08-1983 SSN: 401-65-9987 selenium@mieweb.com
        linkPat('Anderson, Frederick (MIE-10025) DOB: 02-08-1983 SSN: 401-65-9987 selenium@mieweb.com', 'Portal User')
        linkPat('Washburn, Eleanor (MIE-10029) DOB: 11-03-1965 SSN: 201-44-6542 selenium@mieweb.com', 'Portal User')
        linkPat('Garza, Inez (MIE-10028) DOB: 10-13-1970 SSN: 501-44-6231 selenium@mieweb.com', 'Portal User')
        linkPat('Garza, Inez (MIE-10028) DOB: 10-13-1970 SSN: 501-44-6231 selenium@mieweb.com', 'Backup Supervisor')
        linkPortal('Hart', mrn='MIE-10019')

        # Link relationships Acardi
        d.navigate(WCURL.LAYOUT + 'module=MIE&name=UserPatientsLELayout&tabmodule=admin&t=Access+Control&user_id=36&realm=Employees&use_portal=0')
        linkPat('Harris, Christine M. (MIE-10008) DOB: 03-11-1975 SSN: 879-44-3777 selenium@mieweb.com', 'Portal User') #Anderson, Frederick (MIE-10025) DOB: 02-08-1983 SSN: 401-65-9987 selenium@mieweb.com
        linkPat('Harris, Christine M. (MIE-10008) DOB: 03-11-1975 SSN: 879-44-3777 selenium@mieweb.com', 'Supervisor') #Anderson, Frederick (MIE-10025) DOB: 02-08-1983 SSN: 401-65-9987 selenium@mieweb.com
        linkPat('Anderson, Frederick (MIE-10025) DOB: 02-08-1983 SSN: 401-65-9987 selenium@mieweb.com', 'Supervisor')
        linkPortal('Harris')

        addVisitOrders(questionnaires)

        d.navigate('?f=chart&s=dteditor&t=Document+Types&srch=clinic+summary&dtopp=dtview&dtsopp=dt_val&doc_type=WCPATED')
        d.clickElement(xpath='//input[@value="Edit Document Type"]')
        d.clickElement(id='chart_type_labelelem')
        d.clickElement(xpath='//a[text()="Select All"]')
        d.clickElement(xpath='//input[@name="edit_doc_type"]')

        d.navigate('?f=admin&s=sysconfigmgr&Import=1')
        d.enterFormData('Violence Screening.JSON', id='importfile')
        waitClick('xpath', '//input[@value="Import Selected"]')

        longWait.until(
            EC.visibility_of_element_located(
                (By.ID, 'successdiv')
            )
        )

        d.navigate('?f=layout&module=MASTER&name=EPM_Maintenance&use_portal=0&tabmodule=+')
        d.clickElement(xpath="//button[contains(text(), 'Search')]")
        waitClick('xpath', '//a[contains(text(), "Provider Portal")]')

        # Enable supervisor portal
        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[text()="Portal Setup"]')
        d.clickElement(xpath='//h2[text()="General Configuration"]')
        waitClick('id', 'DPCB_portal_enable_employer')
        Select(d.getElement(id='DPI_preferred_partition')).select_by_visible_text('MIE')
        d.clickElement(xpath='//h2[text()="General Configuration"]/..//button') # click next button
        d.verifyElementPresent(xpath='//a[@id="access-url"]')

        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[text()="Patient Portal"]')
        d.clickElement(id='DPI_portal_appt_type_2')

        for opt in d.getElements(xpath="//div[@id='apt-req']//input[@type='checkbox']"):
            if opt.is_displayed():
                clickEle(opt)

        d.clickElement(xpath="//div[contains(@id, 'Patient Portal Modules_My Appointments')]//input[@type='submit']")

        # Add report injury to doc types allowed in portal
        d.clickElement(xpath='//h2[text()="Configuration"]')
        d.clickElement(xpath='//h2[text()="Configuration"]/..//a[text()="Add message types"]')

        if d.switchToPopup():
            d.clickElement(xpath='//input[@type="submit" and @value="Edit"]')
            d.enterAutocomplete('le_ct_document_list_dt_description_display_ac', 'Questionnaire-Lead', 0, 'Questionnaire-Lead')
            d.clickElement(id='le_ct_document_list_button')
            d.enterAutocomplete('le_ct_document_list_dt_description_display_ac', 'Questionnaire-Travel', 0, 'Questionnaire-Travel')
            d.clickElement(id='le_ct_document_list_button')
            d.enterAutocomplete('le_ct_document_list_dt_description_display_ac', 'Questionnaire-Clinical Question', 0, 'Questionnaire-Clinical Question')
            d.clickElement(id='le_ct_document_list_button')
            d.clickElement(id='save')
            d.closePopup()

        wd.refresh()
        d.clickElement(xpath='//h2[text()="Configuration"]')
        d.clickElement(id='DPCB_enable_prefill_from_context')
        d.clickElement(id='DPCB_show_esign_docs')
        d.clickElement(id='DPCB_show_completed_questionnaires')
        d.clickElement(xpath='(//span[contains(@id, "reply_template")])[3]')
        d.runJS('return jQuery(".enable-reply a").first().click()')
        d.clickElement(xpath='//strong[contains(text(), "Documents")]')
        # Close configuration section
        d.clickElement(xpath='//h2[text()="Configuration"]/following-sibling::div[@class="edit-buttons"]//button')

        wait.until(
            EC.invisibility_of_element_located(
                (By.ID, 'DPCB_enable_prefill_from_context')
            )
        )

        d.clickElement(xpath="//div[contains(text(), 'Select Modules')]")
        d.clickElement(xpath="//input[@value='Form Link 1']")
        d.clickElement(xpath="//input[@value='Monitoring Status']")
        d.clickElement(xpath="//input[@value='Layout Link 1']")

        waitClick('xpath', '//div[@id="dash_uml_available_layouts_win"]//input[@value="Save"]', refresh=1)

        d.enterFormData('Patient History Form', id='DPI_cust_form_name_1')
        d.enterAutocomplete('DPI_custom_form_1_jsname', 'Patient', 0, 'Patient History - Form')
        d.clickElement(id='custom-form-submit-1')

        d.enterAutocomplete('symptom_monitor_jsname', 'COVID-19 Symptom', 0, 'COVID-19 Symptom Monitoring Questionnaire')
        d.clickElement(id='sym-submit')

        Select(d.getElement(id='DPI_custom_lay_name_1')).select_by_visible_text('Portal Custom Layout')
        d.clickElement(id='custom-lay-submit-1')

        # Toolbar is not expanding, even when using JS function, instead force redirect
        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[contains(text(), "Employer Portal")]')
        d.clickElement(xpath="//div[contains(text(), 'Select Modules')]")
        d.clickElement(xpath="//input[@value='Reports']")
        d.clickElement(xpath="//input[@value='Order Status']")
        d.clickElement(xpath="//input[@value='Questionnaire Link 1']")
        # Unselect Supervisor Scheduling
        d.clickElement(xpath="//input[@value='Supervisor Scheduling']")
        waitClick('xpath', '//div[@id="available-modules"]//input[@value="Submit"]', refresh=1)

        d.enterFormData('Supervisor Questionnaire Link', id='DPI_cust_mod_name_superv_1')
        d.enterAutocomplete('questLinkACsuperv_1_jsname', 'Ergonomic', 0, 'Ergonomic Questionnaire')
        d.clickElement(id='custom-link-submit-superv_1')

        d.clickElement(xpath='//td[contains(text(), "Allowed questionnaires")]/..//a')
        d.clickElement(id='checkall0')
        d.clickElement(id='ok_me0')
        d.clickElement(xpath="//div[contains(@id, 'Send a Message')]//div[@class='portal-module-footer']//input[@type='submit']")

        d.startSection('Configure Reports')
        d.enterFormData('Just click the button, it\'s not that hard!', id='DPI_reports_instruction_txt_superv')
        d.clickElement(id='employer_reports_dropdownarrow')

        longWait.until(
            EC.element_to_be_clickable(
                (By.ID, 'employer_reports')
            )
        )

        d.clickElement(id='employer_reports')
        d.clickElement(id='employer_reports_labelelem')
        d.clickElement(xpath="//div[contains(@id, 'Modules_Reports')]//div[@class='portal-module-footer']//input[@type='submit']")
        d.endSection() # End configure reports

        d.clickElement(xpath='//h2[text()="Configuration"]')

        longWait.until(
            EC.element_to_be_clickable(
                (By.ID, 'DPCB_enable_prefill_from_context_superv')
            )
        )

        d.pause(5)
        # wait for JS to fully process
        d.clickElement(id='DPCB_enable_prefill_from_context_superv')
        d.clickElement(id='DPCB_enable_prefill_from_other_employee_superv')
        echo('Setting Messages Custom Title')
        d.getElement(id='DPI_message_center_alt_name_superv').clear()
        d.enterFormData('Messages Custom Title', id='DPI_message_center_alt_name_superv')
        echo('Setting Messages Custom Header')
        # This prevents "tab" key from "enterFormData" method from firing
        d.getElement(id='DPI_message_center_alt_header_superv').clear()
        d.getElement(id='DPI_message_center_alt_header_superv').send_keys('Messages Custom Header')

        d.clickElement(xpath='//td[contains(text(), "Questionnaires for Supervisors")]/..//a')
        d.clickElement(id='checkall1')
        d.clickElement(id='ok_me1')
        d.clickElement(xpath='(//a[text()="Add message types"])[1]')

        if d.switchToPopup():
            d.clickElement(xpath='//input[@type="submit" and @value="Edit"]')
            d.enterAutocomplete('le_ct_document_list_dt_description_display_ac', 'Clinic', 0, 'Clinic Summary/Patient Education')
            d.clickElement(id='le_ct_document_list_button')
            d.clickElement(id='save')
            d.closePopup()

        d.clickElement(xpath='//h2[text()="Configuration"]')

        wait.until(
            EC.invisibility_of_element_located(
                (By.ID, 'DPCB_enable_prefill_from_context_superv')
            )
        )

        d.startSection('Configure Applicant Portal')
        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[text()="Portal Setup"]')
        d.clickElement(xpath='//h2[text()="Applicant Portal Setup"]')
        d.clickElement(xpath="//input[@value='Run Setup']")

        longWait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Portal Management:Applicant Portal")]')
            )
        )

        d.clickElement(xpath='//h2[text()="Configuration"]')
        d.clickElement(id='DPCB_app_portal_enable_print')
        d.clickElement(id='DPCB_app_portal_enable_ssn')
        d.clickElement(id='DPCB_app_portal_enable_email')
        d.pause(5)
        d.clickElement(xpath="//a[text()='Add Questionnaires']")
        d.clickElement(id='checkall0')
        d.clickElement(id='ok_me1')
        d.enterFormData('Selenium Applicant Portal Description Add a new applicant', id='DPI_app_portal_desc')
        d.enterFormData('Selenium Applicant form title', id='DPI_app_portal_form_title')
        d.enterFormData('Selenium Applicant form directions', id='DPI_app_portal_form_directions')
        d.enterFormData('Selenium Applicant portal questionnaire directions', id='DPI_app_portal_questionnaire_directions')
        d.clickElement(xpath='//h2[text()="Configuration"]')
        d.navigate('?func=admin&subfunc=roleeditor&t=Security+Role+Editor')

        d.clickElement(xpath='//a[text()="Applicant"]/../following-sibling::td/a[text()="Edit"]')

        applicantSettings = [
            {"security_value": "1", "module_name": "WebChart", "category_name": "Limit to Portal"},
            {"security_value": "1", "module_name": "E-Chart", "category_name": "Limited to Default Tab"},
            {"security_value": "4", "module_name": "E-Chart", "category_name": "Document Permissions"},
            {"security_value": "4", "module_name": "E-Chart", "category_name": "Manage Observations"},
            {"security_value": "4", "module_name": "E-Chart", "category_name": "Demographics"},
            {"security_value": "1", "module_name": "EMR", "category_name": "View Encounters"}
        ]

        for setting in applicantSettings:
            select = d.getElement(xpath='//td[contains(text(), "' + setting['category_name'] + '")]/following-sibling::td[1]/select')
            Select(select).select_by_value(setting['security_value'])

        d.enterFormData('applicant portal', id='sec_role_comment')
        d.clickElement(value='Update Role')

        d.endSection() # END Configure Applicant Portal

        d.navigate('?f=layout&module=Previews&name=Questionnaires&obs_form_name=Travel%20Questionnaire&pat_id=' + str(pat_id))
        screen('Testing Preview Mode')

        d.startSection('Push document to Patient Portal')

        d.navigate(WCURL.ECHART)
        d.enterFormData(patLast, xpath='//input[@name="sstring"]')
        d.clickElement(xpath='//input[@type="submit"]')
        d.clickElement(xpath='//a[contains(text(), "' + patLast + '")]')
        d.clickElement(xpath='//a[contains(text(), "Add Document")]')
        d.clickElement(xpath='//a[contains(@title, "WCDOCNOT")]')
        d.enterFormData('Pushing this document to the Patient Portal', id='file')
        d.clickElement(name='submit_document')
        d.clickElement(xpath='//a[text()="Request Signature"]')
        d.enterAutocomplete('user_search_ac', 'Anderson', 0, 'Anderson, Frederick ( Better Corp. -  Mountain View, CA United States 94041 - 500 Castro Street  )')
        d.enterFormData('Pushing this document, adding a comment', id='comment')
        d.clickElement(xpath='//input[@value="Request signature"]')
        d.endSection() # end 'Grant portal access'

        d.endSection() # end Push document to Patient Portal

        d.startSection('Applicant Portal')
        d.navigate('?f=layout&module=MASTER&name=EPM_Maintenance&use_portal=0&tabmodule=+')
        d.clickElement(xpath="//button[contains(text(), 'Search')]")
        waitClick('xpath', '//a[contains(text(), "Provider Portal")]', expect=('xpath', '//span[contains(., "Portal Management")]'))

        # Can't force open toolbar, need to click button using JS
        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[text()="Applicant Portal"]')
        d.clickElement(id='ap-url')

        if d.switchToPopup():
            d.enterFormData('Aris', id='new_app_first_name')
            d.enterFormData('Eracleous', id='new_app_last_name')
            d.getElement(id='app-dob').send_keys('09252013')
            echo('Added DOB entry')
            d.enterFormData('111-22-3333', id='new_app_ssn')
            d.enterFormData('dsmith@mieweb.com', id='new_app_email')
            d.clickElement(id='form-save')

            longWait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '(//a/span[contains(text(), "begin")])[1]')
                )
            )

            dismissAppTimeout()
            d.screenshot()
            partialScreen('Applicant Available Questionnaires')
            d.screenshot()
            d.clickElement(xpath='(//a/span[contains(text(), "begin")])[1]')
            dismissAppTimeout()
            d.screenshot()
            answerQuestions(dismissAppPopup=False)
            d.screenshot()
            dismissAppTimeout()
            d.screenshot()
            dismissAppTimeout()
            screen('Finished applicant questionnaires')
            dismissAppTimeout()
            d.screenshot()
            d.clickElement(id='app-sign-out')
            d.screenshot()
            dismissAppTimeout()
            d.clickElement(id='log-confirm-btn')
            d.screenshot()
            d.verifyElementPresent(xpath='//span[contains(text(), "Selenium Applicant form title")]')
            d.screenshot()
            d.closePopup()

        verifyApp = d.miedb.dbQuery(
            '''
                SELECT
                    birth_date,
                    ssn,
                    email,
                    first_name,
                    last_name
                FROM
                    patients
                WHERE
                    first_name = 'Aris'
            '''
        ).getRes()[0]

        if verifyApp['ssn'] != '111223333':
            d.screenshot()
            fail('Applicant SSN invalid')
            d.screenshot()
            echo(verifyApp['ssn'])
            d.screenshot()

        if verifyApp['birth_date'].strftime('%Y-%m-%d') != '2013-09-25':
            d.screenshot()
            fail('Applicant Birth date invalid')
            d.screenshot()
            echo(verifyApp['birth_date'].strftime('%Y-%m-%d'))
            d.screenshot()

        if verifyApp['email'] != 'dsmith@mieweb.com':
            d.screenshot()
            fail('Applicant email invalid')
            d.screenshot()
            echo(verifyApp['email'])
            d.screenshot()

        d.endSection() # END applicant portal

        d.startSection('Patient Portal') # -- START Patient PORTAL --
        d.startSection('Homepage')
        login('selenium', 'selenium')
        employeeHome()

        d.startSection('Complete consent form')
        waitClick('xpath', '//div[@id="consent-forms"]//a')
        answerQuestions()
        d.endSection()

        partialScreen('portal help modal')
        d.clickElement(id='modal-close')
        multiScreen('Employee home page')
        d.clickElement(id='portal-header-view')
        d.screenshot('Available users dropdown')
        d.endSection() # end 'Portal Homepage'

        d.startSection('Open Form')
        # Patient History Form
        homepageBtn('Patient History Form')

        if d.switchToPopup():
            screen('Printable Form Link', widgetWait=True)
            d.closePopup()

        d.clickElement(id='portal-user-menu-top')
        d.clickElement(xpath='//div[@id="portal-user-menu-exp"]//span[contains(text(), "Patient History Form")]')

        if d.switchToPopup():
            d.verifyElementPresent(xpath='//body/embed')
            d.closePopup()

        d.endSection()

        d.startSection('Verify Access Link') # Start Message Center
        d.clickElement(id='portal-user-menu-top')
        d.clickElement(id='access-link')
        partialScreen('Access Menu From Link')
        d.clickElement(xpath='//a[contains(text(), "Provider Portal")]')
        d.endSection()

        d.startSection('Message Center') # Start Message Center
        d.startSection('Questionnaires')
        clickBell()

        d.startSection('Send a Message')
        d.miedb.dbQuery(
            '''
                UPDATE obs_forms
                SET required = 'requireAnswer(this)'
                WHERE form_item_type = 'item'
                AND obs_form_id = %d
                AND conditional = ''
                AND required = ''
                LIMIT 1
            ''' % (getFlowsheetID(patient['questionnaire']))
        )

        d.miedb.dbQuery(
            '''
                UPDATE obs_forms
                SET required = 'requireDatetime(this)'
                WHERE form_item_type = 'datetm'
                AND obs_form_id = %d
            ''' % (getFlowsheetID(patient['questionnaire']))
        )

        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  patient['questionnaire'] + '")]/following-sibling::td[1]//a')

        longWait.until(EC.element_to_be_clickable((By.XPATH, '(//textarea)[1]')))
        try:
            wd.find_element_by_css_selector('input[type="date"]').send_keys('09252013')
        except AttributeError:
            from selenium.webdriver.common.by import By
            wd.find_element(By.CSS_SELECTOR, 'input[type="date"]').send_keys('09252013')

#        waitClick('css_selector', '.active .form-save')
        if d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]'), expected_return=True, timeout=90):
            d.clickElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]')
        elif d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]'), expected_return=True, timeout=90):
            d.clickElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]')

        d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=True, timeout=90)
        d.waitFor(d, lambda d: d.getElement(xpath='//h1[contains(., "Thank You")]'), expected_return=False, timeout=90)
        screen('Test hard required')
        d.clickElement(xpath='//button[@class="reset-all modal-close-x"]')

        # Verify Save for later button
        wait.until(
            EC.invisibility_of_element_located(
                (By.ID, 'required-questions')
            )
        )

        scrollFinished()
        d.enterFormData('Testing the Save for later button', xpath='(//textarea)[1]')
        d.enterFormData('Two textareas should have saved info', xpath='(//textarea)[2]')
        findClick('css_selector', '.yes_btn')
        waitClick('css_selector', '.save-progress')

        longWait.until(EC.element_to_be_clickable((By.XPATH, '(//input[@value="resume"])[1]')))
        partialScreen('Employee saved for later')
        d.clickElement(xpath='(//input[@value="resume"])[1]')
        d.verifyElementPresent(xpath='//textarea[text()="Testing the Save for later button"]')
        d.verifyElementPresent(xpath='//textarea[text()="Two textareas should have saved info"]')
        d.verifyElementPresent(xpath='//input[@type="radio" and @value="Yes" and @checked="1"]')
        clickBell()
        waitClick('id', 'all-message-opt') # Previously: d.clickElement(id='all-message-opt')
        screen('Verify in progress and doc hidden')
        d.clickElement(xpath='//button[contains(text(), "Cancel")]')
        clickBell()
        partialScreen('Verify cancellation')

        d.startSection('Verify inline cancel button')
        # test internal cancel
        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  patient['questionnaire'] + '")]/following-sibling::td[1]//a')

        # Verify Save for later button
        d.enterFormData('Testing the Save for later button', xpath='(//textarea)[1]')
        d.enterFormData('Two textareas should have saved info', xpath='(//textarea)[2]')
        findClick('css_selector', '.yes_btn')
        waitClick('css_selector', '.save-progress')

        longWait.until(EC.element_to_be_clickable((By.XPATH, '(//input[@value="resume"])[1]')))
        partialScreen('Employee saved for later')
        d.clickElement(xpath='(//input[@value="resume"])[1]')
        d.verifyElementPresent(xpath='//textarea[text()="Testing the Save for later button"]')
        d.verifyElementPresent(xpath='//textarea[text()="Two textareas should have saved info"]')
        d.verifyElementPresent(xpath='//input[@type="radio" and @value="Yes" and @checked="1"]')
        encOrderID = d.getElement(xpath='//input[@name="enc_order_id"]').get_attribute('value')
        cancelQuest = d.getElement(xpath='//body')
        findClick('css_selector', '.cancel-questionnaire')

        wait.until(
            staleness_of(cancelQuest)
        )

        cancelStatus = d.miedb.dbQuery(
            '''
                SELECT
                    eo.status,
                    e.closed,
                    e.deleted,
                    d.storage_type
                FROM
                    encounter_orders eo
                LEFT JOIN
                    encounters e ON e.encounter_id = eo.enc_id
                LEFT JOIN
                    lab_requests lr ON lr.enc_order_id = eo.enc_order_id
                LEFT JOIN
                    documents d ON d.doc_id = lr.doc_id
                WHERE
                    eo.enc_order_id = %u
                ORDER BY
                    eo.enc_order_id DESC
                LIMIT
                    1
            ''' % (int(encOrderID))
        ).getRes()[0]

        if cancelStatus['status'] == -1:
            echo('Encounter order cancelled')
        else:
            fail('Encounter order not cancelled')

        if cancelStatus['closed'] == 1:
            echo('Encounter closed')
        else:
            fail('Encounter not closed')

        if cancelStatus['deleted'] == 1:
            echo('Encounter deleted')
        else:
            fail('Encounter not deleted')

        if cancelStatus['storage_type'] == 0:
            echo('Document deleted')
        else:
            fail('Document not deleted')

        d.endSection() # Verify inline cancel
        d.endSection() # End send a message

        d.startSection('Validate File Upload')
        clickBell()
        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  uploadFile + '")]/following-sibling::td[1]//a')
        try:
            fileEle = wd.find_element_by_css_selector('input[type="file"]')
        except AttributeError:
            from selenium.webdriver.common.by import By
            fileEle = wd.find_element(By.CSS_SELECTOR, 'input[type="date"]').send_keys('09252013')

        # Make file input visible so that MIE Driver can perform file upload
        d.runJS('return jQuery(arguments[0]).css("opacity", "1");', fileEle)
        d.enterFormData('corrupt_image.jpg', id=fileEle.get_attribute('id') )

        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#growls-tr > div')
            )
        )

        d.verifyElementPresent(xpath='//div[@id="growls-tr"]/div')
        clickBell()
        d.clickElement(xpath='//button[contains(text(), "Cancel")]')
        d.endSection() # End Validate File Upload

        d.startSection('Clinician Orders')
        addVisitOrders([resumeClinician], skip_required=1)
        clickBell()
        longWait.until(EC.element_to_be_clickable((By.XPATH, '(//input[@value="begin"])[1]')))
        d.verifyElementPresent(xpath='//td[contains(text(), "' +  resumeClinician + '")]')  # len(d.getElements(xpath='//input[@value="begin"]'))
        clickBell()
        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  resumeClinician + '")]/following-sibling::td[1]//a')
        submitQuestions()
        clickBell()
        longWait.until(EC.element_to_be_clickable((By.XPATH, '(//input[@value="begin"])[1]')))

        if eleFound('xpath', '//td[contains(text(), "' +  resumeClinician + '")]'):
            fail('Patient resume clinician order failed')

        for orderDue in range(0, len(d.getElements(xpath='//input[@value="begin"]'))):
            waitClick('xpath', '(//input[@value="begin"])[1]')
#            if d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]'), expected_return=True, timeout=90):
#                d.clickElement(xpath='//button[contains(@class, "form-save") and @value="SUBMIT"]')
#            elif d.waitFor(d, lambda d: d.getElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]'), expected_return=True, timeout=90):
#                d.clickElement(xpath='//button[contains(@class, "form-save")][contains(., "NEXT") or contains(., "next") or contains(., "Next")]')
            d.screenshot('post_orderdue_in_range_o_len_getElements_input_value_begin_replaced_waitclick_with_if_else_waitfor_clickelement_form_save_submit_else_waitfor_clickelement_form_save_next')
            answerQuestions()
            d.screenshot('post_answer_questions_for_orderdue_in_range_o_len_getElements_input_value_begin_replaced_waitclick_with_if_else_waitfor_clickelement_form_save_submit_else_waitfor_clickelement_form_save_next')

        d.endSection() # end clinician

        d.startSection('Prefill From Context')

        # Create new questionnaire of same doc_type
        clickBell()
        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  questionnaires[1] + '")]/following-sibling::td[1]//a')
        d.clickElement(id='uniform-obs_result_prefill_context_0')
        d.verifyElementPresent(xpath='//h2[contains(text(), "Prefill answers from document")]')
        findClick('css_selector', '.view-prefill-doc')

        wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#review-prefill-doc.doc-loaded')
            )
        )

        wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, 'button.view-prefill-doc[disabled]')
            )
        )

        partialScreen('Preview prefilling document')
        d.clickElement(xpath='//button/span[contains(text(), "CONTINUE")]')
        screen('Review Prefill')
        d.endSection() # end Prefill From Context'

        addVisitOrders([calculation])
        clickBell()
        longWait.until(EC.element_to_be_clickable((By.XPATH, '(//input[@value="begin"])[1]')))
        d.clickElement(xpath='(//input[@value="begin"])[1]')
        d.startSection('Print preview')
        d.runJS(
            '''
                Array.prototype.forEach.call(document.getElementsByTagName('style'), function(style) {
                    style.innerText = style.innerText.replace(/@media print/gi, '@media screen');
                });
            '''
        )

        screen('Print preview')
        wd.refresh()
        d.endSection() # END: Print Preview

        d.startSection('Verify calculations')
        answerQuestions(responsiveBreakpoint=False)
        d.endSection()

        login('employee', 'selenium')

        d.clickElement(xpath='//a[contains(text(), "Provider Portal")]')
        d.clickElement(id='modal-close')

        # Close timezone modal
        d.screenshot('checkthetimezoneselenium')
        waitClick('xpath', '//button[contains(text(), "Update")]', invisible=(By.CLASS_NAME, 'modal-backdrop'))
        clickBell()
        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')

        d.clickElement(xpath='//td[contains(text(), "' +  patient['questionnaire'] + '")]/following-sibling::td[1]//a')

        answerQuestions()

        d.startSection('Upload file in questionnaire')

        d.miedb.dbQuery(
            '''
                UPDATE obs_forms
                SET required = 'requireAnswer(this)'
                WHERE form_item_type = 'file'
                AND obs_form_id = %d
                AND conditional = ''
                AND required != ''
                LIMIT 1
            ''' % (getFlowsheetID(patient['file_upload']))
        )

        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  patient['file_upload'] + '")]/following-sibling::td[1]//a')
        answerQuestions()
        d.endSection() # END: Upload file in questionnaire

        d.startSection('Conditional questionnaires') # Start conditional testing
        d.miedb.dbQuery(
            '''
                UPDATE obs_forms
                SET conditional = 'patient_age < 10'
                WHERE obs_form_id = %d
            ''' % (getFlowsheetID(conditional))
        )
        d.clickElement(xpath='//a[contains(text(), "Send a Message")]')
        d.clickElement(xpath='//td[contains(text(), "' +  conditional + '")]/following-sibling::td[1]//a')
        d.verifyElementPresent(xpath=css2xpath('div.conditional.collapsed[data-conditional="patient_age < 10"]'))
        echo('Conditional evaluated to false')
        clickBell()
        d.miedb.dbQuery(
            '''
                UPDATE obs_forms
                SET conditional = 'patient_age > 10'
                WHERE obs_form_id = %d
            ''' % (getFlowsheetID(conditional))
        )
        d.clickElement(xpath='//input[@value="resume"]')
        d.verifyElementPresent(xpath=css2xpath('div.conditional.expanded[data-conditional="patient_age > 10"]'))
        echo('Conditional evaluated to true')
        d.endSection() # END conditional testing

        d.startSection('Verify direct link')
        login('employee', 'selenium', dirLink='?f=layout&module=Patient+Portal&name=Create+Order&order_name=Ask+a+Clinical+Question&svar_cobrand_patid=43')
        d.verifyElementPresent(xpath='//h1[contains(text(), "Ask a Clinical Question")]')
        d.clickElement(id='uniform-consent-box')
        answerQuestions()
        d.endSection() # end Verify direct link

        d.startSection('Message Reply Workflow')
        login('nurse', 'selenium')
        d.clickElement(xpath='//a[contains(text(), "Nursing")]')
        waitClick('xpath', '(//td[@class="tasklist__realm__Nursing_ID_cell"])[1]/a', expect=('xpath', '//input[@type="button" and @value="Reply"]'))
        d.clickElement(xpath='//input[@type="button" and @value="Reply"]')
        d.enterFormData('Testing the reply workflow. this is a Nurse', id='notes')
        d.clickElement(xpath='//input[@name="addtaskcomplete"]')

        login('employee', 'selenium')
        waitClick('xpath', '//a[contains(text(), "Provider Portal")]')
        clickBell()
        d.clickElement(xpath='//span[contains(text(), "Questionnaire-Clinical Question")]')
        d.clickElement(id='comments-btn')
        d.verifyElementPresent(xpath='//span[contains(., "Nicole Simmons")]')
        d.verifyElementPresent(xpath='//span[contains(text(), "An employee has asked a clinical question on the portal.")]')
        d.verifyElementPresent(xpath='//span[contains(text(), "Testing the reply workflow. this is a Nurse")]')
        findClick('css_selector', '.msg-contact')
        d.verifyElementPresent(xpath='//div[@class="inner-thread"]//span[contains(text(), "Testing the reply workflow. this is a Nurse")]')
        d.verifyElementPresent(xpath='//div[@class="inner-thread"]//span[contains(text(), "An employee has asked a clinical question on the portal.")]')
        d.endSection() # END: Message Reply Workflow

        d.startSection('Review pushed document')
        clickBell()
        d.clickElement(xpath='//span[contains(text(), "WCDOCNOT")]')
        d.verifyElementPresent(xpath='//div[contains(text(), "Pushing this document to the Patient Portal")]')
        d.endSection() #end Review pushed document'

        login('selenium', 'selenium')

        employeeHome()

        d.endSection() # end answer a questionnaire

        d.startSection('Review Documents')
        clickBell()
        d.clickElement(id='all-message-opt')
        d.clickElement(xpath='(//div[@id="message-row-wrapper"]//li[@class="mmi-edit-row clearfix"]//a//span[contains(text(), "Injection")])[1]')
        screen('Review a document')
        clickBell()
        d.clickElement(id='all-message-opt')

        # Read messages
        d.verifyElementPresent(xpath='//span[@class=""]/../..//span[contains(text(), "Injection")]')
        d.verifyElementPresent(xpath='//span[@class=""]/../..//span[contains(text(), "Questionnaire-Travel")]')
        d.verifyElementPresent(xpath='//span[@class=""]/../..//span[contains(text(), "Questionnaire-Lead")]')

        d.clickElement(xpath='(//div[@id="message-row-wrapper"]//li[@class="mmi-edit-row clearfix"]//a//span[contains(text(), "Injection")])[1]')
        d.clickElement(id='actions-btn')
        d.clickElement(id='mark-unread')
        d.clickElement(id='new-message-opt')
        clickBell()
        d.verifyElementPresent(xpath='//span[@class="mc-unread"]/../..//span[contains(text(), "Selenium Selenium")]/../..//span[contains(text(), "Injection")]')
        d.endSection() # END review documents

        d.endSection() # end Message Center

        d.startSection('Other Health Resources')
        employeeHome()
        homepageBtn('Other Health Resources')
        multiScreen('other health resources')
        d.endSection() # end 'Other Health Resources'

        d.startSection('Request an Appointment')
        d.clickElement(id='portal-header-home') # return to portal home page
        homepageBtn('My Appointments')
        d.clickElement(id='request-appt-submit')

        answerQuestions()

        screen('existing_appointments')
        d.endSection() # end 'Request an Appointment'

        d.startSection('Schedule an Appointment')

        #Setup Schedules
        login('selenium', 'selenium', dirLink='?func=scheduler&s=schedules&opp=sched_edit&sched_id=9')
        d.clickElement(id='startdateYEAR')
        d.enterFormData('2000', id='startdateYEAR')
        d.clickElement(id='enddateYEAR')
        d.enterFormData('2000', id='enddateYEAR')
        d.clickElement(value='Save')

        d.navigate('?func=scheduler&s=schedules&opp=sched_edit&sched_id=6')
        d.clickElement(id='startdateYEAR')
        d.enterFormData('2000', id='startdateYEAR')
        d.clickElement(id='enddateYEAR')
        d.enterFormData('2000', id='enddateYEAR')
        d.clickElement(value='Save')

        #Add a waitlist appointment
        d.navigate('?f=scheduler&s=appt_wizard')
        d.enterAutocomplete('pat_id_patac', 'Hart, ', 0, 'Hart, William S. (MIE-10019) DOB: 11-30-1954 SSN: 111-11-1111 selenium@mieweb.com')
        d.enterAutocomplete('res_idac', 'Lab', 0, 'Lab Testing ( IN United States )')
        d.enterAutocomplete('typeac', 'Office', 0, 'Office Visit Follow Up')
        d.enterAutocomplete('locationac', 'Off', 0, 'Office')
        d.clickElement(value='Save')

        d.navigate('?f=layout&module=MASTER&name=EPM_Maintenance&use_portal=0&tabmodule=+')

        d.clickElement(xpath="//button[contains(text(), 'Search')]")
        waitClick('xpath', '//a[contains(text(), "Provider Portal")]')

        # Can't force open toolbar, need to click button using JS
        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[text()="Patient Portal"]')
        d.clickElement(id='DPI_portal_appt_type_1')

        # Select appt type from multiselect to test required comments
        d.runJS('return jQuery("#comments_req_dropdownarrow").click();')
        d.runJS('return jQuery("#comments_req_td input[type=checkbox][value=AUDIO]").prop("checked",true);')
        d.runJS('return jQuery("#comments_req_dropdownarrow").click();')
        d.clickElement(xpath="//div[contains(@id, 'Patient Portal Modules_My Appointments')]//input[@type='submit']")

        login('selenium', 'selenium')
        employeeHome()
        homepageBtn('My Appointments')
        d.clickElement(xpath='//a[contains(text(),"Schedule")]')
        longWait.until(
            EC.element_to_be_clickable(
                (By.ID, 'form-save')
            )
        )
        Select(d.getElement(id='APPT_startdate')).select_by_visible_text('Fri 02-02-2007 10:30am (ET)')
        d.clickElement(id='form-save')

        d.clickElement(xpath='//a[contains(text(),"schedule a new appointment")]')

        # Select appointment type
        Select(d.getElement(id='APPT_type')).select_by_visible_text('Audiogram')
        wait.until(
            EC.visibility_of_element_located(
                (By.ID,'APPT_comment')
            )
        )
        screen('Comments Required')
        d.enterFormData('Hello world!', id='APPT_comment')

        longWait.until(
            EC.element_to_be_clickable(
                (By.ID, 'form-save')
            )
        )
        d.clickElement(id='form-save')

        if int( # Check for 2 appointment confirmation emails
            d.miedb.dbQuery(
                '''
                    SELECT
                        COUNT(*) AS count
                    FROM
                        documents
                    WHERE
                        pat_id = %d AND
                        doc_type = 'EAPTC'
                ''' % (pat_id)
            ).getRes()[0]['count']
        ) == 2:
            echo('Appointment confirmation emails found.')
        else:
            fail('Appointment confirmation email not found!')

        screen('Schedule an Appointment Confirm')

        #Test PO location restrictions
        login('selenium', 'selenium', dirLink='?f=chart&s=leditor&tabmodule=admin&tabselect=System&opp=Add')

        #Add new Selenium Clinic location
        d.enterFormData('TEST', id='code')
        d.enterFormData('Selenium Clinic', id='description')
        d.enterFormData('1234 Main Street', id='address1')
        d.enterFormData('Fort Wayne', id='city')
        Select(d.getElement(id='state')).select_by_visible_text('Indiana')
        d.enterFormData('46814', id='zip_code')
        d.clickElement(value='Add')

        #Set schedule to use Selenium Clinic Location
        d.navigate('?func=scheduler&s=schedules&opp=sched_edit&sched_id=6')
        d.enterAutocomplete('loc_ac', 'Selenium Clinic', 0, 'Selenium Clinic')
        d.clickElement(value='Save')

        #Set location of Provider Portal PO to Selenium Clinic
        d.navigate('?f=chart&s=pat&t=Locations&v=dashboard&pat_id=41')
        d.enterAutocomplete('location_pat_location', 'Selenium Clinic', 0, 'Selenium Clinic')
        d.clickElement(value='Add')
        d.clickElement(value='Submit')

        #Disable appointment confirmation/cancellation emails
        d.navigate('?f=layout&module=MASTER&name=EPM_Maintenance&use_portal=0&tabmodule=+')

        d.clickElement(xpath="//button[contains(text(), 'Search')]")
        waitClick('xpath', '//a[contains(text(), "Provider Portal")]')
        d.clickElement(xpath='//span[@id="Portal_20Management_tab"]')
        d.clickElement(xpath='//a[text()="Patient Portal"]')

        #Disable appointment confirmation/cancellation emails
        d.clickElement(id='DPCB_appt_email_disable')
        d.clickElement(xpath="//div[contains(@id, 'Patient Portal Modules_My Appointments')]//input[@type='submit']")

        #Schedule another appointment and confirm Selenium Clinic is only option available
        login('selenium', 'selenium')
        employeeHome()
        homepageBtn('My Appointments')
        d.clickElement(xpath='//a[contains(text(),"schedule a new appointment")]')

        # Select appointment type
        Select(d.getElement(id='APPT_type')).select_by_visible_text('Pre-Placement Exam')

        wait.until(
            EC.visibility_of_element_located(
                (By.ID,'APPT_comment')
            )
        )

        Select(d.getElement(id='APPT_startdate')).select_by_visible_text('Fri 02-02-2007 10:00am (ET)')

        longWait.until(
            EC.element_to_be_clickable(
                (By.ID, 'form-save')
            )
        )
        d.clickElement(id='form-save')

        if int( # Make sure we still only have 2 appointment confirmation email document after disabling them
            d.miedb.dbQuery(
                '''
                    SELECT
                        COUNT(*) AS count
                    FROM
                        documents
                    WHERE
                        pat_id = %d AND
                        doc_type = 'EAPTC'
                ''' % (pat_id)
            ).getRes()[0]['count']
        ) == 2:
            echo('Still only 2 appointment confirmation email found after disabling them via portal setting.')
        else:
            fail('More than 2 appointment confirmation email found!')

        screen('Schedule an Appointment PO Restriction Confirm')
        d.endSection() # end 'Schedule an Appointment'

        d.startSection('My Medical Info')
        employeeHome()
        homepageBtn('My Medical Info')
        screen('My Medical Info')
        d.endSection() # -- END MMI --

        d.startSection('Monitoring Status')
        employeeHome()
        homepageBtn('Monitoring Status')
        screen('Monitoring Status')
        d.endSection()

        #Test Custom Layout
        d.startSection('Custom Layout')
        employeeHome()
        homepageBtn('Portal Custom Layout')
        d.verifyElementPresent(xpath='//h1[contains(text(), "Portal Custom Layout Test!")]')
        d.endSection()

        d.endSection() # -- END EMPLOYEE PORTAL --

        d.startSection('Employer Portal')

        d.startSection('Homepage')
        d.clickElement(id='portal-user-name')
        d.clickElement(id='goto-sv-portal')
        screen('Employer Portal Home')
        d.endSection()

        d.startSection('Message Center') # Start Message Center

        d.startSection('Answer Questionnaires')
        clickBell()
        d.clickElement(xpath='//a[contains(text(),"Send a Message")]')
        d.clickElement(id='uniform-obs_result_order_options_0')
        d.clickElement(id='uniform-obs_result_employee_options_0')
        screen('Employer Send a Message')
        d.clickElement(id='begin-msg')

        d.startSection('Verify Save for later button')

        # Verify Save for later button
        d.enterFormData('Testing the Save for later button. Employer', xpath='(//div[contains(@class, "text_type") and not(contains(@class, "collapsed"))]//input[@type="text"])[1]')
        d.enterFormData('Two items should have saved info. Employer', xpath='(//div[contains(@class, "text_type") and not(contains(@class, "collapsed"))]//input[@type="text"])[2]')
        findClick('css_selector', '.yes_btn')
        d.clickElement(xpath='//button[@class="cb-color save-progress"]') #findClick('css_selector', '.save-progress')
        longWait.until(EC.element_to_be_clickable((By.XPATH, '//a/span[contains(text(), "resume")]')))
        d.verifyElementPresent(xpath='//a/span[contains(text(), "resume")]')
        partialScreen('Supervisor save for later')
        d.clickElement(xpath='//a/span[contains(text(), "resume")]')
        d.verifyElementPresent(xpath='//input[@value="Testing the Save for later button. Employer"]')
        d.verifyElementPresent(xpath='//input[@value="Two items should have saved info. Employer"]')
        d.verifyElementPresent(xpath='//input[@type="radio" and @value="Yes" and @checked="1"]')
        submitQuestions()
        d.endSection()

        # Verify Prefill from context
        d.startSection('Prefill From Context')
        waitClick('xpath', '//a[@id="portal-header-notify" and contains(@href, "pat_id=' + str(pat_id) + '")]')
        d.clickElement(xpath='//a[contains(text(),"Send a Message")]')
        d.clickElement(id='uniform-obs_result_order_options_0')
        d.clickElement(id='uniform-obs_result_employee_options_0')
        d.clickElement(id='begin-msg')
        d.clickElement(id='uniform-obs_result_prefill_context_0')
        d.verifyElementPresent(xpath='//h2[contains(text(), "Prefill answers from document")]')
        findClick('css_selector', '.view-prefill-doc') # view-prefill-doc radio-list-preview

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, 'portal-doc-wrapper')
            )
        )

        screen('Preview prefilling document supervisor')
        d.clickElement(xpath='//button/span[contains(text(), "CONTINUE")]')
        screen('Employer Review Prefill')
        d.endSection()

        d.startSection('Employer Response Workflow')
        clickBell()
        screen('Employer Response Workflow')

        # testing superv_response permission queries
        d.miedb.dbQuery(
            '''
                DELETE FROM user_moveable_layout WHERE pat_id = 41 AND layout_name = 'Send a Message' AND module_name = 'Employer Portal Modules'
            '''
        )

        d.clickElement(xpath='//a/span[contains(text(), "begin")]')
        eleFound('id', 'portal-doc-title', wait=True)
        d.miedb.dbQuery(
            '''
                INSERT INTO user_moveable_layout (pat_id, user_id, layout_name, module_name, col_order, collapsed) VALUES (41, 0, 'Send a Message', 'Employer Portal Modules', 6, 0)
            '''
        )

        wd.refresh()

        # Testing send a message superv permissions
        answerQuestions(responsiveBreakpoint=False, mmi=False)
        screen('After superv response submitted')

        d.miedb.dbQuery(
            '''
                UPDATE
                    charttabs
                SET
                    inclusive = 0
                WHERE
                    tabname = 'Supervisor Documents'
            '''
        )

        wd.refresh()
        screen('Exclude doc_types')

        d.miedb.dbQuery(
            '''
                UPDATE
                    charttabs
                SET
                    where_clause = "DATE(service_date) > '2017-01-01' AND DATE(service_date) < '2019-02-19'"
                WHERE
                    tabname = 'Supervisor Documents'
            '''
        )

        wd.refresh()
        screen('Chart tab where clause exclude types')

        d.miedb.dbQuery(
            '''
                UPDATE
                    charttabs
                SET
                    inclusive = 1
                WHERE
                    tabname = 'Supervisor Documents'
            '''
        )

        d.endSection() # END Employer Response Workflow
        d.endSection() # END answer questionnaires
        d.endSection() # END Message Center

        d.startSection('Order Status')
        d.clickElement(id='portal-header-home') # return to portal home page
        homepageBtn('Order Status')
        screen('Supervisor Order Status')
        d.endSection() # END order status

        d.startSection('Reports')
        d.clickElement(id='portal-header-home')
        homepageBtn('Reports')
        screen('Available Reports')
        d.clickElement(text='COVID Symptom Monitoring')

        echo('Waiting for DataVis report to load')

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//td[text()="MIE-10025"]')
            )
        )

        d.verifyElementPresent(xpath='//td[text()="MIE-10025"]')
        d.verifyElementPresent(xpath='//td[text()="MIE-10008"]')
        d.verifyElementPresent(xpath='//td[text()="Anderson, Frederick"]')
        d.verifyElementPresent(xpath='//td[text()="Harris, Christine"]')

        d.endSection() # END reports
        d.startSection('Custom Questionnaire Link')
        #portal-user-menu-top portal-header-home
        d.clickElement(id='portal-header-home')
        d.clickElement(xpath='//div[@id="landing-grid"]//span[contains(text(), "Supervisor Questionnaire Link")]')
        screen('Followed Custom Questionnaire Link')
        d.clickElement(id='uniform-obs_result_employee_options_0')
        d.clickElement(id='begin-msg')
        d.verifyElementPresent(xpath='//h1[contains(text(), "Ergonomic Questionnaire")]')
        d.verifyElementPresent(xpath='//span[contains(text(), "What level of physical effort is required to do your job?")]')
        d.endSection() # END Custom Questionnaire Link
        d.endSection() # END employer portal

        d.startSection('Review Documents')

        # Verify first Portal Questionnaire document
        docSummary()
        d.clickElement(xpath='(//a[text()="Portal Questionnaire"])[1]')
        verifyDocHeaders()

        # Verify Request an Appointment document
        docSummary()
        d.clickElement(xpath='//a[contains(text(),"Questionnaire-Request an Appointment")]')
        verifyDocHeaders()
        verifyDocAnswers([
            ('Demographics', 'Hart, William S.'),
            ('Please complete the following questions', ''),
            ('Preferred day(s) of the week for your appointment', ''),
            ('Monday', 'Yes'),
            ('Preferred time of day', 'AM'),
            ('Tuesday', 'No')
        ])

        # Verify second Portal Questionnaire document
        docSummary()
        d.clickElement(xpath='(//a[text()="Portal Questionnaire"])[2]')
        verifyDocHeaders()

        # Verify remaining Questionnaire documents
        for questionnaire in questionnaires:
            docSummary()
            d.clickElement(xpath='//a[contains(text(), "Questionnaire-' + questionnaire.split(' ')[0] + '")]')

            if questionnaire == 'Lead Questionnaire':
                verifyDocAnswers([
                    ('Do you have new close contact with lead in your present job?', 'Yes'),
                    ('What percent of your time is spent in close contact with lead?', ''),
                    ('In what form is the lead?', 'Fumes'),
                    ('What is the nature of your contact with lead?', 'Sampling (tasting)'),
                    ('Where do you perform the majority of your work?', 'Inside')
                ])
            else:
                partialScreen(questionnaire + ' doc')

        d.startSection('Verify document deleted')
        docSummary()

        if len(
            d.getElements(xpath='//em[text()="Deleted"]/../..//a[text()="Questionnaire-' + patient['questionnaire_doc_type'] + '"]')
        ) == 2:
            echo('Deleted document found')
        else:
            fail('A document was not deleted as expected.')
            screen('doc not deleted')

        d.endSection() # END verify document deleted

        docSummary(anderson_id)

        d.clickElement(xpath='(//a[text()="Portal Document File Upload"])[1]')
        screen('Verify Questionnaire Doc Uploaded', widgetWait=True)

        docSummary(harris_id)
        d.clickElement(xpath='//a[contains(text(), "Questionnaire-' + supervQuestion.split(' ')[0] + '")]')
        partialScreen('Supervisor Driven Doc')
        d.endSection() # end review documents

        d.startSection('Verify Encounter status')

        if int( # querying db is much faster than breaking frameset and checking JS var
            d.miedb.dbQuery(
                '''
                    SELECT
                        COUNT(*) AS count
                    FROM
                        encounters
                    WHERE
                        pat_id = %d AND
                        closed = 1 AND
                        visit_type = 'QUESTIONS'
                ''' % (pat_id)
            ).getRes()[0]['count']
        ) == 7:
            echo('Encounters closed as expected')
        else:
            fail('One or more encounters was not closed as expected.')
            screen('encounters not closed')

        if int( # querying db is much faster than breaking frameset and checking JS var
            d.miedb.dbQuery(
                '''
                    SELECT
                        COUNT(*) AS count
                    FROM
                        encounters
                    WHERE
                        pat_id = %d AND
                        closed = 1 AND
                        deleted = 1 AND
                        visit_type = 'QUESTIONS'
                ''' % (pat_id)
            ).getRes()[0]['count']
        ) == 3:
            echo('Deleted and closed encounter found')
        else:
            fail('An encounter was not closed and deleted as expected.')
            screen('encounter not closed and deleted')

        d.endSection() # End verify encounter status

    except Exception as e:
        fail(e)
    finally:
        # Regardles of what the size is, when we end the test, set the
        # window size back to the default.
        resetWinSize()
        d._driver.fullscreen_window()
