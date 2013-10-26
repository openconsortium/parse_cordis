from lxml import etree
from collections import defaultdict

def getMapping():
	m = defaultdict(str)
	m['title'] = 'title'
	m['status'] = 'desc_status'
	m['objectives'] = 'objective'

	m['project_acronym'] = 'projectacronym'
	m['project_call'] = 'call_identifier'
	m['reference_number'] = 'projectreference'
	m['rcn'] = 'rcn'
	m['programme_acronym'] = 'programmeacronym'
	m['subprogramme_area'] = 'subprogrammearea'
	m['programme_type'] = 'programmetype'
	m['contract_type'] = 'contract_type'
	m['contract_type_desc'] = 'contract_type_desc'
	m['subject_index'] = 'subjectindex'
	m['subject_index_code'] = 'subjectindexcode'
	
	m['start_date'] = 'projectstartdate'
	m['end_date'] = 'projectenddate'
	m['duration'] = 'projectduration'
	m['cost'] = 'projectcost'
	m['funding'] = 'projectfunding'

	m['rec_qv_date'] = 'rec_qv_date'
	m['last_updated'] = 'last_update_date'
	m['publication_date'] = 'rec_publication_date'
	m['creation_date'] = 'rec_creation_date'

	return m

def parse(rcn):
	# url = "http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&rcn=" + str(rcn)
	tree = etree.parse('/Users/pvhee/code/parse_cordis/parse_cordis/tests/project.xml')

	# print(etree.tostring(doc, pretty_print=True))

	# print doc
	# print doc.find(/'hit')
	root = tree.getroot()

	p = defaultdict(str)

	hit = tree.find('responsedata').find('hit')
	# print hit.find('title').text
	# 
	


	for k,v in getMapping().iteritems():
		p[k] = hit.find(v).text
		# print k
		# print v

	# m['']

	# p['title'] = hit.find('title').text
	# p['project_acronym'] = hit.find('projectacronym').text


	return p


