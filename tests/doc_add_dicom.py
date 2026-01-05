def main(d, WCURL):
    """
    Verifies the functionality of uploading a DICOM document
    """
    DICOM_SETUP = '?f=dicom&dcfunc=aeedit&tabmodule=admin&tabselect=Dicom+Setup'
    d.navigate(DICOM_SETUP)

    d.clickElement(text='View Application Entities')
    d.clickElement(text='Add Entity')
    d.enterFormData('WCPRINT', name='title')
    d.clickElement(id='submit_ae')

    d.navigate(WCURL.CHART_HART_WILLIAM)
    d.clickElement(text='Add Document')
    d.clickElement(text='File')
    d.enterFormData('DICOM Image', id='storage_type')
    
    d.enterFormData('Selenium DICOM Test', id='subject')
    d.enterFormData('SeleniumDicom.dcm', name='file')
    d.clickElement(name='submit_document')
    d.screenshot("DICOM Document Preview")


