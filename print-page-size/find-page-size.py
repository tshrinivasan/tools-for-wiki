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

wikisource_language = config.get('settings','wikisource_language')

wiki_url = "https://" + wikisource_language + ".wikisource.org/w/api.php"

book_name = config.get('settings','book_name')
start_page_number = config.get('settings','start_page_number')
end_page_number = config.get('settings', 'end_page_number')




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


if not os.path.isdir("./log"):
            os.mkdir("./log")



# create a file handler
log_file = './log/find_page_size_' + timestamp + '_log.txt'

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


data_file = open(book_name + ".txt",'w+')

def find_page_size(pagename):


	page = wikitools.Page(wiki, pagename, followRedir=True)
        
	logging.info("Reading " + "https://ta.wikisource.org/wiki/"+page.title)

	metadata =  page.getHistory(content=False)

        size =  metadata[0]['size']

	if size <=1000:
        	data_file.write(pagename + " ~ " + str(size)  + "\n")		

        logging.info("page size for " +  pagename + " is " + str(size)  )
        




counter = 1




for number in range(int(start_page_number), int(end_page_number) +1 ):

	page_name = book_name + "/" + str(number)


	logging.info("Reading page " + str(counter))
	
	find_page_size(page_name)


		
        counter = counter + 1
        
	

        time.sleep(2)

data_file.close()

logging.info("Completed!")
