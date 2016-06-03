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

	new_content = """{{nop}}
[[File:""" + str(pagename.split("/1")[0]) + """|center|240px]]
{{nop}}
"""
	


	page.edit(text = new_content,summary = "அட்டைப்படம் சேர்க்கப்பட்டது")

        logging.info("Added cover image")
        
book = open("book-names.txt","r")

counter = 1

for line in book:
#	print line
	filename = line.split("File:")[1]
	logging.info("Editing for Book " + str(counter))
        add_license_content(filename.strip()+"/1")
        
        counter = counter + 1
        
        time.sleep(2)
	
	


logging.info("Completed!")
