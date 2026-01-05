from wcunittest import wcElement

STORAGE_TYPE = 4    # html storage type
DOC_TYPE = 'VISIT'  # generic html doc type
PAT_ID = 18         # William Hart's chart

def setSystemSetting(d, args):
    args.append(False)
    d.wcutils.SetSystemSetting(*args)

def setSecurityPermission(d, args):
    args.append(False)
    d.wcutils.SetPermission(*args)

def main(d, WCURL):
    u = d.getWCUnitTest('Upload an html document using the file upload method')
    u.setup(lambda d: d.navigate('?f=chart&s=doc&opp=add&pat_id={0}&filter=file&storage_type={1}'.format(PAT_ID,STORAGE_TYPE)), reason='Visit the file upload page')
    u.setup(lambda d: d.enterFormData('printDocument.html', name='file'), reason='Select the sample html document')
    u.setup(lambda d: d.enterFormData(DOC_TYPE, name='doc_type'), reason='Set the Document Type')
    u.verifyElements([
        wcElement('xpath', "//span[contains(@class, 'information') and contains(., 'has been uploaded successfully!')]"),
        wcElement('xpath', "//div[contains(@class, 'document_wrapper')]"),
        wcElement('value', 'Search Document'),
    ], reason='Ensure upload succeeded with expected elements')
    u.test(lambda d: d.clickElement(value='Add Document'), reason='Upload it')

    u = d.getWCUnitTest('Upload the html document with CSS')
    u.setup(lambda d: d.navigate('?f=chart&s=doc&opp=add&pat_id={0}&filter=file&storage_type={1}'.format(PAT_ID,STORAGE_TYPE)), reason='Visit the file upload page')
    u.setup(lambda d: d.enterFormData('printDocumentCSS.html', name='file'), reason='Select the sample html document')
    u.setup(lambda d: d.enterFormData(DOC_TYPE, name='doc_type'), reason='Set the Document Type')
    u.verifyElements([
        wcElement('xpath', "//span[contains(@class, 'information') and contains(., 'has been uploaded successfully!')]"),
        wcElement('xpath', "//div[contains(@class, 'document_wrapper')]"),
        wcElement('value', 'Search Document'),
    ], reason='Ensure upload succeeded with expected elements')
    u.test(lambda d: d.clickElement(value='Add Document'), reason='Upload it')

    # Get the id of the document we just uploaded
    res = d.miedb.dbQuery("SELECT doc_id FROM documents WHERE storage_type=%s ORDER BY doc_id DESC LIMIT 2", STORAGE_TYPE);
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['doc_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    cssdoc_id = res.getRow(0)['doc_id']
    doc_id = res.getRow(1)['doc_id']

    u = d.getWCUnitTest('Print the document with WebKit as the default rendering engine')
    u.setup(setSystemSetting, ['E-Chart', 'HTML Printing', 'Rendering Engine', '1'], reason='Set the system setting')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a print')
    u.setup(lambda d: d.pause(7), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('WebKit Document'), reason='Screenshot the result')

    u = d.getWCUnitTest('Print the document with Gecko as the default rendering engine')
    u.setup(setSystemSetting, ['E-Chart', 'HTML Printing', 'Rendering Engine', '2'], reason='Set the system setting')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a print')
    u.setup(lambda d: d.pause(15), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Gecko Document'), reason='Screenshot the result')

    u = d.getWCUnitTest('Print the CSS document with WebKit')
    u.setup(setSystemSetting, ['E-Chart', 'HTML Printing', 'Rendering Engine', '1'], reason='Set the system setting')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(cssdoc_id)), reason='Request a print')
    u.setup(lambda d: d.pause(7), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('CSS Webkit Document'), reason='Screenshot the result')

    u = d.getWCUnitTest('Stream the document straight to PDF with WebKit')
    u.setup(setSystemSetting, ['E-Chart', 'HTML Printing', 'Rendering Engine', '1'], reason='Set the system setting')
    u.setup(lambda d: d.navigate('?f=stream&doc_id={0}&pdf_rawdata=1'.format(doc_id)), reason='Stream document as PDF')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('WebKit PDF'), reason='Screenshot the result')

    u = d.getWCUnitTest('Stream a TIFF document straight to PDF')
    u.setup(setSystemSetting, ['E-Chart', 'HTML Printing', 'Rendering Engine', '1'], reason='Set the system setting')
    u.setup(lambda d: d.navigate('?f=stream&doc_id=172&pdf_rawdata=1'.format(doc_id)), reason='Stream TIFF document as PDF')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('WebKit PDF'), reason='Screenshot the result')

    u = d.getWCUnitTest('Verify legacy rendering of html when the only content is a span with textContent')
    u.setup(lambda d: d.miedb.dbExec("UPDATE documents_txt SET txt_value='<span>I should be visible</span>' WHERE doc_id=%s", doc_id), reason='Make the document have a single span with text and nothing else')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--&print_legacy_html_render'.format(doc_id)), reason='Request a legacy print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Legacy Span Edge Case'), reason='Screenshot the result')

    # Test printing an XML document from printDocumentStyled.xml
    # u = d.getWCUnitTest('Add an XML document and layout stylesheel')
    # layout_html = d.wcutils.readFile('printDocumentXMLStylesheetPROG.html')
    # u.setup(lambda d: d.miedb.dbExec("INSERT INTO layout SET module='Stylesheet',name='PROG',layout_html={0}".format(layout_html)),reason='Create XML style sheet layout for PROG')
    # u.setup(lambda d: d.navigate('?f=chart&s=doc&opp=add&pat_id={0}&filter=file'.format(PAT_ID)), reason='Visit the file upload page')
    # u.setup(lambda d: d.enterFormData('printDocumentStyled.xml', name='file'), reason='Select the sample xml document')
    # u.setup(lambda d: d.enterFormData('PROG', name='doc_type'), reason='Set the Document Type')
    # u.verifyElements([
    #     wcElement('xpath', "//span[contains(@class, 'information') and contains(., 'has been uploaded successfully!')]"),
    #     wcElement('xpath', "//div[contains(@class, 'document_wrapper')]"),
    #     wcElement('value', 'Search Document'),
    # ], reason='Ensure upload succeeded with expected elements')
    # u.test(lambda d: d.clickElement(value='Add Document'), reason='Upload it')

    # # Get the id of the document we just uploaded
    # res = d.miedb.dbQuery("SELECT doc_id FROM documents WHERE storage_type=27 ORDER BY doc_id DESC LIMIT 1");
    # if not res:
    #     d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
    #     return
    # if not res.getRow(0) or not res.getRow(0)['doc_id']:
    #     d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
    #     return
    # doc_id = res.getRow(0)['doc_id']

    # u = d.getWCUnitTest('Print the document with WebKit as the default rendering engine')
    # u.setup(setSystemSetting, ['E-Chart', 'HTML Printing', 'Rendering Engine', '1'], reason='Set the system setting')
    # u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a print')
    # u.setup(lambda d: d.pause(7), reason='Let the print render and reload')

    # Document Restrictions tests

    # Get the selenium user id
    res = d.miedb.dbQuery("(SELECT user_id FROM users WHERE username=%s)",d.getUserData('selenium_username'))
    if not res:
        d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
        return
    if not res.getRow(0) or not res.getRow(0)['user_id']:
        d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
        return
    USER_ID = res.getRow(0)['user_id']

    u = d.getWCUnitTest('Print with Revoked PHI')
    u.setup(setSecurityPermission, ['WebChart', 'Revoke PHI Access', '1'], reason='Revoke PHI access')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(setSecurityPermission, ['WebChart', 'Revoke PHI Access', '0'], reason='Reset PHI access')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print without PHI Access'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print without Document View')
    u.setup(setSecurityPermission, ['E-Chart', 'Document Permissions', '0'], reason='Revoke the permission')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print without Document View'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with Document View')
    u.setup(setSecurityPermission, ['E-Chart', 'Document Permissions', '3'], reason='Grant the permission')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Print with Document View'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restricted Document Type, non-allowed')
    u.setup(lambda d: d.miedb.dbExec("UPDATE document_types SET restricted=1 WHERE doc_type=%s", DOC_TYPE), reason='Restrict the Doc Type')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print Restricted Document Type'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with Restricted Document Type, allowed')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO document_types_restricted (doc_type,allowed_id,id_type) VALUES (%s,%s,'user')",DOC_TYPE,USER_ID), reason='Grant restriction access')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Print allowed Restricted Document Type'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Limited to Restricted and Restricted, allowed Document Type')
    u.setup(setSecurityPermission, ['E-Chart', 'Limited to Restricted Items', '1'], reason='Set the permission')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print with Limited, allowed access'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Limited to Restricted and Restricted, non-allowed Document Type')
    u.setup(lambda d: d.miedb.dbExec("DELETE FROM document_types_restricted WHERE doc_type=%s AND allowed_id=%s AND id_type='user'",DOC_TYPE,USER_ID), reason='Remove restriction access')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print with Limited, restricted Restricted Document Type'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with Limited To Restricted and Unrestricted Document Type')
    u.setup(lambda d: d.miedb.dbExec("UPDATE document_types SET restricted=0 WHERE doc_type=%s", DOC_TYPE), reason='Un-Restrict the Doc Type')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(setSecurityPermission, ['E-Chart', 'Limited to Restricted Items', '0'], reason='Clear the permission')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print with Limited, Un-Restricted Document Type, no-access'), reason='Screenshot the failed result')

    # Get the id of our default charttab
    DEFTABNAME = d.wcutils.GetPreference(d.getUserData('selenium_username'),'E-Chart','Defaults','Starting Folder')
    if DEFTABNAME:
        res = d.miedb.dbQuery("SELECT ctab_id FROM charttabs WHERE tabname=%s", DEFTABNAME)
        if not res:
            d.reportCommandStatus('dbQuery Failed', '', False, d.miedb.dbError(), '')
            return
        if not res.getRow(0) or not res.getRow(0)['ctab_id']:
            d.reportCommandStatus('dbQuery returned no results', '', False, '', '')
            return
        DEFCTAB = res.getRow(0)['ctab_id']
    else:
        d.reportCommandStatus('Default Tabname not found', '', False, '', '')
        return

    u = d.getWCUnitTest('Print with Limited to Default Tab, not in tab')
    u.setup(setSecurityPermission, ['E-Chart', 'Limited to Default Tab', '0'], reason='Set the permission')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print Document not on Default Tab'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with Limited to Default Tab, in tab')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO charttab_doctypes (ctab_id,doc_type) VALUES (%s,%s)",DEFCTAB,DOC_TYPE), reason='Add Doc Type to exclusive ChartTab')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM charttab_doctypes WHERE ctab_id=%s AND doc_type=%s",DEFCTAB,DOC_TYPE), reason='DB Cleanup')
    u.teardown(setSecurityPermission, ['E-Chart', 'Limited to Default Tab', '1'], reason='DB Cleanup')
