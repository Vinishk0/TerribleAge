from random import choice

inventory_bot = [(6, 2, 'card_1_1'), (2, 5, 'card_1_2'), (5, 2, 'card_1_3'), (1, 3, 'card_1_4'), (3, 2, 'card_1_5')]
bot_cards = []


class NormalBot():
    def __init__(self):
        self.place_occupied = []
        self.deck = []

    def return_func(self, deck, new_laid_place, new_laid_card):
        self.deck = deck
        self.new_laid_place = new_laid_place
        self.new_laid_card = new_laid_card
        self.choice_card()
        self.choice_place()
        card = self.card
        self.card = []
        return card, self.place, self.deck

    def choice_card(self, delete=None):
        if delete == None:
            if self.deck and len(inventory_bot) < 6:
                self.new_card = choice(self.deck)
                del self.deck[self.deck.index(self.new_card)]
                inventory_bot.append(self.new_card)
            if inventory_bot and len(self.place_occupied) < 4:
                if self.new_laid_card[0] >= 3:
                    inventory_bot.sort(key=lambda x: (x[1], x[0]))
                    self.card = inventory_bot[-1]
                elif self.new_laid_card[1] >= 3:
                    inventory_bot.sort(key=lambda x: (x[0], x[1]))
                    self.card = inventory_bot[-1]
                else:
                    self.card = choice(inventory_bot)
                    del inventory_bot[inventory_bot.index(self.card)]
            else:
                self.card = None
        else:
            del self.place_occupied[delete]

    def choice_place(self):
        if self.new_laid_place not in self.place_occupied:
            self.place = self.new_laid_place
            self.place_occupied.append(self.place)
        else:
            breakk = False
            for i in range(4):
                if i not in self.place_occupied:
                    self.place_occupied.append(i)
                    self.place = i
                    breakk = True
                    break
            if not breakk:
                self.place = None
