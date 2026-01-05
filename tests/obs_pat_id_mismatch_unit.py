"""
@owners: dhaneline
"""
from wcunittest import wcElement

# Verify error from attempting to edit an observation not belonging to the specified patient

def main(d, WCURL):
	t = d.getWCUnitTest('Verify an Observation not belonging to the patient can not be edited')
	t.setup(lambda d: d.navigate('?f=chart&s=pat&pat_id=18&v=ob&obopp=edit&obs_id=1&t=Observations+%28IH%29'))
	t.verifyElements([
		wcElement('xpath', '//*[contains(text(), "The obs_id provided DOES NOT belong to this pat_id!!")]'),
	], reason='This observation belongs to John Doe, NOT William Hart')
	t.test()
