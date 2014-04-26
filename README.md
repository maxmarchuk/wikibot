wikibot
=========

Summary
--------
A bot that parses Wikipedia HTML pages for summaries and them out cleanly to an IRC channel.
The script that the bot calls can also be used on its own.

Installation/Usage
--------
There isn't really anything to install; just clone the repo with  
<<<<<<< HEAD

`git clone https://github.com/maxmarchuk/wikibot`

and 

`./wikiparse.py`

to see the usage for the standalone script.

To use the irc bot, create a `settings.ini` file and format it as shown in the example.settings.ini and run

`./ircbot.py <channel> <password>`

=======
`git clone https://github.com/maxmarchuk/wikibot`
and 
`./wikiparse.py`
to see the usage for the standalone script.

To use the irc bot, create a `settings.ini` file and format it as shown in the example.settings.ini and run
`./ircbot.py <channel> <password>`
>>>>>>> 0406fd14d1d10711bfe16ccd02a67eabf0ba4898
Leave the password blank if there is none.

Disclaimer
--------
This is not an efficient or reliable way of getting Wikipedia summaries. I am not using any APIs.
The summaries are extracted from raw HTML and parsed through with BeautifulSoup4 and it was all done as a learning experience.
I do not plan on extending the bot to query an API as there are many bots that do this already.
