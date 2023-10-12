class Hand:
    def __init__(self):
        self.cards = [Card]
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

