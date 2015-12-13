# implementation of card game - Memory

import simplegui
import random

list1 = range(1,9)
list2 = range(1,9)
list3 = []
exposed = []
state = 0
card1 = -1
card2 = -1
counter = 0
label = 0


# helper function to initialize globals
def new_game():
    global list3, exposed, counter, state
    random.shuffle(list1)
    random.shuffle(list2)
    list3 = list1 + list2
    state = 0
    for i in range(len(list3)):
        exposed.append(False)
    counter = 0
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global card1, card2, state, counter
    clicked_card = pos[0] / 50
    if exposed[clicked_card] == False:
        if state == 0 or state == 2:
           state = 1
           card1 = clicked_card
        elif state == 1:
            state = 2
            card2 = clicked_card
            counter += 1
    
    label.set_text("Turns = " + str(counter))
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    width = 50
    height = 100
    for x in range(len(list3)):
        if not exposed[x]:
            canvas.draw_polygon( [(x * width,0) ,(x * width + width, 0),(x * width + width, height),(x * width,height)],3,'Black','Green')
    
    for y in range(len(list3)):
        if exposed[y]:
            canvas.draw_polygon( [(y * width,0) ,(y * width + width, 0),(y * width + width, height),(y * width,height)],3,'Green','Black')
            canvas.draw_text(str(list3[y]),(y * width + 15 , 60),26,'White')
            
            
    
    if state == 2:
        canvas.draw_polygon( [(card1 * width,0) ,(card1 * width + width, 0),(card1 * width + width, height),(card1 * width,height)],3,'Green','Black')
        canvas.draw_polygon( [(card2 * width,0) ,(card2 * width + width, 0),(card2 * width + width, height),(card2 * width,height)],3,'Green','Black')
        canvas.draw_text(str(list3[card1]),(card1 * width + 15 , 60),26,'White')
        canvas.draw_text(str(list3[card2]),(card2 * width + 15 , 60),26,'White')
        if(list3[card1] == list3[card2]):
            exposed[card1] = exposed[card2] = True
        
    elif state == 1:
        canvas.draw_polygon( [(card1 * width,0) ,(card1 * width + width, 0),(card1 * width + width, height),(card1 * width,height)],3,'Green','Black')
        canvas.draw_text(str(list3[card1]),(card1 * width + 15 , 60),26,'White')
    
    



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()




# Always remember to review the grading rubric