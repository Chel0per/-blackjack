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
        self.animation_queue = []
        self.delay_time = 0
        self.delay_target = 0
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
        self.float_top = 60
        self.float_left = 640
        self.x_speed = 0
        self.y_speed = 0

    def set_delay(self,delay:int):
        self.delay_target += delay
    
    def toggle_flip(self):
        self.fliping = True

    def toggle_movement(self,left:int,top:int,time:int):
        self.top_destination = top
        self.float_top = self.rect.top
        self.y_speed = (self.top_destination - self.rect.top)/time
        self.left_destination = left
        self.float_left = self.rect.left
        self.x_speed = (self.left_destination - self.rect.left)/time

    def add_delayed_animation(self,pos_x,pos_y,time,delay):
        self.animation_queue.insert(0,Animation(pos_x,pos_y,time,delay))

    def update(self):

        if self.delay_target != self.delay_time:
            self.delay_time += 1
        else:
            self.delay_target = 0
            self.delay_time = 0
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
                        self.fliping = False
            

            if self.rect.top != self.top_destination:   
                self.float_top += self.y_speed
                self.rect.top = round(self.float_top)

            if self.rect.left != self.left_destination:
                self.float_left += self.x_speed
                self.rect.left = round(self.float_left)
            else:
                if self.animation_queue:
                    if not self.face_up:
                        self.fliping = True
                    animation = self.animation_queue.pop()
                    self.set_delay(animation.delay)
                    self.toggle_movement(animation.pos_x,animation.pos_y,animation.time)                     

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

class Animation:

    def __init__(self,pos_x,pos_y,time,delay):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.time = time
        self.delay = delay

class CardStack(pygame.sprite.Sprite):

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

    def add_card(self,card:Card):
        if len(self.cards) == 0:
            self.image = self.back_image
        self.cards.append(card)

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

    def empty(self):
        self.cards = []
        self.value = 0
        self.busted = False

    def can_change_value(self) -> bool:
        can_change_list = [card for card in self.cards if card.can_change_value]
        return len(can_change_list) > 0
    
    def rearrange_dealer_hand(self):
        n = len(self.cards)
        pos_x = 400 - (n*50 + (n - 1)*4)/2
        for i in range(n):
            if i != n - 1:
                self.cards[i].add_delayed_animation(pos_x,100,40,0)
            else:
                self.cards[i].add_delayed_animation(pos_x,100,40,(n - 3)*40)
            pos_x += 54

class Button(pygame.sprite.Sprite):
    def __init__(self,pos_x:int,pos_y:int,content:str,group:pygame.sprite.Group,game:Game):
        super().__init__()
        self.game = game
        self.enabled = False
        self.to_enable = False
        self.to_end_busted_round = False
        self.to_start_round = False
        self.to_stand = False
        self.skip_next_instruction = False
        self.content = content
        self.delay_time = 0
        self.delay_target = 0
        self.empty_image = pygame.image.load("images/Buttons/empty_button.png")
        self.unhovered_image = pygame.image.load(f"images/Buttons/{self.content}_button.png")
        self.hovered_image = pygame.image.load(f"images/Buttons/{self.content}_button_hovered.png")
        self.image = self.empty_image
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        self.delay_time = 0
        self.delay_target = 0
        self.group = group
        self.group.add(self)
    
    def enable(self,delay:int):
        self.to_enable = True
        self.add_delay(delay)

    def add_delay(self,delay:int):
        self.delay_target += delay

    def disable(self):
        self.enabled = False
        self.image = self.empty_image

    def update(self):
        mouse_pos = pygame.mouse.get_pos()           
        if self.delay_target != self.delay_time:
            self.delay_time += 1
        else:
            self.delay_target = 0
            self.delay_time = 0

            if self.to_enable:
                self.enabled = True
                self.image = self.unhovered_image
                self.to_enable = False

            if self.to_start_round:
                card_sprites.empty()
                self.game.start_round()
                self.to_start_round = False

            if self.to_stand:
                self.add_delay(self.game.stand() + 120)
                self.to_end_busted_round = True
                self.to_stand = False
                self.skip_next_instruction = True
                
            if self.to_end_busted_round and not self.skip_next_instruction:
                self.to_end_busted_round = False
                self.game.end_round("busted")
                self.add_delay(40)
                self.to_start_round = True
                player_hand_value.add_changes(
                    [{
                        "type":"text",
                        "value":"",
                        "delay":0
                    },
                    {
                        "type":"color",
                        "value":(255,255,255),
                        "delay":0
                    }]
                )
                dealer_hand_value.add_changes(
                    [{
                        "type":"text",
                        "value":"",
                        "delay":0
                    },
                    {
                        "type":"color",
                        "value":(255,255,255),
                        "delay":0
                    }]
                ) 
            elif self.skip_next_instruction:
                self.skip_next_instruction = False

            if self.rect.collidepoint(mouse_pos):
                if self.enabled:
                    self.image = self.hovered_image
                    if pygame.mouse.get_pressed()[0] == 1 and self.content == "hit":
                        for sprite in self.group:
                            sprite.disable()
                        game.hit()
                        if game.player_hand.value < 21:
                            self.group.sprites()[0].enable(40)
                            self.group.sprites()[1].enable(40)
                            self.group.sprites()[2].enable(40)
                        else:
                            self.add_delay(120)                  
                            self.to_end_busted_round = True
                    elif pygame.mouse.get_pressed()[0] == 1 and self.content == "stand":
                        for sprite in self.group:
                            sprite.disable()
                        self.game.dealer_hand.cards[1].toggle_flip()
                        self.add_delay(40)
                        self.to_stand = True

            else:
                if self.enabled:
                    self.image = self.unhovered_image

