#!/usr/bin/python
import sys
import re
import urllib2
from bs4 import BeautifulSoup 
from subprocess import call

def cleanOutput(toClean):
    #perform a regex sweep to remove all of the numbers that 
    #are contained in square brackets or parens
    nobrackets = removeBracksAndParens(toClean) 

	#remove spaces before periods	
    periods = re.sub(r'\ \.', '.', nobrackets)

	#remove spaces before commas 
    commas = re.sub(r'\ ,', ',', periods)
    final = re.sub(r'\ \ ', ' ', commas)
    return final

def removeBracksAndParens(str):
    ret = ''
    skipBracket = 0
    skipParens = 0
    for i in str:
        if i == '[':
            skipBracket += 1
        elif i == '(':
            skipParens += 1
        elif i == ']' and skipBracket > 0:
            skipBracket -= 1
        elif i == ')'and skipParens > 0:
            skipParens -= 1
        elif skipBracket == 0 and skipParens == 0:
            ret += i
    return ret

def wikisearch(array):
    
    opener = urllib2.build_opener()

    #Set the user agent to some browser
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    #trim up the array and swap the spaces with underscores 
    search_term = array 
    search_term = search_term.strip(' ')
    print "\nSearching for " + search_term.title()
    if(search_term == 'slim' or search_term == 'Slim'):
        noslim = "I'm sorry, that information is confidential."
        return noslim
    search_term = search_term.replace(' ', '_').strip()

    url = "http://en.wikipedia.org/w/index.php?title=" + search_term + "&printable=yes"

    try:
        infile = opener.open(url)
    except urllib2.HTTPError, e:
        print "Unable to find your search term. "
        return ""
        #sys.exit()

    openedfile = infile.read()
    soup = BeautifulSoup(openedfile)

    #find all of the paragraph tags
    paragraphs = soup.find_all('p')

    #get the first paragraph tag's content
    summary = paragraphs[0].text

    #check to see if search term is ambigious 
    if summary.find("may refer to") > 0: 
        return "Please disambiguate your search term."
        #disambiguate -- show the person which options are allowed
        lists = soup.find_all('li')
        for li in lists:
            if len(li.find('a').contents) > 0:
                print li.find('a').contents[0]
        sys.exit()
   
    return cleanOutput(summary)
if __name__ == '__main__':

    parameters = '' 

    if len(sys.argv) <= 1:
        print 'No search term supplied.'
        print 'Usage: ./wikiparse <search term>'
        sys.exit()

    #build the parameter based on command line input
    for i in range(1, len(sys.argv)):
        parameters += ' ' +  str(sys.argv[i]) 

    print wikisearch(parameters)
