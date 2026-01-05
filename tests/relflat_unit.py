"""
	@owner: aaronc
"""
from wcunittest import wcElement, wcDBRecord

def createPatients(d):
	if not d.miedb.dbExec("INSERT INTO patients (last_name) VALUES "\
		"('Relation_A'), ('Relation_B'), ('Relation_C'), ('Relation_D'), ('Relation_E'), ('Relation_F'),"\
		"('Copy_A'), ('Copy_B')"):
		d.reportCommandStatus('DB Statement Failed', d.miedb.dbError(), False, '', '')
	if not d.miedb.dbExec("INSERT INTO relation_types (relation_type, flatten) VALUES "\
		"('Testing Relationship', 1),"\
		"('Copy Relationship', 2)"):
		d.reportCommandStatus('DB Statement Failed', d.miedb.dbError(), False, '', '')

def insertRelationships(d, parent, child, relation_type='Testing Relationship'):
	if not d.miedb.dbExec("INSERT INTO pat_pat_relations (pat_id, related_pat_id, relation_type_id) VALUES "\
		"((SELECT pat_id FROM patients WHERE last_name='{0}'), (SELECT pat_id FROM patients WHERE last_name='{1}'), (SELECT relation_type_id FROM relation_types WHERE relation_type='{2}'))".
		format(parent, child, relation_type)):
		d.reportCommandStatus('DB Statement Failed', d.miedb.dbError(), False, '', '')

def verifyRelationship(wcunit, parent, child, myReason):
	wcunit.verifyDB([
			wcDBRecord("FROM pat_pat_relflat ppr INNER JOIN patients pparent ON pparent.pat_id = ppr.pat_id INNER JOIN patients pchild ON pchild.pat_id = ppr.pat_isa "\
				"WHERE pparent.last_name='{0}' AND pchild.last_name='{1}'".format(parent, child), {
					'pparent.last_name AS parent': parent,
					'pchild.last_name AS child': child
				}),
		], reason=myReason)

def main(d, WCURL):
	wcunit = d.getWCUnitTest('Validate Single Relationship')
	wcunit.setup(createPatients, reason="Make some patients for linking")
	wcunit.setup(lambda d: insertRelationships(d, 'Relation_D', 'Relation_E'), reason="Start a tree")
	verifyRelationship(wcunit, 'Relation_D', 'Relation_E', 'Make sure that a single relationship works')
	wcunit.test()

	wcunit = d.getWCUnitTest('Validate Grandchild')
	wcunit.setup(lambda d: insertRelationships(d, 'Relation_E', 'Relation_F'), reason="Link a child to a record that is already a child to make a grandchild")
	verifyRelationship(wcunit, 'Relation_E', 'Relation_F', 'Make sure that a child relationship is added')
	verifyRelationship(wcunit, 'Relation_D', 'Relation_F', 'Make sure grandchild relationship is added')
	wcunit.test()

	wcunit = d.getWCUnitTest('Validate Disconnected Relationship')
	wcunit.setup(lambda d: insertRelationships(d, 'Relation_B', 'Relation_C'))
	verifyRelationship(wcunit, 'Relation_B', 'Relation_C', 'Make sure that a single relationship works')
	wcunit.test()

	wcunit = d.getWCUnitTest('Validate Grandparent')
	wcunit.setup(lambda d: insertRelationships(d, 'Relation_A', 'Relation_B'), reason="Link a parent to a record that is already a parent to make a grandparent")
	verifyRelationship(wcunit, 'Relation_A', 'Relation_B', 'Make sure that a parent relationship is added')
	verifyRelationship(wcunit, 'Relation_A', 'Relation_C', 'Make sure grandparent relationship is added')
	wcunit.test()

	wcunit = d.getWCUnitTest('Validate Tree Joining')
	wcunit.setup(lambda d: insertRelationships(d, 'Relation_C', 'Relation_D'), reason="Link two trees together to make great-grandparents/children")
	verifyRelationship(wcunit, 'Relation_A', 'Relation_F', 'Make sure relationship from the top of the tree to the bottom works')
	wcunit.test()

	wcunit = d.getWCUnitTest('Validate Flatten Copy')
	wcunit.setup(lambda d: insertRelationships(d, 'Copy_A', 'Copy_B', 'Copy Relationship'), reason="Flatten = 2 relationship")
	verifyRelationship(wcunit, 'Copy_A', 'Copy_B', 'Make sure relationship of flatten=2 gets copied')
	wcunit.test()