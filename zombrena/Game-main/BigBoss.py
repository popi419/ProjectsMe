import os

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
from Vector import Vector


SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")
TANK_SHEET_URL = os.path.join(SPRITESHEET_PATH, "boss2.png")

TANK_SHEET_WIDTH = 512
TANK_SHEET_HEIGHT = 1024
TANK_SHEET_COLUMNS = 4
TANK_SHEET_ROWS = 9
STEP = 0


class SpritesheetTank:
    def __init__(self, imgurl, width, height, columns, rows, frame_duration):
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

    def update_index(self):
        # iterate over column
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns

    def tankBossHealthy_rot(self, arc_degree):
        # returns which direction the sprite should be relative to player, used for when tank is in healthy sprite

        if arc_degree < -math.pi or arc_degree > 0:
            self.frame_index[1] = 1
        elif arc_degree < 0 or arc_degree > math.pi:
            self.frame_index[1] = 0

    def tankBossHurt_rot(self, arc_degree):
        # returns which direction the sprite should be relative to player, used for when tank is in hurt sprite

        if arc_degree < -math.pi or arc_degree > 0:
            self.frame_index[1] = 3
        elif arc_degree < 0 or arc_degree > math.pi:
            self.frame_index[1] = 2

    def tankBossNearDeath_rot(self, arc_degree):
        # returns which direction the sprite should be relative to player, used for when tank is in near death sprite

        if arc_degree < -math.pi or arc_degree > 0:
            self.frame_index[1] = 5
        elif arc_degree < 0 or arc_degree > math.pi:
            self.frame_index[1] = 4

    def draw(self, canvas, pos):
        global STEP
        self.frame_clock += 1
        if self.frame_clock % self.frame_duration == 0:
            self.update_index()
            self.frame_clock = 0

        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )

        source_size = (self.frame_width, self.frame_height)
        dest_centre = pos
        dest_size = (175, 175)
        img_rot = 0

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          dest_centre,
                          dest_size,
                          img_rot)


class TankBoss:
    def __init__(self, position):
        self.spritesheet = SpritesheetTank(TANK_SHEET_URL, TANK_SHEET_WIDTH, TANK_SHEET_HEIGHT, TANK_SHEET_COLUMNS, TANK_SHEET_ROWS, 30)
        self.position = position
        direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.velocity = direction.get_normalized().multiply(0.4) # zombieMoveSpeed
        self.size = 50

        # basic zombie health
        self.health = 1600

    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())

    def rotate_self(self, arc_degree):
        if arc_degree < -math.pi or arc_degree > 0:
            self.spritesheet.frame_index[1] = 1
        elif arc_degree < 0 or arc_degree > math.pi:
            self.spritesheet.frame_index[1] = 0

    def update(self):
        self.position.add(self.velocity)
        # self.followPlayer(thePlayer.position.get_p())

    def followPlayer(self, playerPos):
        moveToPlayer = Vector(playerPos.x, playerPos.y) - self.position
        if moveToPlayer.length() < 100: # zombie chargerange
            self.velocity = moveToPlayer.get_normalized().multiply(0.5) # zombiechargespeed
        else:
            self.velocity = moveToPlayer.get_normalized().multiply(0.4) # zombieMoveSpeed

    def hit(self, bullet):
        # activated when hit
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= 10 + bullet.radius # zombieSize

    def hurt(self, dmg):
        self.health -= dmg

    def knockback(self, bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)



