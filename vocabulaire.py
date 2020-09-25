#! /usr/bin/python3
import os, random, definition

def ignore_parenthesis(mot):
	i = 0
	while i < len(mot):
		if mot[i] == '(':
			while mot[i] != ')':
				mot = mot[:i] + mot[i + 1:]
			mot = mot[:i] + mot[i + 1:]
		else:
			i = i + 1
	return mot

def rearrange_word(mot):
	if not mot.isalpha():
		mot = ignore_parenthesis(mot)
		if "formes verbales" in mot:
			mot = mot[20:-1]
	return mot

def mode_menu(biglist, rand1, rand2, found, seed, definitions, expressions, score, total, mode):
	os.system("cls")
	print("_________________________________________")
	print(mode.upper())
	print("_________________________________________")
	print("")
	print("Mot: {}".format(biglist[rand1][rand2]))
	print("")
	if found != None:
		if len(definitions) > 0: 
			print("Définition(s):")
			i = 0
			while i < len(definitions) and i < 5:
				print(str(i + 1) + ") " + definitions[i])
				i = i + 1
		if len(expressions) > 0: 
			print("Expression(s):")
			i = 0
			while i < len(expressions) and i < 5:
				print(str(i + 1) + ") " + expressions[i])
				i = i + 1
	if mode == "homonymes" or mode == "paronymes":
		print("Trouvé(s): {}/{}".format(len(found), len(biglist[rand1]) - 1))
		if len(found) == 0:
			print()
		else :
			for i in range(len(found)):
				if i == len(found) - 1:
					print(str(i + 1) + '.' + found[i])
				else:
					print(str(i + 1) + '.' + found[i],end=', ')
	print("_________________________________________")
	print("Seed: {}".format(seed))
	print("Score: {}/{}".format(score, total))
	if (total == 0):
		print("Pourcentage de connaissance: 100%")
	else :
		print("Pourcentage de connaissance: {}%".format(score/total*100))
	print("Rounds restants: {}".format(len(biglist)))

def definition_menu(mot):
	os.system("cls")
	print("_________________________________________")
	print("DEFINITION")
	print("_________________________________________")
	print("")
	print("Mot: {}".format(mot))
	print("")

	#fetching the definitions
	mot = (rearrange_word(mot))
	definitions = []
	expressions = []
	if not os.path.exists("definitions/" + mot + ".txt"):
		definition.fetch(mot)
	fichier = open("definitions/" + mot + ".txt", 'r')
	for line in fichier:
		if line[0] == '*':
			definitions.append(line[1:])
		elif line[0] == '&':
			expressions.append(line[1:])

	if len(definitions) > 0: 
		print("Définition(s):")
		i = 0
		while i < len(definitions) and i < 5:
			print(str(i + 1) + ") " + definitions[i])
			i = i + 1
	if len(expressions) > 0: 
		print("Expression(s):")
		i = 0
		while i < len(expressions) and i < 5:
			print(str(i + 1) + ") " + expressions[i])
			i = i + 1
	print("_________________________________________")

def endgame(score, total):
	os.system("clear")
	print("Stats:")
	print("Score: {}/{}".format(score, total))
	print("Pourcentage de connaissance: {}%".format(score/total))
	print("Vous êtes nul.")

def session(mode):
	#reading part
	f = open("{}.txt".format(mode), "r")
	biglist = []
	line = f.readline()
	while line:
		biglist.append(line.strip().split('/'))
		line = f.readline()

	#seed part
	os.system("cls")
	seed = input("Veuillez choisir un seed: ")
	if seed != "":
		random.seed(int(seed))
	else:
		seed = random.randint(0, 1000)
		random.seed(seed)
		
	#setting up the session
	score = 0
	total = 0
	while len(biglist) > 0:

		#round part
		#chosing random word
		rand1 = random.randint(0, len(biglist) - 1)
		rand2 = random.randint(0, len(biglist[rand1]) - 1)
		mot = rearrange_word(biglist[rand1][rand2])

		#fetching the definitions
		definitions = []
		expressions = []
		if not os.path.exists("definitions/" + mot + ".txt"):
			definition.fetch(mot)
		fichier = open("definitions/" + mot + ".txt", 'r')
		for line in fichier:
			if line[0] == '*':
				definitions.append(line[1:])
			elif line[0] == '&':
				expressions.append(line[1:])

		#setting up the round
		found = []
		while len(found) < len(biglist[rand1]) - 1:
			mode_menu(biglist, rand1, rand2, found, seed, definitions, expressions, score, total, mode)
			#user's answer
			answer = input("Réponse: ")

			#give up
			if answer == "":
				for i in range(len(biglist[rand1])):
					if biglist[rand1][i] != biglist[rand1][rand2] and biglist[rand1][i] not in found:
						found.append(biglist[rand1][i])
						total = total + 1

			#attempt to answer
			else :
				if answer[0] == '[' and answer[-1] == ']':
					answer = answer[0] + "formes verbales de " + answer[1:]
				if answer != biglist[rand1][rand2] and answer not in found:
					i = 0
					while i < len(biglist[rand1]) and answer != ignore_parenthesis(biglist[rand1][i]):
						i = i + 1
					if i < len(biglist[rand1]):
						found.append(biglist[rand1][i])
						score = score + 1
						total = total + 1
		
		#round finished

		answer = None
		if mode == "lexique":
			found = None
			mode_menu(biglist, rand1, rand2, found, seed, definitions, expressions, score, total, mode)
			input("Appuyez sur Enter pour afficher les définitions et expressions\n")
		while answer != "":
			if mode == "lexique":
				found = []
			mode_menu(biglist, rand1, rand2, found, seed, definitions, expressions, score, total, mode)
			if mode == "homonymes" or mode == "paronymes":
				answer = input("Terminé ! Entrer le numéro du mot pour connaître sa définition, ou rien du tout pour continuer !\n")
				if answer.isdigit() and int(answer) - 1 < len(found):
					definition_menu(found[int(answer) - 1])
					input("Appuyer sur Enter pour continuer")
			elif mode == "lexique":
				answer = input("Terminé ! Avez-vous oui ou non réussi ? :\n")
				if answer == "oui":
					score = score + 1
				total = total + 1
				answer = ""
		biglist.pop(rand1)
	endgame(score, total)


def main():
	modes = ["homonymes", "paronymes", "lexique"]
	os.system("cls")
	print("Choisissez un mode:")
	for i in range(len(modes) - 1):
		print("{}){}".format(i + 1, modes[i]), end=", ")
	print("{}){}".format(len(modes), modes[-1]))
	answer = input()
	session(modes[int(answer) - 1])

if __name__ == "__main__":
	main()
