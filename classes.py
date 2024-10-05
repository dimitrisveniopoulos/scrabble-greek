import itertools
import json
import random


class SakClass:
    def __init__(self):
        self.letters = None  # All letters in a dictionary
        self.letters_as_string = None  # All letters in a string
        self.letters_left = 0  # Number of letters left in sak

    def randomize_sak(self, letters):
        self.letters = letters
        self.letters_as_string = ""
        for key in self.letters.keys():
            self.letters_as_string += key * self.letters.get(key)[0]
        self.letters_left = len(self.letters_as_string)

    def get_letters(self, available_letters):
        n = 7 - len(available_letters)
        if self.letters_left < n:
            n = self.letters_left

        for i in range(0, n):  # Randomly choosing n letters from the string containing all the letters in the sak
            letter = self.letters_as_string[random.randint(0, self.letters_left - 1)]
            available_letters.append(letter)
            self.letters_as_string = self.letters_as_string.replace(letter, "", 1)
            self.letters_left -= 1

        return available_letters

    def put_back_letters(self, letters):  # Placing letters back in the sak
        for letter in letters:
            self.letters_as_string += letter
        self.letters_left = len(self.letters_as_string)


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.available_letters = []
        self.give_letters = True

    def __repr__(self):
        return self.name

    def add_points(self, points):
        self.score += points


class Human(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def __repr__(self):
        return self.name

    def play(self, words):
        while True:
            word = input("Δώσε λέξη: ")
            if word == "p" or word == "q":
                return word
            if Game.check_word_validity(word, self.available_letters, words):
                return word
            else:
                print("Μη αποδεκτή λέξη. Προσπάθησε ξανά.")


class Computer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.algorithm = 3

    def __repr__(self):
        return self.name

    def play(self, words):
        print("Δώσε λέξη: ", end="")
        if self.algorithm == "1":  # Playing according to the selected algorithm
            return self.min(words)
        elif self.algorithm == "2":
            return self.max(words)
        else:
            return self.smart(words)

    def min(self, words):  # MIN algorithm
        for i in range(2, 8):
            perm = itertools.permutations(self.available_letters, i)
            for word in perm:
                word = ''.join(word)
                valid = Game.check_word_validity(word, self.available_letters, words)
                if valid:
                    print(word)
                    return word
        print("p")
        return "p"

    def max(self, words):  # MAX algorithm
        for i in range(7, 1, -1):
            perm = itertools.permutations(self.available_letters, i)
            for word in perm:
                word = ''.join(word)
                valid = Game.check_word_validity(word, self.available_letters, words)
                if valid:
                    print(word)
                    return word
        print("p")
        return "p"

    def smart(self, words):  # SMART algorithm
        max_word = ""
        max_value = 0
        for i in range(2, 8):
            perm = itertools.permutations(self.available_letters, i)
            for word in perm:
                word = ''.join(word)
                valid = Game.check_word_validity(word, self.available_letters, words)
                if valid:
                    if words[word] > max_value:  # Checking word value
                        max_word = word
                        max_value = words[word]
        if max_value > 0:
            print(max_word)
            return max_word
        else:
            print("p")
            return "p"


class Game:
    def __init__(self, words, letters, player1, player2):
        self.words = words
        self.letters = letters
        self.sak = None
        self.player1 = player1
        self.player2 = player2

    def setup(self):
        self.sak = SakClass()
        self.sak.randomize_sak(self.letters)

    def run(self):
        i = 1  # Player 1 starting first
        while True:
            if i == 1:  # Changing between players
                player = self.player1
                i = 2
            else:
                player = self.player2
                i = 1
            if player.give_letters:  # If player must take new letters, do so
                player.available_letters = self.sak.get_letters(player.available_letters)
            print("----------------------------------------")
            print("Παίκτης: " + str(player) + " - Σκορ: " + str(player.score))
            message = "Διαθέσιμα γράμματα: "
            for letter in player.available_letters:
                message += letter + str(self.letters[letter][1]) + " "
            print(message)
            print("Απομένουν " + str(self.sak.letters_left) + " γράμματα στο σακουλάκι.")

            word = player.play(self.words)  # Word given by player

            if word == "q":
                break
            if word == "p":
                if self.sak.letters_left == 0:  # If player plays 'p' and no letters are left in sak, end the game
                    break
                temp_letters = player.available_letters.copy()  # Saving letters to put them back AFTER taking new ones
                player.available_letters = []
                player.available_letters = self.sak.get_letters(player.available_letters)
                player.give_letters = False
                self.sak.put_back_letters(temp_letters)
                print("Πήγες πάσο. Πήρες νέα γράμματα αλλά χάνεις τη σειρά σου.")
                continue

            # Calculating score and putting back letters
            for letter in word:
                player.available_letters.remove(letter)
            player.give_letters = True
            points = self.words[word]
            player.add_points(points)
            print("Αποδεκτή λέξη! Κέρδισες " + str(points) + " πόντους!")
            print("Παίκτης: " + str(player) + " - Σκορ: " + str(player.score))

    def end(self):
        # Printing final results
        print("----------------------------------------")
        print(str(self.player1) + " - Σκορ: " + str(self.player1.score))
        print(str(self.player2) + " - Σκορ: " + str(self.player2.score))
        winner = self.player1
        if self.player1.score < self.player2.score:
            winner = self.player2
        elif self.player1.score == self.player2.score:
            winner = None
        if winner is not None:
            print("ΝΙΚΗΤΗΣ: " + str(winner))
        else:
            print("ΙΣΟΠΑΛΙΑ")

        # Saving result to history.json file
        with open("history.json") as json_file:
            history = json.load(json_file)
        for i in range(0, 2):
            if history["players"][i]["name"] == str(winner):
                history["players"][i]["wins"] += 1
        with open("history.json", "w") as json_file:
            json.dump(history, json_file)

    @staticmethod
    def check_word_validity(word, available_letters, words):
        # valid variable is True if the word can be formed given the player's available letters
        valid = True
        temp_letters = available_letters.copy()
        for letter in word:
            valid = False
            for l in temp_letters:
                if letter == l:
                    temp_letters.remove(l)
                    valid = True
                    break
            if not valid:
                break
        if valid and words.get(word) is not None:  # If word is valid AND exists in the word dictionary, return true
            return True
