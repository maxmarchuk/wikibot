#!/usr/bin/python
import sys
import urllib2
#import requests
from bs4 import BeautifulSoup 
from subprocess import call


def wikisearch(array):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]

	#get the command line arguments and format it for the URL
	search_term = array 

	search_term = search_term.strip(' ')
	search_term = search_term.replace(' ', '_')
	print "Searching Wikipedia for:", search_term

	url='http://en.wikipedia.org/w/index.php?title=' + search_term + '&printable=yes'

	#grab the file
	infile = opener.open(url)
	openedfile = infile.read()
	soup = BeautifulSoup(openedfile)

	#find all of the paragraph tags
	paragraphs = soup.find_all('p')

	#get the first paragraph
	summary = paragraphs[0].text

	#check to see if search term is ambigious 
	if summary.find("may refer to") > 0:
		print "Ambigous search term."	
		lists = soup.find_all('li')
		for li in lists:
			print li.find('a').contents[0]  
		sys.exit()	

	print summary

wikisearch('Albert Einstein') 
