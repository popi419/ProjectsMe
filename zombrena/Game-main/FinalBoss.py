import os , random

from Vector import *

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700

zombieSize = 10
SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")

#all dimensions for both arms, head, and laser part of boss
FINALBOSS_SHEET_URL = os.path.join(SPRITESHEET_PATH, "boss4.png")

FINALBOSS_SHEET_WIDTH = 512
FINALBOSS_SHEET_HEIGHT = 128
FINALBOSS_SHEET_COLUMNS = 4
FINALBOSS_SHEET_ROWS = 1

FINALBOSSARMS_SHEET_URL = os.path.join(SPRITESHEET_PATH, "GiantArms.png")

FINALBOSSARMS_SHEET_WIDTH = 640 
FINALBOSSARMS_SHEET_HEIGHT = 256


SHEET_URL_LASER = os.path.join(SPRITESHEET_PATH, "pngegg2.png")

SHEET_WIDTH_LASER = 1536
SHEET_HEIGHT_LASER = 2048
SHEET_COLUMNS_LASER = 3
SHEET_ROWS_LASER = 1


class SpritesheetLaser:
    def __init__(self, imgurl, width, height, columns, rows, frame_duration):
        #values for spritesheet
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
        self.dest_size_x = random.randint(150,200)
        self.dest_size_y = 150

    def update(self):
        #simulates animation by iterating over columns with %
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns

    def draw(self, canvas, pos):
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )

        source_size = (self.frame_width, self.frame_height)
        dest_centre = pos
        img_rot = 0

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          dest_centre,
                          (self.dest_size_x, self.dest_size_y),
                          img_rot)


class BossSpritesheet:
    def __init__(self, imgurl, width, height, columns, rows, frame_duration,dest_size):
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
        self.dest_size = dest_size


    def update(self):
        self.frame_clock += 1
        if self.frame_clock % self.frame_duration == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % self.columns

    def draw(self, canvas, pos):
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )

        source_size = (self.frame_width, self.frame_height)
        dest_centre = pos
        
        img_rot = 0

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          dest_centre,
                          self.dest_size,
                          img_rot)


class FinalBoss:
    def __init__(self, position):
        self.spritesheet = BossSpritesheet(FINALBOSS_SHEET_URL,FINALBOSS_SHEET_WIDTH,FINALBOSS_SHEET_HEIGHT,FINALBOSS_SHEET_COLUMNS,FINALBOSS_SHEET_ROWS, 30,(150,150))
        self.position = position
        self.size = 100
        self.velocity = Vector(0,0)

        # final zombie health
        self.health = 2250

        #arm attributes
        self.rightarm = Arm(Vector(40,0),"right",self)
        self.leftarm = Arm(Vector(CANVAS_WIDTH-40,CANVAS_HEIGHT/2),"left",self)
        self.attacktimer = 0

    def update(self,playerpos):
        self.rightarm.spritesheet.update()
        self.leftarm.spritesheet.update()

        
        self.rightarm.generatepos()
        self.leftarm.generatepos()

        self.attacktimer += 1


        if random.random() <= 0.50:
            if not self.rightarm.recharging:
                self.rightarm.attack(playerpos)
        else:
            if not self.leftarm.recharging:
                self.leftarm.attack(playerpos)

                
    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())
        self.rightarm.spritesheet.draw(canvas,self.rightarm.position.get_p())
        self.leftarm.spritesheet.draw(canvas,self.leftarm.position.get_p())

    # self.followPlayer(thePlayer.position.get_p())

    def hit(self, bullet):
        # activated when hit
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= zombieSize + bullet.radius

    def hurt(self, dmg):
        self.health -= dmg

    def knockback(self, bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)



