from typing import Any
import pygame

class Animation(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.animating = False
        self.repeat = 0
        self.sprites = []
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_0.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_1.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_2.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_3.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_5.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_6.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_7.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_8.png"))
        self.sprites.append(pygame.image.load("images/GeneralDesign/shuffle_animation_0.png")) 
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [640,60]

    def update(self):
        if self.animating:
            self.image = self.sprites[int(self.current_sprite)]
            self.current_sprite += 0.25
            if self.current_sprite > len(self.sprites) - 1:
                if self.repeat > 0:
                    self.repeat -= 1
                    self.current_sprite = 0
                else:
                    self.current_sprite = 0
                    self.animating = False

    def animate(self,repeat:int):
        self.animating = True
        self.repeat = repeat

pygame.init()

WIDTH = 800
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Blackjack")

background = pygame.image.load("images/GeneralDesign/table.png")

animation = Animation()
animation_sprites = pygame.sprite.Group()
animation_sprites.add(animation)

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                animation.animate(2)

        WIN.blit(background, (0, 0))
        animation_sprites.draw(WIN)
        animation_sprites.update()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

main()