import pygame
import time 
import random
import sys

class Animation(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.flip_animating = False
        self.sprites = []
        self.sprites.append(pygame.image.load("images/ASpades_flat_mini.png"))
        self.sprites.append(pygame.image.load("images/ASpades_flat_mini_46.png"))
        self.sprites.append(pygame.image.load("images/ASpades_flat_mini_36.png"))
        self.sprites.append(pygame.image.load("images/ASpades_flat_mini_20.png"))
        self.sprites.append(pygame.image.load("images/card_side_view.png"))
        self.sprites.append(pygame.image.load("images/back_flat_mini_20.png"))
        self.sprites.append(pygame.image.load("images/back_flat_mini_36.png"))
        self.sprites.append(pygame.image.load("images/back_flat_mini_46.png"))
        self.sprites.append(pygame.image.load("images/back_flat_mini.png"))
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

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Blackjack")

animation_sprites = pygame.sprite.Group()
animation = Animation(100,100)
animation_sprites.add(animation)

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                animation.flip()

        WIN.fill((0,0,0))
        animation_sprites.draw(WIN)
        animation_sprites.update(0.25)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()