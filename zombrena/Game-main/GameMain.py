try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random, math
from ZombieAI import *
from GameWalls import *
from Weapons import *
from Player import *
from Vector import *
from Overlays import *
from ScientistBoss import *
from BigBoss import *
from ChargerBoss import *
from FinalBoss import *
import random

frame_count = 0
POINT = 0
pixelCount = 0

MaximumWave = 10
WaveCounter = 1  # counting waves
StopGame = False
GameStart = False
Show = True
ShowOverlay = False
enableNext = False
drawDead = False
ShowMenus = True
Won = False
enableESC = True

SOUND_FILE_PATH_MUSIC = os.path.join(os.getcwd(), "sounds")
main_menu_sound_path = os.path.join(SOUND_FILE_PATH_MUSIC, 'mainmenu.ogg')
normal_wave_sound_path = os.path.join(SOUND_FILE_PATH_MUSIC, 'normaltheme.ogg')
charger_wave_sound_path = os.path.join(SOUND_FILE_PATH_MUSIC, 'chargertheme.ogg')
tank_wave_sound_path = os.path.join(SOUND_FILE_PATH_MUSIC, 'tanktheme.ogg')
scientist_wave_sound_path = os.path.join(SOUND_FILE_PATH_MUSIC, 'scientisttheme.ogg')
finalboss_wave_sound_path = os.path.join(SOUND_FILE_PATH_MUSIC, 'finalboss.ogg')
death_sound_path = os.path.join(os.path.join(SOUND_FILE_PATH_MUSIC, 'deaththeme.ogg'))
winner_sound_path = os.path.join(os.path.join(SOUND_FILE_PATH_MUSIC, 'winnertheme.ogg'))


WIDTH, HEIGHT = 700, 700

SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")

# story
lore_book = os.path.join(SPRITESHEET_PATH, "LoreBook.png")
lore_book_image = simplegui.load_image('file:\\' + lore_book)

# main menu
main_menu = os.path.join(SPRITESHEET_PATH, "title_screen.png")
main_menu_image = simplegui.load_image('file:\\' + main_menu)

# instructions
book1 = os.path.join(SPRITESHEET_PATH, "BOOK1.png")
book1_image = simplegui.load_image('file:\\' + book1)

# gunbook
book2 = os.path.join(SPRITESHEET_PATH, 'BOOK2.png')
book2_image = simplegui.load_image('file:\\' + book2)

#deadscreen
deadscreen = os.path.join(SPRITESHEET_PATH, 'deathscreen.png')
deadscreen_image = simplegui.load_image('file:\\' + deadscreen)

# final win screen
winScreen = os.path.join(SPRITESHEET_PATH, "end_screen.png")
winScreen_image = simplegui.load_image('file:\\' + winScreen)

