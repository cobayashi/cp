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

target = form["target"].value

g = Graph()
target_id = rdflib.term.URIRef(form["target"].value)
g.parse('../data/dummy.ttl',format='turtle')
g.remove( (target_id, RDFS.label, None) ) # remove triples about target_is
g.remove( (target_id, cp.job, None) )
g.remove( (target_id, cp.memo, None) )
g.remove( (target_id, cp.reliability, None) )
g.add( (target_id, RDFS.label, Literal(form["edit_name"].value,lang='ja')) )
g.add( (target_id, cp.job, Literal(form["edit_job"].value,lang='ja')) )
g.add( (target_id, cp.memo, Literal(form["edit_memo"].value,lang='ja')) )
g.add( (target_id, cp.reliability, Literal(form["reliability"].value)) )

editedGraph = g.serialize(format='turtle')
file = open("../data/dummy.ttl","w")
file.write(editedGraph)