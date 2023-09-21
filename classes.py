import random

class card_pack:
    def __init__(self):
        self.aces = 4
        self.twos = 4
        self.threes = 4
        self.fours = 4
        self.fives = 4
        self.sixes = 4
        self.sevens = 4
        self.eights = 4
        self.nines = 4
        self.tens = 4
        self.jacks = 4
        self.queens = 4
        self.kings = 4
        self.cards = 52

    def add_pack(self):
        self.aces += 4
        self.twos += 4
        self.threes += 4
        self.fours += 4
        self.fives += 4
        self.sixes += 4
        self.sevens += 4
        self.eights += 4
        self.nines += 4
        self.tens += 4
        self.jacks += 4
        self.queens += 4
        self.kings += 4
        self.cards += 52

    def pick_random_card(self):
        if self.cards == 0:
            return "No card left in the pack!"
        else:
            card = random.randint(1,self.cards)

            if card <= self.aces:
                self.aces -= 1
                self.cards -= 1
                return "You picked an ace!"
            elif card <= self.twos + self.aces:
                self.twos -= 1
                self.cards -= 1
                return "You picked a two!"
            elif card <= self.threes + self.twos + self.aces:
                self.threes -= 1
                self.cards -= 1
                return "You picked a three!"
            elif card <= self.fours + self.threes + self.twos + self.aces:
                self.fours -= 1
                self.cards -= 1
                return "You picked a four!"
            elif card <= self.fives + self.fours + self.threes + self.twos + self.aces:
                self.fives -= 1
                self.cards -= 1
                return "You picked a five!"
            elif card <= self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.sixes -= 1
                self.cards -= 1
                return "You picked a six!"
            elif card <= self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.sevens -= 1
                self.cards -= 1
                return "You picked a seven!"
            elif card <= self.eights + self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.eights -= 1
                self.cards -= 1
                return "You picked an eight!"
            elif card <= self.nines + self.eights + self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.nines -= 1
                self.cards -= 1
                return "You picked a nine!"
            elif card <= self.tens + self.nines + self.eights + self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.tens -= 1
                self.cards -= 1
                return "You picked a ten!"
            elif card <= self.jacks + self.tens + self.nines + self.eights + self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.jacks -= 1
                self.cards -= 1
                return "You picked a jack!"
            elif card <= self.queens + self.jacks + self.tens + self.nines + self.eights + self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.queens -= 1
                self.cards -= 1
                return "You picked a queen!"
            elif card <= self.kings + self.queens + self.jacks + self.tens + self.nines + self.eights + self.sevens + self.sixes + self.fives + self.fours + self.threes + self.twos + self.aces:
                self.kings -= 1
                self.cards -= 1
                return "You picked a king!"





        