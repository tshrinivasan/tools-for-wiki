# -*- coding: utf-8 -*-
import os
import shutil
import sys
import configparser
import datetime
import glob
from wikitools import wiki, api,page
import csv

config = configparser.ConfigParser()
config.read("config.ini")

wikisite_language = config.get('settings','wikisite_language')

wiki_url = "https://" + wikisite_language + ".wikipedia.org/w/api.php"

page_list_file_name = config.get('settings','page_list_file_name')

#wiki = wiki.Wiki(wiki_url)
#print(wiki)






def find_page_size(pagename):
    from wikitools import wiki, api,page

    page = page.Page(wiki, pagename, followRedir=True)
    print("Reading " + "https://" + wikisite_language + ".wikipedia.org/wiki/"+page.title)
    metadata =  page.getHistory(content=False)
    size =  metadata[0]['size']
    return(size)



import csv, subprocess, time, pywikibot, re




data_file = open(page_list_file_name,'r+').readlines()
site = pywikibot.Site('en', 'wikipedia')

for line in data_file:
    print(line)
    
    page = pywikibot.Page(site, line)
    print ((page.getVersionHistory()[0]['size']))