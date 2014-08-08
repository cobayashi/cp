#!/usr/local/bin/python2.7 --
# -*- coding: utf-8 -*-
import os
import cgi
import cgitb
import rdflib
import sys
import re
import pprint
import logging
import urllib

logging.basicConfig()

# Show error as a page description.
sys.stderr = sys.stdout
cgitb.enable()

form = cgi.FieldStorage()
s = form["s"].value
g = rdflib.Graph()

###名前が一致する人物の所属と名前とメモとリソースURIを取得するためのクエリ
query = """
  SELECT ?job ?name ?memo
    WHERE {
      <"""+s+"""> cp:job ?job .
      <"""+s+"""> cp:memo ?memo .
      <"""+s+"""> rdfs:label ?name .
    }
"""


###名前が一致する人物の重要度を取ってくるためのクエリ
qrel = """
  SELECT  ?reliability
    WHERE {
      <"""+s+"""> cp:reliability ?reliability .
    }
"""


###名前が一致する人物の公開タグを取ってくるためのクエリ
qotag = """
  SELECT  ?open_tag
    WHERE {
      <"""+s+"""> cp:open_tag ?open_tag .
    }
"""

###名前が一致する人物の非公開たぐを取得するためのクエリ
qctag = """
  SELECT  ?close_tag
    WHERE {
      <"""+s+"""> cp:close_tag ?close_tag .
    }
"""

###名前が一致する人物の知人を取得するためのクエリ
qknows = """
  SELECT  ?kname ?kjob
    WHERE {
      <"""+s+"""> ns1:knows ?knows .
      ?knows rdfs:label ?kname .
      ?knows cp:job ?kjob .
    }
"""

###議事録の議題（タイトル）を取得するためのクエリ
qsub = """
 SELECT DISTINCT ?s ?subject ?date
    WHERE {
     ?s cp:member <"""+s+"""> .
     ?s dc:subject ?subject .
     ?s dc:date ?date .
    }
  """

g.parse('../data/dummy.ttl',format='turtle')#turtleファイル読む

qres = g.query(query)
qrelres = g.query(qrel)
qores = g.query(qotag)
qcres = g.query(qctag)
qkres = g.query(qknows)###クエリ投げる

g.parse('../data/log.ttl',format='turtle')
qsres = g.query(qsub)

###帰ってきたのをhtmlに成形
print ('Content-type: text/html; charset=UTF-8')
print ("\r\n\r\n")
#for row in qres:
    #print("<div class= 'card_image'><img src='img/meishi.png'/></div><form id='edit'><input type='hidden' name='target' value='%s'><input type='text' name='edit_job' class= 'job_detail' value='%s'><br><input type='text'  class= 'name_detail' name='edit_name' value='%s'><br><select name='reliability'><option value='1'>1</option><option value='2'>2</option><option value='3' selected>3</option><option value='4'>4</option><option value='5'>5</option></select><textarea class= 'memo_detail' name='edit_memo'>%s</textarea><br></form>" % row).encode('utf_8')
for row in qres:
  print("""
  <div class= 'card_image'><img src='img/meishi.png'/></div>
  <form id='edit'>
    <input type='hidden' name='target' value=\""""+s+"""\">
    <input type='text' name='edit_job' class= 'job_detail' value=\""""+row.job+"""\">
    <br>
    <input type='text'  class= 'name_detail' name='edit_name' value=\""""+row.name+"""\">
    <br>
    <select name='reliability'>
      <option value='1'>1</option>
      <option value='2'>2</option>
      <option value='3' selected>3</option>
      <option value='4'>4</option>
      <option value='5'>5</option>
    </select>
    <textarea class= 'memo_detail' name='edit_memo'>"""+row.memo+"""</textarea>
    <br>
  </form>
  """).encode('utf_8')
for rel in qrelres:
  print ("<div class='rel'>reliability: %s</div>" % rel).encode('utf_8')
for otag in qores:
  print ("<div class='open_tag'>%s</div>" % otag).encode('utf_8')
for ctag in qcres:
  print ("<div class='close_tag'>%s</div>" % ctag).encode('utf_8')
print ("<div class='k'>knows:")
for k in qkres:
  print ("<div class='knows'>%s@%s</div>" % k).encode('utf_8')
print ("</div>")
for log in qsres:
  print ("<div class='log'><a href='./cgi/profLinkLog.cgi?s="+urllib.quote(log.s)+"'>subject:"+log.subject+"</a> date:"+log.date+"</div>").encode('utf_8')