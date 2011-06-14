import re
import robotparser
import urllib #actually imports urllib itself
import urllib2
import urlparse
from urlparse import *#imports everything from urlparse
import string
import os
import cPickle
import indexing

patt1=r'([^<>]*?)(<[^>]+?>|</[^>]+?>)(.*)'  #anything, tags , anything
patt2=r'[<>]'				    #for < >
patt3=r'.*<[^<>]*$'		    	    #
patt4=r'''(.*?)(href|src)=["'](.*?)["'](.*)'''    #href search
patt5=r'(\S+)(.*)'			    #to eliminate empty spaces \t \r and spacebars
patt6=r'<link|<img'			    #to remove <link href=''
patt7=r'(.*?)((<script|<style|<!--)|(</script|</style|-->))(.*)'
					    #to remove unwanted data between script styles and comments
patt8=r'(.*?):\d*$'		  	    # url :81 matching
patt9=r'www.(.*)'
patt10=r'(.*)/(.*)'
patt11=r'(^([^./ ]).+)|^./(.*)|^/(.*)|^../(.*)'
patt12=r'([^<>]*)<.*|.*>([^<>]*)|(.*)'
patt13=r'^[^<>]*>(.*)'

p1=re.compile(patt1,re.IGNORECASE)
p2=re.compile(patt2,re.IGNORECASE)
p3=re.compile(patt3,re.IGNORECASE)
p4=re.compile(patt4,re.IGNORECASE)
p5=re.compile(patt5,re.IGNORECASE)
p6=re.compile(patt6,re.IGNORECASE)
p7=re.compile(patt7,re.IGNORECASE)
p8=re.compile(patt8,re.IGNORECASE)
p9=re.compile(patt9,re.IGNORECASE)
p10=re.compile(patt10,re.IGNORECASE)
p11=re.compile(patt11,re.IGNORECASE)
p12=re.compile(patt12,re.IGNORECASE)
p13=re.compile(patt13,re.IGNORECASE)

picdic={}
domain=''
path='./'
hreflist=[]
errorlist={}
count=1
headers={}

