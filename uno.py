import random

HANDSIZE = 2


# determines if card1 can be played on card2
def can_play(card1, card2, chosen_colour):
    if isinstance(card1, Wild):
        return True
    elif isinstance(card2, Wild):
        return card1.colour == chosen_colour
    elif card1.colour == card2.colour:
        return True
    elif type(card1)==type(card2):
        if type(card1) == NumberCard:
            return card1.value == card2.value
        else:
            return True
    return False

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

    def choose_colour(self, colour):
        self.colour = colour

    def chosen_colour(self):
        return self.colour

class WildPlus4(Wild):
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

    def take_card(self):
        card = self.cards.pop()
        return card

    def take_cards(self, n):
        cards = self.cards[:n]
        self.cards = self.cards[n:]
        return cards

# Create player class. 
# By default a player will play the first card they can
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def show(self):
        return self.name

    def show_hand(self):
        card_strs = []
        for card in self.hand:
            card_strs.append(card.show())
        return str(card_strs)
    
    def give_card(self, card):
        self.hand.append(card)

    def give_cards(self, cards):
        self.hand.extend(cards)

    def play_card(self, top_card, chosen_colour):
        # First get the cards that are possible to play
        for card in self.hand:
            if can_play(card, top_card, chosen_colour):
                self.hand.remove(card)
                return card
        # If it reaches here, then no card can be played.
        return None

    def choose_colour(self):
        return ["R", "Y", "G", "B"][random.randint(0,3)]

    def has_cards(self):
        return bool(self.hand)


class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.pile = []
        self.num_players = len(players)
        self.players = players
        self.turn = 0
        self.direction = 1   #direction changes to -1 when reverse is placyed.
        self.chosen_colour = None
        self.winner = None

    def deal_cards(self):
        for player in self.players:
            cards = self.deck.take_cards(HANDSIZE)
            player.give_cards(cards)
        (self.pile).append(self.deck.take_card())

    def print(self):
        print("Top card: " + (self.pile[-1]).show())
        for player in self.players:
            print(player.name + ": " + player.show_hand())

    def next_turn(self):
        next_player = self.players[self.turn]
        input("Next player is " + next_player.show())
        top_card = self.pile[-1]

        # The player gets to play a card.
        next_card = next_player.play_card(top_card, self.chosen_colour)
        if next_card == None:
            # Player has no cards to play
            input(next_player.show() + " has no cards to play.")
            next_player.give_card(self.deck.take_card())
            self.turn = (self.turn + self.direction) % self.num_players
            return

        input(next_player.show() + " played " + next_card.show())


        # If a wild is played the player needs to choose a colour
        if isinstance(next_card, Wild):
            self.chosen_colour = next_player.choose_colour()
            input(next_player.show() + " chooses " + self.chosen_colour + ".")

        # Determine who plays the next turn
        if isinstance(next_card, Reverse):
            self.direction *= -1 
            self.turn = (self.turn + self.direction) % self.num_players
        if isinstance(next_card, Skip):
            self.turn = (self.turn + 2*self.direction) % self.num_players
        else:
            self.turn = (self.turn + self.direction) % self.num_players

        self.pile.append(next_card)

        # See if the player has played their last card
        if not next_player.has_cards():
            self.winner = next_player
            return

        # See if next player needs to pick up cards. If they pick up
        # then their turn is skipped.
        next_player = self.players[self.turn]
        if isinstance(next_card, Plus2):
            input(next_player.show() + " picks up two cards.") 
            next_player.give_cards(self.deck.take_cards(2)) 
            self.turn = (self.turn + self.direction) % self.num_players
        elif isinstance(next_card, WildPlus4):
            input(next_player.show() + " picks up four cards.") 
            next_player.give_cards(self.deck.take_cards(4)) 
            self.turn = (self.turn + self.direction) % self.num_players

    def show_top_card(self):
        return (self.pile)[-1].show()


class Human(Player):
    def __init__(self):
        self.name = input("What is your name? ")
        self.hand = []

    def play_card(self, top_card, chosen_colour):
        
        print(self.name + ": your cards are: ")
        input(self.show_hand())
        # Get playable cards
        playable_cards = []
        for card in self.hand:
            if can_play(card, top_card, chosen_colour):
                playable_cards.append(card)

        if playable_cards == []:
            # Don't have any cards to play
            input(self.name + ": You can't play any cards.")
            return None

        # Choose a card to play
        print(self.name + ": You can play the following:")
        for i in range(len(playable_cards)):
            print(str(i) + ": " + playable_cards[i].show())
        chosen_card = -1
        while chosen_card not in range(len(playable_cards)):
            chosen_card = int(input("Which card do you want to play? "))

        self.hand.remove(playable_cards[chosen_card])

        return playable_cards[chosen_card]


# START THE GAME

print("Welcome to uno!")
num_players = 2
human = Human()
computer = Player("Computer")
players = [human, computer]

game = Game(players)
game.deal_cards()
game.print()
while(game.winner == None):
    game.next_turn()
    #game.print()

print(game.winner.show() + " is the winner!")
