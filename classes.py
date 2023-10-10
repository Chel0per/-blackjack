import random
import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self,suit,value):
        super().__init__()
        self.suit = suit
        self.value = value
        self.face_up = False
        self.animating = False
        self.can_change_value = False
        self.blackjack_value = self.get_value(self.value)

        self.sprites = []
        self.sprites.append(pygame.image.load("images/GeneralDesign/back.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back_46.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back_36.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back_20.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/card_side_view.png"))
        self.sprites.append(pygame.image.load(f"images/{self.suit}/{self.value}{self.suit}_20.png"))
        self.sprites.append(pygame.image.load(f"images/{self.suit}/{self.value}{self.suit}_36.png"))
        self.sprites.append(pygame.image.load(f"images/{self.suit}/{self.value}{self.suit}_46.png"))
        self.sprites.append(pygame.image.load(f"images/{self.suit}/{self.value}{self.suit}.png")) 
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [640,60]

    def toggle_animation(self):
        self.animating = True

    def update(self,hand):

        if self.animating:

            if not self.face_up:
                self.image = self.sprites[int(self.current_sprite)]
                self.current_sprite += 0.25

                if self.current_sprite > len(self.sprites) - 1:
                    self.current_sprite = len(self.sprites) - 1 
                    self.face_up = True
                    self.animating = False
                    while self.rect.top < 500 - len(hand.cards)*20:
                        self.rect.top += 5
                    while self.rect.left > 375:
                        self.rect.left -= 5

            else:
                self.image = self.sprites[int(self.current_sprite)]
                self.current_sprite -= 0.25

                if self.current_sprite < 0:
                    self.current_sprite = 0
                    self.face_up = False
                    self.animating = False
                    while self.rect.top < 700 - len(hand.cards)*20:
                        self.rect.top += 5
                    while self.rect.left > 375:
                        self.rect.left -= 5


    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def get_value(self,card_value):
        if card_value == "Ace":
            self.can_change_value = True
            return 11
        elif card_value == "Two":
            return 2
        elif card_value == "Three":
            return 3
        elif card_value == "Four":
            return 4    
        elif card_value == "Five":
            return 5
        elif card_value == "Six":
            return 6
        elif card_value == "Seven":
            return 7
        elif card_value == "Eight":
            return 8
        elif card_value == "Nine":
            return 9
        else:
            return 10
        
    def change_value(self):
        if self.can_change_value:
            self.blackjack_value = 1
            self.can_change_value = False
            

class CardStack(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()          
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        self.cards = []
        self.image = pygame.image.load("images/GeneralDesign/back.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def add_pack(self):
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(suit,value))

    def add_card(self,suit,value):
        self.cards.append(Card(suit,value))

    def draw_card(self):
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def empty(self):
        self.cards = []
    
    def merge(self,other_stack):
        self.cards.extend(other_stack.cards)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.busted = False

    def add_card(self,card):
        self.cards.append(card)
        self.value = sum(card.blackjack_value for card in self.cards)
        if self.value > 21:
            can_change_list = [card for card in self.cards if card.can_change_value]

            if can_change_list:
                can_change_list[0].change_value()
                self.value = sum(card.blackjack_value for card in self.cards)
            else:
                self.busted = True
            

    

       




        