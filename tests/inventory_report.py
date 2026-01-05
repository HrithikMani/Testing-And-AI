# 
# Webchart Inventory Reports UnitTest

def main(driver, WCURL):

    d = driver
	
    if d.getUserData('inventory_failure'):
        d.reportCommandStatus('','',False,'','Prior Inventory Error - Skipping Test')
        return
		
    d.navigate(WCURL.INVENTORY_REPORT,auto_screenshot=False)


    d.screenshot('NoSearchParams')

    d.enterAutocomplete('search_username_ac','Dav',0) # need better id
    d.clickElement(name='search')
    d.screenshot('SearchDave')

    d.clickElement(name='searchClear')
    d.enterAutocomplete('search_username_ac','Sel',0) # need better id
    d.clickElement(name='search')
    d.screenshot('SearchSelenium')

    d.enterAutocomplete('tS_p_pat_id_patac','Cart',0)
    d.clickElement(name='search')
    d.screenshot('SearchSeleniumCarter')

    d.enterAutocomplete('tS_p_pat_id_patac','Hart',0)
    d.clickElement(name='search')
    d.screenshot('SearchSeleniumCarterHart')

    d.enterFormData(True,xpath="//input[@type='radio' and @name='reportMethod' and @value='1']")
    d.enterMIEDateString('tS_tdate','02-03-2007 16:20')
    d.enterMIEDateString('tS_fdate','02-01-2007 16:20')
    d.clickElement(name='search')
    d.screenshot('SearchTrend')

    d.clickElement(xpath="//input[@alt='Plot Values']")
    if d.switchToPopup():
        d.screenshot('SearchTrendPlot')