class Arm:
    def __init__(self, position,situated,parent):
        self.spritesheet = BossSpritesheet(FINALBOSSARMS_SHEET_URL,FINALBOSSARMS_SHEET_WIDTH,FINALBOSSARMS_SHEET_HEIGHT,5,2, 20,(200,200))
        self.position = position
        self.size = 100
        self.parent = parent
        self.down = True
        self.situated = situated
        self.recharging = False

        if self.situated == "left":
            self.spritesheet.frame_index[1] = 1
        elif self.situated == "right":
            self.spritesheet.frame_index[1] = 0
            
    def generatepos(self):
        #generates a moving arm by updating the y position
        if self.down:
            if self.position.y < CANVAS_WIDTH:
                self.position.y += 3
            else:
                self.down = False
        else:
            if self.position.y > 0:
                self.position.y -= 3
            else:
                self.down = True

    def attack(self, playerPosition):
        self.pre_player_position = playerPosition.copy()
        self.prearm_pos = self.position.copy()
        # getting the direction and velocity
        direction_vector = Vector(self.pre_player_position.x, self.pre_player_position.y) - self.position

        if direction_vector.length() > 0:
            direction = direction_vector.get_normalized()
            # adjust the speed of the boss
            self.velocity = (direction.multiply(1.5))
            # adjust the threshold for the position
            distance_threshold = 1.5

            if direction_vector.length() > distance_threshold:
                self.position = self.position.add(self.velocity)
                self.recharging = False
            else:
                self.stop()
                self.resetposition()
        else:
            self.stop()
            # not sure if self.recharging = True

    def stop(self):
        self.velocity = Vector(0, 0)
            
    def resetposition(self):
        direction_vector = self.prearm_pos - self.position
        if direction_vector.length() > 0:
            direction = direction_vector.get_normalized()
            # adjust the speed of the boss
            self.velocity = (direction.multiply(1.5))
            # adjust the threshold for the position
            distance_threshold = 1.5

            if direction_vector.length() > distance_threshold:
                self.position = self.position.add(self.velocity)

            self.recharging = True

    def hit(self, bullet):
        # activated when hit
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= zombieSize + bullet.radius

    def hurt(self, dmg):
        self.parent.health -= dmg

    def knockback(self, bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)


class LazerWall:
    def __init__(self, x, border, pos):
        # code used for laser attack, specifically the collision
        self.spritesheetLaser = SpritesheetLaser(SHEET_URL_LASER, SHEET_WIDTH_LASER, SHEET_HEIGHT_LASER,
                                                 SHEET_COLUMNS_LASER, SHEET_ROWS_LASER, 10)
        self.x = x
        self.border = border
        self.radius = 10
        self.pos = pos

    def update(self):
        self.spritesheetLaser.update()

    def draw(self, canvas):
        self.spritesheetLaser.draw(canvas, self.pos.get_p())


class Interaction:
    def __init__(self, wheel, keyboard, FinalBoss, wall):
        self.wheel = wheel
        self.keyboard = keyboard
        self.FinalBoss = FinalBoss
        self.wall = wall

    # speed of player
    def draw(self, canvas):
        self.wall.draw(canvas)
        self.update()
        self.FinalBoss.draw(canvas)
        self.FinalBoss.update(self.wheel.pos)
        self.wheel.draw(canvas)
        self.wheel.update()

    def update(self):
        global laserAttack
        if laserAttack == True:
            #draws the laser
            self.FinalBoss.spritesheet.frame_index[0] = 1
            self.wall.update()
            #inits the left and right edges of the "laser"
            leftside = self.wall.x - self.wall.border
            rightside = self.wall.x + self.wall.border

            # deals with collision
            # if (self.wheel.pos.x + self.wheel.radius >= leftside) and (
            #         self.wheel.pos.x - self.wheel.radius <= rightside):
            #     print("HIT")

            global growSize
            # laser grows in size until it reaches a certain point, at which it will slowly begin to shrink until the attack ends
            if (self.wall.spritesheetLaser.dest_size_y < 2500 and growSize):
                self.wall.spritesheetLaser.dest_size_y += 70
            if (self.wall.spritesheetLaser.dest_size_y > 2500):
                growSize = False
            if (growSize == False):
                self.wall.spritesheetLaser.dest_size_x -= 1
                if self.wall.spritesheetLaser.dest_size_x <= 100:
                    self.wall.spritesheetLaser.dest_size_x = random.randint(150,200)
                    self.wall.spritesheetLaser.dest_size_y = 150
                    laserAttack = False
                    growSize = True
                    self.FinalBoss.spritesheet.frame_index[0] = 0

        if self.FinalBoss.attacktimer % 200 == 0:
            laserAttack = True

        if self.keyboard.right:
            self.wheel.vel.add(Vector(0.2, 0))
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-0.2, 0))
        if self.keyboard.up:
            self.wheel.vel.add(Vector(0, -0.2))
        if self.keyboard.down:
            self.wheel.vel.add(Vector(0, 0.2))





