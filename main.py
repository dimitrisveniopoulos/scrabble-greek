from classes import Game, Human, Computer
import json

# Reading words from file and saving them in a dictionary (key: word, value: word's total value)
with open("greek7.txt", encoding='utf8') as f:
    lines = f.readlines()

words = []
for word in lines:
    words.append(word.strip())

letters = {'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1],
           'Ζ': [1, 10], 'Η': [7, 1], 'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2],
           'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10], 'Ο': [9, 1],
           'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 2],
           'Φ': [1, 8], 'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 3]
           }

word_value_dictionary = dict()
for word in words:
    value = 0
    for letter in word:
        value += letters[letter][1]
    word_value_dictionary[word] = value

# Initiating game and printing menu
print("***** SCRABBLE *****")
algorithm = 3  # Smart
while True:
    print("----------------------------------------\n" +
          "1: Σκορ\n" +
          "2: Ρυθμίσεις\n" +
          "3: Παιχνίδι\n" +
          "q: Έξοδος")
    command = str(input("Επιλέξτε: "))
    while command != "1" and command != "2" and command != "3" and command != "q":
        command = str(input("Λάθος εντολή. Επιλέξτε ξανά: "))

    if command == "1":
        with open("history.json") as json_file:
            history = json.load(json_file)
        print("----------------------------------------")
        players = history["players"]
        for player in players:
            print("Όνομα: " + player["name"] + " - Νίκες: " + str(player["wins"]))

    elif command == "2":
        print("----------------------------------------\n" +
              "1: MIN\n" +
              "2: MAX\n" +
              "3: SMART")
        algorithm = input("Επιλέξτε αλγόριθμο για τον υπολογιστή: ")
        while algorithm != "1" and algorithm != "2" and algorithm != "3":
            algorithm = str(input("Λάθος εντολή. Επιλέξτε ξανά: "))
        if algorithm == "1":
            print("Αλγόριθμος που επιλέχθηκε: MIN")
        elif algorithm == "2":
            print("Αλγόριθμος που επιλέχθηκε: MAX")
        else:
            print("Αλγόριθμος που επιλέθηκε: SMART")

    elif command == "3":
        player1 = Human("Dimitris")
        player2 = Computer("Computer")
        player2.algorithm = algorithm
        game = Game(word_value_dictionary, letters, player1, player2)
        game.setup()
        game.run()
        game.end()

    elif command == "q":
        exit()
