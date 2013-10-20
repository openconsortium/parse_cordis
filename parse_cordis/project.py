#!/usr/local/bin/python

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from pprint import pprint
from collections import defaultdict
from htmllaundry import strip_markup
import re
import datetime
import time
from datetime import date
import time
import urllib2
import logging

def pp(d):
  for k,v in d.iteritems():
    print k + "\t" + v



def parseHTML(html, data):

  soup = BeautifulSoup(html)
  p = defaultdict(str)

  title = soup.find("div", class_="projttl")

  p['project_acronym'] = cleanValue(title.find("h1").get_text())
  p['title'] = cleanValue(title.find("h2").get_text())

  dates = soup.find("div", class_="projdates")
  p['start_date'] = cleanValue(dates.b.next_sibling)
  p['end_date'] = cleanValue(dates.b.next_sibling.next_sibling.next_sibling.split(" ")[1])
  
  if dates.find('a'):
    p['project_website'] = cleanValue(dates.find('a').get('href'))  
  else:
    p['project_website'] = ''

  p['objectives'] = cleanValue(soup.find("div", class_="projdescr").find("div", class_="tech").p.get_text())

  details = soup.find("div", class_="projdet")
  box_left = details.find("div", class_="box-left")

  p['reference_number'] = cleanValue(box_left.find(text=re.compile("Project reference")).parent.next_sibling.split(":")[1])
  p['status'] = cleanValue(box_left.find(text=re.compile("Status")).parent.next_sibling.split(":")[1])

  p['cost'] = processMoneyValue(box_left.find(text=re.compile("Total cost")).parent.next_sibling.split(":")[1])
  p['funding'] = processMoneyValue(box_left.find(text=re.compile("EU contribution")).parent.next_sibling.split(":")[1])

  box_right = details.find("div", class_="box-right")
  p['programme_acronym'] = cleanValue(box_right.p.find('a').get_text())
  p['project_call'] = cleanValue(box_right.p.next_sibling.next_sibling.br.next_sibling)


  p['contract_types'] = cleanValue(box_right.find(text=re.compile("Contract type")).parent.next_sibling.next_sibling.next_sibling)

  recinfo = soup.find(id="recinfo")
  p['rcn'] = cleanValue(recinfo.find(text=re.compile("Record number")).parent.next_sibling.split(":")[1].split("/")[0])
  p['last_updated'] = cleanValue(recinfo.find(text=re.compile("Last updated on")).parent.next_sibling.split(":")[1])
  
  # Parse coordinator
  p['coordinator'] = parseContact(soup.find(id="coord"))

  # print p['coordinator']
  # return

  # Parse participants
  p['participants'] = list()
  for participant in soup.find_all("div", class_="participant"):
    p['participants'].append(parseContact(participant))
    # break


  return p

def cleanValue(n):
  if isinstance(n, unicode):
    n = n.lstrip()
    n = n.rstrip()
    n = n.replace("\n", "")
    n = n.encode('utf8')
  return n

def parseContact(c):
  d = defaultdict(str)

  d['name'] = c.find("div", class_="name").get_text()

  country = cleanValue(unicode(c.find("div", class_="country").find("a").previous_sibling))
  d['country'] = country

  content = c.find("div", class_="item-content")
  contact = c.find(text=re.compile("Administrative contact")).replace("Administrative contact:", "")
  parseContactName(cleanValue(contact), d)

  d['address'] = cleanValue(unicode(content.br.next_sibling))

  tel = content.find(text=re.compile("Tel:"))
  if tel:
    d['telephone'] = processPhoneNumber(tel)
  
  fax = content.find(text=re.compile("Fax:"))
  if fax:
    d['fax'] = processPhoneNumber(fax)
  
  return d

# Extracts first name, last name and title from a string
def parseContactName(c, d):
  # d = defaultdict(str)
  fullname = c.split("(")[0]
  parts = fullname.split(" ")
  d['contact_first_name'] = parts[0]
  d['contact_last_name'] = ' '.join(parts[1:]).rstrip()
  d['contact_title'] = re.search('\((.+)\)',c).group(1)
  # return d

def processMoneyValue(v):
  return cleanValue(v.replace("EUR", "").replace(" ", ""))

def processPhoneNumber(v):
  return cleanValue(v.split(":")[1])

def parseContactsTable(t):
  orgs = t.find_all(text=re.compile("Organization name:"))
  names = t.find_all(text=re.compile("Name:"))
  tels = t.find_all(text=re.compile("Tel:"))
  faxs = t.find_all(text=re.compile("Fax:"))
  urls = t.find_all(text=re.compile("URL:"))


  ps = list()
  for i, org in enumerate(orgs):

    # print org.next_element

    p = defaultdict(str)
    name = names[i].next_element

    # true if we miss the first name
    # print str(name)
    if ('<ucase>' in name.encode('utf-8')):
      surname = cleanValue(name.next_element)
      # print name.next_element.next_element
      title = cleanValue(name.next_element.next_element).replace("(", "").replace(")","")
      name = ''
    else:
      # Normal case
      surname = name.next_element.next_element
      title = cleanValue(name.next_element.next_element.next_element).replace("(", "").replace(")","")

    address = names[i].parent.parent.next_sibling.next_sibling

    parts = list()
    for el in address.children:
      el = cleanValue(unicode(el.string))
      if el == "Region:":
        break;
      if el != "None" and el != "":
        parts.append(el)

    if len(parts) == 2:
      p['organization_city'] = parts[0]
      p['organization_country'] = parts[1]
    if len(parts) == 3:
      p['organization_address'] = parts[0]
      p['organization_city'] = parts[1]
      p['organization_country'] = parts[2]
    if len(parts) == 4:
      p['organization_address'] = parts[0]
      p['organization_postcode'] = parts[1]
      p['organization_city'] = parts[2]
      p['organization_country'] = parts[3]


    p['contact_name'] = cleanValue(name)
    p['contact_surname'] = cleanValue(surname)
    p['contact_title'] = cleanValue(title)
    p['organization_name'] = cleanValue(org.next_element)

    p['contact_tel'] = cleanValue(tels[i].next_element)
    p['contact_fax'] = cleanValue(faxs[i].next_element)

    p['organization_website'] = cleanValue(urls[i].next_element.string)

    ps.append(p)

  return ps


def fetchHTMLProject(rcn):
  url = "http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&xslt-template=projects/xsl/projectdet_en.xslt&rcn=" + str(rcn)
  response = urllib2.urlopen(url)
  html = response.read()
  return html

def parse(rcn):
  data = defaultdict(lambda : defaultdict(str))
  html = fetchHTMLProject(rcn)
  p = parseHTML(html, data)
  return p


## Example, like http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&xslt-template=projects/xsl/projectdet_en.xslt&rcn=102131
### Using RCN to fetch the doc.
# html_doc = "data_web/people_network.html"
# html_doc = "http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&xslt-template=projects/xsl/projectdet_en.xslt&rcn=102131"
# response = urllib2.urlopen(html_doc)
# html = response.read()
# print html


# main(102131)

# swarmorgan
# main(106786)

# systemage
# main(105875)

# ISBE
# main(104477)


# Use as project.parse(105875)

