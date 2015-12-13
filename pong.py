# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

player1_points = 0
player2_points = 0

paddle1_pos = 200
paddle2_pos = 80
paddle1_vel = 0
paddle2_vel = 0

ball_pos = [WIDTH / 2,HEIGHT / 2]
ball_vel = [1,1]
player1_press = 0
player2_press = 0



# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if(direction == 'LEFT'):
        ball_vel[0] = -1 * (random.randrange(120, 240) / 60)
        ball_vel[1] = -1 * (random.randrange(60, 180) / 60)
    else:
        ball_vel[0] = +1 * (random.randrange(120, 240) / 60)
        ball_vel[1] = -1 * (random.randrange(60, 180) / 60)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global counter
    global player1_points, player2_points
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    spawn_ball('LEFT')
    player1_points = 0
    player2_points = 0
    
def timer_handler():
    global player1_press, player2_press
    global paddle1_vel, paddle2_vel
    
    if(player1_press == 1 or player1_press == -1):
        paddle1_vel = paddle1_vel + player1_press
    if(player2_press == 1 or player2_press == -1):
        paddle2_vel = paddle2_vel + player2_press
    
   
    
def collision_detection():
    global ball_vel
    global player1_points, player2_points
    
    if(ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH):
        if(ball_pos[1] <= paddle2_pos and ball_pos[1] >= paddle2_pos - PAD_HEIGHT):
            print "hit right paddle"
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] + ball_vel[0] / 10
        else:
            print "miss right paddle"
            player1_points = player1_points + 1
            spawn_ball('LEFT')
    
    elif(ball_pos[0] - BALL_RADIUS <= PAD_WIDTH):
        if( (ball_pos[1] <= paddle1_pos) and (ball_pos[1] >= paddle1_pos - PAD_HEIGHT)):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] + ball_vel[0] / 10
            print "hit left paddle"
        else:
            spawn_ball('RIGHT')
            player2_points = player2_points + 1
            print "miss left paddle"
    
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    

    collision_detection()
    
    #vertical collision test and modify  
    if((ball_pos[1] + BALL_RADIUS >= HEIGHT) or (ball_pos[1] - BALL_RADIUS <= 0)):
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    c.draw_circle(ball_pos ,BALL_RADIUS, 1,"White","White")
    

    # update paddle's vertical position, keep paddle on the screen
    if(paddle1_pos + paddle1_vel >= PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT):
        paddle1_pos = paddle1_pos + paddle1_vel
    if(paddle2_pos + paddle2_vel >= PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT):
        paddle2_pos = paddle2_pos + paddle2_vel
    
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos],[HALF_PAD_WIDTH,
                                          paddle1_pos - PAD_HEIGHT],PAD_WIDTH ,"White")
    c.draw_line([WIDTH - HALF_PAD_WIDTH , paddle2_pos],[WIDTH - HALF_PAD_WIDTH, 
                                          paddle2_pos - PAD_HEIGHT],PAD_WIDTH ,"White")
    
    # draw scores
    c.draw_text(str(player1_points), (150, 50), 30, 'White')
    c.draw_text(str(player2_points), (450, 50), 30, 'White')
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    global player1_press, player2_press
    if(int(key) == 87):
        paddle1_vel = -1
        player1_press  = -1
    elif(int(key) == 83):
        paddle1_vel = +1
        player1_press = 1
    elif(int(key) == 38):
        paddle2_vel = -1
        player2_press = -1
    elif(int(key) == 40):
        paddle2_vel = +1
        player2_press = 1
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    global player1_press, player2_press
    if(int(key) == 87):
        paddle1_vel = 0
        player1_press = 0
    elif(int(key) == 83):
        paddle1_vel = 0
        player1_press = 0
    elif(int(key) == 38):
        paddle2_vel = 0
        player2_press = 0
    elif(int(key) == 40):
        paddle2_vel = 0
        player2_press = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button('reset', new_game,75)

timer = simplegui.create_timer(100,timer_handler)



# start frame
new_game()
frame.start()
timer.start()
