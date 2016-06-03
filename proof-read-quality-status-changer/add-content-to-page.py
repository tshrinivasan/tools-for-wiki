# -*- coding: utf-8 -*-

import os
import shutil
import sys
import ConfigParser
import time
import datetime
import glob
import urllib
import logging
import urllib2
import wikitools
import poster

config = ConfigParser.ConfigParser()
config.read("config.ini")

wiki_username = config.get('settings','wiki_username')
wiki_password = config.get('settings','wiki_password')
wikisource_language = config.get('settings','wikisource_language')

wiki_url = "https://" + wikisource_language + ".wikisource.org/w/api.php"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


if not os.path.isdir("./log"):
            os.mkdir("./log")



# create a file handler
log_file = './log/add_license_' + timestamp + '_log.txt'

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)


try:
            wiki = wikitools.wiki.Wiki(wiki_url)
except:
            message =  "Can not connect with wiki. Check the URL"
            logger.info(message)

login_result = wiki.login(username=wiki_username,password=wiki_password)
message =  "Login Status = " + str(login_result)
logging.info(message)


if login_result == True:
        message =  "\n\nLogged in to "  +  wiki_url.split('/w')[0]
        logging.info(message)
else:
        message =  "Invalid username or password error"
        logging.info(message)
        sys.exit()

def check_for_bot(username):
        user = wikitools.User(wiki,username)
        if 'bot' in user.groups:
                return "True"

logging.info("Checking for bot access rights")
bot_flag = check_for_bot(wiki_username)

if bot_flag:
            logging.info("The user " + wiki_username + " has bot access.")
else:
            logging.info("The user " + wiki_username + " does not have bot access")


def add_license_content(pagename):

	page = wikitools.Page(wiki,"Page:"+ pagename, followRedir=True)
        print page


	logging.info("Editing " + "https://ta.wikisource.org/wiki/"+page.title)

	new_content = """
<big><center>'''﻿உலகளாவிய பொதுக் கள உரிமம் (CC0 1.0)'''</center></big>

இது சட்ட ஏற்புடைய உரிமத்தின் சுருக்கம் மட்டுமே. முழு உரையை https://creativecommons.org/publicdomain/zero/1.0/legalcode என்ற முகவரியில் காணலாம்.

'''பதிப்புரிமை அற்றது''' 

இந்த ஆக்கத்துடன் தொடர்புடையவர்கள், உலகளளாவிய பொதுப் பயன்பாட்டுக்கு என பதிப்புரிமைச் சட்டத்துக்கு உட்பட்டு, தங்கள் அனைத்துப் பதிப்புரிமைகளையும் விடுவித்துள்ளனர்.

நீங்கள் இவ்வாக்கத்தைப் படியெடுக்கலாம்; மேம்படுத்தலாம்; பகிரலாம்; வேறு வடிவமாக மாற்றலாம்; வணிகப் பயன்களும் அடையலாம். இவற்றுக்கு நீங்கள் ஒப்புதல் ஏதும் கோரத் தேவையில்லை.

<center>'''***'''</center>

இது, உலகத் தமிழ் விக்கியூடகச் சமூகமும் ( https://ta.wikisource.org ), தமிழ் இணையக் கல்விக் கழகமும் ( http://tamilvu.org ) இணைந்த கூட்டுமுயற்சியில், பதிவேற்றிய நூல்களில் ஒன்று. இக்கூட்டு முயற்சியைப் பற்றி, https://ta.wikisource.org/s/4kx என்ற முகவரியில் விரிவாகக் காணலாம்.



:::[[File:CC-Zero-badge.svg|100px|left]]                                                         [[File:CC-logo.svg|100px|center]]   





<big><center>'''Universal (CC0 1.0)  Public Domain Dedication'''</center></big>

This is a human readable summary of the legal code found at https://creativecommons.org/publicdomain/zero/1.0/legalcode

'''No Copyright'''

The person who associated a work with this deed has dedicated the work to the public domain by waiving all of his or her rights to the work worldwide under copyright law including all related and neighboring rights, to the extent allowed by law.

You can copy, modify, distribute and perform the work even for commercial purposes, all without asking permission.

<center>'''***'''</center/>

This book is uploaded as part of the collaboration between Global Tamil Wikimedia Community ( https://ta.wikisource.org ) and Tamil Virtual Academy ( http://tamilvu.org ). More details about this collaboration can be found at https://ta.wikisource.org/s/4kx.

"""

	


	page.edit(text = new_content,summary = "added license content")

        logging.info("Added license content")
        
book = open("book-names.txt","r")

counter = 1

for line in book:
#	print line
	filename = line.split("File:")[1]
	logging.info("Editing for Book " + str(counter))
        add_license_content(filename.strip()+"/2")
        
        counter = counter + 1
        
        time.sleep(3)


logging.info("Completed!")
