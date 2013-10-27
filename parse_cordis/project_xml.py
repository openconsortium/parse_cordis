from lxml import etree
from collections import defaultdict

def getMapping(type='project'):
	m = defaultdict(str)

	if type == 'project':
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
	
	elif type == 'organization':
		m['contact_full_name'] = 'contact'
		m['contact_first_name'] = 'contact_first_name'
		m['contact_last_name'] = 'contact_last_name'
		m['contact_title'] = 'contact_title'
		
		m['telephone'] = 'contact_tel'
		m['fax'] = 'contact_fax'

		m['id'] = 'org_id'
		m['name'] = 'legal_name'
		m['acronym'] = 'short_name'

		m['street'] = 'street_name'
		m['city'] = 'town'
		m['po_box'] = 'po_box'
		m['country'] = 'country_ccm'
		m['website'] = 'internet_homepage'
		m['order'] = 'participant_order'

	elif type == 'coordinator':
		m['latitude'] = 'latitude'
		m['longitude'] = 'longitude'
		m['regiondesc'] = 'regiondesc'
		m['regioncode'] = 'regioncode'
		m['citycode'] = 'citycode'
		m['type'] = 'organizationtype_desc'

	elif type == 'partner':
		m['latitude'] = 'tag_part_latitude'
		m['longitude'] = 'tag_part_longitude'
		m['partner_id'] = 'tag_part_participant_id'

	return m

# Data-storage trick from https://gist.github.com/hrldcpr/2012250
def tree(): return defaultdict(tree)


def parse(rcn):
	if rcn.isdigit():
		url = "http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&rcn=" + str(rcn)
	else:
		# Support for using XML files directly
		url = rcn
	
	t = etree.parse(url)
	root = t.getroot()
	hit = t.find('responsedata').find('hit')

	# p = defaultdict(str)
	p = tree()

	# Parse default project attributes
	for k,v in getMapping('project').iteritems():
		try:
			p[k] = hit.find(v).text
		except:
			continue

	# Parse additional partner attributes
	p_extras = defaultdict(str)
	participants_extra = root.xpath("//metadatagroup[@name='tag_participants']/item")
	for p_extra in participants_extra:
		key = p_extra.find("tag_part_organizationname").text
		p_extras[key.lower()] = p_extra.find("tag_part_organizationname").text

	# Partner/participant attributes
	p['participants'] = list()
	participants = root.xpath("//metadatagroup[@name='tag_erc_fields']/item")
	for participant in participants:
		p2 = defaultdict(str)

		for k,v in getMapping('organization').iteritems():
			try:
				p2[k] = participant.find(v).text
			except:
				continue

		if p2['order'] == "1":
			# Add in additional data for the coordinator
			p['coordinator'] = p2['id']
			for k2,v2 in getMapping('coordinator').iteritems():
				try:
					p2[k2] = hit.find(v2).text
				except:
					continue
		else:
			# Add in additional data for participants
			fullname = p2['name']
			if p_extras[fullname.lower()] != "":
				for k2,v2 in getMapping('partner').iteritems():
					try:
						p2[k2] = hit.find(v2).text
					except:
						continue

		p['participants'].append(p2)
	return p


