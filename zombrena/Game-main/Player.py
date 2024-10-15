try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Vector import Vector
import os
import math

SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")

SHEET_URL = os.path.join(SPRITESHEET_PATH, "player.png")

# dimensions of spritesheet    
SHEET_WIDTH = 256
SHEET_HEIGHT = 256
SHEET_COLUMNS = 4
SHEET_ROWS = 4


WIDTH = 700
HEIGHT = 700

SOUND_FILE_PATH = os.path.join(os.getcwd(), "sounds")

class Player:
    # loads spritesheet image along with various dimension values for later drawing
    def __init__(self, pos, imgurl, width, height, columns, rows, frame_duration,radius = 10):
        self.img = simplegui.load_image('file:\\' + imgurl)
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.frame_duration = frame_duration

        self.frame_width = width / columns
        self.frame_height = height / rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

        self.frame_index = [0, 0]
        self.frame_clock = 0
        
        #this part of player deals with movement, collision etc
        self.pos = pos
        self.vel = Vector()
        self.pickupradius = 20 # used for gun pickup
        self.colour = 'White'
        self.img_dest_dim = (128 + self.pickupradius, 128 + self.pickupradius)
        self.IMG_CENTRE = (256, 256)
        self.IMG_DIMS = (512, 512)
        # health and checks to see health
        self.Hit = 0
        self.deadcount = 0
        self.ismoving = False

        sound_path = os.path.join(SOUND_FILE_PATH, 'player_hurt.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

    def setSound(self):
        #when called, play hurtsound
        self.sound.set_volume(0.3)
        self.sound.rewind()
        self.sound.play()

    def update(self):
        # adds velocity to player pos to simulate movement, used in interaction class
        self.pos.add(self.vel)
        self.vel.multiply(0.85)

    def stop(self):
        #immediately stop player movement
        self.vel = Vector(0, 0)

    def hit(self,zombie):
        #activated to check if collision is detected
        distance = self.pos.copy().subtract(zombie.position.copy()).length()
        return distance <= 20 + zombie.size

    def lazer_hit(self,lazer):
        #activated to check if collision is detected
        distance = self.pos.copy().subtract(lazer.pos.copy()).length()
        return distance <= 20 + lazer.radius

    def update_index(self):
        # iterate over columns of spritesheet to simulate animation
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns

    def player_rot(self, arc_degree):
        # code for ensuring player turns to the guns direction when firing

        if arc_degree < -math.pi or arc_degree > 0:
            self.frame_index[1] = 1
        elif arc_degree < 0 or arc_degree > math.pi:
            self.frame_index[1] = 0

    def draw(self, canvas, pos):
        # draw method, frame_clock used for interaction class, animating of sprite

        self.frame_clock += 1
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )
        # source centre for finding centre of the part of spritesheet to use

        source_size = (self.frame_width, self.frame_height)
        dest_centre = pos
        dest_size = (100, 100)
        img_rot = 0

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          dest_centre,
                          dest_size,
                          img_rot)


class Keyboard:
    def __init__(self):
        # various checks used to control player direction and other keyboard related input
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.isLeft = False
        self.isDead = False
        self.space = False
        self.pause = False
        self.equip = False
        self.quit = False
        self.exit = False

    def keyDown(self, key):
        # isDead controls whether player is allowed to move, if they're dead then no
        if key == simplegui.KEY_MAP['w'] and not self.isDead:
            self.up = True
        elif key == simplegui.KEY_MAP['s'] and not self.isDead:
            self.down = True
        elif key == simplegui.KEY_MAP['a'] and not self.isDead:
            self.left = True
            self.isLeft = True
        elif key == simplegui.KEY_MAP['d'] and not self.isDead:
            self.right = True
            self.isLeft = False
        elif key == simplegui.KEY_MAP['e']:
            self.equip = True
        elif key == simplegui.KEY_MAP['space']:
            self.space = True
        # 27 = 'ESC'
        elif key == 27:
            self.quit = True
        # 31 = 'Ctrl'
        elif key == 31 and key == simplegui.KEY_MAP['q']:
            self.exit = True

    def keyUp(self, key):
        # sets checks back to false when key is released
        global STEP
        if key == simplegui.KEY_MAP['w']:
            self.up = False
            STEP = 0
        elif key == simplegui.KEY_MAP['s']:
            self.down = False
            STEP = 0
        elif key == simplegui.KEY_MAP['a']:
            self.left = False
            STEP = 0
        elif key == simplegui.KEY_MAP['d']:
            self.right = False
            STEP = 0
        elif key == simplegui.KEY_MAP['e']:
            self.equip = False
        elif key == simplegui.KEY_MAP['space']:
            self.space = False
