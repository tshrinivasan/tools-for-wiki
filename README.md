# tools-for-wiki

## pdf-upload-commons

### setup

0. clone this repository

1. run following command from the cloned git directory
```
DEV=1 ./bootstrap/bootstrap poetry shell
```

2. run pdf-djvu-uploader-commons-v2.py with username and sourcedir
```
./pdf-upload-commons/pdf-djvu-uploader-commons-v2.py mohan43u /path/to/sourcedir/where/pdf/files/available
```

3. once finished, the python code will move uploaded pdf/djvu file to /path/to/sourcedir/where/pdf/files/available/uploaded directory
