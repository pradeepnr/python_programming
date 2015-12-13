# template for "Stopwatch: The Game"
import simplegui
# define global variables
counter = 0
x = 0
y = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(counter_milli_secs):
    tenth_secs = counter_milli_secs % 10
    counter_secs = counter_milli_secs /10
    secs = counter_secs % 60
    mins = counter_secs / 60

    if(mins == 0):
        display_str = '00'
    elif(mins < 10):
        display_str = '0'+str(mins)
    else:
        display_str = str(mins)
        
    display_str = display_str + ':'
    
    if(secs == 0):
        display_str = display_str + '00'
    elif(secs < 10):
        display_str = display_str + '0' + str(secs)
    else:
        display_str = display_str + str(secs)
    
    
    display_str = display_str + '.'+str(tenth_secs)
    
    return display_str
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def handler_start():
    timer.start()

def handler_stop():
    global x
    global y
    if(timer.is_running()):
        y = y + 1
        if ((counter % 10) == 0):
            x = x + 1
    timer.stop()
    
    
def handler_reset():
    global counter
    global x
    global y
    x = 0
    y = 0
    timer.stop()
    counter = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    counter = counter + 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(counter),(70,70),20,'WHITE')
    reflex_str = str(x)+'/'+str(y)
    canvas.draw_text(reflex_str,(170,20),17,'WHITE')
    
# create frame
frame = simplegui.create_frame("stop watch", 200,150)

# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button("start",handler_start,75)
frame.add_button("stop",handler_stop,75)
frame.add_button("reset",handler_reset,75)

timer = simplegui.create_timer(100,timer_handler)

# start frame
print format(counter)
frame.start()

# Please remember to review the grading rubric