#    u.test(lambda d: d.screenshot('Print allowed Default Tab Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, unsigned, author')
    u.setup(setSecurityPermission, ['E-Chart', 'View Preliminary Documents', '0'], reason='Set the permission')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Print Unsigned Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, requested, author')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO document_sign (doc_id,revision_number,request_user_id,signer_id,status) VALUES (%s,0,5,25,0)",doc_id), reason='Request a Signature')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Print restricted Preliminary Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, signed, author')
    u.setup(lambda d: d.miedb.dbExec("UPDATE document_sign SET status=1 WHERE doc_id=%s AND revision_number=0 AND signer_id=25",doc_id), reason='Sign the Document')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM document_sign WHERE doc_id=%s",doc_id), reason='DB Cleanup')
#    u.test(lambda d: d.screenshot('Print Signed Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, unsigned, non-author')
    u.setup(lambda d: d.miedb.dbExec("UPDATE documents SET origin_id=25,user_id=25 WHERE doc_id=%s",doc_id), reason='Change the Document Author')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print NA Unsigned Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, requested, non-author')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO document_sign (doc_id,revision_number,request_user_id,signer_id,status) VALUES (%s,1,5,25,0)",doc_id), reason='Request a Signature')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print NA restricted Preliminary Document'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, signed, non-author')
    u.setup(lambda d: d.miedb.dbExec("UPDATE document_sign SET status=1 WHERE doc_id=%s AND revision_number=1 AND signer_id=25",doc_id), reason='Sign the Document')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM document_sign WHERE doc_id=%s",doc_id), reason='DB Cleanup')
    u.teardown(lambda d: d.miedb.dbExec("UPDATE documents SET origin_id=%s,user_id=%s WHERE doc_id=%s",USER_ID,USER_ID,doc_id), reason='Reset the Document Author')
    u.teardown(setSecurityPermission, ['E-Chart', 'View Preliminary Documents', '1'], reason='Clear the permission')
