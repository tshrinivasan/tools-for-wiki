# -*- coding: utf-8 -*-
#!/usr/bin/python

from wikitools import wiki
from wikitools import category
import csv
import time
import os
from time import gmtime, strftime

site = wiki.Wiki("https://ta.wikipedia.org/w/api.php") 
#site.login("TshrinivasanBOT", "Vanakkam@1")
# Create object for "Category:Foo"

timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_count(district):

	cat = category.Category(site, district.strip("\n") + " மாவட்ட ஆசிரியர்கள் தொடங்கிய கட்டுரைகள்")

	counter = 0
	for article in cat.getAllMembersGen():
		counter = counter +1

	return counter


total_time = open('csv-to-html-table/data/time_total.html','w')

total_time.write('<link href="../css/bootstrap.min.css" rel="stylesheet">\n')
total_time.write("<p align='right'> இந்தப் பட்டியல் 10 நிமிடத்திற்கு ஒரு முறை இற்றைப்படுத்தப்படுகிறது. கடைசி இற்றை நேரம்   " + timestamp + "<br/>")
total_time.close()

districts = open('districts.txt','r')

articles_count = open("csv-to-html-table/data/articles_count.csv",'w')
articles_count.write("மாவட்டம் , கட்டுரைகள்" +"\n")

for district in districts:
	content = district.strip("\n") + " , " + str(get_count(district)) + "\n"
	print content
	articles_count.write(content)


