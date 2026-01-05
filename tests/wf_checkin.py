def main(d, WCURL):
    """
    Test the checkin process using different methods
    """

    d.wcutils.resetSystem()

    query = "UPDATE appointments SET startdate='2010-01-01 00:00:00'"
    if not d.miedb.dbExec(query):
        d.addErrorMessage(d.miedb.dbError())
        d.reportCommandStatus('dbExec', query, False, '', d.miedb.dbError())
        return

    d.wcutils.insertWCTSession()
    d.navigate(WCURL.OMNISCOPE, report=False)
    
    #$ One Click Checkin
    d.clickElement(text='Scheduler')
    d.enterMIEDate('date',1,1,2010)
    d.clickElement(value='Go')
    d.screenshot('Appointments')
    d.clickElement(xpath="//b[contains(text(),'Hart, William S')]/parent::font/parent::a/parent::font/parent::div/following-sibling::font//a[text()='Checkin']")
    d.verifyAlert('*Do not release info to siblings.')
    d.screenshot('ApppointmentsAfterCheckin')
    
    #$ Checkin From Scheduler
    # Turn off One-click checkin
    if d.wcutils.SetPreference('Scheduler','One-Click Checkin','Use One-Click Checkin',0):
        d.clickElement(text='Scheduler')
        d.enterMIEDate('date',1,1,2010)
        d.clickElement(value='Go')
        d.clickElement(xpath="//b[contains(text(),'Pregnant, Jennifer')]/parent::font/parent::a/parent::font/parent::div/following-sibling::font//font[text()='Checkin']")
        d.screenshot('CheckinScreenBeforeData')
        d.enterFormData('Office Visit-Initial',id='patient_type')
        d.enterMIEDate('serv_date',1,1,2010)
        d.enterFormData('Office',id='location')
        d.enterFormData('Patient checked in by selenium',id='comment')
        d.enterFormData('Waiting Room', id='station_id')
        d.screenshot('CheckinScreenAfterData')
        d.clickElement(value='Save')
        d.screenshot('CheckinScreen')
