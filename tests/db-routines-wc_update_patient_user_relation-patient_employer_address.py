#
# Webchart Database Test Template
#
from dbtest import SelectTest


"""
Test details:
  Turn setting off (System/DB Routine/Sync user address with patient address not employer_address)
  Insert User
  Insert Patient
  Create Relation
  Call wc_update_patient_user_relation(PAT_ID, NO USER_ID)
    - Updates user to patient values
  Prepare test_dict (users query)
  Prepare test_dict2 (patients query)
  Create test objects
  Run Users Query Test, should have Patient values
  Update User back to initial values
  Run Patients Query Test, should have User values
  Delete User
  Delete Patient
"""

insert_str = "INSERT INTO %s (%s) VALUES (%s)"

def prepare_insert(query_dict):
    """Returns a tuple suitable for a SQL query.

    Takes a dictionary and stringifies the keys as columns and also values.
    """

    columns, values = '', ''

    try:
        for k, v in query_dict.iteritems():
            if columns:
                columns += ','
            columns += k
            if values:
                values += ','
            values += "'%s'" % v
    except AttributeError:
        for k, v in query_dict.items():
            if columns:
                columns += ','
            columns += k
            if values:
                values += ','
            values += "'%s'" % v

    return (columns, values)

def main(d, WCURL):
    """
    Database test
    """

    user = {
        'username': 'pur_test_user',
        'first_name': 'Anthony',
        'last_name': 'Stonem',
        'middle_name': 'Q.',
        'alias': 'Tony',
        'title': 'Dr.',
        'degree': 'M.D.',
        'suffix': 'Sr.',
        'address1': '123 Somewhere Lane',
        'address2': 'P.O. Box 2873',
        'address3': 'Guest House',
        'city': 'New York',
        'state': 'NY',
        'zip': '12345',
        'country': 'United States of America',
        'county': 'Notsure',
        'home_phone': '123-456-1234',
        'work_phone': '222-333-4444',
        'cell_phone': '928-394-2058',
        'cellco_id': '5',
        'fax_number': '800-382-4890',
        'email': 'tony@skins.co.uk',
    }

    patient = {
        'username': 'pur_test_patient',
        'first_name': 'Sidney',
        'last_name': 'Jenkins',
        'middle_name': 'W.',
        'preferred_first_name': 'Sid',
        'title': 'Mr.',
        'degree': 'Esquire',
        'suffix': 'Jr.',
        'employer_addr1': '456 Elsewhere Drive',
        'employer_addr2': 'P.O. Box 9482',
        'employer_addr3': 'Dog House',
        'employer_city': 'Los Angeles',
        'employer_state': 'CA',
        'employer_zipcode': '09876',
        'employer_country': 'USA',
        'employer_county': 'Unclear',
        'home_phone': '980-394-9754',
        'work_phone': '999-222-4444',
        'cell_phone': '293-493-3950',
        'cellco_id': '2',
        'fax_number': '900-482-0582',
        'email': 'sid@skins.co.uk',
    }

    # Map of fields differing between tables
    # User to patient
    u2pmap = {
        'alias': 'preferred_first_name',
        'address1': 'employer_addr1',
        'address2': 'employer_addr2',
        'address3': 'employer_addr3',
        'city': 'employer_city',
        'state': 'employer_state',
        'zip': 'employer_zipcode',
        'country': 'employer_country',
        'county': 'employer_county',
    }

    # The reverse, patient to user
    try:
        p2umap = dict((v,k) for k,v in u2pmap.iteritems())
    except AttributeError:
        p2umap = dict((v,k) for k,v in u2pmap.items())

    # We are testing the database,
    # screenshots of the browser are not useful here
    d.setScreenShotOnError(False)

    # Preparation for the tests
    try:
        # Ensure settings are correct
        query = "UPDATE system_settings SET " \
                "value = 0 WHERE " \
                "module = 'System' AND "\
                "section = 'DB Routine' AND "\
                "item = 'Enable PUR Routine'"

        d.miedb.dbExec(query)

        query = "UPDATE system_settings SET " \
                "value = 0 WHERE " \
                "module = 'System' AND "\
                "section = 'DB Routine' AND "\
                "item = 'Sync user address with patient address not employer_address'"

        d.miedb.dbExec(query)

        # insert user
        user_tup = ('users',) + prepare_insert(user)
        d.miedb.dbExec(insert_str % user_tup)

        # grab user_id
        query = "SELECT user_id FROM users " \
                "WHERE first_name = '%s' " \
                "AND middle_name = '%s' " \
                "AND last_name = '%s'"

        userid = d.miedb.dbQuery(
            query % (user['first_name'],
                     user['middle_name'],
                     user['last_name'])
        ).getRow(0)['user_id']

        # insert patient
        pat_tup = ('patients',) + prepare_insert(patient)
        d.miedb.dbExec(insert_str % pat_tup)

        # grab pat_id

        query = "SELECT pat_id FROM patients " \
                "WHERE first_name = '%s' " \
                "AND middle_name = '%s' " \
                "AND last_name = '%s'"

        patid = d.miedb.dbQuery(
            query % (patient['first_name'],
                     patient['middle_name'],
                     patient['last_name'])
        ).getRow(0)['pat_id']

        # create relation
        relation = {
            'id': userid,
            'id_type': 'user',
            'pat_id': patid,
            'role_id': '501',
        }

        rel_tup = ('user_patients',) + prepare_insert(relation)
        d.miedb.dbExec(insert_str % rel_tup)

        # Sync user to patient information
        querystr = "SET @TMP_PUR_PATID={0};"\
                   "SET @TMP_PUR_UID=0;"\
                   "CALL wc_update_patient_user_relation(@TMP_PUR_PATID,@TMP_PUR_UID)"

        if not d.miedb.dbExec(querystr.format(patid)):
            d.addErrorMessage('Error running query: %s' % d.miedb.dbError())
            return
    except Exception as e:
        d.addErrorMessage('Error running query: %s' % e)
        return

    test_dict = {
        'select': [],
        'expr': 'FROM users WHERE user_id = {0}'.format(userid),
        'count': 1,
    }

    test_dict2 = {
        'select': [],
        'expr': 'FROM patients WHERE pat_id = {0}'.format(patid),
        'count': 1,
    }

    # Populate user fields with patient values
    try:
        for k,v in user.iteritems():
            if k in u2pmap:
                pat_k = u2pmap[k]
            else:
                pat_k = k

            test_dict['select'].append((k, [patient[pat_k]]))
    except AttributeError:
        for k,v in user.items():
            if k in u2pmap:
                pat_k = u2pmap[k]
            else:
                pat_k = k

        test_dict['select'].append((k, [patient[pat_k]]))

    # And the reverse
    try:
        for k,v in patient.iteritems():
            if k in p2umap:
                user_k = p2umap[k]
            else:
                user_k = k

            test_dict2['select'].append((k, [user[user_k]]))
    except AttributeError:
        for k,v in patient.items():
            if k in p2umap:
                user_k = p2umap[k]
            else:
                user_k = k

        test_dict2['select'].append((k, [user[user_k]]))

    # Check that non-employer addresses are empty
    non_emp_fields = (
        ('address1', ['', ]),
        ('address2', ['', ]),
        ('address3', ['', ]),
        ('city', ['', ]),
        ('state', ['', ]),
        ('zip_code', ['', ]),
        ('country', ['', ]),
        ('county', ['', ])
    )

    for each in non_emp_fields:
        test_dict2['select'].append(each)

    # Create the test objects
    try:
        query_test = SelectTest(d, test_dict)
        query_test2 = SelectTest(d, test_dict2)
    except ValueError as e:
        d.addErrorMessage('Error creating test object: %s' % e)
        return

    # Get the results
    try:
        # User
        query_test.run_query()

        # Reset user information now that initial test has run
        fmt = "{0}='{1}'"
        updatestr = ''

        try:
            for k,v in user.iteritems():
                if updatestr:
                    updatestr += ','
                updatestr += fmt.format(k, v)
        except AttributeError:
            for k,v in user.items():
                if updatestr:
                    updatestr += ','
                updatestr += fmt.format(k, v)


        querystr = "UPDATE users SET {0} WHERE user_id = {1}".format(updatestr, userid)
        if not d.miedb.dbExec(querystr):
            d.addErrorMessage('Error running query: %s' % d.miedb.dbError())
            d.addErrorMessage('Query: {0}'.format(querystr))
            return

        query_test2.run_query()

        # User
        d.startSection("User")

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

        # End User
        d.endSection()

        #Patient
        d.startSection("Patient")

        # Display results from row count, if defined
        if query_test2.count_error():
            d.startSection('Incorrect number of rows returned')
            d.reportCommandStatus('count_error', 'Given: %d' % query_test2.expected_count(), False, 'Returned: %d' % query_test2.count(), '')
            d.endSection()

        # Display results from columns returned
        for field, rows in query_test2.status():
            d.startSection('Column: ' + field)
            for row in rows:
                d.reportCommandStatus('status', row['given_value'], row['passed'], row['return_value'], '')
            d.endSection()

        # End Patient
        d.endSection()
    except Exception as e:
        d.addErrorMessage('Error running query: %s' % e)
        return

    # Remove Patient and User
    try:
        d.miedb.dbExec("DELETE FROM users WHERE user_id = {0}".format(userid))
        d.miedb.dbExec("DELETE FROM patients WHERE pat_id = {0}".format(patid))
    except Exception as e:
        d.addErrorMessage('Error removing user and/or patient: %s' % e)
        return
