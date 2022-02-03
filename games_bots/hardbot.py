from random import choice


class HardBot():
    # Сложный бот
    def __init__(self):
        self.place_occupied = []
        self.deck = []
        self.inventory_bot = []
        self.bot_cards = []

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
            if self.deck and len(self.inventory_bot) < 6:
                self.new_card = choice(self.deck)
                del self.deck[self.deck.index(self.new_card)]
                dm = self.new_card[0] * 2
                hp = self.new_card[1] * 2
                if dm > 9:
                    dm = 9
                if hp > 9:
                    hp = 9
                self.inventory_bot.append((dm, hp, self.new_card[2]))
            if self.inventory_bot and len(self.place_occupied) < 4:
                if self.new_laid_card[0] >= 3:
                    self.inventory_bot.sort(key=lambda x: (x[1], x[0]))
                    self.card = self.inventory_bot[-1]
                elif self.new_laid_card[1] >= 3:
                    self.inventory_bot.sort(key=lambda x: (x[0], x[1]))
                    self.card = self.inventory_bot[-1]
                else:
                    self.card = choice(self.inventory_bot)
                del self.inventory_bot[self.inventory_bot.index(self.card)]
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
