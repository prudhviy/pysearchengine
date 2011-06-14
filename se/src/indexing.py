import re
import math
import os
import string
import cPickle
import semantic
from semantic import stemming,nonsemantic

patt1=r'(\S+)(.*)'
#patt2=r'(\W+)(.*)'
p1=re.compile(patt1,re.IGNORECASE)
#p2=re.compile(patt2,re.IGNORECASE)
#path='/root/python/urls/vrsiddhartha.ac.in/data/'
rankcal={}
tfcal={}
idfcal={}
rankdict={}

class indexing(stemming,nonsemantic):
        def __init__(self,p):
		self.path=p+'data/'
		print self.path
                try:
                        os.mkdir(self.path+'data1')
                except:
                        print 'directory exists'
	def index(self,file):
                list=[]
                fh=open((self.path+str(file)+'.txt'),'r')
                k=fh.readlines()
                fh.close()
                for each in k:
                        each=self.replace(each)
                        while p1.search(each)!=None:
                                m=p1.search(each)
                                print m.group(1),
				print ' ',
				if m.group(1) not in semantic.stopwords:
					term=self.porter(m.group(1))	
                                	list.append(term)
                                	print term,
				print '|',
                                each=m.group(2)
                f=open((self.path+'data1/'+str(file)+'.txt'),'w')
                cPickle.dump(list,f)
                f.close()
                del list

	def tfidf(self,file,D):
		global rankcal
		global tfcal
		global idfcal
		print 'file ',file
		fh=open((self.path+'data1/'+str(file)+'.txt'),'r')
		lis=cPickle.load(fh)
		tf_num=0
		tf_den=lis.__len__()
		idf_den=1
		for every in lis:
			if every not in rankcal.keys():
				for ech in lis:
					if ech==every:
						tf_num=tf_num+1
				rankcal[every]=[file]
				tfcal[every]=[{file:[tf_num,tf_den]}]
				idfcal[every]={'idf':[D,idf_den]}
				tf_num=0
			else:  #already present
				if file not in rankcal[every]: #new file
					rankcal[every].append(file)
					tmp=idfcal[every]['idf'].pop()+1
					idfcal[every]['idf'].append(tmp)
					tf_num=0
					for ech in lis:
						if ech==every:
							tf_num=tf_num+1
					tfcal[every].append({file:[tf_num,tf_den]})
					tf_num=0
				else:  #current file
					pass
			
		#print rankcal
		print 'no of unique terms ',rankcal.keys().__len__()
		print 100*'-'
	
	def ranking(self):
		global rankdict
		fh=open(self.path+'data1/tfcal.txt','r')
		tfdict=cPickle.load(fh)
		fh.close()
		fh=open(self.path+'data1/idfcal.txt','r')
		idfdict=cPickle.load(fh)
		fh.close()
		tmplis=[]
		tmpdict={}
		for every in tfdict.keys():
			tmp_idf=idfdict[every]['idf']
                        idf=float(math.log(float(tmp_idf[0])/float(tmp_idf[1])))
			for ech in tfdict[every]:
				for term_docid,tmp_tf in ech.iteritems():
					tf=(float(tmp_tf[0])/float(tmp_tf[1]))
					tmpdict[term_docid]=float(tf*idf)
					print 'generating for ',every
					tmplis.append(tmpdict)
					rankdict[every]=tmplis
					tmpdict={}
			tmplis=[]
		print rankdict
		fh=open('./indexfile.txt','w') #fh=open(self.path+'/indexfile.txt','w')
		cPickle.dump(rankdict,fh)
		fh.close()
	def index_start(self,D):
		c=1
		while c<=D:
	                print 'file ',c
        	        self.index(c)
                	c=c+1
                	print 60*'#'
        	print 'Completed'
        	c=1
       		while c<=D:
                	#c=raw_input('enter the file: ')
                	self.tfidf(c,D)
                	c=c+1
        	print 100*'#'
	        print tfcal
        	print 100*'*'
        	print idfcal
        	fh=open(self.path+'data1/tfcal.txt','w')
        	cPickle.dump(tfcal,fh)
        	fh.close()
        	fh=open(self.path+'data1/idfcal.txt','w')
        	cPickle.dump(idfcal,fh)
        	fh.close()
        	self.ranking()

if __name__=='__main__':
	myobj=indexing()
	f=open('/root/python/urls/vrsiddhartha.ac.in/domaininfo.txt','r')
        domain_info=cPickle.load(f)
        f.close()
        D=domain_info[1]
	c=1
	while c<=D:
		print 'file ',c
		myobj.index(c)
		c=c+1
		print 60*'#'
	print 'Completed'
	c=1
	while c<=D:
		#c=raw_input('enter the file: ')
		myobj.tfidf(c,D)
		c=c+1
	print 100*'#'
	print tfcal
	print 100*'*'
	print idfcal
	fh=open(path+'data1/tfcal.txt','w')
        cPickle.dump(tfcal,fh)
        fh.close()
        fh=open(path+'data1/idfcal.txt','w')
        cPickle.dump(idfcal,fh)
        fh.close()
	myobj.ranking()