class webcrawling:
	"""
	#       Web Crawling starts here    #
	#	exceptions included	    #"""
	def __init__(self,url):
		global domain
		global hreflist
		global headers
		global count
		global picdic
		global path

		rp=robotparser.RobotFileParser()	
		self.rp=rp
		headers['User-Agent']='vrsec crawling robot'
                headers['If-Modified-Since']='Sat, 29 Oct 1994 19:43:31 GMT'
                headers['Accept']='text/html'

	        urlstr=urlparse(url)
		print '		urlparsed: ',urlstr
			        
		domain=p9.search(urlstr[1]).group(1)
			
		self.osexception((path+domain))
		self.path=path+domain+'/'
		print '		domain name: ',domain
                self.urlopenexception(domain,domain) #urlretrieve returns a tuple of two objects(filename,mime_hdrs)
		print '		picdic: ',picdic
		self.urlpickle()
	
		self.domain=domain

	def crawl(self,link):
		global hreflist
		global domain
		global count
		global picdic
		
		print 'picdic[link]',picdic[link]
		st=self.openexception((self.path+str(picdic[link])+'.html'))    #reads the file line by line into a list
		print 'generating for ',link
		for item in st:
			m=p4.search(item)    #patt4=r'''(.*?)(href|src)=["'](.*?)["'](.*)'''
			if m!=None:
				#print m.group()
				if (p6.search(m.group(1))==None):    #patt6=r'<link|<img'
					py=self.urlappend(link,m.group(3))
					#print m.group(2);print py;print 20*'*'
					if py!=None:
						py1=p9.search(py)    #patt9=r'www.(.*)'
			                        if py1!=None:
                        			        py=py1.group(1)
							if py not in hreflist:
								self.urlopenexception(py,link)
							else:
								print 'Already in hreflist'
						else:
        						if py not in hreflist:
		                        			self.urlopenexception(py,link)
							else:
								print 'Already in hreflist'
								
				obj=m
				#print 20*'-';print m.group(3)
				while(p4.search(obj.group(4))!=None):
					m1=p4.search(obj.group(4))
					if(m1!=None):
						#print m1.group(2)
						if (p6.search(m1.group(1))==None):
							py=self.urlappend(link,m1.group(3))
							#print m1.group(2);print py;print 20*'*'
							if py!=None:
								py1=p9.search(py)
								if py1!=None:
									py=py1.group(1)
									if py not in hreflist:
										self.urlopenexception(py,link)
									else:
										print 'Already in hreflist'
								else:
									if py not in hreflist:
										self.urlopenexception(py,link)
									else:
										print 'Already in hreflist'
						#print 40*'*'
						obj=m1
	def urlappend(self,link,u):
		global domain
		urls=urlparse(u)
		if urls.scheme not in ['','http','https']:
			return None
                print 'In appending',urls
                if urls.fragment=='':
                	if urls.netloc=='':#not shown domain urls
                        	m=p11.search(u)
				tp=p10.search(link)
				if m!=None:
                                	if m.group(1)!=None:# path
                                        	if tp!=None:
                                                	#print 'return',tp.group(1)+'/'+m.group(1)
                                                        return tp.group(1)+'/'+m.group(1)
                                                else:
                                                        #print 'return',link+'/'+m.group(1)
                                                        return link+'/'+m.group(1)

					elif m.group(3)!=None:# ./path
						if tp!=None:
							return tp.group(1)+'/'+m.group(3)
	                                        else:
							return link+'/'+m.group(3)
					elif m.group(4)!=None:# /path
						return domain+'/'+m.group(4)
					else:	#../path
						k=m.group(5)
						k1=tp.group(1)
						l=r'^../(.*)'
						pl=re.compile(l,re.IGNORECASE)
						while pl.search(k)!=None:
							m1=pl.search(k)
							tmp=p10.search(k1)
							if tmp!=None:
								k1=tmp.group(1)
							k=m1.group(1)
						else:
							tmp=p10.search(k1)
							if tmp!=None:
								k1=tmp.group(1)
								return k1+'/'+k
							else:
								return k1+'/'+k
							
			else:
                        	if (urls.netloc[-(domain.__len__()):]==domain):#shown domain and sub domain urls
                                	if (urls.query!=''):
                                                return urls.netloc+urls.path+urls.params+'?'+urls.query
                                        else:
                                                return urls.netloc+urls.path+urls.params
				else:
					#print 'inside :81'
					m2=p8.search(urls.netloc)
					if m2!=None:
						if m2.group(1)[-(domain.__len__()):]==domain:
							if urls.query!='':
								return urls.netloc+urls.path+urls.params+'?'+urls.query
							else:
								return urls.netloc+urls.path+urls.params
		#print
	def urlopenexception(self,u,link):
		global hreflist
		global headers
		global errorlist
		global count
		global picdic
		try:
			#print u
			#urls=urlparse('http://'+u)
			#self.rp.set_url("http://"+urls.netloc+"/robots.txt")
			#self.rp.read()
			#if not(self.rp.can_fetch('*',"http://"+u)):
			#	print "http://"+urls.netloc+"/robots.txt"
			#	print "%s not allowed"%(headers['User-Agent'])
			#	print "http://"+u
        		#	return None
		
			#print type(u)
			ul=urllib.quote(u,safe="/$&+,:;=?@")
			print 'quoted url ',ul
			print 'HTML on Page: ',link
			req=urllib2.Request('http://'+ul,None,headers)
			h=urllib2.urlopen(req)
			if h.headers.dict['content-type'].find('text/html')!=-1:
				fh=open(self.path+str(count)+'.html','w')
				print 'CREATING HTML FOR',u
				fh.write(str(unicode(h.read(),errors='ignore')))
                        	fh.close()
				print 
				picdic[u]=count
				count+=1
				hreflist.append(u)
				print 'hrefs length',hreflist.__len__(),'\n'
			else:
				print 'Not HTML'
		except urllib2.URLError,e:
			if u not in errorlist.keys():
				errorlist[u]=str(e)
			print 'HTTPError in opening file: ',e
		except IOError,e:
			if u not in errorlist.keys():	
				errorlist[u]=str(e)
			print 'IOError occured in html validation: ',e
		except Exception,e:
			if (u not in errorlist.keys()):
				errorlist[u]=str(e)
			print 'Error occured ',e
	def urlpickle(self):
                global picdic

                urltxth=open('./urltxt.txt','w')
                piclist=[picdic]
                cPickle.dump(piclist,urltxth)
                urltxth.close()
	def openexception(self,k):
		try:
			fh=open(k,'r')
			r=fh.readlines()
			fh.close()
			return r
		except IOError,e:
			print 'IOError occured in opening file: ',e

	def osexception(self,k):
		try:
			os.mkdir(k)
			os.mkdir(k+'/data')
		except OSError,e:
			print 'OSError occured: ',e
