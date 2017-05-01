#!/usr/bin/python

import xml.etree.ElementTree as ET
import re

tree = ET.parse('2017-fill.CGL')
root = tree.getroot()

# TODO Generate buttons for each player > "playername1"
# TODO Generate buttons for each benc player > "playername2"




tree.write(open('out.xml', 'w'), encoding='utf-8')

#buttons = root.findall('.//ButtonList')
#for b in buttons:
#	print b.find('ButtonNumber').text
#print buttons
