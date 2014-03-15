#!/usr/bin/python
import sys
import urllib2
from bs4 import BeautifulSoup 
from subprocess import call


def wikisearch(array):

	opener = urllib2.build_opener()
    
    #Set the user agent to some browser
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    #trim up the array and swap the spaces with underscores 
	search_term = array 
	search_term = search_term.strip(' ')
	search_term = search_term.replace(' ', '_')

	print "Searching Wikipedia for:", search_term

	url='http://en.wikipedia.org/w/index.php?title=' + search_term + '&printable=yes'

	#Get the file, read it, make it into soup
	infile = opener.open(url)
	openedfile = infile.read()
	soup = BeautifulSoup(openedfile)

	#find all of the paragraph tags
	paragraphs = soup.find_all('p')

	#get the first paragraph tag's content
	summary = paragraphs[0].text

	#check to see if search term is ambigious 
	if summary.find("may refer to") > 0:
		print "Ambigous search term."	
        #disambiguate -- show the person which options are allowed
		lists = soup.find_all('li')
		for li in lists:
			print li.find('a').contents[0] 
		sys.exit()

	print summary

#
#

parameters = '' 

if len(sys.argv) <= 1:
	print 'No search term supplied.'
	print 'Usage: ./wikiparse <search term>'
	sys.exit()
    
#build the parameter based on command line input
for i in range(1, len(sys.argv)):
	parameters += ' ' +  str(sys.argv[i]) 

wikisearch(parameters) 
