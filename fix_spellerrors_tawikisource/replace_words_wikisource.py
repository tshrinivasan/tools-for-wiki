#!/usr/bin/env python
# -*- coding: utf-8 -*-
                                                                                                                            
import sys

import pywikibot
from pywikibot import pagegenerators

language = 'ta'
wikisite = 'wikisource'
list_of_spell_errors = u'விக்கிமூலம்:தானியக்க_மெய்ப்பு/பிழைகள்_பட்டியல்'
category_to_fix = u'பகுப்பு:மெய்ப்பு_பார்க்கப்படாதவை'


site = pywikibot.Site(language,wikisite)
fix_page = pywikibot.Page(site, list_of_spell_errors)

cat = pywikibot.Category(site,category_to_fix)
gen = pagegenerators.CategorizedPageGenerator(cat)

fix_content = fix_page.text
temp_file = open("temp.txt","w")
temp_file.write(fix_content.encode('utf-8'))
temp_file.close()


def do_replace_text(page):

    temp_content = open("temp.txt",'r').readlines()

    for line in temp_content:

        if len(line) > 1:
            find_text = line.split(',')[0].strip()
            replace_text = line.split(',')[1].strip()

#            print  "Finding " + find_text + "  and replacing with   " + replace_text
            original_text = page.text

            new_text = original_text.replace(find_text.decode('utf-8'),replace_text.decode('utf-8'))
            page.text = new_text

    page.save(summary="replaced text")
    


for page in gen:

    print "Working on " + page.title()

    do_replace_text(page)


print "Completed !"
