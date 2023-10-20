This is required when missing pages are added to an existing index and pages in the Page: namespace are already created. Admin privilege is required for using the script. The script is for use in Linux. 

For Linux Users -
cd tools-for-wiki-master
cd move-pages-bn-wikisource
python move-pages.py

Below is described the process with Windows 7.

Install Python 2.7. (https://www.python.org/downloads/windows/)
Install Notepad++. (https://notepad-plus-plus.org/download/v7.5.6.html)
Go to GitHub (https://github.com/tshrinivasan/tools-for-wiki) and download tools-for-wiki-master.zip from the green coloured clone or download button; then extract it; Delete all folders except move-pages-bn-wikisource from the extracted folder. Now move the tools-for-wiki-master folder to C:\Windows\System32.

Right click on the config.ini file and choose Edit with Notepad++. Change like this:

wiki_password = Your password
wikisource_language = en or as appropriate.

Also change the book settings:
book_name = Page:bookname.pdf (or djvu)
start_page_number = --
end_page_number = --
increment_order = --

Along with that, remove the GitHub copyright line in the footer (Don't edit with regular Notepad; that will insert Byte Order Mark at the start of the file)

Start button -- search box -- search for sysdm.cpl -- right click -- Run as Administrator -- Advanced -- Environment Variables -- System variables -- Path -- Insert Python27 and Python\Scripts folders with correct address.

Start button -- search box -- search for cmd.exe -- right click -- Run as Administrator -- Give commands: pip install wikitools and pip install poster.

Add bot user to your user group in the concerned Wikisource.

Now put successive commands in cmd.exe: cd tools-for-wiki-master -- cd move-pages-bn-wikisource -- python move-pages.py

At a time only that portion of the book can be moved where there is no gap in Page: namespace (i.e., no absent/uncreated pages).

Change book settings in config.ini before every bulk move of pages.
