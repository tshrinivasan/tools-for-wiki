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

book_name = config.get('settings','book_name')
increment_order = config.get('settings','increment_order')
start_page_number = config.get('settings','start_page_number')
end_page_number = config.get('settings', 'end_page_number')

indic_numbers = ConfigParser.ConfigParser()
indic_numbers.read('indian_numerals.ini')



def convert_to_indic(language,number):
        if language in ['bn','or','gu','te','ml','kn','sa','as','mr']:
                number_string = ''
                for num in list(str(number)):
                        number_string = number_string + indic_numbers.get(language,num)
                return number_string
        else:
                return number





logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


if not os.path.isdir("./log"):
            os.mkdir("./log")



# create a file handler
log_file = './log/move_pages_' + timestamp + '_log.txt'

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


def move_page(original_pagename, new_pagename):

	page = wikitools.Page(wiki, original_pagename, followRedir=True)
        
	logging.info("Editing " + "https://" + wikisource_language + ".wikisource.org/wiki/"+page.title)

	page.move( new_pagename, reason = "Moved page", noredirect=True)

#	page.edit(text = new_content,summary = "உரிமப்பக்கத்திற்குரிய தரவைப் பதிவேற்றியது")
	
#	print page.getWikiText()

        logging.info("moved " +  original_pagename + " to " + new_pagename )
        




counter = 1

for number in range(int(end_page_number), int(start_page_number) -1, -1 ):

	indic_page_number =  str(convert_to_indic(wikisource_language, number))
        incremented_indic_page_number =  str(convert_to_indic(wikisource_language, int(number) + int(increment_order)))

	original_name = book_name + "/" + str(indic_page_number)
	new_name = book_name + "/" + str(incremented_indic_page_number)

	logging.info("Moving page " + str(counter))
	move_page(original_name, new_name)

	
        counter = counter + 1
        
#	sys.exit()

        time.sleep(8)


logging.info("Completed!")
