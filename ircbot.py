#!/usr/bin/python
'''
    This is an IRC bot to join an IRC channel and find wikipedia summaries based on 
    commands given in that channel.
    usage is the "listenkey".search <search term>.
    you can also say "botname: help" get the usage exampels

'''  
import sys
from twisted.internet import reactor, protocol, ssl
from twisted.words.protocols import irc
import re
import wikiparse
import ConfigParser

#function to get the items from the configurations file
#configuration file should look something like this:
# [irc]
# server: irc.freenode.net
# port: 6667
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
            sys.exit()
    return dict1

Config = ConfigParser.ConfigParser()
Config.read("settings.ini")
server  = ConfigSectionMap("irc")["server"]
nick    = ConfigSectionMap("irc")["nickname"]
ircname = ConfigSectionMap("irc")["realname"]
port = int(ConfigSectionMap("irc")["port"])
listenkey = ConfigSectionMap("irc")["listenkey"]
password = "" 

class Bot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        if password != "":
            print "joining with password", password
            self.join(self.factory.channel, password)
        else:
            self.join(self.factory.channel)

        print "Signed on as %s." % self.nickname
 
    def joined(self, channel):
        print "Joined %s." % channel
 
    def privmsg(self, user, channel, msg):
        print msg
        check(self, msg)
 
class BotFactory(protocol.ClientFactory):
    protocol = Bot
 
    def __init__(self, channel, nickname = nick):
        self.channel = channel
        self.nickname = nickname
        self.ircname = ircname
 
    def clientConnectionLost(self, connector, reason):
        print "Connection lost. Reason: %s" % reason
        connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason


#this function prints ONLY the first few lines of the summary
def wikiSearch(self, term):
    #cmsg(self, "Searching for" + term)
    searchResult = wikiparse.wikisearch(term).encode("utf-8")
    if searchResult == "": 
        cmsg(self, "I couldn't find anything, sorry")
        return

    #make sentences out of the search results based on the puncuation
    sentences = re.split(r'(\.\?\!)\s+)', searchResult) #([A-Z][^\.!?]*[\.!?])', searchResult) 

    print sentences
    if len(sentences) == 1:
        cmsg(self, sentences[0])
    elif len(sentences) == 2:
        cmsg(self, sentences[0] + '. ' + sentences[1] + '.')
    elif len(sentences) >= 3:
        cmsg(self, sentences[0] + '. ' + sentences[1] + '.' + sentences[2] + '.')

def wikiSearchFull(self, term):
    searchResult = wikiparse.wikisearch(term).encode("utf-8")
    if searchResult == "": 
        cmsg(self, "I couldn't find anything, sorry")
        return
    print searchResult
    sentences = re.split(r'([A-Z][^\.!?]*[\.!?])\s+', searchResult) 
    print "sentences", sentences
    for sentence in sentences:
        cmsg(self, sentence)

def cmsg(self, message):
    self.msg('#' + chan, message, 300)

def check(self, msg):
    words = msg.split(' ')

    #if someone is talking to me
    if words[0] == self.nickname + ':':
        if len(words) > 1:
            if words[1].lower() == 'help':
                cmsg(self, "Usage: " + listenkey + "search <search term>")

    #User wants to search for something
    if words[0] == listenkey + 'search':
        if words[1] == '-f':
            wikiSearchFull(self, msg.split('-f')[1])
        else:
            wikiSearchFull(self, msg.split('search')[1])

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Please supply a channel to join as a command line argument (no need to prepend a #)"
        sys.exit()
    if len(sys.argv) == 3:
        password = sys.argv[2]

    chan = sys.argv[1]
    reactor.connectSSL(server, port, BotFactory('#' + chan), ssl.ClientContextFactory())
    reactor.run() 

