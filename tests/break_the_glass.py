# 
# Webchart Emergency Access (Break the glass) testing
#
def main (d, WCURL):
    """
    Search and view patients with Emergency Access
    """

    d.navigate(WCURL.SECURITY_ROLES)
    if d.clickElement(xpath="//div[@id='lv_securityroles_span']/table/tbody[2]/tr/td[3]/font/a/font[text()='Edit']"):
        d.enterFormData('2', name='E-Chart_Limited Access')
        d.enterFormData('Giving Administrator Emergency Access', id='sec_role_comment')
        if d.clickElement(name='rolechange'):
            d.navigate(WCURL.ECHART)
            d.enterFormData('hart', name='sstring')
            if d.clickElement(name='pat_search'):
                d.screenshot('EA_accessible_search')
                if d.clickElement(xpath="//div[@id='lv_lv_ps_results_span']/table/tbody[2]/tr/td/font/a/font[text()='MIE-10019']"):
                    d.screenshot('EA_accessible_chart')
                else:
                    d.addErrorMessage("Unable to find accessible patient")
                d.navigate(WCURL.ECHART)
                if d.clickElement(id='show_rest_pats'):
                    d.enterFormData('hart', name='sstring')
                    if d.clickElement(name='pat_search'):
                        d.screenshot('EA_restricted_search')
                        if d.clickElement(xpath="//div[@id='lv_lv_ps_results_span']/table/tbody[2]/tr/td/font/a/font[text()='HOSPITAL-495653']"):
                            d.screenshot('EA_restricted_chart')
                            if d.clickElement(xpath="//div[@id='wc_main']//font[2]/h3/div/a/font[text()='here']"):
                                d.verifyAlert('You asked for "Emergency Access", are you sure?')
                                d.screenshot('EA_restricted_chart_access')
                            else:
                                d.addErrorMessage("Unable to gain Emergency Access, can't find link")
                        else:
                            d.addErrorMessage("Unable to find restricted chart")
                    else:
                        d.addErrorMessage("Unable to submit patient search")
                else:
                    d.addErrorMessage("Unable to search restricted patients")
                d.navigate(WCURL.ECHART)
                if d.clickElement(xpath="//form[@id='patsearch']/table/tbody/tr/td/font/a[2]/font[text()='Document Search']"):
                    d.screenshot('EA_accessable_doc_search')
                    if d.clickElement(id='sdoc_type_dropdownarrow'):
                        if d.clickElement(xpath="//div[@id='sdoc_type_list_div']//div/nobr/a[text()='Select All']"):
                            if d.clickElement(name='pat_search'):
                                d.screenshot('EA_accessable_doc_search_results')
                                if d.clickElement(xpath="//div[@id='lv_getdoc_span']/table/tbody[2]/tr[2]/td[2]/font/a/font[text()='0000030']"):
                                    d.screenshot('EA_accessable_doc')
                                else:
                                    d.addErrorMessage("Unable to find document")
                            else:
                                d.addErrorMessage("Unable to submit document search form")
                        else:
                            d.addErrorMessage("Unable to select all document types for searching")
                    else:
                        d.addErrorMessage("Unable to find doc type dropdown")
                else:
                    d.addErrorMessage("Unable to find 'Document Search' link on E-Chart")

                d.navigate(WCURL.ECHART)
                if d.clickElement(xpath="//form[@id='patsearch']/table/tbody/tr/td/font/a[2]/font[text()='Document Search']"):
                    d.screenshot('EA_restricted_doc_search')
                    if d.clickElement(id='sdoc_type_dropdownarrow'):
                        if d.clickElement(xpath="//div[@id='sdoc_type_list_div']//div/nobr/a[text()='Select All']"):
                            if d.clickElement(id='show_rest_accts'):
                                if d.clickElement(name='pat_search'):
                                    d.screenshot('EA_restricted_doc_search_results')
                                    if d.clickElement(xpath="//div[@id='lv_getdoc_span']/table/tbody[2]/tr[3]/td[2]/font/a/font[text()='0000007']"):
                                        d.screenshot('EA_restricted_doc')
                                        if d.clickElement(xpath="//div[@id='wc_main']//font[2]/h3/div/a/font[text()='here']"):
                                            d.verifyAlert('You asked for "Emergency Access", are you sure?')
                                            d.screenshot('EA_restricted_doc_access')
                                        else:
                                            d.addErrorMessage("Unable to go to restricted document")
                                    else:
                                        d.addErrorMessage("Unable to find document")
                                else:
                                    d.addErrorMessage("Unable to submit document search form")
                            else:
                                d.addErrorMessage("Unable to search for restricted documents")
                        else:
                            d.addErrorMessage("Unable to select all document types for restricted searching")
                    else:
                        d.addErrorMessage("Unable to find doc type dropdown")
                else:
                    d.addErrorMessage("Unable to find 'Document Search' link on E-Chart")

                d.navigate(WCURL.SECURITY_ROLES)
                if d.clickElement(xpath="//div[@id='lv_securityroles_span']/table/tbody[2]/tr/td[3]/font/a/font[text()='Edit']"):
                    d.enterFormData('1', name='E-Chart_Allow Unrestricted Pat Search')
                    d.enterFormData('Giving Administrator Unrestricted Patient Searching', id='sec_role_comment')
                    if d.clickElement(name='rolechange'):
                        d.navigate(WCURL.ECHART)
                        if d.clickElement(id='show_rest_pats'):
                            d.enterFormData('hart', name='sstring')
                            if d.clickElement(name='pat_search'):
                                d.screenshot('EA_unrestricted_restricted_search')
                            else:
                                d.addErrorMessage("Unable to submit restricted patient search")
                        else:
                            d.addErrorMessage("Unable to search restricted patients")
                    else:
                        d.addErrorMessage("Unable to Edit 'Administrator' Security Role for 'Unrestricted Pat Search'")
                else:
                    d.addErrorMessage("Unable to Edit 'Administrator' Security Role for 'Unrestricted Pat Search'")
            else:
                d.addErrorMessage("Unable to submit patient search form")
        else:
            d.addErrorMessage("Unable to submit Security Role Editor")
    else:
        d.addErrorMessage("Unable to Edit 'Administrator' Security Role for 'Emergency Access'")
