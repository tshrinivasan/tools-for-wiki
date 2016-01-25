import glob
import time
import datetime
import os

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


                

#license = raw_input("Enter the name of the licese file : ")
#license = license.decode('utf-8')

files = []
for filename in glob.glob(u'*.pdf'):
                files.append(filename)

#files.remove(license)

directory_name = "cover-images-"+timestamp

os.mkdir(directory_name)

for pdf in files:
    pdf_name = str(pdf).split('.pdf')[0]


#Extract first page of the pdf file
#pdftk <pdfname> cat <pageno> output <outputfilename>

    command = "pdftk " + pdf +  "  cat 1 output " + directory_name + "/" + pdf_name + "_cover.pdf"
    command = command.encode('utf-8')
    print "\n" +command + " \n"
    os.system(command)

#converting pdf to png
#convert name.pdf name.png

    command = "convert " +  directory_name + "/" + pdf_name + "_cover.pdf " +  directory_name + "/" + pdf_name + "_cover.png"
    command = command.encode('utf-8')
    print "\n" +command + " \n"
    os.system(command)



print "\n\nCompleted!. Check the folder " + directory_name
                
