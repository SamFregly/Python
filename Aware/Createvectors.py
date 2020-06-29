import sys
import time
import optparse


class VectorModel:  				# class name
	def __init__(self, file):    		# constructor 
		self.querylist = []  		# [] = [ ] the spacing is just weird 
		self.filename= file		# this is for the file containing all the queries
		self.vectorlist= []		# this is where the vector will be stored
						# both are initialized as empty
		
		
	def populatelist(filename):		# takes a file as input and populates an array 
						# list with all the strings
		with open("filename") as input:
                        for line in input:					
                                if (len(sys.argv)>1):
                                        line_generator= line.strip("query")
                                        self.querylist.append(line_generator)
		
		
		
	def createlist(self, Parsedfile):                
		for i in range (length(self.querylist)):
			output = 'match -f' + Parsedfile + '-t '+ self.querylist[i] + '> /home/hofstra/Downloads/tempfile1.txt'
			p1= os.system(output)
			p1.wait()
			with open('/home/hofstra/Downloads/tempfile1.txt') as infile:
				copy = False 
				for line in infile:
					if line.strip() == 'linebefore nmatched terms ':
						copy= True				# these lines pull only the line starting with nmatchedterms
					elif line.strip() == 'line after nmatchedterms':
						copy = False 	# stops at the line after nmatchedterms
					elif copy:
						self.vectorlist[i]= line.lstrip('nmatchedterms: ') # strips the uneccessary things so only the number is left
							# and inserts it into vectorlist at the appropriate index.
			
			
	def exportlist():
		file = open('Trainingfile.txt','a+')
		file.write(self.vectorlist)
		file.close()





#os.system(“cd ~/Downloads”) 
#model1 = vectormodel()

#jump into proper directory. 
#loop 
#	send match command through terminal with 
#	match ..... FILE_NAME .... QUERY[i]
	# nmatched from command line with parser thing
#	insert into vector

#return vector 

	

