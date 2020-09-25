#! /usr/bin/python3
import requests

def fetch(mot):
	url = "https://www.larousse.fr/dictionnaires/francais/"
	html = requests.get(url + mot).text.split('\n')
	fichier = open("definitions/" + mot + ".txt", 'x')
	for line in html:
		if '<li class="DivisionDefinition">' in line or '<li class="Locution"' in line:
			if '<li class="DivisionDefinition">' in line: 
				fichier.write('*')
			elif '<li class="Locution"' in line:
				fichier.write('&')
			line = line.strip()
			i = 0
			while i < len(line):
				if line[i] == '<':
					while line[i] != '>':
						i = i + 1
				elif line[i] == '&':
					while line[i] != ';':
						i = i + 1
				else:
					fichier.write(line[i])
				i = i + 1
			fichier.write('\n')
	fichier.close()
