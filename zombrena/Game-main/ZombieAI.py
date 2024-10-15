import os

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math
from Vector import Vector

width = 700
height = 700

# movement size and stuff, feel free to change the speeds to your liking
playerSize = 20
zombieSize = 10
lowiqZombieSize = 10
zombieMoveSpeed = 0.4  # default movement speed of normal zombies
lowiqZombieSpeed = 0.4  # default movement speed of dumb zombie
undergroundZombieSpeed = 0.6 # higher speed while underground
chargeSpeed = 0.5  # this is the speed when it charges the player
chargeRange = 100  # radius around the player
slowdownSpeed = 0.2 #the underground zombie 'slows' down when it reaches the player because it pops out of the ground

fatZombieMoveSpeed = 0.3
fatZombieChargeSpeed = 0.4  
fatZombieSize = 35  
fatZombieChargeSize = 40

toughZombieMoveSpeed = 0.35
toughZombieInitialHealth = 30

spawnTime = 2000
frame_count = 0

zombiesList = []
lowiqZombiesList = []
undergroundZombiesList = []
fatZombiesList = []
toughZombiesList = []

currentPixelZombie = 0

SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")

SHEET_URL = os.path.join(SPRITESHEET_PATH, "zombiesprite.png")
SHEET_URL2 = os.path.join(SPRITESHEET_PATH, "spritesheetgroundzombie.png")

SHEET_WIDTH = 256
SHEET_HEIGHT = 256
SHEET_COLUMNS = 4
SHEET_ROWS = 4
STEP = 0


class Spritesheet:
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
        dest_size = (100, 100)
        img_rot = 0

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          dest_centre,
                          dest_size,
                          img_rot)

class Zombie:
    def __init__(self, position):
        #instantiates spritesheet of zombie to instance of zombie
        self.spritesheet = Spritesheet(SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS, 30)
        #holds position, direction and speed of zombie
        self.position = position
        direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.velocity = direction.get_normalized().multiply(zombieMoveSpeed)
        #size of zombie for radius based methods
        self.size = 25
        #basic zombie health
        self.health = 20

    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())

    def rotate_self(self,arc_degree):
        #method to ensure zombie always uses correct direction of sprite
        if arc_degree < -math.pi or arc_degree > 0:
            self.spritesheet.frame_index[1] = 1
        elif arc_degree < 0 or arc_degree > math.pi:
            self.spritesheet.frame_index[1] = 0

    def update(self):
        # adds velocity speed to zombie pos to simulate movement
        self.position.add(self.velocity)

    def followPlayer(self, playerPos):
        # takes player position and begins moving the zombie towards direction of player
        moveToPlayer = Vector(playerPos.x, playerPos.y) - self.position
        if moveToPlayer.length() < chargeRange:
            self.velocity = moveToPlayer.get_normalized().multiply(chargeSpeed)
        else:
            self.velocity = moveToPlayer.get_normalized().multiply(zombieMoveSpeed)

    def hit(self,bullet):
        #checks to see if bullet collides with zombie
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= zombieSize + bullet.radius

    def hurt(self,dmg):
        #used for instances where zombie needs to be damaged
        self.health -= dmg

    def knockback(self,bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)


class LowIQZombie:
    def __init__(self, position):
        self.spritesheet = Spritesheet(SHEET_URL2, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS, 30)
        self.position = position
        self.velocity = Vector(random.choice([-1, 1]) * lowiqZombieSpeed, random.choice([-1, 1]) * lowiqZombieSpeed)
        self.initial_movement_distance = 0
        self.initial_movement_phase = True
        self.following = False
        self.size = 25

        #dumb zombie health
        self.health = 10

    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())

    def update(self):
        if self.initial_movement_phase:
            self.position.add(self.velocity)
            self.initial_movement_distance += self.velocity.length()
            if self.initial_movement_distance >= 70:
                self.initial_movement_phase = False
                self.velocity = Vector(0, 0)

    def followPlayer(self, playerPos):
        moveToPlayer = Vector(playerPos[0], playerPos[1]) - self.position
        if moveToPlayer.length() < chargeRange:
            self.following = True
            self.velocity = moveToPlayer.get_normalized().multiply(chargeSpeed)
        else:
            self.following = False

            if random.randint(0, 50) == 0:
                self.velocity = Vector(random.choice([-1, 1]) * lowiqZombieSpeed, random.choice([-1, 1]) * lowiqZombieSpeed)

    def stop(self):
        self.velocity = Vector(0, 0)

    def hit(self,bullet):
        #activated when hit
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= lowiqZombieSize + bullet.radius

    def hurt(self,dmg):
        self.health -= dmg

    def knockback(self,bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)


