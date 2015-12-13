# Rock-paper-scissors-lizard-Spock template

import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    # fill in your code below
    number = number % 5
    if (number == 0):
        return "rock"
    elif (number == 1):
        return "Spock"
    elif (number == 2):
        return "paper"
    elif (number == 3):
        return "lizard"
    elif(number == 4):
        return "scissors"
    else:
        return "Impossible"
    # convert number to a name using if/elif/else
    # don't forget to return the result!

    
def name_to_number(name):
    # fill in your code below
    if (name == "rock"):
        return 0
    elif (name == "Spock"):
        return 1
    elif (name == "paper"):
        return 2
    elif (name == "lizard"):
        return 3
    elif (name == "scissors"):
        return 4
    else:
        return "Error"
    # convert name to number using if/elif/else
    # don't forget to return the result!


def rpsls(name): 
    # fill in your code below

    # convert name to player_number using name_to_number
    player_num = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    computer_num = random.randrange(1,100) % 5
    # compute difference of player_number and comp_number modulo five
    diff = ( player_num - computer_num )
    # use if/elif/else to determine winner
    #var winner
    #if diff == -4 or diff == -3 or diff == 1 or diff == 2:
    if (computer_num - player_num) % 5 <= 2:
        winner = player_num
    else:
        winner = computer_num
    # convert comp_number to name using number_to_name
    computer_name = number_to_name(computer_num)
    # print results
    print "player chooses " + name
    print "computer chooses " + computer_name
    if computer_num == player_num:
        print "Player and computer tie!"
    elif winner == computer_num:
        print "computer wins"
    else:
        print "player wins"
    print "\n"
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


