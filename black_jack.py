# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
dealer = 0
player = 0
deck = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []


    def __str__(self):
        # return a string representation of a hand
        n = len(self.hand)
        str_val = "Hand contains "
        i = 0
        while i < n:
            str_val += str(self.hand[i])
            str_val = str_val + " "
            i += 1
        return str_val

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        n = len(self.hand)
        i = 0
        ace_count = 0
        while i < n:
            value += VALUES[self.hand[i].get_rank()]
            if self.hand[i].get_rank() == 'A':
                ace_count += 1
            i += 1
        
        for n in range(ace_count):
            if value + 10 < 21:
                value += 10
        return value
        
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        n = len(self.hand)
        i = 0
        while i < n and i < 5:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.hand[i].get_rank()), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.hand[i].get_suit()))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [i * CARD_SIZE[0] + pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            i +=1

 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []

        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck.append(Card(SUITS[i],RANKS[j]))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        if len(self.deck) > 0:
            return self.deck.pop(len(self.deck) - 1)
    
    def __str__(self):
        # return a string representing the deck
        n = len(self.deck)
        str_val = "DECK contains "
        i = 0
        while i < n:
            str_val += str(self.deck[i])
            str_val = str_val + " "
            i += 1
        return str_val



#define event handlers for buttons
def deal():
    global outcome, in_play
    global dealer, player, deck
    # your code goes here
    deck = Deck()
    dealer = Hand()
    player = Hand()
    deck.shuffle()
    outcome = ""
    
    player. add_card(deck.deal_card())
    dealer. add_card(deck.deal_card())
    player. add_card(deck.deal_card())
    dealer. add_card(deck.deal_card())
    
    print "Player's Hand" 
    print "    " + str(player)
    print ""
    print "Dealer's Hand"
    print "    " + str(dealer)
    
    in_play = True

def hit():
    global in_play, outcome, score
    # replace with your code below
    
    # if the hand is in play, hit the player
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
    else:
        outcome = "Player is bursted"
        print outcome
        in_play = False
        score -=1
        print "score =" + str(score)
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global score, in_play, outcome
    # replace with your code below
    if player.get_value() > 21:
        outcome = "Player is bursted"
        score -=1
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
    if dealer.get_value() > 21:
        outcome = "Dealer is bursted"
        score +=1
    if player.get_value() <= dealer.get_value():
        outcome = "Dealer Wins"
        score -=1
    else:
        outcome = "Player Wins"
        score +=1
    in_play = False
    
    print outcome
    print "score =" + str(score)
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    canvas.draw_text("Blackjack", [100, 40], 30, 'Black')
    canvas.draw_text("Score " +str(score), [300,40],25,'Black')
    
    canvas.draw_text("Dealer", [100,100], 25,'Black')
    dealer.draw(canvas,[100,120])
    
    canvas.draw_text("Player", [100,280], 25,'Black')
    player.draw(canvas,[100,300])
    
    canvas.draw_text(outcome, [100, 250], 25, 'Black')
    if in_play == True:
        canvas.draw_text("Hit or Stand?",[250,280],25,'Black')
    else:
        canvas.draw_text("New Deal?",[250,280],25,'Black')
    #Score

    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric