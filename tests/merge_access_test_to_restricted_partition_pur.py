# Test: merge_access_test_to_restricted_partition_pur.py
# Ticket: Bug #19025
# Author: alehmann
# Date: 3-28-2014
# Description: Test that when the MERGE TO patient is accessible due to restricted partition but user has PUR
# the merge succeeds

import uiconvenience
import merge_access_test

def main( d, WCURLS ):
    test_name="merge_access_test_to_restricted_partition_pur"
    purs={('MIE-10019', 'Hart, William S.'): 'Attending Physician'}
    user_access_set = frozenset((
        ('Limited Access:', 'No'),
        ('Restrict Access by Partition:', 'Yes')))
    partition_restrict_dict={'MIE': {}}
    lock_dict={}

    href_dict=merge_access_test.setup(
        d,
        WCURLS,
        test_name=test_name,
        base_mrn="MIE-10019",
        purs=purs,
        partition_restrict_dict=partition_restrict_dict,
        lock_dict=lock_dict,
        user_access_set=user_access_set)

    uiconvenience.merge_MRNs(
        d,
        to_MRN='MIE-10019',
        from_MRN='TEST-41205328' )
