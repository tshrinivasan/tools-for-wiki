#!/usr/bin/python
# -*- coding: utf-8 -*-

from wikidataintegrator import wdi_core
from wikidataintegrator import wdi_login
import csv
import time

input_file = "data.csv"
language_code = 'ta'
wikidata_username = 'USERNAME'
wikidata_password = 'PASSWORD'

login_session = wdi_login.WDLogin(user=wikidata_username, pwd=wikidata_password)


def set_new_label(item_id,label,language_code):

	wikidata_item = wdi_core.WDItemEngine(wd_item_id=item_id)

	wikidata_item.set_label(label, lang=language_code)

	wikidata_item.write(login_session)

	print "Wrote the new label. check the link " + 'https://www.wikidata.org/wiki/' + item_id + "\n"



f = open(input_file, 'r')
reader = csv.reader(f, delimiter='~')
for row in reader:
	try:
		set_new_label(row[0],row[1],language_code)
		time.sleep(5)
	except Exception as e:
		print "Error on " + row[0] 
		print  str(e)
		print "\n"

