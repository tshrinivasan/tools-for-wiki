# -*- coding: utf-8 -*-
import os
import shutil
import sys
import configparser
import datetime
import glob
import csv
import requests

S = requests.Session()

config = configparser.ConfigParser()
config.read("config.ini")

wikisite_language = config.get('settings','wikisite_language')

wikisite = config.get('settings','wikisite')

wiki_url = "https://" + wikisite_language + "." + wikisite + ".org/w/api.php"

page_list_file_name = config.get('settings','page_list_file_name')


data_file = open(page_list_file_name,'r+').readlines()

out_file = open("page_with_size.csv","a")

for line in data_file:

    PARAMS = {
    "action": "query",
    "format": "json",
    "titles": line.strip(),
    "prop": "info",
    "inprop": "url|talkid"
    }

    R = S.get(url=wiki_url, params=PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]
    for k, v in PAGES.items():
        print(v["title"] + " has " + str(v["length"]) + " bytes.")

        out_file.write(v["title"] + "~" + str(v["length"]) + "\n")

