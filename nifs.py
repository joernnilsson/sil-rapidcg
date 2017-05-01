#!/usr/bin/python
# encoding=utf8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import re
import json
import urllib2
import time
import sys
import codecs

today = time.strftime("%Y-%m-%d") if len(sys.argv) == 1 else sys.argv[1]
nifsTournamentId = 5;


shirtGraphicUrl = "C:\Documents and Settings\Broadcast Pix\My Documents\My Pictures\spelar.png"

nifsUrlMatches = "http://api.nifs.no/tournaments/" + str(nifsTournamentId) + "/matches?date="+today
nifsUrlMatch = "http://api.nifs.no/matches/"

def getJson(url):
	req = urllib2.Request(url)
	req.add_header('Content-Type', 'application/json')
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
	req.add_header('Accept', 'application/json')
	response = urllib2.urlopen(req)
	data = json.loads(response.read())
	return data

def modal(msg):
	try:
		a = input('\n' + msg + '. Trykk enter for å lukke vinduet\n')
	except:
		pass
	exit(0)

# Hent kamper
matches = getJson(nifsUrlMatches)

# Velg kamp
print "Dagens kamper:"
idx = 1;
for match in matches:
	print "\t" + str(idx) + ". " + match["name"]
	idx = idx + 1

#selected = input("Tast inn kampnummer og trykk enter: ")
selected = 4
if(selected < 1 or selected > idx):
	modal("ERROR: Ugyldig kampnummer")
nifsMatchId = matches[selected-1]["id"]
selectedMatchUrl = nifsUrlMatch + str(nifsMatchId)
print ""
print "Valgt kamp:", matches[selected-1]["name"], selectedMatchUrl


# Hent kampdata
match = getJson(selectedMatchUrl);
home = { "keeper": [], "defenders": [], "midfield": [], "strikers": [], "bench": [], "formation": "", "key": "homeTeam", "table": "hometeam", "players": 0}
away = { "keeper": [], "defenders": [], "midfield": [], "strikers": [], "bench": [], "formation": "", "key": "awayTeam", "table": "awayteam", "players": 0}
teams = [home, away]

for team in teams:
	team["name"] = match[team["key"]]["name"]
	for p in match[team["key"]]["persons"]:
		xpos = p["position"]["x"] if p["position"] and p["position"]["x"] else 0
		ypos = p["position"]["y"] if p["position"] and p["position"]["y"] else 0
		pdata = { "x": xpos, "y": ypos, "shirtName": p["shirtName"], "shirtNumber": p["shirtNumber"], "name": p["name"], "nifsId": p["id"]}
		if p["startsOnTheBench"]:
			team["bench"].append(pdata)
		elif ypos == 1:
			team["keeper"].append(pdata)
		elif ypos < 5:
			team["defenders"].append(pdata)
		elif ypos < 7:
			team["midfield"].append(pdata)
		elif ypos:
			team["strikers"].append(pdata)

		team["formation"] = str(len(team["defenders"])) + "-" + str(len(team["midfield"])) + "-" + str(len(team["strikers"]))

	# Order players from right to left
	team["defenders"] = sorted(team["defenders"], key=lambda k: k['x'], reverse=False) 
	team["midfield"] = sorted(team["midfield"], key=lambda k: k['x'], reverse=False) 
	team["strikers"] = sorted(team["strikers"], key=lambda k: k['x'], reverse=False) 

	# Does the team have enough players?
	if (len(team["keeper"]) + len(team["defenders"]) + len(team["midfield"]) + len(team["strikers"])) < 11:
		modal("ERROR: Ikke nok spillere på " + team["key"] + " (ikke ennå tilgjengelig på nifs.no)")

# Print details	
for team in teams:
	print ""
	print team["name"], "(" + team["formation"] + ")"
	print "\t", "Keeper:"
	print "\t -", team["keeper"][0]["shirtNumber"], team["keeper"][0]["shirtName"]
	print "\t", "Forsvar:"
	for p in team["defenders"]:
		print "\t -", p["shirtNumber"], p["shirtName"]
	print "\t", "Midtbane:"
	for p in team["midfield"]:
		print "\t -", p["shirtNumber"], p["shirtName"]
	print "\t", "Angrep:"
	for p in team["strikers"]:
		print "\t -", p["shirtNumber"], p["shirtName"]
	print "\t", "På benken:"
	for p in team["bench"]:
		print "\t -", p["shirtNumber"], p["shirtName"]


# Write xml file
xml = ''
xml = xml + '<?xml version="1.0" standalone="yes"?>\n'
xml = xml + '<root>\n'

# Parse text file lines into xml
for team in teams:

	xml = xml + ' <' + team["table"] + '>\n'

	players = team["keeper"] + team["defenders"] + team["midfield"] + team["strikers"] + team["bench"]

	# Hash the grid
	grid = {}

	for p in players:
		x = str(p["x"])
		y = str(p["y"])
		grid[x + y] = p

	# Generate links for complete grid
	for x in range(1,7):
		for y in range(1,7):
			k = str(x) + str(y)
			if(k in grid):
				p = grid[k];
				num = p["shirtNumber"]
				name = p["shirtName"]
				fullname = p["name"]
				t = shirtGraphicUrl
			else:
				num = ""
				name = ""
				fullname = ""
				t = ""

			# Grid
			xml = xml + '  <' + k +'r>' + str(num) + '</' + k +'r>\n'
			xml = xml + '  <' + k +'n>' + name + '</' + k +'n>\n'
			xml = xml + '  <' + k +'g>' + t + '</' + k +'g>\n'



	# Legacy links
	i = 1;
	for p in players:

		num = p["shirtNumber"]
		name = p["shirtName"]
		fullname = p["name"]
		key = str(team["key"][0])


		xml = xml + '  <' + key +str(i)+'nr>' + str(num) + '</' + key +str(i)+'nr>\n'
		xml = xml + '  <' + key +str(i)+'lastname>' + name + '</' + key +str(i)+'lastname>\n'
		xml = xml + '  <' + key +str(i)+'full>' + fullname + '</' + key +str(i)+'full>\n'

		i = i + 1

	xml = xml + ' </' + team["table"] + '>\n'

xml = xml + '</root>'



f = codecs.open('data.xml', 'w', "utf-8")
f.write(xml)
f.close()

modal("Datafil er ferdig oppdatert")



