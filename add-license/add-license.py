import glob
import time
import datetime
import os

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


                

license = raw_input("Enter the name of the licese file : ")
licese = licese.decode('utf-8')

files = []
for filename in glob.glob(u'*.pdf'):
                files.append(filename)

files.remove(license)

directory_name = "license-added-"+timestamp

os.mkdir(directory_name)

for pdf in files:
    command = "pdfunite " + license +  " " + pdf + " " +  directory_name + "/" + pdf
    command = command.encode('utf-8')
    print command + " \n"
    os.system(command)



print "\n\nCompleted!. Check the folder " + directory_name
                
