import os
import os.path
import json
from wcunithelpers import wcRemoteFile, wcFile, process_json_queries
from dbtest import execute_interface

def validate(d):
    u = d.getWCUnitTest("Validate baseline vs test file")
    baseline_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testlib', 'hr_feed_tests.json')
    test_path = 'hr_feed_tests_updated.json'
    u.verifyFile(wcFile(baseline_path), wcFile(test_path), reason='Ensure the file contents are what is expected')
    u.test()

def main(d, WCURL):
    d.startSection("HR Feed Setup")
    res = d.miedb.dbQuery('''SET @app_name := 'Sample Applicant Employer';
        INSERT INTO patients SET last_name=@app_name,first_name='',birth_date=NOW(),edit_date=NOW(),create_date=NOW();
        SET @applicant_pat_id:=LAST_INSERT_ID();
        INSERT INTO patient_mrns SET pat_id=@applicant_pat_id, wc_partition='EO', mrnumber='test_applicant_hr_feed';
        INSERT INTO patient_extended_values SET pat_id=@applicant_pat_id, ext_id=(SELECT ext_id FROM patient_extended_index WHERE name = 'chart_registration_partition'), value='APP';
        INSERT INTO pat_chart_types SET pat_id=@applicant_pat_id, chart_type_id=(SELECT chart_type_id FROM chart_types WHERE description = 'Employer Organization');

        -- TODO: move this into a setup sql hook when the hr testing framework supports those
        -- for now, we need it to prove that having multiple obs_codes won't cause issues
        INSERT INTO observation_codes (obs_type, obs_group, obs_group_name, obs_name, interface) VALUES ('CWE', 8, 'Race CDC', 'CDC Race', 'dontuseme');

        SELECT 1 AS ok;
    ''')
    d.endSection()

    d.startSection("HR Feed Install")
    res = d.miedb.dbQuery('''SET NAMES 'utf8' COLLATE 'utf8_unicode_ci';

        -- Set Variables
        SET @interface_name := 'test_hr_feed';

        SET @filename := 'hr_feed_sample*.csv';

        SET @set_opt_username_lookup := 1;

        SET @set_opt_hold_demo := 0;

        SET @set_opt_portal_pat := 1;
        SET @primary_eo := (SELECT pat_id FROM patients WHERE last_name='Better Corp.' LIMIT 1);

        SET @set_opt_portal_pat_secondary := 1;
        SET @secondary_eo := (SELECT pat_id FROM patients WHERE last_name='Sample Applicant Employer' LIMIT 1);

        SET @set_opt_route_system_id := 1;
        SET @opt_route_system_id_value := 'TEST_ADT';

        SET @set_opt_chunk_size := 1;

        SET @set_opt_portal_user_super_relationship := 0;
        -- TODO do we just assume this is 1 if we want this turned on? Or does this need to be looked up? 
        SET @opt_portal_user_super_relations_value = 0;
            
        SET @set_opt_multi_field_delim := 1;         
        SET @opt_multi_field_delim_value := '|';     

        -- Interface Chart Creation
        INSERT INTO patients
            (last_name, interface, extern_id1, username)
        SELECT
            @interface_name AS 'last_name',
            @interface_name AS 'interface',
            @interface_name AS 'extern_id1',
            @interface_name AS 'username'
        FROM
            DUAL
        WHERE
            (@interface_patid := (SELECT pat_id FROM patients WHERE username = @interface_name)) IS NULL
        ;

        SET @interface_patid := (SELECT pat_id FROM patients WHERE username = @interface_name);

        INSERT INTO patient_mrns
            (pat_id, wc_partition, mrnumber)
        SELECT
            @interface_patid AS 'pat_id',
            'INTERFACE' AS 'wc_partition',
            @interface_name AS 'mrnumber'
        FROM
            DUAL
        WHERE
            NOT EXISTS(SELECT id FROM patient_mrns WHERE pat_id = @interface_patid AND wc_partition = 'INTERFACE')
        ;

        INSERT IGNORE INTO pat_chart_types 
            SET pat_id=@interface_patid, 
            chart_type_id=(
                SELECT chart_type_id 
                FROM chart_types 
                WHERE description = 'Interface'
            )
        ;

        SET @interface_userid := (SELECT id FROM user_patients WHERE id_type = 'user' AND role_id = 501 AND pat_id = @interface_patid);

        UPDATE
            users
        SET
            status = 1,
            realm = 'MIE',
            security_role_id = (SELECT security_role_id FROM security_roles WHERE security_role_name = 'View Only')
        WHERE
            user_id = @interface_userid
        ;

        INSERT IGNORE INTO user_realms (user_id, realm) VALUES (@interface_userid, 'MIE');

        -- Document / Lab Request creation
        INSERT INTO documents
            (doc_type, pat_id, storage_type, interface, ext_doc_id)
        SELECT
            'EXECDEF' AS 'doc_type',
            @interface_patid AS 'pat_id',
            13 AS 'storage_type',
            @interface_name AS 'interface',
            @interface_name AS 'ext_doc_id'
        FROM
            DUAL
        WHERE
            NOT EXISTS(SELECT doc_id FROM documents WHERE interface = @interface_name AND ext_doc_id = @interface_name)
        ;

        SET @interface_docid := (SELECT doc_id FROM documents WHERE interface = @interface_name AND ext_doc_id = @interface_name);

        INSERT IGNORE INTO documents_txt (doc_id, subject) VALUES (@interface_docid, @interface_name);

        INSERT INTO lab_requests
            (doc_id, request_name, interface)
        SELECT
            @interface_docid AS 'doc_id',
            'HR Interface' AS 'request_name',
            @interface_name AS 'interface'
        FROM
            DUAL
        WHERE
            NOT EXISTS(SELECT request_id FROM lab_requests WHERE doc_id = @interface_docid AND request_name = 'HR Interface')
        ;

        SET @dml_requestid := (SELECT request_id FROM lab_requests WHERE doc_id = @interface_docid AND request_name = 'HR Interface');

        -- HRLookupUsername
        SET @opt_username_lookup := 'HRLookupUsername';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_username_lookup, @interface_name
        FROM DUAL
        WHERE NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_username_lookup);
        SET @obscode_username_lookup := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_username_lookup LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_username_lookup, @opt_username_lookup, '1', @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_username_lookup AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_username_lookup)
        ;

        -- HRHoldDemographics
        SET @opt_hold_demo := 'HRHoldDemographics';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_hold_demo, @interface_name
        FROM DUAL
        WHERE 
            @set_opt_hold_demo AND
            NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_hold_demo)
        ;

        SET @obscode_hold_demo := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_hold_demo LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_hold_demo, @opt_hold_demo, '1', @interface_name
        FROM
            DUAL
        WHERE
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_hold_demo)
        ;

        -- HRPortalPatID
        SET @opt_portal_pat := 'HRPortalPatID';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_portal_pat, @interface_name
        FROM DUAL
        WHERE NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_portal_pat)
        ;

        SET @obscode_portal_pat := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_portal_pat LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_portal_pat, @opt_portal_pat, @primary_eo, @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_portal_pat AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_portal_pat_secondary)
        ;

        -- Secondary (onboarding) HRPortalPatID
        SET @opt_portal_pat_secondary := 'HRApplicantPatID';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_portal_pat_secondary, @interface_name
        FROM DUAL
        WHERE NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_portal_pat_secondary)
        ;

        SET @obscode_portal_pat_secondary := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_portal_pat_secondary LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_portal_pat_secondary, @opt_portal_pat_secondary, @secondary_eo, @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_portal_pat_secondary AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_portal_pat_secondary)
        ;

        -- HRRouteSystemID
        SET @opt_route_system_id := 'HRRouteSystemID';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_route_system_id, @interface_name
        FROM DUAL
        WHERE 
            NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_route_system_id)
        ;

        SET @obscode_route_system_id := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_route_system_id LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_route_system_id, @opt_route_system_id, @opt_route_system_id_value, @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_route_system_id AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_route_system_id)
        ;

        -- HRChunkSize
        SET @opt_chunk_size := 'HRChunkSize';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_chunk_size, @interface_name
        FROM DUAL
        WHERE NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_chunk_size)
        ;

        SET @obscode_chunk_size := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_chunk_size LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_chunk_size, @opt_chunk_size, '5000', @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_chunk_size AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_chunk_size)
        ;

        -- HRPortalUserSuperRelationships
        SET @opt_portal_user_super_relations := 'HRPortalUserSuperRelationships';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_portal_user_super_relations, @interface_name
        FROM DUAL
        WHERE NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_portal_user_super_relations)
        ;

        SET @obscode_portal_user_super_relations := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_portal_user_super_relations LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_portal_user_super_relations, @opt_portal_user_super_relations, @opt_portal_user_super_relations_value, @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_portal_user_super_relationship AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_portal_user_super_relations)
        ;

        -- MultiFieldDelimiter
        SET @opt_multi_field_delim := 'MultiFieldDelimiter';

        INSERT INTO `observation_codes` (`wc_uuid`, `obs_name`, `interface`)
        SELECT wc_ordered_uuid(UUID()), @opt_multi_field_delim, @interface_name
        FROM DUAL
        WHERE 
            @set_opt_multi_field_delim AND
            NOT EXISTS (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_multi_field_delim)
        ;

        SET @obscode_multi_field_delim := (SELECT obs_code FROM observation_codes WHERE obs_name = @opt_multi_field_delim LIMIT 1);

        INSERT INTO observations
            (pat_id, request_id, obs_code, obs_name, obs_result, interface)
        SELECT
            @interface_patid, @dml_requestid, @obscode_multi_field_delim, @opt_multi_field_delim, @opt_multi_field_delim_value, @interface_name
        FROM
            DUAL
        WHERE
            @set_opt_multi_field_delim AND
            NOT EXISTS (SELECT obs_id FROM observations WHERE request_id = @dml_requestid AND obs_code = @obscode_multi_field_delim)
        ;
 
        INSERT INTO datafeed_interface (pat_id, name, incoming_table_name, config)
        VALUES (
            @interface_patid, @interface_name, 'hr_feed_data',
            JSON_OBJECT(
                'path', 'hr',
                'filename', @filename,
                'format', 'csv',
                'preserve_original_as_json', TRUE,
                'columns', JSON_ARRAY(
                    JSON_OBJECT('value', 'EE', 'db', 'patient_mrns_globalid_partition'),
                    JSON_OBJECT('csv', 'Employee ID', 'req', 'r', 'db', 'patient_mrns_globalid'),
                    JSON_OBJECT('csv', 'SSO ID / Username', 'req', 'bp', 'db', 'patients_username'),
                    JSON_OBJECT('csv', 'Badge ID Number for Kiosk Checkin', 'req', 'bp', 'db', 'patient_mrns_badgeid'),
                    JSON_OBJECT('csv', 'Birth Date', 'req', 'r', 'db', 'patients_birth_date'),
                    JSON_OBJECT('csv', 'Email Address', 'req', 'bp', 'db', 'patients_email'),
                    JSON_OBJECT('csv', 'Employee Work Status', 'req', 'bp', 'db', 'patient_admin_status_code'),
                    JSON_OBJECT('csv', 'Employee Work Status Description', 'req', 'cr', 'db', 'patient_admin_status_code_desc'),
                    JSON_OBJECT('csv', 'Supervisor ID', 'req', 'bp', 'db', 'pur_supervisor_id'),
                    JSON_OBJECT('csv', 'Supervisor ID Partition', 'req', 'cr', 'db', 'pur_supervisor_id_partition'),
                    JSON_OBJECT('csv', 'Last Name', 'req', 'r', 'db', 'patients_last_name'),
                    JSON_OBJECT('csv', 'First Name', 'req', 'bp', 'db', 'patients_first_name'),
                    JSON_OBJECT('csv', 'Middle Name', 'req', 'o', 'db', 'patients_middle_name'),
                    JSON_OBJECT('csv', 'Preferred Last Name', 'req', 'o', 'db', 'patients_preferred_last_name'),
                    JSON_OBJECT('csv', 'Preferred First Name', 'req', 'o', 'db', 'patients_preferred_first_name'),
                    JSON_OBJECT('csv', 'Preferred Middle Name', 'req', 'o', 'db', 'patients_preferred_middle_name'),
                    JSON_OBJECT('csv', 'Title', 'req', 'o', 'db', 'patients_title'),
                    JSON_OBJECT('csv', 'Degree', 'req', 'o', 'db', 'patients_degree'),
                    JSON_OBJECT('csv', 'Suffix', 'req', 'o', 'db', 'patients_suffix'),
                    JSON_OBJECT('csv', 'Home Address 1', 'req', 'o', 'db', 'patients_address1'),
                    JSON_OBJECT('csv', 'Home Address 2', 'req', 'o', 'db', 'patients_address2'),
                    JSON_OBJECT('csv', 'Home Address 3', 'req', 'o', 'db', 'patients_address3'),
                    JSON_OBJECT('csv', 'Home County', 'req', 'o', 'db', 'patients_county'),
                    JSON_OBJECT('csv', 'Home City', 'req', 'o', 'db', 'patients_city'),
                    JSON_OBJECT('csv', 'Home State', 'req', 'o', 'db', 'patients_state'),
                    JSON_OBJECT('csv', 'Home Zip', 'req', 'o', 'db', 'patients_zip_code'),
                    JSON_OBJECT('csv', 'Home Country', 'req', 'o', 'db', 'patients_country'),
                    JSON_OBJECT('csv', 'Employer Name', 'req', 'o', 'db', 'patients_employer_name'),
                    JSON_OBJECT('csv', 'Work Address 1', 'req', 'o', 'db', 'patients_employer_addr1'),
                    JSON_OBJECT('csv', 'Work Address 2', 'req', 'o', 'db', 'patients_employer_addr2'),
                    JSON_OBJECT('csv', 'Work Address 3', 'req', 'o', 'db', 'patients_employer_addr3'),
                    JSON_OBJECT('csv', 'Work County', 'req', 'o', 'db', 'patients_employer_county'),
                    JSON_OBJECT('csv', 'Work City', 'req', 'o', 'db', 'patients_employer_city'),
                    JSON_OBJECT('csv', 'Work State', 'req', 'o', 'db', 'patients_employer_state'),
                    JSON_OBJECT('csv', 'Work Zip', 'req', 'o', 'db', 'patients_employer_zipcode'),
                    JSON_OBJECT('csv', 'Work Country', 'req', 'o', 'db', 'patients_employer_country'),
                    JSON_OBJECT('csv', 'Home Phone', 'req', 'o', 'db', 'patients_home_phone'),
                    JSON_OBJECT('csv', 'Work Phone', 'req', 'cr', 'db', 'patients_work_phone'),
                    JSON_OBJECT('csv', 'Cell Phone', 'req', 'o', 'db', 'patients_cell_phone'),
                    JSON_OBJECT('csv', 'Fax Number', 'req', 'bp', 'db', 'patients_fax_number'),
                    JSON_OBJECT('csv', 'Alternate Phone', 'req', 'o', 'db', 'patients_alternate_phone'),
                    JSON_OBJECT('csv', 'SSN', 'req', 'o', 'db', 'patients_ssn'),
                    JSON_OBJECT('csv', 'Sex', 'req', 'o', 'db', 'patients_sex'),
                    JSON_OBJECT('csv', 'Gender', 'req', 'o', 'db', 'obs_gender_identity_obs_result'),
                    JSON_OBJECT('csv', 'Pronouns', 'req', 'o', 'db', 'obs_personal_pronouns_obs_result'),
                    JSON_OBJECT('csv', 'Ethnicity', 'req', 'o', 'db', 'obs_ethnicity_obs_result'),
                    JSON_OBJECT('csv', 'Race', 'req', 'o', 'db', 'obs_race_obs_result'),
                    JSON_OBJECT('csv', 'Marriage Status', 'req', 'o', 'db', 'patients_marital_status'),
                    JSON_OBJECT('csv', 'Emergency Contact Name', 'req', 'o', 'db', 'patients_emergency_contact'),
                    JSON_OBJECT('csv', 'Emergency Contact Phone', 'req', 'o', 'db', 'patients_emergency_phone'),
                    JSON_OBJECT('csv', 'Death Date', 'req', 'o', 'db', 'patients_death_date'),
                    JSON_OBJECT('csv', 'Position Title', 'req', 'o', 'db', 'obs_position_title_obs_result'),
                    JSON_OBJECT('csv', 'BLS Job Strength', 'req', 'o', 'db', 'obs_bls_obs_result'),
                    JSON_OBJECT('csv', 'Job Code', 'req', 'o', 'db', 'patient_admin_job_code'),
                    JSON_OBJECT('csv', 'Job Code Description', 'req', 'o', 'db', 'patient_admin_job_code_desc'),
                    JSON_OBJECT('csv', 'Regular / Temporary', 'req', 'o', 'db', 'pev_reg_temp'),
                    JSON_OBJECT('csv', 'Full / Part Time', 'req', 'o', 'db', 'pev_full_part'),
                    JSON_OBJECT('csv', 'Person Type', 'req', 'o', 'db', 'pev_person_type_desc'),
                    JSON_OBJECT('csv', 'Hire Date', 'req', 'o', 'db', 'patient_admin_hire_datetime'),
                    JSON_OBJECT('csv', 'Termination Date', 'req', 'o', 'db', 'patient_admin_termination_datetime'),
                    JSON_OBJECT('csv', 'Effective Date', 'req', 'o', 'db', 'pev_effective_date'),
                    JSON_OBJECT('csv', 'Medical Anniversary', 'req', 'o', 'db', 'pev_hsp_med_anniv'),
                    JSON_OBJECT('csv', 'Default Clinic Location', 'req', 'cr', 'db', 'patient_admin_clinic_location'),
                    JSON_OBJECT('csv', 'Default Clinic Location Description', 'req', 'cr', 'db', 'patient_admin_clinic_location_desc'),
                    JSON_OBJECT('csv', 'Employee Class', 'req', 'o', 'db', 'patient_admin_employee_class'),
                    JSON_OBJECT('csv', 'Employee Class Description', 'req', 'cr', 'db', 'patient_admin_employee_class_desc'),
                    JSON_OBJECT('csv', 'Location', 'req', 'o', 'db', 'patient_admin_location'),
                    JSON_OBJECT('csv', 'Location Description', 'req', 'cr', 'db', 'patient_admin_location_desc'),
                    JSON_OBJECT('csv', 'Facility Code', 'req', 'o', 'db', 'patient_admin_facility_code'),
                    JSON_OBJECT('csv', 'Facility Description', 'req', 'cr', 'db', 'patient_admin_facility_code_desc'),
                    JSON_OBJECT('csv', 'Building', 'req', 'o', 'db', 'patient_admin_building_code'),
                    JSON_OBJECT('csv', 'Building Description', 'req', 'cr', 'db', 'patient_admin_building_code_desc'),
                    JSON_OBJECT('csv', 'Company Code', 'req', 'o', 'db', 'patient_admin_company_code'),
                    JSON_OBJECT('csv', 'Company Description', 'req', 'cr', 'db', 'patient_admin_company_code_desc'),
                    JSON_OBJECT('csv', 'Department / Floor Code', 'req', 'o', 'db', 'patient_admin_floor_code'),
                    JSON_OBJECT('csv', 'Department Description / Floor Description', 'req', 'cr', 'db', 'patient_admin_floor_code_desc'),
                    JSON_OBJECT('csv', 'Business Area Unit', 'req', 'o', 'db', 'patient_admin_employee_group'),
                    JSON_OBJECT('csv', 'Business Area Description', 'req', 'cr', 'db', 'patient_admin_employee_group_desc'),
                    JSON_OBJECT('csv', 'Cost Center Code', 'req', 'o', 'db', 'patient_admin_cost_center_code'),
                    JSON_OBJECT('csv', 'Cost Center Description', 'req', 'cr', 'db', 'patient_admin_cost_center_code_desc'),
                    JSON_OBJECT('csv', 'Custom MRN', 'req', 'o', 'webchart_mrn', JSON_ARRAY('CSTM')),
                    JSON_OBJECT('csv', 'Custom PEV', 'req', 'o', 'webchart_pev', JSON_ARRAY('pev_custom')),
                    JSON_OBJECT('csv', 'Custom OBS', 'req', 'o', 'webchart_obs', JSON_ARRAY('obs_custom'))
                )
            )
        )
        ON DUPLICATE KEY UPDATE
            incoming_table_name = VALUES(incoming_table_name),
            config = VALUES(config)
        ;

        SELECT @interface_docid AS 'doc_id';
    ''').getRes()[0]

    doc_id = str(res['doc_id'])
    d.endSection()

    d.startSection('Run Interface Manager For HR Feed')
    execute_interface(d,doc_id,runall=True)
    d.endSection()

    d.startSection('Read JSON file')
    input_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testlib', "hr_feed_tests.json")
    with open(input_file_path, "r") as json_file:
        json_data = json.load(json_file)
    d.endSection()

    d.startSection('Process JSON file')
    process_json_queries(json_data,d)
    d.endSection()

    d.startSection('Output JSON file')
    output_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload', "hr_feed_tests_updated.json")
    with open(output_file_path, "w") as output_file:
        json.dump(json_data, output_file, indent=4)
    d.endSection()

    d.startSection('Validate JSON file')
    validate(d)
    d.endSection()