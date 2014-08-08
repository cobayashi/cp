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
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, FOAF

RDF.type
# = rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
RDFS.label
# = rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label')
FOAF.knows
# = rdflib.term.URIRef(u'http://xmlns.com/foaf/0.1/knows')
cp = Namespace("http://linkdata.org/property/rdf1s949i#")
cp.job
cp.memo
cp.reliability
cp.open_tag
cp.close_tag

# Show error as a page description.
sys.stderr = sys.stdout
cgitb.enable()

form = cgi.FieldStorage()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")

#文字列だったのを分割して配列に
target = form["target"].value
try:
	openarray = form["open"].value.split(',')
except KeyError:
	openarray = []
try:
	closearray = form["close"].value.split(',')
except KeyError:
	closearray = []	
try:
	knowsarray = form["knows"].value.split(',')
except KeyError:
	knowsarray = []	



#あたらしいタグに書き換え
g = Graph()
target_id = rdflib.term.URIRef(form["target"].value)
g.parse('../data/dummy.ttl',format='turtle')
g.remove( (target_id, cp.open_tag, None) ) # remove open_tag
g.remove( (target_id, cp.close_tag, None) )
g.remove( (target_id, FOAF.knows, None) )

for o in openarray :
	g.add( (target_id, cp.open_tag, Literal(o,lang='ja')) )
for c in closearray :
	g.add( (target_id, cp.close_tag, Literal(c,lang='ja')) )
for k in knowsarray :
	g.add( (target_id, FOAF.knows, rdflib.term.URIRef(k) ) )

#上書き
editedGraph = g.serialize(format='turtle')
with open("../data/dummy.ttl","w") as f:
    f.write(editedGraph)
