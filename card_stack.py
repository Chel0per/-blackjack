from __future__ import annotations
import pygame
import random

class CardStack(pygame.sprite.Sprite):

    back_image = pygame.image.load("images/GeneralDesign/back.png")
    empty_image = pygame.image.load("images/GeneralDesign/back.png")

    def __init__(self,pos_x:int,pos_y:int):
        super().__init__()          
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        self.cards = [Card]
        self.back_image = pygame.image.load("images/GeneralDesign/back.png")
        self.empty_image = pygame.image.load("images/GeneralDesign/back.png")
        self.image = self.empty_image
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def add_pack(self):
        if len(self.cards) == 0:
            self.image = self.back_image
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(suit,value))

    def add_card(self,suit:str,value:str):
        if len(self.cards) == 0:
            self.image = self.back_image
        self.cards.append(Card(suit,value))

    def draw_card(self) -> Card:
        if len(self.cards) == 0:
            return None
        elif len(self.card) == 1:
            self.image = self.empty_image
            return self.cards.pop()
        else:
            return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def empty(self):
        self.cards = []
        self.image = self.empty_image
    
    def merge(self,other_stack:CardStack):
        if len(self.cards) == 0:
            return None
        self.cards.extend(other_stack.cards)
        other_stack.empty()

