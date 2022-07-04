# tools-for-wiki

## pdf-upload-commons

### setup

1. run following command from the project top dir
```
DEV=1 ./bootstrap/bootstrap poetry shell
```

2. change directory to pdf-upload-commons
```
cd pdf-upload-commons
```

3. run pdf-djvu-uploader-commons-v2.py with username and sourcedir
```
./pdf-djvu-uploader-commons-v2.py mohan43u /path/to/sourcedir/where/pdf/files/available
```

4. once finished, the python code will move uploaded pdf/djvu file to /path/to/sourcedir/where/pdf/files/available/uploaded directory
