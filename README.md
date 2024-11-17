# tools-for-wiki

## pdf-upload-commons

### setup

0. clone this repository
1. run pdf-djvu-uploader-commons-v2.py with username and sourcedir (replace `mohan43u` with your wikimedia account's `username`)
```
./scripts/venvrun.sh ./pdf-upload-commons/pdf-djvu-uploader-commons-v2.py mohan43u /path/to/sourcedir/where/pdf/files/available
```
3. once finished, the python code will move uploaded pdf/djvu file to /path/to/sourcedir/where/pdf/files/available/uploaded directory

## pdf-crop-scale

this tool is used to crop pdf files with specific parameters

### setup

0. clone this repository
1. run following command to get detailed help, follow the examples given in the help message
```
./scripts/venvrun.sh ./pdf-crop-scale/pdf-crop-scale.py --help
```

## columncombine

This tool is used to combine two files in column order

### setup

0. clone this repository
1. run following command to combine two files in column order with tilde as delimiter
```
./scripts/venvrun.sh ./columncombine/columncombine.py file1.txt file2.txt
```

## previous-pageno-generator

This tool is used to generate previous page numbers

### setup

0. clone this repository
1. run following command to generate previous page number in each line based on next page number in the next line
```
./scripts/venvrun.sh ./previous-pageno-generator/previous-pageno-generator.py file.txt
```