def draw(canvas, image):
    image_width = image.get_width()
    image_height = image.get_height()
    canvas.draw_image(image, (image_width // 2, image_height // 2),
                      (image_width, image_height), (350, 350), (700, 700))


class Interaction:

    def __init__(self, player, level, keyboard, floor, zombiesList, lowiqZombiesList, overlay, wavecounter,
                 healthbar, gunbar,bossbar):

        self.player = player
        self.level = level
        self.keyboard = keyboard
        self.floor = floor
        self.zombiesList = zombiesList
        self.lowiqZombiesList = lowiqZombiesList

        self.mainmenumusic = simplegui._load_local_sound(main_menu_sound_path)
        self.mainmenumusic.set_volume(0.3)
        self.wavemusic = simplegui._load_local_sound(normal_wave_sound_path)
        self.wavemusic.set_volume(0.3)
        self.chargermusic = simplegui._load_local_sound(charger_wave_sound_path)
        self.chargermusic.set_volume(0.3)
        self.tankmusic = simplegui._load_local_sound(tank_wave_sound_path)
        self.tankmusic.set_volume(0.3)
        self.finalbossmusic = simplegui._load_local_sound(finalboss_wave_sound_path)
        self.finalbossmusic.set_volume(0.3)
        self.deathmusic = simplegui._load_local_sound(death_sound_path)
        self.deathmusic.set_volume(0.3)
        self.scientistmusic = simplegui._load_local_sound(scientist_wave_sound_path)
        self.scientistmusic.set_volume(0.3)
        self.winnertheme = simplegui._load_local_sound(winner_sound_path)
        self.winnertheme.set_volume(0.3)

        self.showGunBook = False
        self.showInstructions = False
        self.showStory = False

        #gunlist
        self.gunlistCopy = gunlist.copy()        

        # overlays
        self.overlay = overlay
        self.wavecounter = wavecounter
        self.healthbar = healthbar
        self.gunbar = gunbar
        self.points = points
        self.bossbar = bossbar

        self.merged_zombie_list = []
        self.zombie_removal = []

        # playerhealth bar
        self.lasthit = 0

        #boss health
        self.normalWave = False
        self.spawnedboss = False
        self.boss = None
        self.boss2 = None

        #zombie spawnrate
        self.spawnrate = 100

        #Final boss objects
        self.tempBoss = FinalBoss(Vector(350, 55))
        self.FinalBoss = self.tempBoss
        self.LazerWall = LazerWall(350, 5, Vector(CANVAS_WIDTH / 2, 0))
        self.laserAttack = False
        self.growSize = True
        self.FinalBossRound = False
        self.FinalBossdead = False

        # player collision
        self.in_collision = False
        self.collision_timer = simplegui.create_timer(3000, self.end_collision)

        # gun attriutes
        self.primarygun = Pistol(self.player.pos.copy(), 17, "held")
        self.gunonfloor = gunlist[random.randint(0, len(gunlist) - 1)]
        self.list_of_bullets = []
        self.bullet_removal = []

        # swapping gun attributes
        self.swapnumber = 0
        self.canpickup = False
        self.swapped = False
        self.swaptimer = simplegui.create_timer(1500, self.swapdelay)

        self.mousepos = None


    def playTrack(self,track):
        # pauses all tracks currently playable, rewinds and plays given track
        self.mainmenumusic.pause()
        self.wavemusic.pause()
        self.chargermusic.pause()
        self.tankmusic.pause()
        self.finalbossmusic.pause()
        self.deathmusic.pause()
        self.scientistmusic.pause()
        self.winnertheme.pause()
        track.rewind()
        track.play()


    def click(self, pos):
        global GameStart
        x1, y1 = 445, 635
        x2, y2 = 695, 685
        # check if the instructions are shown or not
        # if so allow the player to click the position
        if self.showStory:
            if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                # Clicked on the box in instructions screen, move to gunbook
                self.showInstructions = True
                self.showStory = False
                if self.showInstructions:
                    pos = (0,0)
                    # to avoid accidentally set pos to 0,0 during the game (bug)
                    return
        if self.showInstructions:
            # if clicked, gunbook becomes True and instructions becomes False
            # position also becomes (0,0) to avoid not showing gunbook
            # when the co-ordinates of both screens are the same (300, 300, 400, 400)
            if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                # Clicked on the box in instructions screen, move to gunbook
                self.showGunBook = True
                self.showInstructions = False
                if self.showGunBook:
                    pos = (0,0)
                    # to avoid accidentally set pos to 0,0 during the game (bug)
                    return
        # if gunbook is true, allow the player to click the positions
        if self.showGunBook:
            if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                # Clicked on gunbook, start the game
                GameStart = True
                self.primarygun.fireratehandler.start()
                for i in range(0, len(gunlist)):
                    gunlist[i].fireratehandler.start()
                #start the timer only after all the screens are gone
                showZombieTimer.start()

                self.swaptimer.start()

                self.showGunBook = False
                # return so that the position of the click on the gun book
                # isn't registered as a gun shot until next click after gunbook
                return

        # if game starts, the player is not dead and it's not showing overlay
        # 1-> game should start before click
        # 2-> when the player is dead, click is not allowed to avoid shooting when he's dead
        # 3-> can shoot if not during overlays
        if GameStart and not self.keyboard.isDead and not ShowOverlay and not Won:
            self.primarygun.click(pos, self.list_of_bullets)

            self.mousepos = pos


    def try_move_player(self, direction):
        new_pos = self.player.pos.copy()
        new_pos.add(direction)

        # Stop the player from advencing when it hits the wall
        # When showing the overlay screen, stop the movement of the player
        if not ShowOverlay:
            if not self.level.hit(new_pos):
                self.player.pos = new_pos
            else:
                self.player.stop()
        else:
            self.player.stop()

    def try_move_zombie(self):
        for i in self.merged_zombie_list:
            if isinstance(i, ChargerBoss):
                if not self.level.hit(i.position):
                    i.update(self.player)
            elif isinstance(i, ScientistBoss):
                if not self.level.hit(i.position):
                    i.update(self.player, self.list_of_bullets)
                else:
                    i.updateteleport()
                    i.teleport(Vector(WIDTH / 2, HEIGHT / 2))
            else:
                if not self.level.hit(i.position) or self.level.try_hit(i.position):
                    i.update()

    def pickupgun(self):
        # method for picking up guns
        distance = self.player.pos.copy().subtract(self.gunonfloor.pos.copy()).length()

        if distance + self.player.pickupradius - self.gunonfloor.pickupradius <= self.gunonfloor.pickupradius and not self.swapped:
            gun1pos = self.primarygun.pos
            gun2pos = self.gunonfloor.pos

            self.gunonfloor.switchstate(gun1pos)
            self.primarygun.switchstate(gun2pos)
            self.tempgun = self.primarygun
            self.swapped = True
            return self.gunonfloor, self.primarygun

        return self.primarygun, self.gunonfloor

    def swapdelay(self):
        # provides a delay between pickup of the gun
        # every 2nd second it can pickup
        self.swapnumber += 1
        self.canpickup = self.swapnumber % 2 == 0
        if self.swapnumber % 2 == 0:
            self.swapped = False

    def find_degree_of_rotation(self, pos1, pos2):
        # takes 2 vectors and gets the rotational angle between
        direction = pos1.subtract(pos2)
        return -math.atan2(direction.x, direction.y)

    def end_collision(self):
        # end collision timer
        self.in_collision = False
        self.collision_timer.stop()

    def updatedamageplayer(self):
        if int(self.player.Hit) > self.lasthit:
            self.healthbar.frame_index[1] += 1

        self.lasthit = self.player.Hit


    def update(self):
        global ShowOverlay
        # if overlay screen is not shown move the player
        if not ShowOverlay:
            # adjusting gun placement on player
            if self.player.frame_index[1] == 1:
                pos = self.player.pos.copy().add(Vector(-10, 15))
            else:
                pos = self.player.pos.copy().add(Vector(10, 15))

            self.primarygun.pos = pos

            # adjusting health bar
            self.updatedamageplayer()

            # adjusting player rotation
            if self.mousepos != None:
                self.primarygun.update(self.mousepos)
                # updating player's rotation

                # finds angle between player and mouseclick
                gun_arc_degree = self.find_degree_of_rotation(Vector(self.mousepos[0], self.mousepos[1]),
                                                              self.player.pos.copy())
                self.player.player_rot(gun_arc_degree)

            # removing bullets
            for bullet in self.bullet_removal:
                for bullet2 in self.list_of_bullets:
                    if bullet == bullet2:
                        self.list_of_bullets.remove(bullet)

            # zombie rotation
            for rotate_zom in self.merged_zombie_list:
                if isinstance(rotate_zom, Zombie) or isinstance(rotate_zom, ScientistBoss):
                    # finds angle between zombie and player and rotates zombie acordingly
                    zom_arc_degree = self.find_degree_of_rotation(self.player.pos.copy(), rotate_zom.position.copy())
                    rotate_zom.rotate_self(zom_arc_degree)
                if isinstance(rotate_zom, TankBoss):
                    zom_arc_degree = self.find_degree_of_rotation(self.player.pos.copy(),
                                                                  rotate_zom.position.copy())
                    if 0 < rotate_zom.health <= 600:
                        rotate_zom.spritesheet.tankBossNearDeath_rot(zom_arc_degree)
                    elif 600 < rotate_zom.health <= 1200:
                        rotate_zom.spritesheet.tankBossHurt_rot(zom_arc_degree)
                    else:
                        rotate_zom.spritesheet.tankBossHealthy_rot(zom_arc_degree)

            # zombie removal
            for zombie in self.zombie_removal:
                for zombie2 in self.merged_zombie_list:
                    if zombie == zombie2:
                        if isinstance(zombie, LowIQZombie):
                            self.lowiqZombiesList.remove(zombie)
                        elif isinstance(zombie, Zombie):
                            self.zombiesList.remove(zombie)
                        else:
                            self.zombiesList.remove(zombie)

                        self.merged_zombie_list.remove(zombie)

            #healthbar updating
            if self.boss != None:
                self.bosshealth = self.boss.health
                if self.boss2 != None:
                    self.bosseshealth = (self.boss.health,self.boss2.health)

            if self.FinalBossRound and not self.FinalBossdead:
                #Final BOSS ATTACK
                if self.laserAttack == True:
                    self.FinalBoss.spritesheet.frame_index[0] = 1
                    self.LazerWall.update()
                    leftside = self.LazerWall.x - self.LazerWall.border
                    rightside = self.LazerWall.x + self.LazerWall.border
                    if (self.player.pos.x + self.player.pickupradius >= leftside) and (
                        self.player.pos.x - self.player.pickupradius <= rightside):
                        if not self.in_collision and not ShowOverlay:
                            self.in_collision = True
                            self.player.setSound()
                            self.player.Hit += 1
                            self.collision_timer.start()
                    
                    if (self.LazerWall.spritesheetLaser.dest_size_y < 2500 and self.growSize):
                        self.LazerWall.spritesheetLaser.dest_size_y += 70
                    if (self.LazerWall.spritesheetLaser.dest_size_y > 2500):
                        self.growSize = False
                    if (self.growSize == False):
                        self.LazerWall.spritesheetLaser.dest_size_x -= 1
                        if self.LazerWall.spritesheetLaser.dest_size_x <= 100:
                            self.LazerWall.spritesheetLaser.dest_size_x = random.randint(150,200)
                            self.LazerWall.spritesheetLaser.dest_size_y = 150
                            self.laserAttack = False
                            self.growSize = True
                            self.FinalBoss.spritesheet.frame_index[0] = 0

                #every 3.3 seconds it attacks with lazer
                if self.FinalBoss.attacktimer % 200 == 0:
                    self.laserAttack = True

                if self.FinalBoss.health < 0:
                    #kills final boss
                    del self.FinalBoss
                    self.FinalBossdead = True

            # picking up guns from floor
            if self.canpickup:
                self.primarygun, self.gunonfloor = self.pickupgun()

            # updating player location and sprite
            if self.keyboard.right:
                self.try_move_player(Vector(2, 0))

            elif self.keyboard.left:
                self.try_move_player(Vector(-2, 0))

            if self.keyboard.up:
                self.try_move_player(Vector(0, -2))

            elif self.keyboard.down:
                self.try_move_player(Vector(0, 2))

            # With space
            if self.keyboard.right and self.keyboard.space:
                self.try_move_player(Vector(2, 0))

            elif self.keyboard.left and self.keyboard.space:
                self.try_move_player(Vector(-2, 0))

            if self.keyboard.up and self.keyboard.space:
                self.try_move_player(Vector(0, -2))

            elif self.keyboard.down and self.keyboard.space:
                self.try_move_player(Vector(0, 2))

            # check the player is moving to run animations
            if self.keyboard.right or self.keyboard.left or self.keyboard.up or self.keyboard.down:
                self.player.ismoving = True
            else:
                self.player.ismoving = False

            self.try_move_zombie()

            # player animation
            global STEP, StopGame, enableNext, enableESC
            if STEP != 0:
                self.player.frame_clock += 1

            if self.player.frame_clock % self.player.frame_duration == 0 and self.player.ismoving:
                self.player.update_index()
            elif not self.player.ismoving:
                self.player.frame_index[0] = 0

            if self.player.Hit >= 3:
                # deals with player death and animation of the sprite
                self.keyboard.isDead = True
                enableESC = False
                # stop the game and kill all zombies
                StopGame = True
                ShowOverlay = False
                enableNext = False
                self.killAllZombies()

                if self.keyboard.isLeft:
                    self.player.frame_index[1] = 3
                else:
                    self.player.frame_index[1] = 2

                if self.player.deadcount < 60:
                    # moves the player a little when they die
                    if not self.keyboard.isLeft:
                        self.player.frame_index[1] = 2
                    else:
                        self.player.frame_index[1] = 3

                    self.player.deadcount += 1
                    self.player.frame_clock += 1
                    self.player.vel.multiply(0)

                    if self.player.frame_clock % self.player.frame_duration == 0:
                        self.player.update_index()
                    else:
                        self.player.vel.multiply(0)
                        self.player.frame_index[0] = 3

    def reset_game(self):
        global GameStart, Show, ShowOverlay, WaveCounter, StopGame, enableNext, drawDead, ShowMenus, Won, enableESC

        # reset these to False
        self.showGunBook = False
        self.showInstructions = False
        self.showStory = False

        #resets the gun objects
        self.gunlistCopy = gunlist.copy()
        
        enableESC = True
        Won = False
        GameStart = False
        Show = True
        ShowOverlay = False
        
        #this is reseting the points
        self.points.numbers = Numbers((225, 120))
        
        WaveCounter = 1
        StopGame = False
        enableNext = False
        drawDead = False
        ShowMenus = True
        # reset player's position
        self.player.pos = Vector(300, 100)
        # reset player's spritesheet to [0, 0]
        self.player.frame_index = [0, 0]
        # dead becomes false when reset
        self.keyboard.isDead = False
        # reset Hit = 0
        self.player.Hit = 0
        self.healthbar.frame_index[1] = 0
        self.lasthit = 0

        #resets boss health
        self.boss = None
        self.boss2 = None

        #resets spawnrate for zombies
        self.spawnrate = 100
        
        #resets finalboss
        self.FinalBossdead = False
        self.FinalBossRound = False
        self.FinalBoss = self.tempBoss 
        

        # restart the wave counter
        self.wavecounter.frame_index = [0, 0]
        self.primarygun = Pistol(self.player.pos.copy(), 17, "held")
        self.gunonfloor = gunlist[random.randint(0, len(gunlist) - 1)]
        self.primarygun.fireratehandler.start()
        self.gunonfloor.fireratehandler.start()

        #re-start timers for all guns
        for i in range(0, len(gunlist)):
            gunlist[i].fireratehandler.start()

        self.killAllZombies()
        showZombieTimer.stop()


    def stopTimers(self):
        # stopping gun timers
        for i in range(0, len(gunlist)):
            gunlist[i].fireratehandler.stop()

        # stop zombie timer
        deadTimer.stop()
        showZombieTimer.stop()
        self.swaptimer.stop()
        self.playTrack(self.mainmenumusic)
        # stop gun timers
        self.primarygun.fireratehandler.stop()
        self.gunonfloor.fireratehandler.stop()

    def draw(self, canvas):
        # Starting Screen
        global GameStart, Show, ShowOverlay, Won, frame_count, POINT, enableESC

        # if player is alive (ie. start game)
        if not self.keyboard.isDead:
            draw(canvas, main_menu_image)
            if self.showStory and not Won:
                draw(canvas, lore_book_image)
            if self.showInstructions and not Won:
                draw(canvas, book1_image)
            if self.showGunBook and not Won:
                draw(canvas, book2_image)
            if Won:
                self.list_of_bullets.clear()
                draw(canvas, winScreen_image)

        elif self.keyboard.isDead:
            deadTimer.start()
            #esc is set to False to avoid looping starting screen
            # if the user click 'esc' when the player is dying
            enableESC = False
            if drawDead:
                self.draw_dead_screen(canvas)
                deadTimer.stop()
                enableESC = True

        # if quit and esc is enabled
        if self.keyboard.quit and enableESC:
            self.list_of_bullets.clear()
            self.stopTimers()
            self.restoreBrokenWalls()
            self.showZombieHandler()
            self.reset_game()

            if self.keyboard.space:
                self.showStory = True
                self.keyboard.quit = False

        if self.keyboard.space:
            self.showStory = True

        if GameStart and not self.keyboard.quit and not drawDead and not Won:
            ShowMenus = False
            self.update()

            # floor and zombies first
            self.floor.draw(canvas)
            self.gunonfloor.draw(canvas)

            # timer starts and then zombie comes out
            if Show and not StopGame and showZombieTimer.is_running():
                self.merged_zombie_list = self.lowiqZombiesList + self.zombiesList
                for zombie in self.merged_zombie_list:
                    zombie.draw(canvas)
                    if isinstance(zombie, ChargerBoss):
                        zombie.update(self.player)
                        global STEP
                        if STEP != 0:
                            zombie.spritesheet.frame_clock += 1
                        if zombie.spritesheet.frame_clock % zombie.spritesheet.frame_duration == 0:
                            zombie.spritesheet.update_index()

                        zom_arc_degree = self.find_degree_of_rotation(zombie.pre_player_position.copy(),
                                                                      zombie.position.copy())
                        zombie.spritesheet.chargerBoss_rot(zom_arc_degree)

                    elif not isinstance(zombie, ScientistBoss):
                        if not isinstance(zombie,FinalBoss):
                            # if its a normal zombe
                            zombie.update()

                    if isinstance(zombie, Zombie):
                        zombie.followPlayer(self.player.pos)
                    if isinstance(zombie, TankBoss):
                        zombie.followPlayer(self.player.pos)

                    if self.player.hit(zombie):
                        # if not showing overlay play the sound
                        # if showing overlay, don't play the sound & not get hit
                        if not self.in_collision:
                            self.in_collision = True
                            self.player.setSound()
                            self.player.Hit += 1
                            self.collision_timer.start()

                    if zombie.health < 0:
                        self.zombie_removal.append(zombie)
                        self.points.increment()
                        if isinstance(zombie,ScientistBoss):
                            self.rareorbital()

                # spawn frames
                if frame_count % self.spawnrate == 0:
                    spawnZombie()
                if frame_count % 200 == 0:
                    spawnLowiqZombie()

                # new boss if even wave
                if (self.wavecounter.frame_index[0] + 1) % 2 == 0 and not self.spawnedboss:
                    self.spawnboss()
                    self.spawnedboss = True
                elif (self.wavecounter.frame_index[0] + 1) % 2 != 0 and not self.normalWave:
                    self.normalWave = True
                    self.playTrack(self.wavemusic)

                frame_count += 1

            # draws level last and player last
            self.level.draw(canvas)
            self.player.draw(canvas, self.player.pos.get_p())
            self.player.update()
            self.primarygun.draw(canvas)

            if self.FinalBossRound and not self.FinalBossdead:
                #checks if its final round and its not dead
                self.LazerWall.draw(canvas)
                self.FinalBoss.draw(canvas)
                self.FinalBoss.update(self.player.pos)

                if self.player.hit(self.FinalBoss) or self.player.hit(self.FinalBoss.leftarm) or self.player.hit(self.FinalBoss.rightarm):
                    # if not showing overlay play the sound
                    # if showing overlay, don't play the sound & not get hit
                    if not self.in_collision and not ShowOverlay:
                        self.in_collision = True
                        self.player.setSound()
                        self.player.Hit += 1
                        self.collision_timer.start()

            # finally draw overlays
            self.draw_point(canvas)
            self.draw_wave(canvas)
            self.healthbar.draw(canvas)
            self.drawgunbar(canvas)

            #draws boss healthbar
            if (self.wavecounter.frame_index[0] + 1) % 2 == 0 and self.spawnedboss:
                if (self.wavecounter.frame_index[0] + 1) != 8:
                    self.bossbar.draw(canvas,self.bosshealth,self.maxbosshealth)
                else:
                    self.bossbar.draw_multiple(canvas,self.bosseshealth,self.maxbosseshealth)

            # check wave count to avoid flashing of overlay screen at the end
            if not self.wavecounter.frame_index[0] > MaximumWave - 1 and ShowOverlay:
                # delete all bullets when the overlay is shown
                self.list_of_bullets.clear()
                self.overlay.draw_handler(canvas)

        # important code that only draws them and then updates them once
        # updates and also checks for bullet deletion
        for bullet in self.list_of_bullets:
            bullet.draw(canvas)
            bullet.update()

            # if the bullet is a muzzleflash instantly remove it
            if isinstance(bullet, MuzzleFlash):
                if bullet.timer % 5 == 0:
                    self.bullet_removal.append(bullet)

            # removes bullets that are offscreen
            if (bullet.pos.get_p()[0] > WIDTH) or (bullet.pos.get_p()[1] > HEIGHT):
                self.bullet_removal.append(bullet)

            # removes bullets that have timers
            if hasattr(bullet, "orbitaltimer"):
                # runs for 1 seconds if orbital laser
                if bullet.orbitaltimer % 50 == 0:
                    self.bullet_removal.append(bullet)

            if hasattr(bullet, "damageplayer"):
                if bullet.damageplayer:
                    if self.player.lazer_hit(bullet):
                        if not self.in_collision:
                            self.player.setSound()
                            # scentist's lazer hit palyer
                            self.player.Hit += 0.15
                            self.collision_timer.start()

            if hasattr(bullet, "lasertimer"):
                # runs for 0.5 seconds if orbital laser
                if bullet.lasertimer % 30 == 0:
                    self.bullet_removal.append(bullet)

            # hitting the zombie mechanic
            if self.merged_zombie_list != None:
                for zombie in self.merged_zombie_list:
                    # if it isnt a muzzleflash
                    if not isinstance(bullet, MuzzleFlash) and (not hasattr(bullet, "damageplayer")) or (
                            hasattr(bullet, "damageplayer") and bullet.damageplayer == False):
                        if zombie.hit(bullet):
                            zombie.hurt(bullet.dmg)
                            zombie.knockback(bullet)

                            if not isinstance(bullet, OrbitalLaser):
                                self.bullet_removal.append(bullet)

            #special exception for hitting final boss
            if self.FinalBossRound and not self.FinalBossdead:
                if not isinstance(bullet, MuzzleFlash) and (not hasattr(bullet, "damageplayer")) or (
                            hasattr(bullet, "damageplayer") and bullet.damageplayer == False):
                    if self.FinalBoss.hit(bullet):
                        self.FinalBoss.hurt(bullet.dmg)
                        self.FinalBoss.knockback(bullet)

                    #can dmg the hands
                    if self.FinalBoss.rightarm.hit(bullet):
                        self.FinalBoss.hurt(bullet.dmg)
                        self.FinalBoss.knockback(bullet)
                        
                    if self.FinalBoss.leftarm.hit(bullet):
                        self.FinalBoss.hurt(bullet.dmg)
                        self.FinalBoss.knockback(bullet)

            # bullets hitting the wall and get removed
            # try_hit (bullet can damage the wall)
            if self.level.hit(bullet.pos) and not self.level.try_hit(bullet.pos) and not isinstance(bullet,
                                                                                                    OrbitalLaser):
                self.bullet_removal.append(bullet)

            # if after all checks are done the bullet will delete after 5 seconds
            if not isinstance(bullet, MuzzleFlash) and not isinstance(bullet,
                                                                      OrbitalLaser) and bullet.duration % 300 == 0:
                self.bullet_removal.append(bullet)

    def showZombieHandler(self):
        global Show, MaximumWave, GameStart, StopGame, ShowOverlay, enableNext, Won

        if GameStart and not StopGame:
            Show = False
            ShowOverlay = True
            showZombieTimer.stop()
            self.wavecounter.frame_index[0] += 1
            self.killAllZombies()

            #increases zombies
            self.addmorezombies()

            if self.wavecounter.frame_index[0] > MaximumWave - 1:
                ShowOverlay = False
                # Stop the timers after the maximum cycles
                showZombieTimer.stop()
                StopGame = True
                enableNext = False
                Won = True
                self.playTrack(self.winnertheme)
                
            self.spawnedboss = False
            self.normalWave = False

        enableNext = True

    def deadTimeHandler(self):
        global drawDead
        drawDead = True
        self.playTrack(self.deathmusic)

    def spawnboss(self):
        # spawns bosses, plays their theme song
        if not self.spawnedboss:
            if (self.wavecounter.frame_index[0] + 1) == 2:
                self.playTrack(self.tankmusic)
                self.boss = TankBoss(Vector(350, 350))
                self.zombiesList.append(self.boss)
    
                #boss health values
                self.bosshealth = self.boss.health
                self.maxbosshealth = self.boss.health
            
            elif (self.wavecounter.frame_index[0] + 1) == 4:
                self.playTrack(self.chargermusic)
    
                self.boss = ChargerBoss(Vector(350, 350))
                self.zombiesList.append(self.boss)

                #boss health values
                self.bosshealth = self.boss.health
                self.maxbosshealth = self.boss.health
            
            elif(self.wavecounter.frame_index[0] + 1) == 6:
                self.playTrack(self.scientistmusic)
            
                self.boss = ScientistBoss(Vector(WIDTH / 2, HEIGHT / 2))
                self.zombiesList.append(self.boss)

                #boss health values
                self.bosshealth = self.boss.health
                self.maxbosshealth = self.boss.health

            
            elif(self.wavecounter.frame_index[0] + 1) == 8:
                self.playTrack(self.tankmusic)

                self.boss = TankBoss(Vector(350, 350))
                self.boss2 = ChargerBoss(Vector(350, 350))
            
                self.zombiesList.append(self.boss)
                self.zombiesList.append(self.boss2)

                #boss health values
                self.bosseshealth = (self.boss.health,self.boss2.health)
                self.maxbosseshealth = (self.boss.health,self.boss2.health)
            
            elif(self.wavecounter.frame_index[0] + 1) == 10:
                self.playTrack(self.finalbossmusic)

                self.FinalBossRound = True

                self.boss = self.FinalBoss
                self.bosshealth = self.boss.health
                self.maxbosshealth = self.boss.health

    def killAllZombies(self):
        for zombie in self.zombiesList:
            self.zombiesList.clear()
            self.merged_zombie_list.clear()
        for zombie in self.lowiqZombiesList:
            self.lowiqZombiesList.clear()
            self.merged_zombie_list.clear()

    def buttonHandler(self):
        global Show, ShowOverlay, enableNext, GameStart, Won
        Show = True
        ShowOverlay = False
        showZombieTimer.start()
        # make a copy of gunlist so that the real
        # items in gunlist is not removed top prevent error after victory and reset
        # where gunlist has 0 items
        
        if enableNext:
            self.restoreBrokenWalls()
            # new gun every wave
            # check if gunlist is empty or not (for wave 10)
            if self.gunlistCopy:
                gun = self.gunlistCopy[random.randint(0, len(self.gunlistCopy) - 1)]
                self.gunlistCopy.remove(gun)
                self.gunonfloor = gun
            enableNext = False

    def restoreBrokenWalls(self):
        for i in range(0, 10):  # rows
            for j in range(0, 10):  # columns
                if self.level.hit_count[i][j] > 0:
                    self.level.hit_count[i][j] = 0


    def addmorezombies(self):
        self.spawnrate -= 9

    def rareorbital(self):
        if random.random() < 0.20:
            self.gunonfloor = Orbital(Vector(WIDTH / 2, HEIGHT / 2), 3, "dropped")

    def draw_point(self, canvas):
        self.points.draw(canvas)
        

    def draw_wave(self, canvas):
        self.wavecounter.draw(canvas)

    def draw_home(self, canvas):
        canvas.draw_text("PRESS SPACE TO START", (WIDTH // 2 - 150, HEIGHT / 2), 30, "Red")

    def draw_dead_screen(self, canvas):
        draw(canvas,deadscreen_image)

    def drawgunbar(self, canvas):
        self.gunbar.frame_index = self.primarygun.overlayindex
        self.gunbar.draw(canvas)


# frame
frame = simplegui.create_frame("ZOMBRENA", WIDTH, HEIGHT)

# floor and level
floor = Floor(LEVEL_GRID)
brokenCell = BrokenGlass(LEVEL_GRID)
level = Level(LEVEL_GRID, brokenCell)

# list of guns that the player can aquire
gunlist = [
    Shotgun(Vector(WIDTH / 2, HEIGHT / 2), 2, "dropped"),
    PipeRevolver(Vector(WIDTH / 2, HEIGHT / 2), 6, "dropped"),
    PipeRifle(Vector(WIDTH / 2, HEIGHT / 2), 30, "dropped"),
    Revolver(Vector(WIDTH / 2, HEIGHT / 2), 6, "dropped"),
    Marksman(Vector(WIDTH / 2, HEIGHT / 2), 60, "dropped"),
    Pistolx4(Vector(WIDTH / 2, HEIGHT / 2), 17 * 4, "dropped"),
    LaserRifle(Vector(WIDTH / 2, HEIGHT / 2), 30, "dropped"), ]

# overlays
wavecounter = Wavecounter()
overlay = Overlay()
healthbar = Healthbar()
gunbar = GunBar()
points = Points()
bossbar = BossBar()

# charcters and keyboard
keyboard = Keyboard()
character = Player(Vector(300, 100),SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS, 10)

interaction = Interaction(character, level, keyboard, floor, zombiesList, lowiqZombiesList, overlay, wavecounter,
                          healthbar, gunbar,bossbar)

# frame sets
frame.set_draw_handler(interaction.draw)
frame.set_keyup_handler(keyboard.keyUp)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_mouseclick_handler(interaction.click)

# timers
showZombieTimer = simplegui.create_timer(30000, interaction.showZombieHandler)
deadTimer = simplegui.create_timer(2000, interaction.deadTimeHandler)

# add a button before the start of the wave to start the wave
if not StopGame:
    nextButton = frame.add_button('Next', interaction.buttonHandler)

interaction.playTrack(interaction.mainmenumusic)
frame.start()



