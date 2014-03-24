from lxml import etree
from collections import defaultdict

# Data-storage trick from https://gist.github.com/hrldcpr/2012250
def tree(): return defaultdict(tree)

# Define a mapping for <new element> = <old element XPATH>
def getMapping(type):
	m = tree()

	if type == 'project':
		m['title'] = 'title'
		m['status'] = 'desc_status'
		m['status_code'] = 'projectstatus'
		m['objectives'] = 'objective'
		m['project_website'] = 'projecturl'

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

	# Additional fields for the coordinator parsed from top-level
	elif type == 'coordinator':
		m['latitude'] = 'latitude'
		m['longitude'] = 'longitude'
		m['regiondesc'] = 'regiondesc'
		m['regioncode'] = 'regioncode'
		m['citycode'] = 'citycode'
		m['type_desc'] = 'organizationtype_desc'
		m['type_code'] = 'organizationtype_code'
		m['type_num'] = 'organizationtype_num'

	# Additional fields for a non-coordinating partner parsed from the extra array 
	elif type == 'partner':
		m['latitude'] = 'tag_part_latitude'
		m['longitude'] = 'tag_part_longitude'
		m['partner_id'] = 'tag_part_participant_id'

	# For parsing coordinator info from the root of the XML. Used for older projects
	elif type == 'coordinator_root':
		m['name'] = 'organizationname'
		m['contact_full_name'] = 'contact'
		m['contact_last_name'] = 'contact_lastname'
		m['telephone'] = 'contact_tel'
		m['fax'] = 'contact_fax'
		m['country'] = 'countrycode'
		m['city'] = 'citydesc'
		m['address'] = 'address'

	# For parsing parte info from the extra array. Used for older projects
	elif type == 'partner_extra':
		m['name'] = 'tag_part_organizationname'
		m['contact_full_name'] = 'tag_part_contact'
		m['contact_last_name'] = 'tag_part_contact_last_name'
		m['country'] = 'tag_part_countrycode'
		m['city'] = 'tag_part_citydesc'
		m['address'] = 'tag_part_address'
		m['po_box'] = 'tag_part_postcode'
		m['type_desc'] = 'tag_part_organizationtype_desc'
		m['type_code'] = 'tag_part_organizationtype_code'
		m['type_num'] = 'tag_part_organizationtype_num'

	return m

def parse(rcn):
	if rcn.isdigit():
		url = "http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&rcn=" + str(rcn)
		# print "Parsing URL " + url + "..."
	else:
		# Support for using XML files directly
		url = rcn
	
	t = etree.parse(url)
	root = t.getroot()
	hit = t.find('responsedata').find('hit')

	# Contains our final mapping
	data = tree()

	# Parse default project attributes
	mapAttributes(hit, data, 'project')

	# Parse additional partner attributes, and store by partner name (i.e. org. name) 
	p_extras = tree()
	participants_extra = root.xpath("//metadatagroup[@name='tag_participants']/item")

	for p_extra in participants_extra:
		key = p_extra.find("tag_part_organizationname").text.lower()
		mapAttributes(p_extra, p_extras[key], 'partner')

	# Partner/participant attributes
	data['participants'] = list()
	participants = root.xpath("//metadatagroup[@name='tag_erc_fields']/item")


	for participant in participants:
		p2 = defaultdict(str)
		mapAttributes(participant, p2, 'organization')

		if p2['order'] == "1":
			# Add in additional data for the coordinator
			data['coordinator'] = p2['id']
			mapAttributes(hit, p2, 'coordinator')
		else:
			# Add in additional data for participants
			key_org = p2['name'].lower()
			if key_org in p_extras:
				for k2,v2 in p_extras[key_org].iteritems():
					p2[k2] = v2

		# Add this element to the data array
		data['participants'].append(p2)
	
	# XML files for older projects only support participants_extra, so that's our primary source
	if len(participants) == 0 and len(participants_extra) > 0:

		# Parse coordinator
		coord = defaultdict(str)
		mapAttributes(hit, coord, 'coordinator')
		mapAttributes(hit, coord, 'coordinator_root')
		data['participants'].append(coord)

		# Parse the other participants, they are stored in extra
		for p_extra in participants_extra:
			p2 = defaultdict(str)
			mapAttributes(p_extra, p2, 'partner')
			mapAttributes(p_extra, p2, 'partner_extra')
			data['participants'].append(p2)

	return data

# Map attributes from the XML source "hit" to the tree "p", for the givem type
def mapAttributes(hit, p, type):
	for k,v in getMapping(type).iteritems():
		try:
			# Look for the key in the XML source
			# print v + '-->'
			text = hit.find(v).text
			# print "\t" +text

			# Minimal cleanup of mapping values
			if (k == 'latitude' or k == 'longitude'):
				text = text.replace(',', '.')

			# Remove trailing whitespaces
			text = text.strip()

			# Add to the mapping to our data array
			p[k] = text
		except:
			continue