#    u.test(lambda d: d.screenshot('Print NA Signed Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, requested, requester')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO document_sign (doc_id,revision_number,request_user_id,signer_id,status) VALUES (%s,2,%s,25,0)",doc_id,USER_ID), reason='Request a Signature')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request a restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print Req restricted Preliminary Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with Restrict Preliminary, signed, requester')
    u.setup(lambda d: d.miedb.dbExec("UPDATE document_sign SET status=1 WHERE doc_id=%s AND revision_number=2 AND signer_id=25",doc_id), reason='Sign the Document')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request an allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d: d.miedb.dbExec("DELETE FROM document_sign WHERE doc_id=%s",doc_id), reason='DB Cleanup')
    u.teardown(setSecurityPermission, ['E-Chart', 'View Preliminary Documents', '1'], reason='Clear the permission')
#    u.test(lambda d: d.screenshot('Print Req Signed Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with NMC Only, not portal linked')
    u.setup(setSecurityPermission, ['WebChart', 'NMC only', '1'], reason='Set the permission')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request restricted print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Print Document w/o portal setup'), reason='Screenshot the No Access message')
#https://zeus-web.med-web.com/webchart/wct98074/webchart.cgi?set_focus_to&f=chart&s=print&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--&doc_id=541

    u = d.getWCUnitTest('Print with NMC Only, portal linked, not document linked')
    u.setup(setSecurityPermission, ['WebChart', 'NMC only', '1'], reason='Set the permission')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO user_patients SET id=%s,id_type='user',pat_id=%s,role_id=1",USER_ID,PAT_ID),reason='Portal Setup - Self')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO user_patients SET id=%s,id_type='user',pat_id=%s,role_id=501",USER_ID,PAT_ID),reason='Portal Setup - 501')
    u.setup(lambda d: d.miedb.dbExec("INSERT INTO pat_pat_relations SET pat_id=%s,relation_type_id=15,related_pat_id=41",PAT_ID),reason='Portal Setup - PO')
    u.setup(lambda d: d.miedb.dbExec("UPDATE session_extended_values SET value=43 WHERE session_id='WCTESTSESSION' AND name='cobrand_pat_id'"),reason='Link Session to PO')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
