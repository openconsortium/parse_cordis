#!/usr/local/bin/python

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from collections import defaultdict
from htmllaundry import strip_markup
import urllib2
import logging

def parseHTML(html):
  soup = BeautifulSoup(html)

  l = list()

  # title = soup.find("div", class_="tab_fullresult")

  tbody = soup.table.tbody
  for tr in tbody.find_all("tr"):
    i=0
    for td in tr.find_all("td"):
      i=i+1
      if i == 7:
        val = cleanValue(td.get_text())
        l.append(val)

  return l

def parseHTMLNew(html):
  soup = BeautifulSoup(html)

  l = list()

  divs = soup.find_all("div", class_="resultItem")
  for div in divs:
    item = div.find("input")
    if item:
      val = item.get('value').split(":")
      if len(val) > 1:
        l.append(val[0])

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
  print "Parsing URL " + url + "..."
  response = urllib2.urlopen(url)
  html = response.read()
  return html

def fetchHTMLNew(count):
  params = "REF_PROGRAMMEACRONYM=FP7"
  url = "http://cordis.europa.eu/newsearch/index.cfm?combo_orderby=REC_QV_DATE%3Anumberdecreasing&controlsession=false&page=resultListGET&comboresultperpage=" + str(count) + "&formid=form_proj&useraction=advanced_search&" + params + "&js=1"
  print "Parsing URL " + url + "..."
  response = urllib2.urlopen(url)
  # print url
  html = response.read()
  return html

def parse(query_code, count=10):
  html = fetchHTML(query_code, count)
  l = parseHTML(html)
  return l

def parseNew(count=10):
  html = fetchHTMLNew(count)
  l = parseHTMLNew(html)
  return l

