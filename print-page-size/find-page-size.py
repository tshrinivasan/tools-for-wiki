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
import csv
import operator


config = ConfigParser.ConfigParser()
config.read("config.ini")

wiki_username = config.get('settings','wiki_username')
wiki_password = config.get('settings','wiki_password')

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




data_file = open(book_name + ".csv",'w+')

def find_page_size(pagename):


	page = wikitools.Page(wiki, pagename, followRedir=True)
        
	logging.info("Reading " + "https://ta.wikisource.org/wiki/"+page.title)

	metadata =  page.getHistory(content=False)

        size =  metadata[0]['size']

	if size <=1000:
        	data_file.write("#[[" + pagename + "]]" + " ~ " + str(size)  + "\n")		

        logging.info("page size for " +  pagename + " is " + str(size)  )
        




counter = 1




for number in range(int(start_page_number), int(end_page_number) +1 ):

	page_name = book_name + "/" + str(number)


	logging.info("Reading page " + str(counter))
	
	find_page_size(page_name)


		
        counter = counter + 1
        
	

        time.sleep(2)

data_file.close()




data = csv.reader(open(book_name + ".csv"),delimiter='~')
sortedlist = sorted(data, key=operator.itemgetter(1))    # 0 specifies according to first column we want to sort
#now write the sorte result into new CSV file
with open("Sorted.csv", "wb") as f:
     fileWriter = csv.writer(f, delimiter='~')
     for row in sortedlist:
          fileWriter.writerow(row)





prefix = """==அறிவிப்புகள்==

==1000 பைட்டுகளுக்குள் உள்ள பக்கங்கள் ==

[[பகுப்பு:வடிவமைப்பு பற்றிய உரையாடல்கள்]]

"""

with open("Sorted.csv", 'r') as sortedfile:

	filewriter = open("file_with_prefix.txt","w")
	filewriter.write(prefix)

	for row in sortedfile:
		filewriter.write(row)

	filewriter.write("\n")
	filewriter.write("மேற்கண்டப் பக்கங்களை மேம்படுத்த, குறைவான நேரமே தேவைப்படும். எனவே, முதலில் இவற்றை மேம்படுத்தக் கோருகிறேன்.")
	filewriter.write("--~~~~")


filewriter.close()


wiki_content = open("file_with_prefix.txt","r")

wiki_page = book_name.replace('Page','Index_talk')
page = wikitools.Page(wiki, wiki_page, followRedir=True)

with open("file_with_prefix.txt","r") as content:
	wiki_content = content.read()


page.edit(text = wiki_content, summary = "மெய்ப்புக்கான குறிப்புகள் இடப்பட்டது")

logging.info("Added content to " + wiki_page)


logging.info("Completed!")
