#!/usr/local/bin/python2.7 --
# -*- coding: utf-8 -*-
import os
import cgi
import cgitb
import rdflib
import sys
import re
import pprint
import urllib
import logging
import datetime
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, FOAF, DC

sys.stderr = sys.stdout
cgitb.enable()

form = cgi.FieldStorage()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")

query = """
	SELECT DISTINCT ?date ?subject ?s
	 WHERE {
		?s dc:date ?date .
		?s dc:subject ?subject .
	 }
"""

query2 = """
	SELECT ?member ?name ?s
	 WHERE {
	 	?s cp:member ?member .
	 	?member rdfs:label ?name .
	 }
"""

g = Graph()
g.parse('../data/log.ttl',format='turtle') # 議事録のデータ
qres = g.query(query)
g.parse('../data/dummy.ttl',format='turtle')
nameRes = g.query(query2)

member = ""
for find in nameRes:
	member += (find.name).encode('utf_8')

for list in qres:
	print ( """
		<title>議事録一覧</title>
		<a href='./profLinkLog.cgi?s="""+urllib.quote(list.s).encode('utf_8')+"""'>"""+(list.subject).encode('utf_8')+"""</a>
		<span style='color:lightgrey;'>"""+(list.date).encode('utf_8')+"""</span><br>
		"""+member+"""<br>
		<br>
	""")