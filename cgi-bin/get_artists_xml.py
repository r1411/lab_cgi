import sys 
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import db
import cgi
import xml.etree.ElementTree as ET

artists = db.get_all_artists()

root = ET.Element('artists')
for artist in artists:
    artist_element = ET.SubElement(root, 'artist')
    artist_name = ET.SubElement(artist_element, 'name')
    artist_name.text = artist[1]
    artist_country = ET.SubElement(artist_element, 'country')
    artist_country.text = artist[3]
    artist_birthday = ET.SubElement(artist_element, 'birthday')
    artist_birthday.text = artist[2]

tree = ET.ElementTree(root)
ET.indent(tree)

print(f'Content-Type: application/octet-stream; name="artists.xml"\n')
ET.dump(tree)