from Vector import *
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import os
import math ,random

SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")
SOUND_FILE_PATH = os.path.join(os.getcwd(), "sounds")


class Weapon:
    #this is the main parent class that adds functionality to all the guns
    def __init__(self,pos,magsize,state = "dropped"):
        #weapon functionaility state
        self.state = state
        
        #image attributes
        self.image = None
        self.image_centre = None
        self.image_dims = None
        self.size = None
        self.frame_index = [0,0]

        #animation attributes
        self.animationtimer = 0
        self.shooting = False
        self.shootinganimate = False

        #firerate attributes
        self.firerate = 500 #default fire rate (0.5 seconds)
        self.fireratehandler = simplegui.create_timer(self.firerate, self.fire)
        self.fireratehandler.start()

        #the positional attributes
        self.rotation = 0
        self.pos = pos
        self.vel = Vector()
        self.rotated = False
        self.pickupradius = 30

        #attributes for bullets of the weapon
        self.magsize = magsize
        self.clip = magsize
        self.proj_speed = 20

    def _init_Image_dimension(self):
        #usual image loading
        self.image = simplegui.load_image('file:\\' + self.image_path)
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        #each animated shot will consist of 5 frames 
        self.frame_width = self.image.get_width() / 5 
        self.frame_height = self.image.get_height() / 2
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def _init_barrel_exit(self):
        #this method inintialises where the barrel would be at any time
        border_x = self.size[0]/2
        angled_barrel = Vector(border_x,0).rotate_rad(self.rotation)
        self.barrel_ext = angled_barrel

    def switchstate(self,newpos):
        #switches the functionality of gun
        if self.state == "dropped":
            self.pos = newpos
            self.state = "held"

        elif self.state == "held":
            self.pos = newpos
            self.state = "dropped"

    def draw(self, canvas):
        #added when sprites are made

        #source img dimensions    
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (self.frame_width, self.frame_height)

        #destination img dimentions
        dest_centre = (self.pos.x, self.pos.y)
        dest_size = self.size
    
        canvas.draw_image(self.image,
                          source_centre,
                          source_size,
                          dest_centre,
                          dest_size,
                          self.rotation)

    def animate(self):
        if self.animationtimer % 5 == 0:
            self.frame_index[0] = (self.frame_index[0] + 1) % 5
            if self.frame_index[0] == 4:
                self.shootinganimate = False

    def fire(self):
        #this timer handler models firerate
        self.shooting = False

    def rotate_self(self,pos):
        #rotates gun
        direction = Vector(pos[0],pos[1]).subtract(self.pos.copy())
        initial_image_rotation = math.pi/2
            
        self.rotation = initial_image_rotation -math.atan2(direction.x,direction.y)

        #GUN FRAME SWITCHING MAY HAVE TO RENDER IMAGES ON LEFT AS UPSIDE DOWN
        if self.rotation < -math.pi/2 or self.rotation > math.pi/2 and self.rotated == False:
            self.frame_index[1] = 1
            self.rotated = True
        elif self.rotation < math.pi/2 or self.rotation > math.pi + 2 and self.rotated == True:
            self.frame_index[1] = 0
            self.rotated = False

    #updates position of gun will update frames later
    def update(self,mousepos):
        if self.state == "held" and mousepos != None:
            self.rotate_self(mousepos)

            self.animationtimer += 1
            if self.shootinganimate == True:
                self.animate()

    def shoot(self,position,list_of_bullets):
        #this creates bullets and shoots them (shooting occurs in interact)
        #calc speed of projectile
        direction = Vector(position[0],position[1]).subtract(self.pos.copy()).normalize()
        Velocity = direction.multiply(self.proj_speed)
        
        #creates a bullet infront of the gun
        self._init_barrel_exit()
        bullet = Projectile(self.pos.copy().add(self.barrel_ext),Velocity,self.damage)

        #changes bullet image's trajectory by getting the negative arctan of the velocity
        bullet.rotation = -math.atan2(Velocity.x,Velocity.y)
        list_of_bullets.append(bullet)

        #simulates a muzzle Flash
        Flash = MuzzleFlash(self.pos.copy().add(self.barrel_ext),(50,50))
        Flash.rotation = -math.atan2(Velocity.x,Velocity.y)
        
        list_of_bullets.append(Flash)
        self.shooting = True

    #click handler is here (can be moved later if need be)
    def click(self,position,list_of_bullets):
        if self.state == "held" and not self.shooting:
            self.shoot(position,list_of_bullets)
            self.shootinganimate = True
            self.sound.set_volume(0.2)
            self.sound.rewind()
            self.sound.play()

        


