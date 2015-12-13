# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
time1 = 0
started = False
MAX_ROCK = 12

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 150)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos [0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos [1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle = self.angle + self.angle_vel
        fwd_vector = angle_to_vector(self.angle)
        if(self.thrust):
            self.vel[0] = self.vel[0] + fwd_vector[0] * 1.1
            self.vel[1] = self.vel[1] + fwd_vector[1] * 1.1
        #friction
        self.vel[0] = self.vel[0] * .9
        self.vel[1] = self.vel[1] * .9        
    
    def update_angle_velocity(self,sign):
        if(sign > 0):
            self.angle_vel = self.angle_vel + math.radians(3)
        else:
            self.angle_vel = self.angle_vel - math.radians(3)

    def update_thrust(self, thrust):
        self.thrust = thrust
        if(self.thrust):
            self.image_center[0] = self.image_center[0] + self.image_size[0]
            ship_thrust_sound.play()
        else:
            self.image_center[0] = self.image_center[0] - self.image_size[0]
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global missile_group
        pos = [0,0]
        fwd_vector = angle_to_vector(self.angle)
        pos[0] = self.pos[0] + fwd_vector[0] * ship_info.get_radius()
        pos[1] = self.pos[1] + fwd_vector[1] * ship_info.get_radius()
        vel = [0,0]
        vel[0] = self.vel[0] + fwd_vector[0] * 6
        vel[1] = self.vel[1] + fwd_vector[1] * 6
        
        missile_group.add(Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound))
            
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
         
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        global time
        img_index = (self.age % self.lifespan) // 1
        img_center = self.image_center
        if self.animated:
            img_center = [self.image_center[0] + img_index * self.image_size[0],self.image_center[1]]
        canvas.draw_image(self.image, img_center, self.image_size, self.pos, self.image_size, self.angle)
        
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) # % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) #% HEIGHT
        self.angle = self.angle + math.radians(self.angle_vel)
        self.age +=1
        
        if self.age > self.lifespan:
            return True
        else:
            return False
        
    def collide(self, other_obj):
        obj1_pos = self.get_position()
        obj2_pos = other_obj.get_position()
        sq_x = (obj1_pos[0]-obj2_pos[0]) * (obj1_pos[0]-obj2_pos[0])
        sq_y = (obj1_pos[1]-obj2_pos[1]) * (obj1_pos[1]-obj2_pos[1])
        dis_btw = math.sqrt(sq_x + sq_y)
        
        if dis_btw > (self.get_radius() + other_obj.get_radius()):
           return False
        else:
            return True

def group_group_collide(group_one, group_two):
    copy_grp_one = group_one.copy()
    remove_ele = set([])
    for ele in copy_grp_one:
        if group_collide(group_two, ele):
            remove_ele.add(ele)
    collision_num = len(remove_ele)
    for ele in remove_ele:
        group_one.discard(ele)
        
    return collision_num
        
def group_collide(group_sprite, other_obj):
    remove_elements = set([])
    
    for ele in group_sprite:
        if ele.collide(other_obj):
            remove_elements.add(ele)
 #self, pos, vel, ang, ang_vel, image, info, sound = None):   
    for rm in remove_elements:
        explosion_group.add(Sprite(rm.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
        group_sprite.remove(rm)
        
    if len(remove_elements) > 0:
        return True
    else:
        return False
        
def draw(canvas):
    global time, started, a_rock_group, score, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    #score
    canvas.draw_text("score   "+str(score), (20, 20), 25, 'White')
    canvas.draw_text("lives   "+str(lives), (WIDTH *3 /4,20), 25, 'White')
    # draw ship and sprites
    my_ship.draw(canvas)
    
    if group_collide(a_rock_group, my_ship):
        lives -=1
    if lives == 0:
        started = False
        rock_grp_copy = a_rock_group.copy()
        for ele in rock_grp_copy:
            a_rock_group.discard(ele)
    
    score = score + group_group_collide(missile_group, a_rock_group)
    # update ship and sprites
    my_ship.update()
    process_sprite_group(a_rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock_group, started
    
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    angle_vel = random.random() * .2 - .1
    
    if len(a_rock_group) < MAX_ROCK and started:
        rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
        if not rock.collide(my_ship):
            a_rock_group.add(rock)

# update and draw the rocks
def process_sprite_group(sprite_grp, canvas):
    rm_set = set([])
    for sp in sprite_grp:
        sp.draw(canvas)
        if sp.update():
            rm_set.add(sp)
    
    for rm in rm_set:
        sprite_grp.remove(rm)
    

#keyDown handler
def keydown(key):
    if(key == simplegui.KEY_MAP['left']):
       my_ship.update_angle_velocity(-1)
    elif(key == simplegui.KEY_MAP['right']):
       my_ship.update_angle_velocity(1)
    elif(key == simplegui.KEY_MAP['up']):
        my_ship.update_thrust(True)
    elif(key == simplegui.KEY_MAP['space']):
         my_ship.shoot()
    

#keyUp handler
def keyup(key):
    if(key == simplegui.KEY_MAP['left']):
       my_ship.update_angle_velocity( 1 )
    elif(key == simplegui.KEY_MAP['right']):
       my_ship.update_angle_velocity(-1)
    elif(key == simplegui.KEY_MAP['up']):
        my_ship.update_thrust(False)
        
#mouseclick handler
def mouse_handler(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()

        
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
