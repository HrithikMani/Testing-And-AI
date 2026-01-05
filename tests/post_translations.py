"""
Post-test for translation statistics across different languages.

This module checks for missing translations in each language by comparing
with the common translation database, and automatically inserts them into
the central translation database.
"""

from typing import Any, Tuple, List

import miemysql

def get_translation_stats(d: Any, lang_code: str) -> Tuple[int, str, str]:
    """
    Query database for missing translations for a specific language.
    
    Args:
        d: The driver object that provides database access
        lang_code: The language code to check
        
    Returns:
        Tuple containing count of missing translations, stdout and stderr
    """
    query = """
   SELECT count(*)
    FROM label_translate AS lt
    LEFT JOIN rxdb_utf8.common_label_translate AS ct
    ON ct.lang_code = %s                 -- 'zh-hant'
    AND ct.context = lt.context
    AND ct.value = lt.value
    AND ct.trans IS NOT NULL
    AND ct.trans != ''
    WHERE lt.lang_code = 'en-wc'
  AND lt.status = 1
  AND ct.lang_code IS NULL; 
    """
    
    result = d.miedb.dbQuery(query, lang_code)
    if result is None:
        return 0, "", ""

    # Extract count from result
    count = 0
    if hasattr(result, 'res') and 'rows' in result.res and result.res['rows']:
        count = int(result.res['rows'][0][0])
    
    return count, "", ""


def insert_label_translate_to_central(d: Any, central_conn: Any, lang_code: str = 'en-wc') -> Tuple[int, str]:
    """
    Insert label_translate records from test database to central database.
    
    Args:
        d: The driver object providing access to test database
        central_conn: MySQL connection to central database
        lang_code: Language code to insert (default: 'en-wc')
        
    Returns:
        Tuple containing count of inserted records and status message
    """
    # First, get data from the test database (d.miedb)
    select_query = """
    SELECT lang_code, context, value, trans, status, trans_type
    FROM label_translate 
    WHERE lang_code = %s AND status = 1;
    """
    
    test_result = d.miedb.dbQuery(select_query, lang_code)
    
    if test_result is None or not hasattr(test_result, 'res') or 'rows' not in test_result.res:
        return 0, "No records found in test database"
    
    rows = test_result.res['rows']
    if not rows:
        return 0, "No records to insert"
    
    # Insert into central database
    insert_count = 0
    errors = []
    
    for row in rows:
        # Escape strings for SQL
        lang_code = str(row[0]).replace("'", "''")
        context = str(row[1]).replace("'", "''") if row[1] else ''
        value = str(row[2]).replace("'", "''") if row[2] else ''
        trans = str(row[3]).replace("'", "''") if row[3] else ''
        status = str(row[4]).replace("'", "''") if row[4] else ''
        trans_type = str(row[5]).replace("'", "''") if row[5] else ''
        
        insert_query = f"""
        INSERT IGNORE INTO label_translate 
            (lang_code, context, value, trans, status, trans_type)
        VALUES ('{lang_code}', '{context}', '{value}', '{trans}', '{status}', '{trans_type}')
        """
        
        try:
            central_conn.dbQuery(insert_query)
            insert_count += 1
        except Exception as e:
            errors.append(f"Error inserting row: {str(e)}")
    
    if errors:
        for i in errors:
            d.reportCommandStatus('ERROR MSG', i, True, '', '', warn=True) 
        return insert_count, f"Inserted {insert_count} records with {len(errors)} errors"
    
    return insert_count, f"Successfully inserted {insert_count} records"


