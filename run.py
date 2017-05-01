#!/usr/bin/python

import xml.etree.ElementTree as ET

tree = ET.parse('2017-base.CGL')
root = tree.getroot()

buttons = root.findall('.//ButtonList')
for b in buttons:
	print b.find('ButtonNumber').text


print buttons