import os

from Vector import *

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

charging = False
SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")

CHARGER_SHEET_URL = os.path.join(SPRITESHEET_PATH, "boss3.png")

CHARGER_SHEET_WIDTH = 512
CHARGER_SHEET_HEIGHT = 1024
CHARGER_SHEET_COLUMNS = 4
CHARGER_SHEET_ROWS = 9

STEP = 0

class SpritesheetCharger:
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

    def chargerBoss_rot(self, arc_degree):

        if arc_degree < -math.pi or arc_degree > 0:
            self.frame_index[1] = 3
        elif arc_degree < 0 or arc_degree > math.pi:
            self.frame_index[1] = 2

    def draw(self, canvas, pos):
        self.frame_clock += 6
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )

        source_size = (self.frame_width, self.frame_height)
        dest_centre = pos
        dest_size = (125, 125)
        img_rot = 0

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          dest_centre,
                          dest_size,
                          img_rot)


class ChargerBoss:
    def __init__(self, position):
        self.spritesheet = SpritesheetCharger(CHARGER_SHEET_URL, CHARGER_SHEET_WIDTH, CHARGER_SHEET_HEIGHT, CHARGER_SHEET_COLUMNS, CHARGER_SHEET_ROWS, 60)
        self.position = position
        self.velocity = Vector(0, 0)
        self.size = 25
        self.health = 400
        self.pre_player_position = Vector(100, 100)
        self.current_player_position = Vector(100, 100)

    def charge(self, playerPosition):
        global charging
        self.pre_player_position = playerPosition.copy()
        # getting the direction and velocity
        direction_vector = Vector(self.pre_player_position.x, self.pre_player_position.y) - self.position

        # > 0 to avoid divide by 0 error.
        if direction_vector.length() > 0:
            direction = direction_vector.get_normalized()
            # adjust the speed of the boss
            self.velocity = (direction.multiply(1.5))
            # adjust the threshold for the position
            distance_threshold = 1.5

            if direction_vector.length() > distance_threshold:
                self.position = self.position.add(self.velocity)
                charging = True
            else:
                self.stop()
                charging = False
        else:
            self.stop()
            charging = False

    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())

    def update(self, player):
        self.current_player_position = player.pos
        #self.position.add(self.velocity)

        if not charging:
            self.charge(self.current_player_position)
        else:
            self.charge(self.pre_player_position)

    def hurt(self, dmg):
        self.health -= dmg

    def stop(self):
        self.velocity = Vector(0, 0)

    def hit(self, bullet):
        # activated when hit
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= self.size + bullet.radius

    def knockback(self, bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)

    # simulating bullets go through the boss
    def check_collision_on_boss(self):
        if self.hit(self.ball):
            self.chargerBoss.hurt(50)

    # simulating player goes through the boss
    def check_collison_on_player(self):
        if self.hit(self.ball):
            self.ball.health -= 0.6
