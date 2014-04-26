#!/usr/bin/python
import sys
import re
import urllib2
from bs4 import BeautifulSoup 
from subprocess import call

def cleanOutput(toClean):
    #perform a regex sweep to remove all of the numbers that 
    #are contained in square brackets. e.g. "1234[5]" -> "1234"
    #nobrackets = re.sub(r'\[[0-9]\]', '', output_to_clean) 
    #noparens = re.sub(r'\([^)]*\)', '', nobrackets)
    #nocitation = noparens.replace("[citation needed]", "") 
    nobrackets = removeBrackets(toClean) 
    #final = nobrackets.replace(' ,', '')
    final = re.sub(r'\ \.', '.', nobrackets)
    final = re.sub(r'\ ,', ',', final)
    final = re.sub(r'\ \ ', ' ', final)
    return final

def removeBrackets(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
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
        return "DISAMBIGUATE!"
    '''
        #disambiguate -- show the person which options are allowed
        lists = soup.find_all('li')
        for li in lists:
            if len(li.find('a').contents) > 0:
                print li.find('a').contents[0]
        sys.exit()
    '''
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
