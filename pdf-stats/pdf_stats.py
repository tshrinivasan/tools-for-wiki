import pypdftk #install pypdftk with 'sudo pip install pypdftk'
import os
import re
import csv
import humanize #install humanize with 'sudo pip install humanize'
import time
import datetime
import glob

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

file_path = "./"

#files = []
#for filename in glob.glob('*.pdf'):
#                files.append(filename)



myDir = "."
files = []
for root, dirnames, filenames in os.walk(myDir):
    files.extend(glob.glob(root + "/*.pdf"))



#dirList=os.listdir(file_path) #list all the files in the directories
file_write = open('pdf_stats_' + timestamp + '.csv', 'w') #writing no.of pages into a csv file
file_write.write("No~FileName~PageCount~Size~")
file_write.write("\n")
file_write.write("\n")
print "\n\n"
counter = 1
for fname in files:
	data_find = str(counter) + '~' + fname +'~'+ str(pypdftk.get_num_pages(fname)) + '~' + humanize.naturalsize(os.path.getsize(fname)) + '~'  # giving file path with the name of the file
	print data_find # test with printing the data
	file_write.write(str(data_find)) 
	file_write.write("\n")	
	counter = counter + 1
file_write.close()

print "\nWrote the PDF stats to the file " + 'pdf_stats_' + timestamp + '.csv' + '\n\n'
