from parse_cordis import project

def setup_module():
	'do some setup here'
	print "JAJAJ"
	pass

def test_numbers():
	assert 3*4 == 12 

def test_project():
	p = project.parse(105875)
	print p