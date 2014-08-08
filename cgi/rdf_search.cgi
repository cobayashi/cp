#!/usr/local/bin/python2.7 --
# -*- coding: utf-8 -*-
import os
import cgi
import cgitb
import rdflib
import sys
import re
import pprint
import json


# Show error as a page description.
sys.stderr = sys.stdout
cgitb.enable()

form = cgi.FieldStorage()
q = form["query"].value
g = rdflib.Graph()
query = """
	SELECT DISTINCT ?name ?job ?memo ?s
    WHERE {
    	?s <http://linkdata.org/property/rdf1s949i#job> ?job .
      	?s <http://linkdata.org/property/rdf1s949i#memo> ?memo .
      	?s <http://www.w3.org/2000/01/rdf-schema#label> ?name .
      	OPTIONAL {?s <http://linkdata.org/property/rdf1s949i#close_tag> ?ctag }.
        OPTIONAL {?s <http://linkdata.org/property/rdf1s949i#open_tag> ?otag }.
      	FILTER (regex(?name, \""""+q+"""\",\"i\") || regex(?memo, \""""+q+"""\",\"i\") || regex(?job, \""""+q+"""\",\"i\")|| regex(?otag, \""""+q+"""\",\"i\") || regex(?ctag, \""""+q+"""\",\"i\"))
    }
"""#qを含む人物の名前所属メモを取得するためのクエリ

result = g.parse('../data/dummy.ttl',format='turtle')
qres = g.query(query)
hits = []
counter = 0
for row in qres:
  #print("<div class='profile'><div class= 'name'>%s</div><div class= 'job'>%s</div><div class= 'memo'>%s</div></div>" % row).encode('utf_8')
  counter=counter+1
  i = {"key":counter,"name":row.name,"job":row.job,"memo":row.memo,"s":row.s}
  hits.append(i)
print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")
print json.dumps(hits)