class Display(pygame.sprite.Sprite):

    def __init__(self,text,font,color,pos_x,pos_y):
        super().__init__()
        self.delay_time = 0
        self.delay_target = 0
        self.to_change = False
        self.change_queue = []
        self.text = text
        self.font = font
        self.color = color
        self.img = font.render(text,True,color)
        self.pos_x = pos_x
        self.pos_y = pos_y
           
    def update(self):
        WIN.blit(self.img,(self.pos_x,self.pos_y))
        if self.delay_time != self.delay_target:
            self.delay_time += 1
        else:
            if self.change_queue:
                changes = self.change_queue.pop()
                for change in changes:
                    match change["type"]:
                        case "text":
                            self.change_text(change["value"])
                            self.add_delay(change["delay"])
                        case "color":
                            self.change_color(change["value"])
                            self.add_delay(change["delay"])

    def change_text(self,new_text):
        self.text = new_text
        self.img = self.font.render(self.text,True,self.color)

    def change_color(self,new_color):
        self.color = new_color
        self.img = self.font.render(self.text,True,self.color)

    def change_position(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def add_delay(self,delay:int):
        self.delay_target += delay

    def add_changes(self,changes):
        self.change_queue.insert(0,changes)

class Game:
    def __init__(self,player_hand:Hand,dealer_hand:Hand,game_stack:CardStack,discard_stack:CardStack):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.game_stack = game_stack
        self.discard_stack = discard_stack

        self.game_stack.add_pack()
        self.game_stack.add_pack()
        self.game_stack.add_pack()
        self.game_stack.add_pack()
        self.game_stack.shuffle()

    def start_round(self):
        card1 = self.game_stack.draw_card()
        card_sprites.add(card1)
        card1.toggle_flip()
        card1.toggle_movement(375 + 18*len(self.player_hand.cards),460 - 20*len(self.player_hand.cards),40)
        self.player_hand.add_card(card1)
        player_hand_value.add_delay(40)
        player_hand_value.add_changes(
            [{
                "type":"text",
                "value":str(card1.blackjack_value),
                "delay":40
            }]
        )

        card2 = self.game_stack.draw_card()
        card_sprites.add(card2)
        card2.set_delay(20)
        card2.toggle_flip()
        card2.toggle_movement(348,100,40)
        self.dealer_hand.add_card(card2)
        dealer_hand_value.add_delay(60)
        dealer_hand_value.add_changes(
            [{
                "type":"text",
                "value":str(card2.blackjack_value),
                "delay":0
            }]
        )

        card3 = self.game_stack.draw_card()
        card_sprites.add(card3)
        card3.set_delay(40)
        card3.toggle_flip()
        card3.toggle_movement(375 + 18*len(self.player_hand.cards),460 - 20*len(self.player_hand.cards),40)
        self.player_hand.add_card(card3)
        player_hand_value.add_changes(
            [{
                "type":"text",
                "value":str(self.player_hand.value),
                "delay":0
            }]
        )

        card4 = self.game_stack.draw_card()
        card_sprites.add(card4)
        card4.set_delay(60)
        card4.toggle_movement(402,100,40)
        self.dealer_hand.add_card(card4)

        if game.player_hand.value < 21:
            hit_button.enable(100)
            stand_button.enable(100)
            double_button.enable(100)
        else:
            hit_button.to_end_busted_round = True
            hit_button.skip_next_instruction = True
            hit_button.add_delay(220) 
     
        if game.player_hand.cards[0].blackjack_value == game.player_hand.cards[1].blackjack_value:
            split_button.enable(100)

    def hit(self):
        card = self.game_stack.draw_card() 
        card_sprites.add(card)
        card.toggle_flip()
        card.toggle_movement(375 + 18*len(self.player_hand.cards),460 - 20*len(self.player_hand.cards),40)
        self.player_hand.add_card(card)
        player_hand_value.add_delay(40)
        changes = [{"type":"text","value":str(self.player_hand.value),"delay":0}]
        if self.player_hand.value > 21:
            changes.append(
                {
                    "type":"color",
                    "value":(255,0,0),
                    "delay":0
                }
            )
        player_hand_value.add_changes(changes)

    def stand(self) -> int:
        card_delay = 0
        if self.dealer_hand.value < 17 or (self.dealer_hand.value == 17 and self.dealer_hand.can_change_value()):
            dealer_hand_value.add_changes([{"type":"text","value":str(self.dealer_hand.value),"delay":40}])
        else:
            dealer_hand_value.add_changes([{"type":"text","value":str(self.dealer_hand.value),"delay":0}])
                
        while self.dealer_hand.value < 17 or (self.dealer_hand.value == 17 and self.dealer_hand.can_change_value()):
            card = self.game_stack.draw_card()
            card_sprites.add(card)
            self.dealer_hand.add_card(card)
            if self.dealer_hand.value < 17 or (self.dealer_hand.value == 17 and self.dealer_hand.can_change_value()):
                changes = [{"type":"text","value":str(self.dealer_hand.value),"delay":40}]
            else:
                changes = [{"type":"text","value":str(self.dealer_hand.value),"delay":0}]
                if self.dealer_hand.value > 21:
                    changes.append({"type":"color","value":(255,0,0),"delay":0})
            dealer_hand_value.add_changes(changes)          
            self.dealer_hand.rearrange_dealer_hand()
            card_delay += 40

        return card_delay        

    def end_round(self,state:str):
        match state:
            case "busted":
                for card in self.player_hand.cards:
                    card.toggle_flip()
                    card.toggle_movement(110,60,40)
                    if card.value == "Ace":
                        card.blackjack_value = 11
                        card.can_change_value = True
                    self.discard_stack.add_card(card)

                self.player_hand.empty()

                for card in self.dealer_hand.cards:
                    if card.face_up:
                        card.toggle_flip()
                    card.toggle_movement(110,60,40)
                    if card.value == "Ace":
                        card.blackjack_value = 11
                        card.can_change_value = True
                    self.discard_stack.add_card(card)

                self.dealer_hand.empty()

pygame.init()

WIDTH = 800
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Blackjack")

background = pygame.image.load("images/GeneralDesign/table.png")

card_sprites = pygame.sprite.Group()

player_hand_value = Display("",pygame.font.SysFont("Arial",24),(255,255,255),390,545)
dealer_hand_value = Display("",pygame.font.SysFont("Arial",24),(255,255,255),390,60)

display_sprites = pygame.sprite.Group()
display_sprites.add(dealer_hand_value)
display_sprites.add(player_hand_value)

game_stack = CardStack(640,60)
discard_stack = CardStack(110,60)
stack_sprites = pygame.sprite.Group()
stack_sprites.add(game_stack)
stack_sprites.add(discard_stack)

player_hand = Hand()
dealer_hand = Hand()

game = Game(player_hand,dealer_hand,game_stack,discard_stack)

button_sprites = pygame.sprite.Group()
hit_button = Button(485,470,"hit",button_sprites,game)
stand_button = Button(237,470,"stand",button_sprites,game)
double_button = Button(485,511,"double",button_sprites,game)
split_button = Button(237,511,"split",button_sprites,game)

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                game.start_round()

        WIN.blit(background, (0, 0))
        stack_sprites.draw(WIN)
        card_sprites.draw(WIN)
        button_sprites.draw(WIN)
        button_sprites.update()
        card_sprites.update()
        display_sprites.update()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()