# -*- coding: utf-8 -*-

import os
import shutil
import sys
import configparser
import time
import datetime
import glob
import urllib
import logging
import requests
#import urllib2
#import wikitools
#import poster

config = configparser.ConfigParser()
config.read("config.ini")

wiki_username = config.get('settings','wiki_username')
wiki_password = config.get('settings','wiki_password')
wikisource_language = config.get('settings','wikisource_language')

wiki_url = "https://" + wikisource_language + ".wikisource.org/w/api.php"
#wiki_url = "https://en.wikisource.beta.wmflabs.org/w/api.php"

book_name = config.get('settings','book_name')
increment_order = config.get('settings','increment_order')
start_page_number = config.get('settings','start_page_number')
end_page_number = config.get('settings', 'end_page_number')

reason = config.get('settings','reason')

indic_numbers = configparser.ConfigParser()
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
        S = requests.Session()

        URL = wiki_url

        # Step 1: Retrieve a login token
        PARAMS_1 = {
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_1)
        DATA = R.json()

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
        
        
except:
        message =  "Can not connect with wiki. Check the URL"
        logger.info(message)
        sys.exit()
        

PARAMS_2 = {
    "action": "login",
    "lgname": wiki_username,
    "lgpassword": wiki_password,
    "format": "json",
    "lgtoken": LOGIN_TOKEN
}

R = S.post(URL, data=PARAMS_2)
DATA = R.json()

# Step 3: While logged in, retrieve a CSRF token
PARAMS_3 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_3)
DATA = R.json()
#print(DATA)

if "csrftoken" in DATA["query"]["tokens"]:
        CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]



if len(CSRF_TOKEN) >4:
        message =  "\n\nLogged in to "  +  wiki_url.split('/w')[0]
        logging.info(message)
else:
        message =  "Invalid username or password error"
        logging.info(message)
        sys.exit()

        


def move_page(original_pagename, new_pagename):
        PARAMS_4 = {
                "action": "move",
                "format": "json",
                "from": original_pagename,
                "to": new_pagename,
                "reason": reason,
                "movetalk": "1",
                "noredirect": "1",
                "token": CSRF_TOKEN
        }

        R = S.post(url=URL, data=PARAMS_4)
        DATA = R.text
        
        print(DATA)

        if not "error" in DATA:
                logging.info("Moved " + original_pagename + " to " + new_pagename)
        else:
                logging.info("Found ERROR")


def page_exists(page_name):
        page_url = "https://" + wikisource_language + ".wikisource.org/wiki/" + page_name
#        page_url = "https://en.wikisource.beta.wmflabs.org/wiki/" + page_name

        r = requests.head(f"{page_url}")

        if r.status_code == 200:
                return True
        if r.status_code == 301:
                return True
        elif 400 <= r.status_code < 500:
                return False
        else:
                return None        



counter = 1

for number in range(int(end_page_number), int(start_page_number) -1, -1 ):

        indic_page_number =  str(convert_to_indic(wikisource_language, number))
        incremented_indic_page_number =  str(convert_to_indic(wikisource_language, int(number) + int(increment_order)))

        original_name = book_name + "/" + str(indic_page_number)
        new_name = book_name + "/" + str(incremented_indic_page_number)

        logging.info("original_name = " + original_name)
        logging.info("new_name = " + new_name)

        #print(valid_site("https://en.wikisource.beta.wmflabs.org/wiki/Page:Kungl_teatrarna_J_Svanberg_del_1.pdf/304"))
#        print(page_exists(original_name))
        if page_exists(original_name) == True:
                logging.info("Moving page " + str(counter))

                move_page(original_name, new_name)
        else:
                logging.info("Page is not found . " + original_name)
                logging.info("exiting now.")
                sys.exit()
        counter = counter + 1
        
#	sys.exit()

        time.sleep(8)


logging.info("Completed!")