class UndergroundZombie:
    def __init__(self, position):
        self.position = position
        direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.velocity = direction.get_normalized().multiply(undergroundZombieSpeed)
        self.health = 20
        self.size = 25

    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(), zombieSize, 1, "Yellow", "Yellow")

    def update(self):
        self.position.add(self.velocity)
        self.followPlayer(thePlayer.position.get_p())

    def followPlayer(self, playerPos):
        moveToPlayer = Vector(playerPos[0], playerPos[1]) - self.position
        if moveToPlayer.length() < chargeRange:
            self.velocity = moveToPlayer.get_normalized().multiply(slowdownSpeed)
        else:
            self.velocity = moveToPlayer.get_normalized().multiply(undergroundZombieSpeed)

    def hit(self, bullet):
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= zombieSize + bullet.radius

    def hurt(self, dmg):
        self.health -= dmg

    def knockback(self, bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)

#just fat zombies with more health
class FatZombie:
    def __init__(self, position):
        self.spritesheet = Spritesheet(SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS, 30)
        self.position = position
        direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.velocity = direction.get_normalized().multiply(fatZombieMoveSpeed)
        self.size = fatZombieSize
        self.health = 100
        self.isCharging = False

    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())

    def update(self):
        self.position.add(self.velocity)
        self.followPlayer(thePlayer.position.get_p())  

    def followPlayer(self, playerPos):
        moveToPlayer = Vector(playerPos[0], playerPos[1]) - self.position
        if moveToPlayer.length() < chargeRange:
            self.isCharging = True
            self.velocity = moveToPlayer.get_normalized().multiply(fatZombieChargeSpeed) 
        else:
            self.isCharging = False
            self.velocity = moveToPlayer.get_normalized().multiply(fatZombieMoveSpeed)

# tough zombies are basically conehead zombies from pvz, the more damage they take, the more limbs or armor they lose, i also made it so that they slow down everytime they lose a part
class ToughZombie:
    def __init__(self, position):
        self.spritesheet = Spritesheet(SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS, 30)
        self.position = position
        direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.velocity = direction.get_normalized().multiply(toughZombieMoveSpeed)
        self.size = zombieSize 
        self.health = toughZombieInitialHealth
        self.initial_speed = toughZombieMoveSpeed

    def draw(self, canvas):
        self.spritesheet.draw(canvas, self.position.get_p())

    def update(self):
        self.position.add(self.velocity)
        self.followPlayer(thePlayer.position.get_p())  

    def followPlayer(self, playerPos):
        moveToPlayer = Vector(playerPos[0], playerPos[1]) - self.position
        if moveToPlayer.length() < chargeRange:
            self.velocity = moveToPlayer.get_normalized().multiply(self.initial_speed)
        else:
            self.velocity = moveToPlayer.get_normalized().multiply(self.initial_speed)

    def hit(self, bullet):
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        if distance <= zombieSize + bullet.radius:
            self.hurt(bullet.damage)

    def hurt(self, dmg):
        self.health -= dmg
        if self.health > 0:
            speed_reduction = (1 - (self.health / toughZombieInitialHealth)) * 0.5
            self.velocity = self.velocity.multiply(1 - speed_reduction)
        else:
            self.velocity = Vector(0, 0)

    def knockback(self, bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)


# spawn parameters
def spawnZombie():
    sides = random.choice(['top', 'bottom', 'left', 'right'])
    if sides == 'top':
        pos = Vector(random.randint(0, width), 0)
    elif sides == 'bottom':
        pos = Vector(random.randint(0, width), height - 0)
    elif sides == 'left':
        pos = Vector(0, random.randint(0, height))
    else:
        pos = Vector(width - 0, random.randint(0, height))
    zombiesList.append(Zombie(pos))

def spawnLowiqZombie():
    global currentPixelZombie
    pos = Vector(random.randint(0, width), random.randint(0, height))

    lowiqZombiesList.append(LowIQZombie(pos))

def spawnUndergroundZombie():
    sides = random.choice(['top', 'bottom', 'left', 'right'])
    if sides == 'top':
        pos = Vector(random.randint(0, width), 0)
    elif sides == 'bottom':
        pos = Vector(random.randint(0, width), height)
    elif sides == 'left':
        pos = Vector(0, random.randint(0, height))
    else:
        pos = Vector(width, random.randint(0, height))
    undergroundZombiesList.append(UndergroundZombie(pos))

def spawnFatZombie():
    sides = random.choice(['top', 'bottom', 'left', 'right'])
    if sides == 'top':
        pos = Vector(random.randint(0, width), 0)
    elif sides == 'bottom':
        pos = Vector(random.randint(0, width), height)
    elif sides == 'left':
        pos = Vector(0, random.randint(0, height))
    else:
        pos = Vector(width, random.randint(0, height))
    fatZombiesList.append(FatZombie(pos))

def spawnToughZombie():
    sides = random.choice(['top', 'bottom', 'left', 'right'])
    if sides == 'top':
        pos = Vector(random.randint(0, width), 0)
    elif sides == 'bottom':
        pos = Vector(random.randint(0, width), height)
    elif sides == 'left':
        pos = Vector(0, random.randint(0, height))
    else:
        pos = Vector(width, random.randint(0, height))
    toughZombiesList.append(ToughZombie(pos))

