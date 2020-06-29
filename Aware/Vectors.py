import sys
import time
import optparse
import os
import string 
import re

class VectorModel:  				
	def __init__(self, file):  
		self.querylist = []   
		self.queryfile= file	
		self.vectorlist= []
		
						
		
		
	def populatelist(self, queryfile): #DONE!!!!!!!!!!!!!!!
		with open(self.queryfile) as input:
			#for line in open(filename)
				self.querylist = [line.rstrip('\n') for line in open(self.queryfile)] 
				#self.querylist.append(lines)
			
                        #for line in input:					
                         #       if (len(sys.argv)>1):
                                #        lin
								#e_generator= line#strip("query")
                                 #       self.querylist.append(line_generator2)
		

 		
	def createlist(self, Parsedfile):   
		for i in range (len(self.querylist)):
			output =('match -f' + Parsedfile + '-t '+ self.querylist[i] + '> tempfile.txt')
			#"(echo stuff&echo.test 1285235d&echo.thing & echo.line4 & echo stuff&echo.test 98765&echo.thing)> tempfile.txt"
			p1= os.system(output)
			with open('tempfile.txt') as infile:
			# change to open('/home/hofstra /Downloads/tempfile.txt')
				copy = False 
				for line in infile:
					if line.strip() == 'stuff':
						copy= True  # these lines pull only the line before nmatchedterms
					elif line.strip() == 'thing':
						copy = False 	# stops at the line after nmatchedterms
					elif copy:
						self.vectorlist.append(line.strip('test ')) # strips the uneccessary things so only the number is left
							# and inserts it into vectorlist at the appropriate index.
		
		
	def exportlist(self):  
		
		file = open('Trainingfile.txt','a+')
		#strip_list= list(map(str.split('\n'), self.vectorlist))
		for i in range (len(self.vectorlist)):
			self.vectorlist[i] = re.sub('[^0-9]', '', self.vectorlist[i])
		#print(self.vectorlist) # prints same as strip_list
		file.write('[')
		for i in range (len(self.vectorlist)):
			trainoutput= self.vectorlist[i]+ ', ' 
			file.write(trainoutput)
		file.write('0] \n')
		file.close()

s = VectorModel('querytest.txt')
s.populatelist("querytest.txt")
s.createlist('querytest.txt')
s.exportlist()
#print(s.querylist)

#print(s.queryfile)