#    u.test(lambda d: d.screenshot('Print portal Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with NMC Only, datasend_route linked, source patient')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO datasend_route (item_type,item_id,item_sub_id,recipient_id,active) VALUES ('doc',%s,0,25,1)",doc_id), reason='Create Datasend Route')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO user_patients (id,id_type,role_id,pat_id) VALUES (25,'user',11,%s)",PAT_ID), reason='Create recipient user_patient relation')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO user_patients (id,id_type,role_id,pat_id) VALUES (%s,'user',11,%s)",USER_ID,PAT_ID), reason='Create my user_patient relation')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM datasend_route WHERE item_type='doc' AND item_id=%s",doc_id),reason='DB Cleanup')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM user_patients WHERE id=25 AND id_type='user' AND pat_id=%s AND role_id=11",PAT_ID),reason='DB Cleanup')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM user_patients WHERE id=%s AND id_type='user' AND pat_id=%s AND role_id=11",USER_ID,PAT_ID),reason='DB Cleanup')
#    u.test(lambda d: d.screenshot('Print source DS linked Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with NMC Only, datasend_route linked, other patient')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO datasend_route (item_type,item_id,item_sub_id,recipient_id,active) VALUES ('doc',%s,0,25,1)",doc_id), reason='Create Datasend Route')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO user_patients (id,id_type,role_id,pat_id) VALUES (25,'user',11,27)"), reason='Create recipient user_patient relation')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO user_patients (id,id_type,role_id,pat_id) VALUES (%s,'user',11,27)",USER_ID), reason='Create my user_patient relation')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM datasend_route WHERE item_type='doc' AND item_id=%s",doc_id),reason='DB Cleanup')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM user_patients WHERE id=25 AND id_type='user' AND pat_id=27 AND role_id=11"),reason='DB Cleanup')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM user_patients WHERE id=%s AND id_type='user' AND pat_id=27 AND role_id=11",USER_ID),reason='DB Cleanup')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print other DS linked Document'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with NMC Only, role linked')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO user_patients (id,id_type,role_id,pat_id) VALUES (%s,'user',11,%s)",USER_ID,PAT_ID), reason='Create my user_patient relation')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM user_patients WHERE id=%s AND id_type='user' AND pat_id=%s AND role_id=11",USER_ID,PAT_ID),reason='DB Cleanup')
#    u.test(lambda d: d.screenshot('Print associated Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with NMC Only, PO linked')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO user_patients (id,id_type,role_id,pat_id) VALUES (%s,'user',11,27)",USER_ID), reason='Link to my PO')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO pat_pat_relations (pat_id,related_pat_id,relation_type_id) VALUES (%s,27,100)",PAT_ID), reason='Relate Patient to PO')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM user_patients WHERE id=%s AND id_type='user' AND pat_id=27 AND role_id=11",USER_ID),reason='DB Cleanup')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM pat_pat_relations WHERE pat_id=%s AND related_pat_id=27 AND relation_type_id=100",PAT_ID),reason='DB Cleanup')
#    u.test(lambda d: d.screenshot('Print PO access Document'), reason='Screenshot the successful result')

    u = d.getWCUnitTest('Print with NMC Only, Portal Supervisor linked')
    # todo

    u = d.getWCUnitTest('Print with datasend_route recipient, author')
    u.setup(setSecurityPermission, ['E-Chart', 'Restrict by Document Send', '1'], reason='Set the permission')
    u.setup(lambda d: d.miedb.dbExec("INSERT IGNORE INTO datasend_route (item_type,item_id,item_sub_id,recipient_id,active) VALUES ('doc',%s,2,%s,1)",doc_id,USER_ID), reason='Create Datasend Route')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    d.wcErrorLog.ignore('(4070)Document access denied!')
