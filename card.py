import pygame

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

    def toggle_flip(self):
        self.fliping = True

    def toggle_movement(self):
        self.moving = True

    def update(self,hand:Hand):

        if self.animating:

            if not self.face_up:
                self.image = self.sprites[int(self.current_sprite)]
                self.current_sprite += 0.25

                if self.current_sprite > len(self.sprites) - 1:
                    self.current_sprite = len(self.sprites) - 1 
                    self.face_up = True
                    self.animating = False

            else:
                self.image = self.sprites[int(self.current_sprite)]
                self.current_sprite -= 0.25

                if self.current_sprite < 0:
                    self.current_sprite = 0
                    self.face_up = False
                    self.animating = False
        
        if self.moving:
            pass

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