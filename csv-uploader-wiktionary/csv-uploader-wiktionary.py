#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywikibot
import csv


site = pywikibot.Site('ta','wiktionary')


def add_page(pagename,content):
            page = pywikibot.Page(site,pagename)
            page.text = content
            summary_content = str(content.encode('utf-8').split('{{subst:')[1])
            page.save(summary=summary_content)


rownum=0
with open('content.csv', 'rb') as f:
            reader = csv.reader(f,delimiter="~")
            for row in reader:
                        if rownum == 0:
                                    header = row
                        else:
                                      add_page(row[0].decode('utf-8'),row[1].decode('utf-8'))
                                      
                        rownum = rownum+1



print("Completed !")


