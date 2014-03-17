#!/usr/bin/python
import socket
import re
import sys
import wikiparse

server  = "irc.cat.pdx.edu"       
port    = 6667 
channel = "#wikibot"
nick    = "wikibot"
ircname = "Wikipedia Bot"
keyword = "!wiki"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.recv(4096)
irc.send("NICK "+ nick +"\n")
irc.send("USER "+ nick +" "+ nick +" "+ nick +" :" + ircname + "\n")
#irc.send("PRIVMSG nickserv :iNOOPE\r\n")
irc.send("JOIN "+ channel +"\n")
irc.send("PRIVMSG "+ channel + " : Hello everybody! BREAK ME!\r\n")

def say(sentence):
    irc.send("PRIVMSG "+ channel + " :" + sentence + "\r\n")
    
def lookup(search_term):
    result = wikiparse.wikisearch(search_term) 
    print result
    say(result)
    '''
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', result) 
    for sentence in sentences:
        say(sentence + '.')
    ''' 
while 1: 

    text=irc.recv(2040)  
    print text 
    if text.find("PING") != -1:
        irc.send("PONG " + text.split()[1] + "\r\n")
        print "PONG"

    message = text.split(':')[2]
    
    if message.find("!wikibot ") != -1: 
        user = text.split(':')[1].split('!')[0]
        command = message.rsplit("!wikibot")[1].lstrip()
        lookup(command)
        

