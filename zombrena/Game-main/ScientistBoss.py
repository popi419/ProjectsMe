from Vector import *

from Weapons import Orbital,OrbitalLaser

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
import random, os
SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")


class ScientistBoss:
    def __init__(self, position):
        #image attributes
        image_path = os.path.join(SPRITESHEET_PATH, 'ScientistBoss.png')
        self.image = simplegui.load_image('file:\\' + image_path)
        
        self.frame_duration = 20

        self.frame_width = 320 / 5
        self.frame_height = (128*2) / 4
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

        self.frame_index = [0, 0]
        self.frame_clock = 0

        #positional attributes
        self.position = position
        direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.velocity = direction.get_normalized().multiply(1)
        self.size = 25
        self.teleporting = False
        self.teleporttimer = 0
        self.left = False

        #boss zombie health
        self.health = 550

        #boss attacks
        self.gun = Orbital(self.position,100,"held")
        self.attacktimer = 0
        self.attackinterval = 90 # every 1.5 secs he attacks

    def teleport(self,middle):
        #teleports him to midle of screen
        self.teleporting = True
        if self.teleporttimer % 5 == 0:
            if self.frame_index[0] == 3:    
                self.position = middle
                self.teleporting = False

    def updateteleport(self):
        self.teleporttimer += 1

    def aimgun(self,playerpos):
        #rotates the gun toward player
        self.gun.rotate_self(playerpos)

    def update_index(self):
        # iterate over column
        self.frame_index[0] = (self.frame_index[0] + 1) % 5

    def draw(self, canvas):
        #draws boss
        self.frame_clock += 1
        if self.frame_clock % self.frame_duration == 0:
            self.update_index()
            self.frame_clock = 0

        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )

        source_size = (self.frame_width, self.frame_height)
        dest_centre = (self.position.x,self.position.y)
        dest_size = (100, 100)
        img_rot = 0
        
        canvas.draw_image(self.image,
                          source_centre,
                          source_size,
                          dest_centre,
                          dest_size,
                          img_rot)

        #draws gun
        self.gun.draw(canvas)

    def rotate_self(self,arc_degree):
        #code for rotating sprites
        if not self.teleporting:
            if arc_degree < -math.pi or arc_degree > 0:
                self.frame_index[1] = 1
                self.left = True
            elif arc_degree < 0 or arc_degree > math.pi:
                self.frame_index[1] = 0
                self.left = False
        else:
            if arc_degree < -math.pi or arc_degree > 0:
                self.frame_index[1] = 3
                self.left = True
            elif arc_degree < 0 or arc_degree > math.pi:
                self.frame_index[1] = 2
                self.left = False

    def update(self,player,list_of_bullets):
        self.attacktimer += 1
        
        self.gun.animationtimer += 1
        if self.gun.shootinganimate:
            self.gun.animate()
        
        #adjusting gun placement on boss
        if self.frame_index[1] == 1:
            pos = self.position.copy().add(Vector(-25, 15))
        else:
            pos = self.position.copy().add(Vector(25, 15))
            
        self.gun.pos = pos

        #constantly rotates gun aim
        self.aimgun(player.pos.copy().get_p())

        if self.attacktimer % self.attackinterval == 0:
            self.gun.boss_shoot(player.pos.copy().get_p(),list_of_bullets)
            self.gun.shootinganimate = True
            self.gun.sound.set_volume(0.2)
            self.gun.sound.rewind()
            self.gun.sound.play()

        self.position.add(self.velocity)
        self.Back_away_from_Player(player.pos.copy().get_p())

    def Back_away_from_Player(self, playerPos):
        #makes the zombie back away from player
        backoffPlayer = Vector(playerPos[0], playerPos[1]) - self.position
        if backoffPlayer.length() > 100:
            self.velocity = -backoffPlayer.get_normalized().multiply(2)

    def hit(self,bullet):
        #activated when hit
        distance = self.position.copy().subtract(bullet.pos.copy()).length()
        return distance <= self.size + bullet.radius

    def hurt(self,dmg):
        self.health -= dmg

    def knockback(self,bullet):
        normal = self.position.copy().subtract(bullet.pos).normalize()
        self.velocity.reflect(normal)