#    u.test(lambda d: d.screenshot('Print as author recipient of Document'), reason='Screenshot the failed result')

    u = d.getWCUnitTest('Print with datasend_route recipient, non-author')
    u.setup(lambda d: d.miedb.dbExec("UPDATE documents SET origin_id=25 WHERE doc_id=%s",doc_id), reason='Change the Document Author')
    u.setup(lambda d: d.navigate('?set_focus_to&f=chart&s=print&doc_id={0}&print_reason&print_send_method=0&print_render_in_detail=1&print_printer_name=My+Computer&print_priority=2&print_submit_print=--+Print+--'.format(doc_id)), reason='Request allowed print')
    u.setup(lambda d: d.pause(6), reason='Let the print render and reload')
    u.teardown(lambda d:d.miedb.dbExec("DELETE FROM datasend_route WHERE item_id=%s AND item_type='doc' AND recipient_id=%s",doc_id,USER_ID),reason='DB Cleanup')
    u.teardown(lambda d: d.miedb.dbExec("UPDATE documents SET origin_id=%s WHERE doc_id=%s",USER_ID,doc_id), reason='Reset the Document Author')
    u.teardown(setSecurityPermission, ['E-Chart', 'Restrict by Document Send', '0'], reason='Clear the permission')
    u.teardown(setSecurityPermission, ['WebChart', 'NMC only', '0'], reason='Clear the permission')
#    u.test(lambda d: d.screenshot('Print as non-author recipient of Document'), reason='Screenshot the successful result')
