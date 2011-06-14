#!/usr/bin/python

import cgi
#import cgitb; cgitb.enable()
import semantic
from semantic import stemming,nonsemantic
import re
import math
import time
import cPickle
import urllib2

patt1=r'(\S+)(.*)'
#patt2=r'(\W+)(.*)'
p1=re.compile(patt1,re.IGNORECASE)
#p2=re.compile(patt2,re.IGNORECASE)
univ_dict={}
univ_rank={}
univ_result={}
univ_list=[]
rank_url={}
match_doc=[]

class querying(stemming,nonsemantic):
	def __init__(self):
		pass
	def query(self):
		#print "Content-type: text/html\n\n"
		lis=[]
		list=cgi.FieldStorage()
		if list.has_key('query'):
			print "Content-type: text/html\n\n"
			var1=list['query'].value
			var1=self.replace(var1)
			#print "<p>you have entered<b> %s</b><p>"%(var1)
			ret_value=var1
			while p1.search(var1)!=None:
                                m=p1.search(var1)
                                if m.group(1) not in semantic.stopwords:
                                        term=self.porter(m.group(1))
                                        lis.append(term)
                                var1=m.group(2)
			fh=open('./indexfile.txt','r')
			indexlist=cPickle.load(fh)
			fh.close()
			tmp_lis=[]
			for each in lis:
				if indexlist.has_key(each):
					univ_list.append(each)
					tmp_list=indexlist[each]
					for every in tmp_list:
						for o in every.keys():
							tmp_lis.append(o)
					univ_dict[each]=tmp_lis
					univ_rank[each]=tmp_list
					tmp_lis=[]
			#print "<p>%s</p>"%(univ_dict)
			if univ_dict.__len__()!=0:
				ln=univ_dict.values().__len__()
				tmp_lis=univ_dict.values()
				iter=0
				for ech in tmp_lis[0]:
					for i in range(1,ln):
						if ((ech in tmp_lis[i]) and (ech not in match_doc)):
							iter=iter+1
					if iter==(ln-1):
						match_doc.append(ech)
					iter=0
				#print "<p>univ_dict<br>%s<br>univ_rank<br>%s<br>univ_list<br>%s<br>match_doc<br>%s</p>"%(univ_dict,univ_rank,univ_list,match_doc)
			tmp_rank=float(0)
			for a in match_doc:
				for every in univ_list:
					for ech in univ_rank[every]:
						if ech.keys()[0]==a:
							tmp_rank=tmp_rank+ech.values()[0]
							#print "<p>%s</p>"%a
				univ_result[a]=tmp_rank
			#print univ_result
			fh=open('./urltxt.txt','r')
			url_list=cPickle.load(fh)
			url_dict=url_list[0]
			for i,j in url_dict.iteritems():
				if j in match_doc:
					rank_url[univ_result[j]]=i
			fh.close()
			#print "<p><br>%s<br></p>"%rank_url
			tmp_rank=[]
			tmp_url=[]
			for i,j in rank_url.iteritems():
				tmp_rank.append(i)
			tmp_rank.sort()
			tmp_rank.reverse()
			#print tmp_rank
			return [tmp_rank,ret_value]
		else:
			#print "<p>u have forgot something<br></p></body></html>"
			#url = "http://python.org/pypi"
			print "Location: main.html\n\n"
			#raise SystemExit
			#req=urllib2.HTTPRedirectHandler()
			#req.redirect_request('main.html')
	def htmlpage(self):
		global rank_url
		start=float(time.clock())
		ret_list=self.query()
		end=float(float(time.clock())-start)
		if ret_list==None:
			return None
		tmp_rank=ret_list[0]
		#print "Content-type: text/html\n\n"
		print '''<html><title>Py Search Engine</title><head>
<meta name="author" content="Yerneni Bhaskar Teja" />
<meta name="description" content="Search Engine" />
<meta name="keywords" content="Query,Results,Search,Python" />
<meta http-equiv="Content-Type" content="text/html" />
<style type="text/css">
.stats { background-color:#94e4e8 }
table.stats { border-width:thin;border-color:#0000cd;border-style:solid;}
.href { font-size=100%% }
input.query{ border-width:thin;border-color:#000000;border-style:solid;}
input.submit{ border-width:thin;border-color:#000000;border-style:solid;}
</style>
<script type="text/javascript">
function load()
{
window.document.getElementById("query").focus();
}
</script></head>
<body onload="load()"><form action="querying.py" method="get">
<input type="text" value="%s" size=45 class="query" name="query" id="query" maxlength=2048 title="web search">&nbsp;&nbsp;
<input type="submit" value="Search &raquo;" class="submit">&nbsp;&nbsp;
<b class="href"><a href="main.html">Search home</a>&nbsp;&nbsp;<a href="http://www.orkut.co.in/Main#Community.aspx?cmm=87161974&refresh=1" target="_blank">Community</a>&nbsp;&nbsp;&nbsp;<a href="aboutse.html">About</a></b></form>'''%(ret_list[1])
		print '''<table class="stats" border="0" width="100%%"><tr><td align="left">%d Search results found</td><td align="right">calculated time: %f Seconds</td></tr></table>'''%(tmp_rank.__len__(),end)
		if tmp_rank.__len__()==0:
			print '''<br>Oops!...possibly the keyword you have entered may not be present on www.vrsiddhartha.ac.in<br>Suggestions:<br>*Make sure all words are spelled correctly.<br>
*Try different keywords.<br>*Try more general keywords.<br>*Try fewer keywords.<br><b>still no luck?<br>Send me your feedback:<a href="mailto:prudhviy@gmail.com"> prudhviy@gmail.com</a></b>'''
		print '''<table class="t1" border="0" width=100% height=10 cellspacing=1 cellpadding=5>'''
		for every in tmp_rank:
                	result='http://'+rank_url[every]
                        print '''<tr><td><a href="%s" title="%s">%s</a></td>
</tr>'''%(result,str(every),result)
                print """</table>"""
		print '''</body></html>'''
		
if __name__=='__main__':
	myobj=querying()
	myobj.htmlpage()
