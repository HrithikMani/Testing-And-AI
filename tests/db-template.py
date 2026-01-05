#
# Webchart Database Test Template
#
from dbtest import SelectTest

def main (d, WCURL):
    """
    Database test
    """

    """
    Populate 'test_dict' with your column and row results. The template will
    handle the rest.

    test_dict['select'] is an array of tuples. Each tuple consists of column
    name, and an array of row values.

    e.g. ("user_id", ['1', '2', '3'])

    This is read as: For column 'user_id' in this query, expect value '1' for
    row 1, value '2' for row 2, etc.

    If the returned value does not match the given value, the test fails.

    test_dict['expr'] is a select_expr that can be used to define conditions
    for the query.

    test_dict['count'] optionally verifies the number of rows returned.

    This example test_dict will generate this query:
    'SELECT user_id, column_2 FROM table_name WHERE user_id > 0'

    Expected rows returned:
    1: user_id '1', column_2 'row1 value'
    2: user_id '2', column_2 'row2 value'
    3: user_id '3', column_2 'row3 value'
    """

    test_dict = { 'select': [("user_id",
                              ['1',
                               '2',
                               '3']),
                             ("column_2",
                              ['row1 value',
                               'row2 value',
                               'row3 value']),],
                  'expr': 'FROM table_name WHERE user_id > 0',
                  'count': 3 }

    # We are testing the database, screenshots of the browser are not useful here
    d.setScreenShotOnError(False)

    try:
        query_test = SelectTest(d, test_dict)
    except ValueError as e:
        d.addErrorMessage('Error creating test object: %s' % e)
        return

    try:
        query_test.run_query()

        # Display results from row count, if defined
        if query_test.count_error():
            d.startSection('Incorrect number of rows returned')
            d.reportCommandStatus('count_error', 'Given: %d' % query_test.expected_count(), False, 'Returned: %d' % query_test.count(), '')
            d.endSection()

        # Display results from columns returned
        for field, rows in query_test.status():
            d.startSection('Column: ' + field)
            for row in rows:
                d.reportCommandStatus('status', row['given_value'], row['passed'], row['return_value'], '')
            d.endSection()
    except Exception as e:
        d.addErrorMessage('Error running query: %s' % e)
        return
