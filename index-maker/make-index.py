# -*- coding: utf-8 -*-

import wikitools
import poster
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
from wikitools import category

config = ConfigParser.ConfigParser()
config.read("config.ini")

wiki_username = config.get('settings','wiki_username')
wiki_password = config.get('settings','wiki_password')
wikisource_language_code = config.get('settings','wikisource_language_code')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


if not os.path.isdir("./log"):
    os.mkdir("./log")


# create a file handler
log_file = './log/index_maker_' + timestamp + '_log.txt'

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)



logger.info("Running index_maker.py ")

logger.info("Wiki Username = " + wiki_username)
logger.info("Wiki Password = " + "Not logging the password")
logger.info("wikisource_language_code = " + wikisource_language_code)

wiki_url = "https://" + wikisource_language_code + ".wikisource.org/w/api.php"

logger.info("Wiki URL = " + wiki_url)


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


commons_url = "https://commons.wikimedia.org/w/api.php"

commons = wikitools.wiki.Wiki(commons_url)



counter = 1

cat = category.Category(commons, "PDF files in Tamil with OCR conversion")
# iterate through all the pages in ns 0
for pdf in cat.getAllMembersGen(namespaces=[6]):
        print str(counter) + ".    " + pdf.title.encode('utf-8')
        pdf_name = pdf.title.encode('utf-8').split("File:")[1]
        #pdf_name = "சிந்தனைப் பந்தாட்டம்.pdf"
        index_page = wikitools.Page(wiki,"Index:"+ pdf_name, followRedir=True)
        edit_summary  = "Index creation"
        
        content = " "
        
        #if index_page.exists:
          #      print index_page.getWikiText()
            #    logger.info("page already there")
        #else:
            
        content_part1 = """
{{:MediaWiki:Proofreadpage_index_template
|Type=book
|Title=
|Language=ta
|Volume=
|Author=
|Translator=
|Editor=
|Illustrator=
|School=
|Publisher=
|Address=
|Year=
|Key=
|ISBN=
|OCLC=
|LCCN=
|BNF_ARK=
|ARC=
|Source=
|Image=1
|Progress=C
|Number of pages=
|File size=
|Category=
|Pages=<pagelist 
1=நூலட்டை
2= உரிமம்


/>
|Volumes=
|Remarks=
|Width=
|Css=
|Header=
|Footer=

}}
"""

        content = content_part1 
        if bot_flag:
                        index_page.edit(text=content,summary=edit_summary,bot="True")
        else:
                        index_page.edit(text=content,summary=edit_summary)
                #        print index_page.getWikiText()
        message = "Created Index at https://" + wikisource_language_code + ".wikisource.org/wiki/Index:" + pdf_name + "\n"
        logging.info(message)
                
                
#        sys.exit()
                
        counter = counter + 1

        time.sleep(10)
        logging.info("=========")
        



                                                                                                                                  
