# INSTALL

sudo pip3 install wikidataintegrator
sudo pip3 install tqdm

run the above command to install the python module wikidataintegrator.


# Details

The script set_label_in_wikidata.py is used to set the label in desired language for the items defined in a CSV file.

The file data.csv should have the item id and label in your language and alias. The should be seperated by ~ .

Then, edit the file set_label_in_wikidata.py and set the parameters wikidata_username and wikidata_password.

Then, run it via

python3 set_label_in_wikidata.py


# Sample data

Q9170~கோசி மண்டலம்~
Q9172~லும்பினி மண்டலம்~test


# Note

The data.csv should have 3 columns. item id, label, and alias. If you have alias, end the line with Empty ~ as in sample line 1
