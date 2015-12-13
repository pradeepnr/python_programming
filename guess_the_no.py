# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random


# initialize global variables used in your code
secret_num = 0
no_of_guess = 0
total_guess = 0
range_100 = 1

# helper function to start and restart the game
def new_game():
    # remove this when you add your code
    global secret_num
    global no_of_guess
    global total_guess
    
    no_of_guess = 0
    if range_100:
        secret_num = random.randrange(0, 100)
        total_guess = 7
        print "New Game : Guess the number [0,100]"
    else:
        secret_num = random.randrange(0,1000)
        total_guess = 9
        print "New Game : Guess the number [0,1000]"
    
    print ""



# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global secret_num
    global total_guess
    global range_100
    
    range_100 = 1
    
    new_game()
    # remove this when you add your code    


def range1000():
    # button that changes range to range [0,1000) and restarts
    global secret_num
    global total_guess
    global range_100
    
    range_100 = 0
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global total_guess
    global secret_num
    global no_of_guess
    
    if (no_of_guess >= total_guess):
        print "Number was ",secret_num
        print "game over restart"
        new_game()
        return
    
    guess_int = int(guess)
    if (range100 and (guess_int < 0 or guess_int > 100)):
        print "Guess between [0,100]"
        return
    elif (range1000 and (guess_int < 0 or guess_int > 1000)):
        print "Guess between [0,1000]"
        return
    
    no_of_guess += 1
    print "guessed no ",guess_int
    if (guess_int == secret_num):
        print "Guess correct"
        print "total guess count ",no_of_guess,"\n"
        new_game()
    elif (guess_int > secret_num):
        print "less than that"
        print "no of guess = ",no_of_guess,"\n"
    else:
        print "more than that"
        print "no of guess = ",no_of_guess,"\n"


    
# create frame
frame = simplegui.create_frame("guess num",300,300)


# register event handlers for control elements
frame.add_input('guess',input_guess,85)
frame.add_button("range 100",range100,85)
frame.add_button("range 1000",range1000,85)
frame.add_button("new game",new_game,85)

# call new_game and start frame
new_game()
frame.start()


# always remember to check your completed program against the grading rubric
