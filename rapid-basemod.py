#!/usr/bin/python

import xml.etree.ElementTree as ET
import re

tree = ET.parse('2017-base.CGL')
root = tree.getroot()

taglinks = root.findall('.//TagLinks')
for tl in taglinks:
	if tl.find('FileName').text == "lagoppstilling-sogndal-grid":
		m = re.match("([0-9])([0-9])(.)", tl.find('TagName').text)
		if m:
			x = m.group(1)
			y = m.group(2)
			t = m.group(3)
			tl.find('TagLink').text = "[data:hometeam] " + x + y + t

tree.write(open('out.xml', 'w'), encoding='utf-8')

#buttons = root.findall('.//ButtonList')
#for b in buttons:
#	print b.find('ButtonNumber').text
#print buttons
