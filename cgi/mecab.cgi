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
import MeCab

# Show error as a page description.
sys.stderr = sys.stdout
cgitb.enable()

g = rdflib.Graph()
form = cgi.FieldStorage()

print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")


j=form["job"].value
memo = form["memo"].value
memo = memo.decode("utf-8")

def extractKeyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text)
    keywords = []
    while node:
        if node.feature.split(",")[0] == "名詞":
            keywords.append(node.surface)
        node = node.next
    return keywords


memo = memo.encode('utf_8')
keywords = extractKeyword(memo)
print("<div class='tag_memo'>"+memo+"</div>")



###抽出した名詞をタグとして追加
print("<div class='tag_cloud'>")
for q in keywords:
    print("<div class='tag'>"+q+"</div>")
print("</div>")




###関連人物の検索
result = g.parse('../data/dummy.ttl',format='turtle')
keywords.insert(0,j)
print("<div class='relation_list'>")
for q in keywords:
    query = """
    SELECT DISTINCT ?s ?name
    WHERE {
        ?s <http://linkdata.org/property/rdf1s949i#job> ?job .
        ?s <http://www.w3.org/2000/01/rdf-schema#label> ?name .
        OPTIONAL {?s <http://linkdata.org/property/rdf1s949i#close_tag> ?ctag }.
        OPTIONAL {?s <http://linkdata.org/property/rdf1s949i#open_tag> ?otag  }.
        FILTER (regex(?name, \""""+q+"""\",\"i\") || regex(?otag, \""""+q+"""\",\"i\") || regex(?ctag, \""""+q+"""\",\"i\") || regex(?job, \""""+q+"""\",\"i\"))
    }
    """
    
    qres = g.query(query)
    if len(qres)!=0:
        print("<div class='relation_tag'>「"+q+"」つながり</div>")
    for row in qres:
        print("<div class='relation' id='%s'>%s</div>" % row).encode('utf_8')
    
print("</div>")