class MuzzleFlash:
    #basic class to simulate a muzzle flash
    def __init__(self,pos,size):
        image_path = os.path.join(SPRITESHEET_PATH, 'Muzzle_flash.png')
        self.image = simplegui.load_image('file:\\' + image_path)
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())
        self.size = size
        self.pos = pos
        self.timer = 0
        self.rotation = 0

    def draw(self, canvas):
        dest_centre = (self.pos.x, self.pos.y)
        dest_size = self.size
    
        canvas.draw_image(self.image,
                          self.image_centre,
                          self.image_dims,
                          dest_centre,
                          dest_size,
                          self.rotation)

    def update(self):
        self.timer +=1
        

class Projectile:
    #this is the main projectile class
    def __init__(self,pos,vel = Vector(0,0),damage = 10):
        #image attributes
        #pathing for gun sprites
        image_path = os.path.join(SPRITESHEET_PATH, 'bullet.png')
        
        self.image = simplegui.load_image('file:\\' + image_path)
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())
        self.size = (50,50)
        self.radius = self.size[0]/2
        
        #the positional attribute
        self.pos = pos
        self.vel = vel
        self.rotation = 0

        #active duration
        self.duration = 0
        
        #damage attributes
        self.dmg = damage

    #for animated projectiles
    def _init_Image_dimension(self):
        self.frame_width = self.image.get_width() / self.col
        self.frame_height = self.image.get_height() 
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def draw(self, canvas):
        canvas.draw_image(self.image,
                          self.image_centre,
                          self.image_dims,
                          self.pos.get_p(),
                          self.size,
                          self.rotation)

    def update(self):
        self.pos.add(self.vel)
        self.duration += 1


class LaserBeam(Projectile):
    #projectile for LaserBeam
    def __init__(self,pos,vel = Vector(0,0),damage = 30):
        Projectile.__init__(self,pos)
        image_path = os.path.join(SPRITESHEET_PATH, 'lazer.png')
        
        self.image = simplegui.load_image('file:\\' + image_path)
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())
        self.size = (50,50)
        self.radius = self.size[0]/2

        #the positional attribute
        self.pos = pos
        self.vel = vel
        self.rotation = 0

        #damage attributes
        self.dmg = damage

    def update(self):
        self.pos.add(self.vel)
        self.duration += 1


class OrbitalLaser(Projectile):
    #projectile for orbital lazer
    def __init__(self,pos,vel = Vector(0,0),damage = 10,sound = None,damageplayer = False):
        Projectile.__init__(self,pos,vel)
        image_path = os.path.join(SPRITESHEET_PATH, 'orbital.png')
        
        self.image = simplegui.load_image('file:\\' + image_path)
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())
        self.size = (100,100)
        self.radius = self.size[0]/2

        #this is so it knows how to calculate the beam from the top
        self.blast_index = [0,0]
        self.blastframes = 10
        self.blast_tube = [10,0]
        self.col = 20

        self.orbitaltimer = 0
        
        #the positional attribute
        self.pos = pos
        self.vel = vel
        self.rotation = 0

        self._init_Image_dimension()

        #damage attributes
        self.dmg = damage
        self.damageplayer = damageplayer

        #sound
        self.sound = sound

    def playblast(self):
        #plays the blast SFX for bosses
        self.sound.set_volume(0.2)
        self.sound.play()

    def draw(self, canvas):
        #added when sprites are made

        #source img for blast dimensions    
        blast_centre = (self.frame_width*self.blast_index[0]+self.frame_centre_x,
                         self.frame_height*self.blast_index[1]+self.frame_centre_y)
        blast_size = (self.frame_width, self.frame_height)

        canvas.draw_image(self.image,
                          blast_centre,
                          blast_size,
                          self.pos.get_p(),
                          self.size,
                          self.rotation)

        #draw the rest of the lazer
        self._init_rest_of_lazer(canvas)
        #animate the blast
        self._update_index()

    def _init_rest_of_lazer(self,canvas):
        blast_centre = (self.frame_width*self.blast_tube[0]+self.frame_centre_x,
                         self.frame_height*self.blast_tube[1]+self.frame_centre_y)
        blast_size = (self.frame_width, self.frame_height)

        #for the rest of the screen from the top to pos it adds more obital blast tubes
        y = 0
        while (y <= self.pos.y):
            dest_centre = (self.pos.x, self.pos.y - y - self.size[1])
            canvas.draw_image(self.image,
                          blast_centre,
                          blast_size,
                          dest_centre,
                          self.size,
                          self.rotation)
            
            y += self.size[1]

    def _update_index(self):
        ##animates the blast
        if self.orbitaltimer % 6 == 0:
            self.blast_index[0] = (self.blast_index[0] + 1) % self.blastframes
            self.blast_tube[0] = (self.blast_tube[0] + 1) % self.blastframes + 10

    def update(self):
        self.orbitaltimer += 1


