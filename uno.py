import random

# Create object for a single card. 
class Card:
    pass

class ColourCard(Card):
    def __init__(self, colour):
        self.colour = colour

    def colour():
        return self.colour

class NumberCard(ColourCard):
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value

    def show(self):
        return "(" + self.colour + ", " + str(self.value) + ")"

    def value(self):
        return self.value

class Reverse(ColourCard):
    def show(self):
        return "(" + self.colour + ", R)"

class Skip(ColourCard):
    def show(self):
        return "(" + self.colour + ", S)"

class Plus2(ColourCard):
    def show(self):
        return "(" + self.colour + ", +2)"

class Wild(Card):
    def show(self):
        return "Wild"

class WildPlus4(Card):
    def show(self):
        return "Wild+4"


class Deck:

    cards = []

    def __init__(self):
        
        colours = ["R", "Y", "B", "G"]

        for colour in colours:

            # add plus 2 cards, coloured special cards
            for i in range(2):
                (self.cards).append(Reverse(colour))
                (self.cards).append(Skip(colour))
                (self.cards).append(Plus2(colour))

            # add standard cards
            for value in range(10):
                (self.cards).append(NumberCard(colour, value))
                if value != 0:
                    (self.cards).append(NumberCard(colour, value))

        # add wild cards
        for i in range(4):
            (self.cards).append(Wild())
            (self.cards).append(WildPlus4())

        random.shuffle(self.cards)
    
    def show(self):
        out = []
        for card in self.cards:
            out.append(card.show())
        return out

    def size(self):
        return len(self.cards)



deck = Deck()
print(deck.show())
print(deck.size())
