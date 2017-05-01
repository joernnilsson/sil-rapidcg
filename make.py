#!/usr/bin/python
# encoding=utf8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import re


# Make Xml structure
root = Element('root')
hometeam = SubElement(root, 'hometeam')
awayteam = SubElement(root, 'awayteam')

xml = ''
xml = xml + '<?xml version="1.0" standalone="yes"?>\n'
xml = xml + '<root>\n'

# Read text files


# Parse text file lines into xml
for t in [('hometeam', 'home.txt'), ('awayteam', 'away.txt')]:
	with open(t[1]) as p:
		ls = p.readlines()
	i = 1;
	xml = xml + ' <' + t[0] + '>\n'
	for p in ls:
		l = p.strip()
		idx = p.find(" ")
		num = l[0:idx]
		name = l[idx+1:].split(' ')[-1]
		xml = xml + '  <' + t[0][0] +str(i)+'nr>' + num + '</' + t[0][0] +str(i)+'nr>\n'
		xml = xml + '  <' + t[0][0] +str(i)+'lastname>' + name + '</' + t[0][0] +str(i)+'lastname>\n'
		xml = xml + '  <' + t[0][0] +str(i)+'full>' + l + '</' + t[0][0] +str(i)+'full>\n'
		i = i + 1
		print t[0]+':', l
	xml = xml + ' </' + t[0] + '>\n'
	


xml = xml + '</root>'

f = open('data.xml', 'w')
f.write(xml)
f.close()
try:
	a = input('\nDatafil er ferdig oppdatert! Trykk enter for å lukke vinduet\n')
except:
	pass	