def insert_translate_to_central(d: Any, central_conn: Any) -> Tuple[int, str]:
    """
    Insert translate records from test database to central database.
    
    Args:
        d: The driver object providing access to test database
        central_conn: MySQL connection to central database
        
    Returns:
        Tuple containing count of inserted records and status message
    """
    # Query test database for translate records with label_translate join
    select_query = """
     SELECT 
            CONCAT('LANG_NAV-', lt.context) AS name,
                t.trans_from,
            t.trans_to,
            t.details
        FROM label_translate lt
        LEFT JOIN translate t 
            ON t.name = CONCAT('LANG_NAV-', lt.context)
            AND t.trans_from = lt.value
        WHERE lt.lang_code = 'en-wc' AND lt.status = 1;
    """

   
    
    test_result = d.miedb.dbQuery(select_query)
    
    if test_result is None or not hasattr(test_result, 'res') or 'rows' not in test_result.res:
        return 0, "No records found in test database"
    
    rows = test_result.res['rows']
    if not rows:
        return 0, "No records to insert"
    
    # Insert into central database
    insert_count = 0
    errors = []
    
    for row in rows:
        # Escape strings for SQL
        name = str(row[0]).replace("'", "''") if row[0] else ''
        trans_from = str(row[1]).replace("'", "''") if row[1] else ''
        trans_to = str(row[2]).replace("'", "''") if row[2] else ''
        details = str(row[3]).replace("'", "''") if row[3] else ''
        
        insert_query = f"""
        INSERT IGNORE INTO translate 
            (name, trans_from, trans_to, details)
        VALUES ('{name}', '{trans_from}', '{trans_to}', '{details}')
        """
        
        try:
            central_conn.dbQuery(insert_query)
            insert_count += 1
        except Exception as e:
            errors.append(f"Error inserting row: {str(e)}")
    
    if errors:
        return insert_count, f"Inserted {insert_count} records with {len(errors)} errors"
    
    return insert_count, f"Successfully inserted {insert_count} records"


def main(d: Any, _: Any) -> None:
    """
    Main function that checks translation statistics for all languages
    and inserts missing translations into central database.
    
    Args:
        d: The driver object providing access to WebChart functions
        _: Unused parameter
    """
    
    # Connect to central database (separate from d.miedb)
    try:
        central_conn = miemysql.MySQLClient(
            host='zeus-db2',
            user='root',
            password='pmg2bhok',
            dbname='wc_miehr_wctlang_central',
            port=3306
        )
    except Exception as e:
        d.startSection('Translation Statistics')
        d.reportCommandStatus('Connect to Central DB', '', True, '', 
                            f'Failed to connect to central database: {str(e)}', warn=True)
        d.endSection()
        return
    
    # Section 1: Insert translations into central database
    d.startSection('Insert Translatable Strings found in this test to Central Database',
                  comments='Copying strings from test database to central database',warn=True)
    
    # Insert label_translate records
    label_count, label_msg = insert_label_translate_to_central(d, central_conn, 'en-wc')
    d.reportCommandStatus('Insert label_translate', label_msg, True, '', '', warn=True)
    
    # Insert translate records
    translate_count, translate_msg = insert_translate_to_central(d, central_conn)
    d.reportCommandStatus('Insert translate', translate_msg, True, '', '', warn=True)
    
    d.endSection()
    
    # Section 2: Get list of available languages
    lang_query = "SELECT DISTINCT lang_code FROM languages_supported WHERE lang_code != 'en';"
    lang_result = d.miedb.dbQuery(lang_query)
    
    if lang_result is None:
        d.startSection('Translation Statistics')
        d.reportCommandStatus('Get Languages', '', True, '', 'Failed to query languages', warn=True)
        d.endSection()
        central_conn.close()
        return
    
    if not hasattr(lang_result, 'res') or 'rows' not in lang_result.res or not lang_result.res['rows']:
        d.startSection('Translation Statistics')
        d.reportCommandStatus('Get Languages', '', True, '', 'No languages found', warn=True)
        d.endSection()
        central_conn.close()
        return
        
    languages: List[str] = [row[0] for row in lang_result.res['rows']]
    
    # Section 3: Translation statistics
    d.startSection('Translation Statistics', 
                  comments='Missing translations per language in rxdb',warn=True)
    
    total_missing = 0
    language_stats = []
    
    # Check each language
    for lang in languages:
        missing_count, stdout, stderr = get_translation_stats(d, lang)
        total_missing += missing_count
        
        status = True  # Always show as info, not error
        message = f"Missing: {missing_count}"
        
        d.reportCommandStatus(f'Language: {lang}', message, status, stdout, stderr, warn=True)
        language_stats.append((lang, missing_count))
    
    # Summary
    summary_msg = f"Total missing translations: {total_missing} | " \
                  f"Inserted label_translate: {label_count} | " \
                  f"Inserted translate: {translate_count}"
    d.reportCommandStatus('Summary', summary_msg, True, '', '',warn=True)
    
    d.endSection()
    
    # Close central database connection
    try:
        central_conn.close()
    except:
        pass