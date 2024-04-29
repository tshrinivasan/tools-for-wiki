# tools-for-wiki

## pdf-upload-commons

### setup

0. clone this repository
1. get `venvshell` by running this command
```
./scripts/venvshell
```
2. run pdf-djvu-uploader-commons-v2.py with username and sourcedir (replace `mohan43u` with your wikimedia account's `username`)
```
./pdf-upload-commons/pdf-djvu-uploader-commons-v2.py mohan43u /path/to/sourcedir/where/pdf/files/available
```
3. once finished, the python code will move uploaded pdf/djvu file to /path/to/sourcedir/where/pdf/files/available/uploaded directory

## pdf-crop-scale

### setup

0. clone this repository
1. get `venvshell` by running this command
```
./scripts/venvshell
```
2. run following command to get detailed help, follow the examples given in the help message
```
./pdf-crop-scale/pdf-crop-scale.py --help
```
