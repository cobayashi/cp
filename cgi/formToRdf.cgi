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

# 謎のもの
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
h = NullHandler()
logging.getLogger("rdflib.term").addHandler(h)


# DC.date
# DC.subject
# DC.discription
cp = Namespace("http://linkdata.org/property/rdf1s949i#")
# cp.member
# cp.reminder


form = cgi.FieldStorage() # POSTで渡したフォーム情報の格納場所

# getfirst('input要素のname属性', 'わからん')　← 合致した最初の値を取得
date = form.getfirst('date', '')
memberURIs= form.getlist('mem')
memberRDFs = []
title = form.getfirst('title', '')
txt1 = form.getfirst('textarea1', '')
txt2 = form.getfirst('textarea2', '')


sys.stderr = sys.stdout
cgitb.enable()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")


d = datetime.datetime.today()
date = d.strftime("%Y/%m/%d/%H.%M.%S")
dailyID = rdflib.term.URIRef("http://example.com/testid/"+date)

# 参加者のURIをRDFの形に変換しておく
for memberURI in memberURIs:
	memberRDFs.append(rdflib.term.URIRef(memberURI))


g = Graph()
g.parse('../data/log.ttl',format='turtle')

g.remove( (dailyID, DC.date, None) )
g.remove( (dailyID, cp.member, None) )
g.remove( (dailyID, DC.subject, None) )
g.remove( (dailyID, DC.discription, None) )
g.remove( (dailyID, cp.reminder, None) )

for memberRDF in memberRDFs:
	g.add( (dailyID, cp.member, memberRDF ) )

g.add( (dailyID, DC.date, Literal(date,lang='ja') ) )	
g.add( (dailyID, DC.subject, Literal(title,lang='ja') ) )
g.add( (dailyID, DC.discription, Literal(txt1,lang='ja') ) )
g.add( (dailyID, cp.reminder, Literal(txt2,lang='ja') ) )

editedGraph = g.serialize(format='turtle') #turtleに変換

query = """
    SELECT DISTINCT ?name
     WHERE{
        <"""+dailyID+"""> cp:member ?member .
        ?member rdfs:label ?name .
     }
"""

g.parse('../data/dummy.ttl',format='turtle')
nameRes = g.query(query)



file = None
try:
    file = open("../data/log.ttl", "w") # 書き込みモードでファイルオープン
    file.write(editedGraph) # 書き込み

    # date, title, txt1, txt2の表示はLiteralを使えばOK print (Literal(date))
    # mamberの場合は、URIをとれてるなら、それをクエリにしてdummy.ttlにリクエスト（レスポンスで名前が返ってくるはず）
    member = ""
    for find in nameRes:
        member += (find.name).encode('utf_8')

    print ("""
        <title>議事録</title>
        <h1>"""+Literal(title).encode('utf_8')+"""</h1>
        <p>日付："""+Literal(date).encode('utf_8')+"""<br>
           参加者："""+member+"""<br>
        内容："""+Literal(txt1).encode('utf_8')+"""<br>
        備忘録："""+Literal(txt2).encode('utf_8')+"""</p>
    """)

except IOError:
	print("IOError")
finally:
    if(file):
        file.close()