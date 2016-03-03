import glob
import time
import datetime
import os

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


                

license = raw_input("Enter the name of the licese file : ")
license = license.decode('utf-8')

files = []
for filename in glob.glob(u'*.pdf'):
                files.append(filename)

files.remove(license)

directory_name = "license-added-"+timestamp

os.mkdir(directory_name)

for pdf in files:

#adding the license pdf as the second page of each pdf file

    command = "pdftk A=" + pdf +  " B=" + license + "  cat A1 B A2-end output " + directory_name + "/" + pdf
    #    command = "pdfunite " + pdf + " "  + license  + " " +  directory_name + "/" + pdf
    command = command.encode('utf-8')
    command = command.replace("(", "\(").replace(")", "\)")
    print "\n" +command + " \n"
    os.system(command)


    print "Removing original file " + pdf
    os.remove(pdf)

print "\n\nCompleted!. Check the folder " + directory_name
                
