import string
stopwords=['about','a','an','are','as','at','and','be','by','for','from','how','in','is','of',\
'on','or','that','the','this','to','was','what','when','where','who','whom','whose','will','with',\
'while']
class nonsemantic:
	def __init__(self):
		pass
	def replace(self,each):
		each=string.lower(each)
                each=string.replace(each,'&lt;','<')
                each=string.replace(each,'&gt;','>')
                each=string.replace(each,'&copy;',' ')
                each=string.replace(each,'&',' and ')
                each=string.replace(each,',',' ')
                each=string.replace(each,';',' ')
                each=string.replace(each,':',' ')
                each=string.replace(each,'?',' ')
                each=string.replace(each,'.',' ')
                each=string.replace(each,'*',' ')
                each=string.replace(each,"'",' ')
                each=string.replace(each,'"',' ')
                each=string.replace(each,'/',' ')
                each=string.replace(each,'|',' ')
                each=string.replace(each,')',' ')
                each=string.replace(each,'(',' ')
                each=string.replace(each,'[',' ')
                each=string.replace(each,']',' ')
                each=string.replace(each,'_',' ')
                each=string.replace(each,'-',' ')
 	        each=string.replace(each,'@',' ')
		return each
class stemming:
	def __init__(self):
		pass
	def step1abc(self,term):
		l=-(term.__len__())
		### step 1a ###
		if term[-1]=='s':
			if term[-4:]=='sses':
				term=term[l:-4]+'ss'
			elif term[-3:]=='ies':
				term=term[l:-3]+'i'
			elif term[-2:]=='ss':
				term=term[l:-2]+'ss'
			elif term[-1:]=='s':
				term=term[l:-1]
			else: pass
		### step 1b ###
		if term[-3:]=='eed':
			st=term[l:-3]
			m=self.mcal(st)
			if m>0:
				term=term[l:-3]+'ee'
		elif (term[-2:]=='ed' and self.vowel_stem(term[l:-2])):
			term=term[l:-2]
			term=self.step1bb(term,l)
		elif (term[-3:]=='ing' and self.vowel_stem(term[l:-3])):
			term=term[l:-3]
			term=self.step1bb(term,l)
		else: pass
		### step 1c ###
		if (term[-1:]=='y' and self.vowel_stem(term[l:-1])):
			term=term[l:-1]+'i'
		#print 'inside 1abc',term
		return term
	def step2(self,term):
		l=-(term.__len__())
		if term[-2:-1]=='a':
			if (term[-7:]=='ational' and (self.mcal(term[l:-7])>0)):
				term=term[l:-7]+'ate'
			elif (term[-6:]=='tional' and (self.mcal(term[l:-6])>0)):
				term=term[l:-6]+'tion'
		if term[-2:-1]=='c':
			if (term[-4:]=='enci' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]+'ence'
			elif (term[-4:]=='anci' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]+'ance'
		if term[-2:-1]=='e':
			if (term[-4:]=='izer' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]+'ize'
		if term[-2:-1]=='l':
			if (term[-3:]=='bli' and (self.mcal(term[l:-3])>0)):
				term=term[l:-3]+'ble'
			elif (term[-4:]=='alli' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]+'al'
			elif (term[-5:]=='entli' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'ent'
			elif (term[-3:]=='eli' and (self.mcal(term[l:-3])>0)):
				term=term[l:-3]+'e'
			elif (term[-5:]=='ousli' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'ous'
		if term[-2:-1]=='o':
			if (term[-7:]=='ization' and (self.mcal(term[l:-7])>0)):
				term=term[l:-7]+'ize'
			elif (term[-5:]=='ation' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'ate'
			elif (term[-4:]=='ator' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]+'ate'
		if term[-2:-1]=='s':
			if (term[-5:]=='alism' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'al'
			elif (term[-7:]=='iveness' and (self.mcal(term[l:-7])>0)):
				term=term[l:-7]+'ive'
			elif (term[-7:]=='fulness' and (self.mcal(term[l:-7])>0)):
				term=term[l:-7]+'ful'
			elif (term[-7:]=='ousness' and (self.mcal(term[l:-7])>0)):
				term=term[l:-7]+'ous'
		if term[-2:-1]=='t':
			if (term[-5:]=='aliti' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'al'
			elif (term[-5:]=='iviti' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'ive'
			elif (term[-6:]=='biliti' and (self.mcal(term[l:-6])>0)):
				term=term[l:-6]+'ble'
		if term[-2:-1]=='g':
			if (term[-4:]=='logi' and (self.mcal(term[l:-4])>0)):
				print 'hi'
				term=term[l:-4]+'log'
		#print 'inside 2',term
		return term
	def step3(self,term):
		l=-(term.__len__())
		if term[-1:]=='e':
			if (term[-5:]=='icate' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'ic'
			elif (term[-5:]=='ative' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]
			elif (term[-5:]=='alize' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'al'
		if term[-1:]=='i':
			if (term[-5:]=='iciti' and (self.mcal(term[l:-5])>0)):
				term=term[l:-5]+'ic'
		if term[-1:]=='l':
			if (term[-4:]=='ical' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]+'ic'
			elif (term[-3:]=='ful' and (self.mcal(term[l:-3])>0)):
				term=term[l:-3]
		if term[-1:]=='s':
			if (term[-4:]=='ness' and (self.mcal(term[l:-4])>0)):
				term=term[l:-4]
		#print 'inside 3',term
		return term
	def step4(self,term):
		l=-(term.__len__())
		if term[-2:-1]=='a':
			if (term[-2:]=='al' and (self.mcal(term[l:-2])>1)):
				term=term[l:-2]
		if term[-2:-1]=='c':
			if (term[-4:]=='ance' and (self.mcal(term[l:-4])>1)):
				term=term[l:-4]
			elif (term[-4:]=='ence' and (self.mcal(term[l:-4])>1)):
				term=term[l:-4]
		if term[-2:-1]=='e':
			if (term[-2:]=='er' and (self.mcal(term[l:-2])>1)):
				term=term[l:-2]
		if term[-2:-1]=='i':
			if (term[-2:]=='ic' and (self.mcal(term[l:-2])>1)):
				term=term[l:-2]
		if term[-2:-1]=='l':
			if (term[-4:]=='able' and (self.mcal(term[l:-4])>1)):
				term=term[l:-4]
			elif (term[-4:]=='ible' and (self.mcal(term[l:-4])>1)):
				term=term[l:-4]
		if term[-2:-1]=='n':
			if (term[-3:]=='ant' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
			elif (term[-5:]=='ement' and (self.mcal(term[l:-5])>1)):
				term=term[l:-5]
			elif (term[-4:]=='ment' and (self.mcal(term[l:-4])>1)):
				term=term[l:-4]
			elif (term[-3:]=='ent' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
		if term[-2:-1]=='o':
			if (term[-3:]=='ion' and (term[-4:-3] in ['s','t']) and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
			elif (term[-2:]=='ou' and (self.mcal(term[l:-2])>1)):
				term=term[l:-2]
		if term[-2:-1]=='s':
			if (term[-3:]=='ism' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
		if term[-2:-1]=='t':
			if (term[-3:]=='ate' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
			elif (term[-3:]=='iti' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
		if term[-2:-1]=='u':
			if (term[-3:]=='ous' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
		if term[-2:-1]=='v':
			if (term[-3:]=='ive' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
		if term[-2:-1]=='z':
			if (term[-3:]=='ize' and (self.mcal(term[l:-3])>1)):
				term=term[l:-3]
		#print 'inside 4',term
		return term
	def step5ab(self,term):
		l=-(term.__len__())
		### step 5a ###
		if term[-1:]=='e':
			if (self.mcal(term[l:-1])>1):
				term=term[l:-1]
			elif ((self.mcal(term[l:-1])==1) and (not self.cvc(term[l:-1]))):
				term=term[l:-1]
		### step 5b ###
		if self.doublec(term):
			if (term[-1:]=='l' and self.mcal(term)>1):
				term=term[l:-1]
		#print 'inside 5',term
		return term
			
		
	def step1bb(self,term,l):
		if term[-2:]=='at':
			term=term[l:-2]+'ate'
		elif term[-2:]=='bl':
			term=term[l:-2]+'ble'
		elif term[-2:]=='iz':
			term=term[l:-2]+'ize'
		elif self.doublec(term) and (term[-1:] not in ['l','s','z']):
			term=term[l:-1]
		elif self.mcal(term)==1 and self.cvc(term):
			term=term+'e'
		else:pass
		return term
	def cvc(self,term):
		form=self.vc_form(term)
		if form[-3:]=='cvc':
			if term[-1:] not in ['w','x','y']:
				return 1
			else:
				return 0
		else:return 0
			
	def doublec(self,str):
		if str[-1:] not in ['a','e','i','o','u','y']:
			if str[-1:]==str[-2:-1]:
				return 1
			else: return 0
		
	
	def vowel_stem(self,str):
		tmp=self.vc_form(str)
		for every in tmp:
			if every=='v':
				return 1
	def mcal(self,s):
		tmpst=self.vc_form(s)
		m=0
		l=-(tmpst.__len__())
		if tmpst[0:1]=='c':
			mstr=tmpst[(l+1):-1]
			#print mstr
			for every in mstr:
				if every=='v':
					m=m+1
		else:
			mstr=tmpst[l:-1]
			for every in mstr:
				if every=='v':
					m=m+1
		#print 'm= ',m
		return m	
	def vc_form(self,st):
		tmpst=''
        	prev=''
        	vlist=['a','e','i','o','u']
        	for every in st:
			#print every
                	if every in vlist:           
                        	if tmpst[-1:]!='v':
                                	tmpst=tmpst+'v'
			else:
                        	if every=='y':
                                	if prev in vlist:
                                        	if tmpst[-1:]!='c':
                                                	tmpst=tmpst+'c'
                                	else:
                                        	if tmpst[-1:]!='v':
                                                	tmpst=tmpst+'v'
                                        	else:
                                                	tmpst=tmpst+'c'
                        	else:
                                	if tmpst[-1:]!='c':
                                        	tmpst=tmpst+'c'
						#print 'else c',every
			prev=every
		#print 'vc format: ',tmpst
		return tmpst
	def porter(self,term):
                #term=raw_input('enter a word: ')
                if term!='' and term.__len__()>3:
                        term=self.step1abc(term)
                        term=self.step2(term)
                        term=self.step3(term)
                        term=self.step4(term)
                        term=self.step5ab(term)
		return term
if __name__=='__main__':
	obj=stemming()
	term=raw_input('enter a word: ')
	term=obj.porter(term)
	print term
