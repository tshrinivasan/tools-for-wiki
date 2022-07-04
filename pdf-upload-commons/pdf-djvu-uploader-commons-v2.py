#!/usr/bin/env python3

from pywikibot import Site
from pywikibot import FilePage
import stat
import sys
import os

class Client:
    def __init__(self, username, sourcedir, destdir = None, siteurl = None):
        self.username = username
        self.sourcedir = sourcedir
        self.destdir = destdir
        self.siteurl = siteurl if siteurl is not None else 'https://commons.wikimedia.org'

    def connect(self):
        self.site = Site(url=self.siteurl)
        self.site.login(user=self.username)
        print('id : %d'%(self.site.userinfo['id']))
        print('name : %s'%(self.site.userinfo['name']))

    def upload(self, localfilename):
        basefilename = os.path.basename(localfilename)
        pagename='File:%s'%(basefilename.replace(' ', '_'))
        page = FilePage(self.site, pagename)
        wikitext0 = """
=={{int:filedesc}}==
{{Book
| Author       = 
| Editor       = 
| Translator   = 
| Illustrator  = 
"""
        title = "| Title        = " + basefilename.split('.')[-2]
        wikitext1 = """
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
        wikitext = wikitext0 + title + wikitext1
        if not page.upload(localfilename, comment=basefilename, text=wikitext):
            print("failed to upload %s"%(localfilename))
            return False
        else:
            print('%s uploaded as %s'%(localfilename, pagename))
            return True

    def run(self):
        if self.destdir is None:
            self.destdir = os.path.join(self.sourcedir, 'uploaded')
            if not os.path.isdir(self.destdir):
                os.mkdir(self.destdir)
        for entry in os.scandir(self.sourcedir):
            if entry.is_file():
                ext = entry.name.split('.')[-1]
                if ext in ['pdf','PDF','djvu','DJVU']:
                    if self.upload(entry.path):
                        os.replace(entry.path, os.path.join(self.destdir, entry.name))

def main():
    if len(sys.argv) < 3:
        print('[usage] %s username sourcedir [destdir] [siteurl]'%(sys.argv[0]))
        sys.exit(1)

    username = sys.argv[1]
    sourcedir = sys.argv[2]
    destdir = sys.argv[3] if len(sys.argv) >= 4 else None
    siteurl = sys.argv[4] if len(sys.argv) >= 5 else None
    client = Client(username, sourcedir, destdir, siteurl)
    client.connect()
    client.run()

if __name__ == '__main__':
    main()
