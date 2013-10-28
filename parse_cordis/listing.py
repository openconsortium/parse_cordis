#!/usr/local/bin/python

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from collections import defaultdict
from htmllaundry import strip_markup
import urllib2
import logging

# def pp(d):
#   for k,v in d.iteritems():
#     print k + "\t" + v

def parseHTML(html):

  soup = BeautifulSoup(html)

  l = list()

  title = soup.find("div", class_="tab_fullresult")

  tbody = soup.table.tbody
  for tr in tbody.find_all("tr"):
    i=0
    for td in tr.find_all("td"):
      i=i+1
      if i == 7:
        val = cleanValue(td.get_text())
        l.append(val)

  return l

def cleanValue(n):
  if isinstance(n, unicode):
    n = n.lstrip()
    n = n.rstrip()
    n = n.replace("\n", "")
    n = n.encode('utf8')
  return n

def fetchHTML(query_code, count):
  url = "http://cordis.europa.eu/search/index.cfm?fuseaction=proj.printResultList&page=1&perPage=" + str(count) + "&q=" + query_code + "&type=adv"
  response = urllib2.urlopen(url)
  html = response.read()
  return html

def parse(query_code, count=10):
  html = fetchHTML(query_code, count)
  l = parseHTML(html)
  return l


## Example, like http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&xslt-template=projects/xsl/projectdet_en.xslt&rcn=102131
### Using RCN to fetch the doc.
# html_doc = "data_web/people_network.html"
# html_doc = "http://cordis.europa.eu/projects/index.cfm?fuseaction=app.csa&action=read&xslt-template=projects/xsl/projectdet_en.xslt&rcn=102131"
# response = urllib2.urlopen(html_doc)
# html = response.read()
# print html

