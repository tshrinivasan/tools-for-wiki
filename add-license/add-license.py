import glob
import time
import datetime
import os

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


                

license = raw_input("Enter the name of the licese file : ")

files = []
for filename in glob.glob('*.pdf'):
                files.append(filename)

files.remove(license)

directory_name = "license-added-"+timestamp

os.mkdir(directory_name)

for pdf in files:
    command = "pdfunite " + license +  " " + pdf + " " +  directory_name + "/" + pdf
    print command + " \n"
    os.system(command)



print "\n\nCompleted!. Check the folder " + directory_name
                
