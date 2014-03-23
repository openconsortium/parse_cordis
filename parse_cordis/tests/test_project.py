from parse_cordis import project_xml
from pprint import pprint
import json

def test_project_systemage_local():
	p = project_xml.parse("parse_cordis/tests/project.xml")
	assert_project_systemage(p)

def test_project_systemage():
	p = project_xml.parse("105875")
	assert_project_systemage(p)

def assert_project_systemage(p):
	assert p['contract_type'] == 'CP-FP'
	assert p['cost'] == '7864905'
	assert p['rcn'] == '105875'
	assert p['project_call'] == 'FP7-HEALTH-2012-INNO'
	assert p['project_acronym'] == 'SYSTEMAGE'
	assert p['programme_type'] == '339'
	assert p['subprogramme_area'] == 'HEALTH.2012.2.2.2-1'
	assert p['title'] == 'Early warning signals of ageing in human stem cells and age-related disorders'
	assert p['coordinator'] == '999988230'
	assert p['status'] == 'Execution'
	assert p['subject_index'] == 'Scientific Research'
	assert p['subject_index_code'] == 'SCI'
	assert p['start_date'] == '2013-01-01'
	assert p['end_date'] == '2017-12-31'
	assert p['duration'] == '60'
	assert p['last_updated'] == '2013-01-10'

	assert len(p['participants']) == 9

	p1 = p['participants'][0]
	assert p1['acronym'] == 'EMBL'
	assert p1['latitude'] == '53.4354286'
	assert p1['id'] == '999988230'
	assert p1['country'] == 'DE'

	p3 = p['participants'][2]
	assert p3['acronym'] == 'AX'
	assert p3['latitude'] == '41.9179844'
	assert p3['id'] == '998152505'
	assert p3['country'] == 'ES'


# http://cordis.europa.eu/projects/rcn/91504_en.html
def test_project_gn3():
	p = project_xml.parse("91504")
	assert len(p['participants']) == 34

	p1 = p['participants'][0]
	assert p1['name'] == 'DELIVERY OF ADVANCED NETWORK TECHNOLOGY TO EUROPE LIMITED'
	assert p1['city'] == 'OXFORD'
	assert p1['country'] == 'GB'

	assert p['project_website'] == 'http://www.geant.net/pages/home.aspx'
	assert p['status_code'] == '2'
	assert p['subject_index_code'] == 'COO,IPS,POL,SCI,TEL'
	assert p['subject_index'] == 'Coordination, Cooperation,Information Processing, Information Systems,Policies,Scientific Research,Telecommunications'
	assert p['title'] == 'Multi-gigabit european research and education network and associated services (GN3)'
	assert p['project_acronym'] == 'GN3'
