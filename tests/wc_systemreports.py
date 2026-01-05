# 
# Webchart System Reports UnitTest
#
def main (driver, WCURL):
    d = driver

    # Open the system reports page
    d.navigate(WCURL.SYSTEM_REPORTS)

    # Set up our values to use for a new system report
    report_name = 'Selenium Report'
    report_desc = 'Selenium Report Desc'
    report_cat = 'Selenium Category'
    report_notes = 'Selenium Report Notes'
    report_sql = "Select CONCAT(p.last_name,', ',p.first_name) from patients p where p.email LIKE '%selenium%'"

    # Now let's click the 'Add Report' link
    d.clickElement(text='Add Report')

    # Fill out a bunch of system report stuff
    d.enterFormData(report_name,id='report_name')
    d.enterFormData(report_desc,id='report_description')
    d.enterFormData(report_notes,id='report_notes')

    # This will open a jsWindow but our API should wait for our form inputs to appear
    # so we should be ok without explicitly waiting for a jswindow to appear
    d.enterFormData('Add New Category',id='report_category')
    d.enterFormData(report_cat,id='new_cat_name')
    d.clickElement(value='Add Category')

    d.enterFormData(report_sql,id='report_sql_query')

    d.clickElement(id='submit_add_explain')

    # Now search for the report we just created
    d.enterFormData(report_name, id='search_value')
    d.clickElement(value='Search')

    # Now run the report
    d.clickElement(id=report_name+'_run_link')

    # Now let's edit the report to make sure all of our original values stuck
    d.clickElement(text='Back to System Report')
    d.enterFormData(report_name, id='search_value')
    d.clickElement(value='Search')
    d.clickElement(id=report_name+'_edit_link')
    d.verifyAttribute('value',report_name,id='report_name')
    d.verifyAttribute('value',report_desc,id='report_description')
    d.verifyAttribute('value',report_notes,id='report_notes')
    d.verifyAttribute('value',report_sql,id='report_sql_query')
    d.verifyAttribute('value',report_cat,id='report_category')

    # Now let's delete the report so that this test could be run again
    d.clickElement(text='Back to System Report')
    d.enterFormData(report_name, id='search_value')
    d.clickElement(value='Search')
    d.clickElement(id=report_name+'_delete_link')
    d.clickElement(value='Yes')