class textpreprocessing(webcrawling):
	#****Text Preprocessing starts here****#
	def __init__(self,max):
		global path
		global domain
		self.path=path+domain+'/'
		c=1
	        while c<=max:
        	        #c=raw_input('enter count:')
                	self.txtpreprocess(c)
                	c=c+1
	def txtpreprocess(self,file):
		#global path
		txtprep=[]
		txt=[]
				
		fh=open((self.path+'data/'+str(file)+'.txt'),'w')

		st=self.openexception((self.path+str(file)+'.html'))    #reads the file line by line into a list
		flag=0 #read data
		flag1=0 #conditional flag to eliminate tagged < useless data >		
		line=1	
		
		for a in st:
			if len(a)>500:
                		#print 'index is ',k.index(a)
                		#print 'length of a ',len(a)
				start=0
				end=500
                		index=st.index(a)
                        	while end<len(a):
                        		l=a[start:end]
                        		st.insert(index,l)
                        		start=end
                        		end=end+500
                        		index=index+1
                		else:
                        		l=a[start:len(a)]
                        		st.insert(index,l)
				st.remove(a)
		print 'splitted'
			
		for a in st:
			
			m2=p3.search(a)
			if m2!=None and flag==0:
				flag1=1
				#print '1line ',line
			m3=p13.search(a)
			if m3!=None and flag==0:
				flag1=0
				#print '0line ',line
				if p3.search(m3.group(1))!=None and flag==0:
					flag1=1
					#print '1line ',line
			while p7.search(a)!=None:
				r3=p7.search(a)
				if r3.group(2)==r3.group(4):
					flag=flag+1;#print 'wflag 0 line ',line;print r3.group(2)
					a=r3.group(5)
				elif r3.group(2)==r3.group(3):
					if flag==0:
						self.txtappend(r3.group(1),flag,flag1,txtprep)
					flag=flag-1;#print 'wflag 1 line ',line;print r3.group(2)
					a=r3.group(5)
				else:
					pass
			else:
				if flag==0:
					self.txtappend(a,flag,flag1,txtprep)
			line=line+1#;print line
		print txtprep.__len__()

		for every in txtprep:
			every=re.sub('&nbsp;',' ',every)
			every=re.sub('&quot;',' ',every)
			every=re.sub('&amp;','&',every)
			while(p5.search(every)!=None):			#patt5=r'^(\s*)$'  
				m5=p5.search(every)
				txt.append(m5.group(1))	#unicode('\x80abc', errors='ignore')
				print m5.group(1),
				print ' ',
				fh.write(m5.group(1)+' ')
				every=m5.group(2)
		
		print txt.__len__()
		print 'file ',file
		print 60*'*' 
		fh.close()
		
		del txtprep
		del txt

	def txtappend(self,a,f,f1,t):
		txtprep=t
		flag=f
		flag1=f1

		m=p1.search(a)
		if (m!=None):
			if (p2.search(m.group(1)) == None):  
				txtprep.append(m.group(1))
				#print 'inside m.g.1',m.group(1)
			if (p2.search(m.group(3)) == None):
				txtprep.append(m.group(3))
				#print 'inside m.g.3',m.group(3)
			obj=m
			while (p1.search(obj.group(3))!=None):  #replace here p1 with p3 for default
				#print "while loop"
				m1=p1.search(obj.group(3))
				
				if (m1!=None):	
					if (p2.search(m1.group(1)) == None):  #r'[<>]'
						txtprep.append(m1.group(1))
						#print 'inside while.m.g.1',m1.group(1)
					obj=m1
				if (p2.search(obj.group(3))==None):
					txtprep.append(obj.group(3))
					#print 'inside while.m.g.3',obj.group(3)
		else:
			m=p12.search(a) #r'([^<>]*)<.*|.*>([^<>]*)|(.*)'
			if flag==0:
				if m!=None:
					if m.group(1)!=None:
						try:
							a=txtprep.pop()
							a=a+m.group(1)
							txtprep.append(a)
							#print 'inside else(1)',m.group(1)
						except:
							txtprep.append(m.group(1))	
					elif m.group(2)!=None:
						txtprep.append(m.group(2))
						#print 'inside else(2)',m.group(2)
					else:
						if flag1==0:
							txtprep.append(m.group(3))
							#print 'inside else(3) ',m.group(3)
							#print ' flag1 is ',flag1
if __name__=='__main__':
	url=raw_input('enter the url(http://www.example.com):')
	#url='http://www.vrsiddhartha.ac.in'
	crawl_obj=webcrawling(url)
	print 'inside main',crawl_obj.domain
	for everyurl in hreflist:
		print 'call hreflist',everyurl
		crawl_obj.crawl(everyurl)
	print 'Error list is as follows',errorlist
	info_list=[crawl_obj.domain,hreflist.__len__()]
	fh=open(path+crawl_obj.domain+'/domaininfo.txt','w')
	cPickle.dump(info_list,fh)
	fh.close()
	fh=open(path+crawl_obj.domain+'/errorlist.txt','w')
	cPickle.dump(errorlist,fh)
	fh.close()
	#txt preprocessing#
	print domain
	fh=open(path+domain+'/domaininfo.txt','r')
	list=cPickle.load(fh)
	fh.close()
	txtpp_obj=textpreprocessing(list[1])
	#indexing#
	indexing_obj=indexing.indexing(path+list[0]+'/')
	indexing_obj.index_start(list[1])
	crawl_obj.urlpickle()
