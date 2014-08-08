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

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")

# duumycard(本人)の登録している名刺の人物のURIとその名前を持ってくる
query = """
	SELECT  ?name ?s
     WHERE {
		<http://linkdata.org/resource/rdf1s949i#dummycard> ns1:knows ?s .
		?s rdfs:label ?name .
     }
"""

g = Graph()
g.parse('../data/dummy.ttl',format='turtle')
qres = g.query(query)

# 「参加者」のプルダウンフォームの中身(dummycardが登録した名刺の人物)を繰り返し検索している
# valueにURI 表示は名前
selectionValues = ""
for row in qres:
	selectionValues += "<option value="+ ( row.s ).encode('utf_8') +">"+( row.name ).encode('utf_8')+"</option>"


print str( """
<title>議事録</title>
<body>
	<h1>議事録の新規作成</h1>
	<form name="formToRdf" action="formToRdf.cgi" method="post">
		<p>
		日付：<input type="date" name="date" value=""><br>
		参加者：<select name="mem" multiple>
		"""+
		selectionValues
		+"""
		</select>
		議題：<input type="text" name="title" value=""><br>
		内容：<br>
		<textarea name="textarea1" rows="8" cols="40"></textarea><br>
		備忘録：<br>
		<textarea name="textarea2" rows="4" cols="40"></textarea><br>
		<input type="submit" value="登録">
		</p>
	</form>
</body>
</html>
""")