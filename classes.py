import random

class Card:
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class CardStack:
    def __init__(self):
        self.suits = ['Hearts','Diamonds','Clubs','Spades']
        self.values = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']
        self.cards = []

    def add_pack(self):
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(suit,value))

    def add_card(self,suit,value):
        self.cards.append(Card(suit,value))

    def shuffle(self):
        random.shuffle(self.cards)

    def empty(self):
        self.cards = []
    
    def merge(self,other_stack):
        self.cards.extend(other_stack.cards)

pack = CardStack()
pack.add_pack()
pack.shuffle()

for card in pack.cards:
    print(card)

    




        