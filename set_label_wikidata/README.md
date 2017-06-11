==INSTALL==

sudo pip install wikidataintegrator

run the above command to install the python module wikidataintegrator.


==Readme==

The script set_label_in_wikidata.py is used to set the label in desired language for the items defined in a CSV file.

The file data.csv should have the item id and label in your language. The should be seperated by ~ .

Then, edit the file set_label_in_wikidata.py and set the parameters wikidata_username and wikidata_password.

Then, run it via

python set_label_in_wikidata.py