class Pistol(Weapon):
    #child weapon class that is a pistol
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites and sound
        self.image_path = os.path.join(SPRITESHEET_PATH, 'pistol_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'pistol.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (65,65)
        self.damage = 10
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [0,0]


class Pistolx4(Weapon):
    #child weapon class that is a pistol
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites and sound
        self.image_path = os.path.join(SPRITESHEET_PATH, '4pistol_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, '4pistol.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (65,65)
        self.damage = 10
        
        self._init_Image_dimension()
        self._init_barrel_exit(0)

        self.overlayindex = [5,0]

    def _init_barrel_exit(self,num):
        #this method inintialises where the barrel would be at any time
        border_x = self.size[0]/2 
        angled_barrel = Vector(border_x,num-19).rotate_rad(self.rotation)
        self.barrel_ext = angled_barrel

    def shoot(self,position,list_of_bullets):
        #this creates bullets and shoots them (shooting occurs in interact)
        for num in range(0,40,10):
            direction = Vector(position[0],position[1]).subtract(self.pos.copy()).normalize()
            Velocity = direction.multiply(self.proj_speed)
        
            #creates a bullet infront of the gun
            self._init_barrel_exit(num)
            bullet = Projectile(self.pos.copy().add(self.barrel_ext),Velocity,self.damage)

            #changes bullet image's trajectory by getting the negative arctan of the velocity

            if num % 10 == 0:
                bullet.rotation = -math.atan2(Velocity.x,Velocity.y)
                list_of_bullets.append(bullet)

                Flash = MuzzleFlash(self.pos.copy().add(self.barrel_ext),(50,50))
                Flash.rotation = -math.atan2(Velocity.x,Velocity.y)
        
                list_of_bullets.append(Flash)
                self.shooting = True


class Revolver(Weapon):
    #child weapon class that is a pistol
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites and sound
        self.image_path = os.path.join(SPRITESHEET_PATH, 'revolver_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'revolver.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (55,55)
        self.damage = 40
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [4,0]


class Shotgun(Weapon):
    #child weapon class that is a shotgun
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites and sound
        self.image_path = os.path.join(SPRITESHEET_PATH, 'db_shotgun_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'db.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (90,90)
        self.damage = 10
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [1,0]

    def shoot(self,position,list_of_bullets):
        #this method overloads the other shoot method
        #this creates bullets and shoots them (shooting occurs in interact)
        #as it is a shotgun it will shoot in a arc
        spread = math.pi / 12
        angles = []
        
        #this makes it so the middle bullet is angled to the cursor
        for number in range(-1,2):
            angles.append(number*spread)

        for angle_of_spread in angles:
            clicklocation = Vector(position[0],position[1])
            
            #calc where proj is going
            direction = clicklocation.subtract(self.pos.copy()).normalize()
            
            #each bullet will now be projected at a diffrent angle
            #it rotates it by a certain number of radians
            #this creates a spread

            rotated_direction = direction.rotate_rad(angle_of_spread)
            
            #added speed
            Velocity = rotated_direction.multiply(self.proj_speed)
        
            #creates a bullet infront of the gun
            self._init_barrel_exit()
            bullet = Projectile(self.pos.copy().add(self.barrel_ext),Velocity,self.damage)

            #changes bullet image's trajectory by getting the negative arctan of the velocity
            bullet.rotation = -math.atan2(Velocity.x,Velocity.y)
            list_of_bullets.append(bullet)

        #simulates a muzzle Flash
        Flash = MuzzleFlash(self.pos.copy().add(self.barrel_ext),(100,50))
        Flash.rotation = -math.atan2(Velocity.x,Velocity.y)
        
        list_of_bullets.append(Flash)
        self.shooting = True


class PipeRevolver(Weapon):
    #Pipe Weapons will have a secondry (burst attack) at a random time but will have significantly lower damage 
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites abd sound
        self.image_path = os.path.join(SPRITESHEET_PATH, 'pipe_rev_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'pipe_revo.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (60,60)
        self.damage = 3
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [2,0]

    def shoot(self,position,list_of_bullets):
        #this method overloads the other shoot method
        #this creates bullets and shoots them (shooting occurs in interact)

        spread = math.pi / 36
        angles = []
        
        #this makes it so the there is never a bullet that doesnt shoot
        ammount_of_bullets = random.randint(-2,3)
        if ammount_of_bullets  <= 0:
            angles.append(0)

        for number in range(ammount_of_bullets):
            angles.append(number*spread)

        for angle_of_spread in angles:
            clicklocation = Vector(position[0],position[1])
            
            #calc where proj is going
            direction = clicklocation.subtract(self.pos.copy()).normalize()
            
            #each bullet will now be projected at a diffrent angle
            #it rotates it by a certain number of radians
            #this creates a spread
            rotated_direction = direction.rotate_rad(angle_of_spread)
                
            #added speed
            Velocity = rotated_direction.multiply(self.proj_speed)
        
            #creates a bullet infront of the gun
            self._init_barrel_exit()
            bullet = Projectile(self.pos.copy().add(self.barrel_ext),Velocity,self.damage)

            #changes bullet image's trajectory by getting the negative arctan of the velocity
            bullet.rotation = -math.atan2(Velocity.x,Velocity.y)
            list_of_bullets.append(bullet)

            Flash = MuzzleFlash(self.pos.copy().add(self.barrel_ext),(75,50))
            Flash.rotation = -math.atan2(Velocity.x,Velocity.y)
        
            list_of_bullets.append(Flash)
            self.shooting = True


class PipeRifle(Weapon):
    #Pipe Weapons will have a secondry (burst attack) at a random time but will have significantly lower damage
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites and sound
        self.image_path = os.path.join(SPRITESHEET_PATH, 'pipe_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'pipe_rifle.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (75,75)
        self.damage = 2
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [3,0]

    def shoot(self,position,list_of_bullets):
        #this method overloads the other shoot method
        #this creates bullets and shoots them (shooting occurs in interact)

        #as it is a shotgun type it will shoot in a arc
        spread = math.pi / 36
        angles = []

        #it can shoot the up to 8 bullets
        startrange = random.randint(-4,0)
        ammount_of_bullets = random.randint(1,4)

        #1/50 chance to shoot whole clip
        if random.random() < 0.02:
            ammount_of_bullets = int(self.clip/2)
            startrange = -int(self.clip/2)
        
        for number in range(startrange,ammount_of_bullets):
            angles.append(number*spread)

        for angle_of_spread in angles:
            clicklocation = Vector(position[0],position[1])
            
            #calc where proj is going
            direction = clicklocation.subtract(self.pos.copy()).normalize()
            
            #each bullet will now be projected at a diffrent angle
            #it rotates it by a certain number of radians
            #this creates a spread
    
            rotated_direction = direction.rotate_rad(angle_of_spread)
                
            #added speed
            Velocity = rotated_direction.multiply(self.proj_speed)
        
            #creates a bullet infront of the gun
            self._init_barrel_exit()
            bullet = Projectile(self.pos.copy().add(self.barrel_ext),Velocity,self.damage)

            #changes bullet image's trajectory by getting the negative arctan of the velocity
            bullet.rotation = -math.atan2(Velocity.x,Velocity.y)
            list_of_bullets.append(bullet)

            Flash = MuzzleFlash(self.pos.copy().add(self.barrel_ext),(30*ammount_of_bullets,70))
            Flash.rotation = -math.atan2(Velocity.x,Velocity.y)
        
            list_of_bullets.append(Flash)
            self.shooting = True


class Marksman(Weapon):
    #this is a semi-auto gun that fires a 3 round burst
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)
    
        #pathing for gun sprites and sound
        self.image_path = os.path.join(SPRITESHEET_PATH, 'marksman_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'marksman.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.damage = 10

        self.size = (95,95)
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [6,0]

    def shoot(self,position,list_of_bullets):
        #this creates bullets and shoots them (shooting occurs in interact)
        for num in range(4,1,-1):
            direction = Vector(position[0],position[1]).subtract(self.pos.copy()).normalize()
            Velocity = direction.multiply(self.proj_speed)
        
            #creates a bullet infront of the gun
            self._init_barrel_exit()
            bullet = Projectile(self.pos.copy().add(self.barrel_ext.multiply(num/2)),Velocity)

            #changes bullet image's trajectory by getting the negative arctan of the velocity
            bullet.rotation = -math.atan2(Velocity.x,Velocity.y)
            list_of_bullets.append(bullet)

            if num == 2:
                Flash = MuzzleFlash(self.pos.copy().add(self.barrel_ext),(50,50))
                Flash.rotation = -math.atan2(Velocity.x,Velocity.y)
        
                list_of_bullets.append(Flash)
                self.shooting = True


class LaserRifle(Weapon):
    #this is a semi-auto gun that fires a 3 round burst
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)
    
        #pathing for gun sprites
        self.image_path = os.path.join(SPRITESHEET_PATH, 'LR_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'lazer.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self.size = (90,90)
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [8,0]

    def shoot(self,position,list_of_bullets):
        direction = Vector(position[0],position[1]).subtract(self.pos.copy()).normalize()
        Velocity = direction.multiply(self.proj_speed)
        
        #creates a bullet infront of the gun
        self._init_barrel_exit()
        laser = LaserBeam(self.pos.copy().add(self.barrel_ext),Velocity)

        #changes bullet image's trajectory by getting the negative arctan of the velocity
        laser.rotation = -math.atan2(Velocity.x,Velocity.y)
        list_of_bullets.append(laser)
        self.shooting = True


class Orbital(Weapon):
    #this is a special weapon that shoots an orbital blast from the top of the screen
    def __init__(self,pos,magsize,state):
        Weapon.__init__(self,pos,magsize,state)

        #pathing for gun sprites
        self.image_path = os.path.join(SPRITESHEET_PATH, 'orbital_spritesheet.png')
        sound_path = os.path.join(SOUND_FILE_PATH, 'orbital_blast.ogg')

        #the blast will have the sound not the gun
        self.sound = simplegui._load_local_sound(sound_path)
        self.blastsound = simplegui._load_local_sound(sound_path)

        self.size = (60,60)
        
        self._init_Image_dimension()
        self._init_barrel_exit()

        self.overlayindex = [7,0]

    def shoot(self,position,list_of_bullets):
        #this creates the orbital lazer
        #calc speed of projectile
        direction = Vector(position[0],position[1]).subtract(self.pos.copy())

        #creates an orbital lazer
        lazer = OrbitalLaser(Vector(position[0],position[1]))

        list_of_bullets.append(lazer)
        self.shooting = True

    def boss_shoot(self,playerposition,list_of_bullets):
        #this creates the orbital lazer for bosses
        #creates an orbital lazer 3

        for i in range(3):
            lazer = OrbitalLaser(Vector(playerposition[0],playerposition[1]).add(Vector(random.randint(-200,200),random.randint(-200,200))),sound = self.blastsound,damageplayer = True)
            list_of_bullets.append(lazer)

        self.shooting = True
