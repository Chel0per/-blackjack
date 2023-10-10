import pygame
import time 
import random
import sys
from classes import Card
from classes import CardStack
from classes import Hand

class Animation(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.flip_animating = False
        self.sprites = []
        self.sprites.append(pygame.image.load("images/Hearts/AceHearts.png"))
        self.sprites.append(pygame.image.load("images/Hearts/AceHearts_46.png"))
        self.sprites.append(pygame.image.load("images/Hearts/AceHearts_36.png"))
        self.sprites.append(pygame.image.load("images/Hearts/AceHearts_20.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/card_side_view.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back_20.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back_36.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back_46.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/back.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def flip(self):
        self.flip_animating = True

    def update(self,speed):

        if self.flip_animating:

            self.image = self.sprites[int(self.current_sprite)]
            self.current_sprite += speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.flip_animating = False 

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
                players_hand.add_card(card)
                card_sprites.add(card)
                card.toggle_animation()

        WIN.blit(background, (0, 0))
        game_stack_sprites.draw(WIN)
        card_sprites.draw(WIN)
        card_sprites.update(players_hand)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()