from parse_cordis import listing
from parse_cordis import project_xml

def test_listing():
	count = 3
	l = listing.parseNew(count)
	
	# Assert the amount of items returned
	assert len(l) == count

	# Assert that the returned items are valid rcns
	for item in l:
		p = project_xml.parse(item)
		assert p['rcn'] == item
