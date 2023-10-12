from __future__ import annotations
from typing import List
import pygame
import time 
import random
import sys

class Card(pygame.sprite.Sprite):

    def __init__(self,suit:str,value:str):
        super().__init__()
        self.suit = suit
        self.value = value
        self.face_up = False
        self.fliping = False
        self.moving = False
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
        self.top_destination = 60
        self.left_destination = 640

    def toggle_flip(self):
        self.fliping = True

    def toggle_movement(self,top:int,left:int):
        self.top_destination = top
        self.left_destination = left

    def update(self,hand:Hand):

        if self.fliping:

            if not self.face_up:
                self.image = self.sprites[int(self.current_sprite)]
                self.current_sprite += 0.25

                if self.current_sprite > len(self.sprites) - 1:
                    self.current_sprite = len(self.sprites) - 1 
                    self.face_up = True
                    self.fliping = False

            else:
                self.image = self.sprites[int(self.current_sprite)]
                self.current_sprite -= 0.25

                if self.current_sprite < 0:
                    self.current_sprite = 0
                    self.face_up = False
                    self.animating = False
        
        if self.rect.top != self.top_destination:
            self.rect.top += 5

        if self.rect.left != self.left_destination:
            self.rect.left -= 5

    def __str__(self) -> str:
        return f"{self.value} of {self.suit}"
    
    def get_value(self,card_value) -> int:
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

    back_image = pygame.image.load("images/GeneralDesign/back.png")
    empty_image = pygame.image.load("images/GeneralDesign/back.png")

    def __init__(self,pos_x:int,pos_y:int):
        super().__init__()          
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        self.cards:List[Card] = []
        self.back_image = pygame.image.load("images/GeneralDesign/back.png")
        self.empty_image = pygame.image.load("images/GeneralDesign/empty_stack.png")
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
        elif len(self.cards) == 1:
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

class Hand:
    def __init__(self):
        self.cards:List[Card] = []
        self.value = 0
        self.busted = False

    def add_card(self,card:Card):
        self.cards.append(card)
        self.value = sum(card.blackjack_value for card in self.cards)
        if self.value > 21:
            can_change_list = [card for card in self.cards if card.can_change_value]

            if can_change_list:
                can_change_list[0].change_value()
                self.value = sum(card.blackjack_value for card in self.cards)
            else:
                self.busted = True

WIDTH = 800
HEIGHT = 600

background = pygame.image.load("images/GeneralDesign/table.png")

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Blackjack")

card_sprites = pygame.sprite.Group()

game_stack = CardStack(640,60)
game_stack.add_pack()
game_stack.shuffle()
game_stack_sprites = pygame.sprite.Group()
game_stack_sprites.add(game_stack)

players_hand = Hand()

def main():
    run = True

    while run:
        card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                card = game_stack.draw_card()
                card_sprites.add(card)
                card.toggle_flip()
                card.toggle_movement(500 - 20*len(players_hand.cards),375 + 20*len(players_hand.cards))
                players_hand.add_card(card)

        WIN.blit(background, (0, 0))
        game_stack_sprites.draw(WIN)
        card_sprites.draw(WIN)
        card_sprites.update(players_hand)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()