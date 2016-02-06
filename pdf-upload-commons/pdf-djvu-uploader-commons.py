#!/usr/bin/python
# -*- coding: utf-8 -*-


import wikitools
import poster
import pyexiv2
import os
import shutil
import sys
import time
import datetime

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


#wiki_url = "MediaWiki API url here"

wiki_url =  "https://commons.wikimedia.org/w/api.php"

wiki_username = ""
wiki_password = ""



try:
	wiki = wikitools.wiki.Wiki(wiki_url)
except:
	print "Can not connect with wiki. Check the URL"


login_result = wiki.login(username=wiki_username,password=wiki_password)

#print "login status = " + str(login_result)
if login_result == True:
	print "Logged in."
else:
	print "Invalid username or password error"
	sys.exit()







path = './'

listing = os.listdir(path)

def filetype(file):
	return file.split(".")[-1]

def filename(file):
	return file.split(".")[-2]


	

def move_file(pdf_file):
	source = pdf_file
	destination = "./uploaded-"+ timestamp + "/" + pdf_file

	if os.path.isdir("uploaded-" + timestamp):
		shutil.move(source,destination)
	else:
		os.mkdir("uploaded-" + timestamp)
		shutil.move(source,destination)		
	print "Moving the file " + pdf_file + " to the folder 'uploaded-" + timestamp + "'"



def upload_pdf_file(pdf_file):
	
                print "Uploading the file " + pdf_file
		file_name = pdf_file
		caption = pdf_file
#		extension = filetype(image)
#                upload_file_name = file_name + "." + extension
                
		file_object=open(pdf_file,"r")
		pdf=wikitools.wikifile.File(wiki=wiki, title=file_name)
        	pdf.upload(fileobj=file_object,comment=caption, ignorewarnings=True)
        

		page_name = pdf_file.replace(" ","_")

		page = wikitools.Page(wiki, "File:" + page_name , followRedir=True)

                wikidata_part1 = """

=={{int:filedesc}}==
{{Book
| Author       = 
| Editor       = 
| Translator   = 
| Illustrator  = 
"""




		wikidata_part2 = """
| Subtitle     = 
| Series title = 
| Volume       = 
| Edition      = 
| Publisher    = 
| Printer      = 
| Date         = 
| City         = 
| Language     = தமிழ்
| Description  = {{ta|1=தமிழக அரசால் அறிவிக்கப்பட்ட நாட்டுடைமை நூல்களில் இதுவும் ஒன்று.}}
| Source       = {{Institution:Tamil Virtual Academy}}
| Image        =  {{PAGENAME}}
| Image page   = 
| Permission   = [[File:Tamil-Nadu-Nationalized-Books-Public-Domain-Declaration.jpg|thumb|left|Letter from Tamil Virtual Academy declaring books nationalized by Tamil Nadu government and released under Creative Commons CC0 1.0 Universal Public Domain Dedication license]]
| Other versions = 
| Wikisource   =s:ta:Index:{{PAGENAME}}
| Homecat      = 
}}

=={{int:license-header}}==
{{cc-zero}}

[[Category:Books in Tamil]]
[[Category:PDF files in Tamil with CC0 1.0 license]]
[[Category:Books from Tamil Virtual Academy]]

"""
		wikidata = wikidata_part1 + "| Title        = " + filename(pdf_file).replace("_"," ") + wikidata_part2

		page.edit(text=wikidata)

                print "File URL = " +  wiki_url.split('/w')[0] + "/wiki/File:" + page_name 

		move_file(pdf_file)
		
for pdf_file in listing:
	if filetype(pdf_file) in ['pdf','PDF','djvu','DJVU']:
		upload_pdf_file(pdf_file)
		



