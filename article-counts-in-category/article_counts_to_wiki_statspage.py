# -*- coding: utf-8 -*-
#!/usr/bin/python

from wikitools import wiki
from wikitools import category
import wikitools
import csv
import time
import os
from time import gmtime, strftime
from datetime import datetime
from pytz import timezone   
import sys 

ist = timezone('Asia/Kolkata')
sa_time = datetime.now(ist)
timestamp =  sa_time.strftime('%Y-%m-%d_%H-%M-%S')

site = wiki.Wiki("https://ta.wikipedia.org/w/api.php") 
site.login("username", "password")
# Create object for "Category:Foo"



def get_count(district):

	cat = category.Category(site, district.strip("\n") + " மாவட்ட ஆசிரியர்கள் தொடங்கிய கட்டுரைகள்")

	counter = 0
	for article in cat.getAllMembersGen():
		counter = counter +1

	return counter




districts = open('./districts.txt','r')

articles_count = open("./csv-to-html-table/data/articles_count.csv",'w')
articles_count.write("மாவட்டம் ~ கட்டுரைகள்" +"\n")

wiki_table = """
{| class='wikitable sortable'
|-
! எண் !! மாவட்டம் !! கட்டுரைகள் 
|-
"""

total_articles = 0
counter = 1
for district in districts:
	content = "<a target='_blank' href='https://ta.wikipedia.org/wiki/பகுப்பு:" + district.strip("\n") + " மாவட்ட ஆசிரியர்கள் தொடங்கிய கட்டுரைகள்'>" + district.strip("\n") + "</a>" + " ~ " + str(get_count(district)) + "\n"
	print content
	articles_count.write(content)

	wiki_table = wiki_table + "|-" + "\n" + "|" + str(counter) + "||" + "[https://ta.wikipedia.org/wiki/பகுப்பு:" + district.strip() + "_மாவட்ட_ஆசிரியர்கள்_தொடங்கிய_கட்டுரைகள்   " + district.strip()  + "] ||" +  str(get_count(district)) + "\n"
	counter = counter + 1
	total_articles = total_articles + get_count(district)
articles_count.close()

wiki_table = wiki_table + "|}"
print wiki_table

wiki_text = wiki_table + "\n\n" + "மொத்தக் கட்டுரைகள் =   " + str("{:,}".format(total_articles))

wiki_text = wiki_text + "\n\n" + "இந்தப் பட்டியல் 10 நிமிடத்திற்கு ஒரு முறை இற்றைப்படுத்தப்படுகிறது. கடைசி இற்றை நேரம்   " + timestamp 

wiki_text = wiki_text + "\n\n" + "TshrinivasanBOT ஆல் இயக்கப்படுகிறது. [https://github.com/tshrinivasan/tools-for-wiki/ மூலநிரல்]"

stats_page = wikitools.Page(site,"விக்கிப்பீடியா:Statistics/தமிழக ஆசிரியர்கள் தொடங்கிய கட்டுரைகள்")

stats_page.edit(text=wiki_text,summary="stats",bot=True)


