#! /usr/bin/env python

import sys
import re


class MarkUp:

	#initialize text, language's name and list_, a list with the text splitted by \n
	def __init__(self,file,language):
	    self.text=open(file,'r').read()
	    self.language=language
	    self.name=file
	    self.list_=self.text.split('\n')
	
	
	#making the text's title if it exists
	def h1(self):	
		if not re.match(r'\w+',self.list_[1]):
			self.list_[0]='<h1> '+self.list_[0]+' </h1>'

			
	#adding all paragraph's titles only between ''\w+''
	def h2(self):
		for n in range(len(self.list_)-2):
			if ( not re.match(r'[\w\-\d]+',self.list_[n]) 
			and not re.match(r'[\w\-\d]+',self.list_[n+2]) 
			and re.match(r'\w+',self.list_[n+1]) ):
				self.list_[n+1]='<h2> '+self.list_[n+1]+' </h2>'
		
		
	#dividing up text in paragraphes
	def par(self):
		
		#reducing all '  ' and similar to ''
		for n in range(len(self.list_)):
			if not re.match(r'[\w<>\-]+',self.list_[n]):
				self.list_[n]=''
		
		#adding a '' at the end of the list to manage indexError
		self.list_.append('')
		
		#taking the index of every space
		space_index = [n for n,el in enumerate(self.list_) if el=='']
		
		#markup paragraph
		
		#to make it run we should define a space something which respects this pattern \w '' \w
		#now this is not working
		#dealing with particular cases of 1 or 2 ''
		if len(space_index)==1:
		#the only '' is the one appended by me
			self.list_[0]='<p> '+self.list_[0]
			self.list_[-1]=self.list_[-1]+' </p>'
			#breaking the following while to avoid repetition
			space_index=None
		
		if len(self.list_)==2 and not re.match(r'\s*',self.list_[1]):
		#there is no title
			self.list_[0]='<p> '+self.list_[0]
			self.list_[space_index.pop(0)]='</p><p> '
			self.list_[-1]=self.list_[-1]+' </p>'
			
		#extract the indexes of the spaces
		sp1=space_index.pop(0)
		while len(space_index):
			sp2=space_index.pop(0)
				#if there is a paragraph insert markup 
			if sp2-sp1>2:
				self.list_[sp1+1]='<p> '+self.list_[sp1+1]
				self.list_[sp2-1]=self.list_[sp2-1]+' </p>'
			sp1=sp2
	
		#removing from list the artificial ''
		self.list_.pop()
	
	
	def lists(self):
		#add spaces to avoid indexError
		self.list_.append('')
		self.list_.append('')
		
		#markup in betweeners
		for n in range(len(self.list_)-2):
			if ( ( re.match(r'[\s*\-]+',self.list_[n]) or re.match(r'\s*<li>',self.list_[n]) ) 
			and re.match(r'[\s*\-]+',self.list_[n+1]) 
			and re.match(r'[\s*\-]+',self.list_[n+2]) ):
				#removing - from the string's beginning
				self.list_[n+1]=self.list_[n+1][self.list_[n+1].index('-')+1:]
				#markup element
				self.list_[n+1]='<li> '+self.list_[n+1]+' </li>'
		
		#markup all last elements
		for n in range(len(self.list_)-1):
			if re.match(r'<li>',self.list_[n]) and re.match(r'\s*\-',self.list_[n+1]):
				#removing - from the string's beginning
				self.list_[n+1]=self.list_[n+1][self.list_[n+1].index('-')+1:]
				#markup element
				self.list_[n+1]='<li> '+self.list_[n+1]+' </ul></li>'
				
		
		
		#markup all first elements
		
		for n in range(len(self.list_)-1):
			if re.match(r'[^\-]+',self.list_[n]) and re.match(r'[\s*\-]+',self.list_[n+1]):
				#removing - from the string's beginning
				self.list_[n+1]=self.list_[n+1][self.list_[n+1].index('-')+1:]
				#markup element
				self.list_[n+1]='<ul><li> '+self.list_[n+1]+' </li>'
		
		
		#removing spaces
		self.list_.pop()
		self.list_.pop()  
		
	
	#to markup mail and numbers you must substitute the list element with a new one, only working 
	#with re.sub() doesn't lead to the correct result, you lost the element just created
	#as soon as you leave the for iteration
	def mail(self):
		mail=re.compile(r'([\w\-\._]+@[\w\-\._]+)')
		self.list_=[re.sub(mail,r'<em>\1</em>',self.list_[n]) for n,el in enumerate(self.list_) ]

	
	def numbers(self):
		number=re.compile('(\d+\-\d+)')
		self.list_=[re.sub(number,r'<em>\1</em>',self.list_[n]) for n,el in enumerate(self.list_)]

	
	#doesn't need any comment. you don't understand? read a fucking book donkey!!!
	def wrap(self):
		self.list_[0]='<html><body> '+self.list_[0]
		self.list_[-1]=self.list_[-1]+' </html></body>'
	
	
	def translate(self):
		self.h1()
		self.mail()
		self.numbers()
		self.h2()
		self.par()
		self.lists()
		self.wrap()
		

	def write(self):
		match=re.search(r'([\w\d_<>]+).[\w\d_<>]+',self.name)
		self.name=match.group(1)+'.html'
		f=open(self.name,'w')
		[f.write(el+'\n') for n,el in enumerate(self.list_) ]
		f.close()
		

if __name__=='__main__':

	html=MarkUp('testo.txt','html')
	html.translate()
	html.write()