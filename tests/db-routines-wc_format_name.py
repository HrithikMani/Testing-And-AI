#
# Webchart Database Test
#
from dbtest import SelectTest

def main (d, WCURL):
    """
    Database routine wc_format_name

    Tests non-legal and legal forms
     - Missing one element, Missing section, Only section, Nothing
    """

    test_dict = { 'select': [("wc_format_name('Sample', 'John', 'M.', '', 'M.D.', 'Sr', 0)",
                              ['Sample Sr, M.D., John M.']),
                             ("wc_format_name('', 'John', 'M.', '', 'M.D.', 'Sr', 0)",
                              ['Sr, M.D., John M.']),
                             ("wc_format_name('Sample', '', 'M.', '', 'M.D.', 'Sr', 0)",
                              ['Sample Sr, M.D., M.']),
                             ("wc_format_name('Sample', 'John', '', '', 'M.D.', 'Sr', 0)",
                              ['Sample Sr, M.D., John']),
                             ("wc_format_name('Sample', 'John', 'M.', '', '', 'Sr', 0)",
                              ['Sample Sr, John M.']),
                             ("wc_format_name('Sample', 'John', 'M.', '', 'M.D.', '', 0)",
                              ['Sample, M.D., John M.']),

                             ("wc_format_name('Sample', '', '', '', 'M.D.', 'Sr', 0)",
                              ['Sample Sr, M.D.']),
                             ("wc_format_name('', 'John', 'M.', '', 'M.D.', '', 0)",
                              ['M.D., John M.']),

                             ("wc_format_name('', '', '', '', 'M.D.', '', 0)",
                              ['M.D.']),
                             ("wc_format_name('Sample', '', '', '', '', 'Sr', 0)",
                              ['Sample Sr']),
                             ("wc_format_name('', 'John', 'M.', '', '', '', 0)",
                              ['John M.']),

                             ("wc_format_name('', '', '', '', '', '', 0)",
                              ['']),

                             ("wc_format_name('Sample', 'John', 'M.', 'T', 'M.D.', 'Sr', 1)",
                              ['T John M. Sample Sr, M.D.']),
                             ("wc_format_name('', 'John', 'M.', 'T', 'M.D.', 'Sr', 1)",
                              ['T John M. Sr, M.D.']),
                             ("wc_format_name('Sample', '', 'M.', 'T', 'M.D.', 'Sr', 1)",
                              ['T M. Sample Sr, M.D.']),
                             ("wc_format_name('Sample', 'John', '', 'T', 'M.D.', 'Sr', 1)",
                              ['T John Sample Sr, M.D.']),
                             ("wc_format_name('Sample', 'John', 'M.', '', 'M.D.', 'Sr', 1)",
                              ['John M. Sample Sr, M.D.']),
                             ("wc_format_name('Sample', 'John', 'M.', 'T', '', 'Sr', 1)",
                              ['T John M. Sample Sr']),
                             ("wc_format_name('Sample', 'John', 'M.', 'T', 'M.D.', '', 1)",
                              ['T John M. Sample, M.D.']),

                             ("wc_format_name('', '', '', '', 'M.D.', '', 1)",
                              ['M.D.']),

                             ("wc_format_name('', '', '', '', '', '', 1)",
                              [''])
                            ], }

    d.setScreenShotOnError(False)

    try:
        query_test = SelectTest(d, test_dict)
    except ValueError as e:
        d.addErrorMessage('Error creating test object: %s' % e)
        return

    try:
        query_test.run_query()

        for field, rows in query_test.status():
            d.startSection('Column: ' + field)
            for row in rows:
                d.reportCommandStatus('status', row['given_value'], row['passed'], row['return_value'], '')
            d.endSection()
    except Exception as e:
        d.addErrorMessage('Error running query: %s' % e)
        return
