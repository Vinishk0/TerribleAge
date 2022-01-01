from random import choice

inventory_bot = []
bot_cards = []


class EasyBot():
    def __init__(self):
        self.place_occupied = []
        self.deck = []

    def return_func(self, deck):
        self.deck = deck
        self.choice_card()
        self.choice_place()
        card = self.card
        self.card = []
        return card, self.place, self.deck

    def choice_card(self):
        if self.deck and len(inventory_bot) < 6:
            self.new_card = choice(self.deck)
            del self.deck[self.deck.index(self.new_card)]
            inventory_bot.append(self.new_card)
        if inventory_bot:
            self.card = choice(inventory_bot)
            del inventory_bot[inventory_bot.index(self.card)]
        else:
            self.card = None

    def choice_place(self):
        breakk = False
        for i in range(4):
            if i not in self.place_occupied:
                self.place_occupied.append(i)
                self.place = i
                breakk = True
                break
        if not breakk:
            self.place = None

