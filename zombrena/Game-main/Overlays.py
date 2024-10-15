try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os

spritesheetsPath = os.path.join(os.getcwd(), "spritesheets")
overlayURL = os.path.join(spritesheetsPath, "overlay2.png")
counterurl = os.path.join(spritesheetsPath, "wavecounter.png")
barurl = os.path.join(spritesheetsPath, "healthbar.png")
gunbarurl = os.path.join(spritesheetsPath, "gunsoverlay.png")
numurl = os.path.join(spritesheetsPath, "numbers.png")
pointnoteurl = os.path.join(spritesheetsPath, "zombskill.png")
bossbarurl = os.path.join(spritesheetsPath, "BossBar.png")

overlay = simplegui.load_image('file:\\' + overlayURL)
counter = simplegui.load_image('file:\\' + counterurl)
healthbr = simplegui.load_image('file:\\' + barurl)
gunbr = simplegui.load_image('file:\\' + gunbarurl)
numbr = simplegui.load_image('file:\\' + numurl)
pointnote = simplegui.load_image('file:\\' + pointnoteurl)
bossbr = simplegui.load_image('file:\\' + bossbarurl)


class Overlay:
    def draw_handler(self, canvas):
        canvas.draw_image(overlay, (32, 32), (64, 64), (350, 350), (700, 700))


class Numbers:
    #class for various numbers in the game
    def __init__(self,centre):
        self.frame_index = [0,0]
        self.image = numbr
        self._init_Image_dimension()
        self.centre = centre
        self.nextnumber = None

    def _init_Image_dimension(self):
        #usual image loading
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        self.frame_width = self.image.get_width() //10
        self.frame_height = self.image.get_height() 
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
    
    def draw(self, canvas):
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (self.frame_width,self.frame_height)
        
        canvas.draw_image(numbr, source_centre,source_size,self.centre, (16, 16))
        
        if self.nextnumber != None:
            self.nextnumber.draw(canvas)

    def increment(self):
        self.frame_index[0] += 1
        if self.frame_index[0] >= 10:
            self.frame_index[0] = 0
            if self.nextnumber == None:
                self.nextnumber = Numbers((self.centre[0]-11,self.centre[1]))
                self.nextnumber.increment()
            else:
                self.nextnumber.increment()

    def decrement(self):
        self.frame_index[0] += 1
        if self.frame_index[0] >= 10:
            self.frame_index[0] = 0
            if self.nextnumber == None:
                self.nextnumber = Numbers((self.centre[0]-11,self.centre[1]))
                self.nextnumber.increment()
            else:
                self.nextnumber.increment()


class Points:
    def __init__(self):
        self.frame_index = [0,0]
        self.image = pointnote
        self.numbers = Numbers((225, 120))
        self._init_Image_dimension()

    def _init_Image_dimension(self):
        #usual image loading
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        self.frame_width = self.image.get_width() 
        self.frame_height = self.image.get_height() 
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
    def draw(self, canvas):
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (self.frame_width,self.frame_height)
        
        canvas.draw_image(pointnote, source_centre,source_size,(200, 100), (75, 75))
        
        self.numbers.draw(canvas)

    def increment(self):
        self.numbers.increment()


class BossBar:
    def __init__(self):
        self.frame_index = [0,0]
        self.image = bossbr
        self._init_Image_dimension()

    def _init_Image_dimension(self):
        #usual image loading
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        self.frame_width = self.image.get_width() 
        self.frame_height = self.image.get_height() 
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
    def draw(self, canvas,health,max_health):
        #for 1 health bar
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (self.frame_width,self.frame_height)
        
        canvas.draw_image(bossbr, source_centre,source_size,(600,600), (80, 80))
        self.draw_health(canvas,health,max_health)

    def draw_multiple(self, canvas,health,max_health):
        #for multiple
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (self.frame_width,self.frame_height)
        
        canvas.draw_image(bossbr, source_centre,source_size,(600,600), (80, 80))
        pos = 620
        for num in range(len(health)):
            pos -= 7
            self.draw_health(canvas,health[num],max_health[num],pos)

    def draw_health(self,canvas,health,max_health,pos = 620):
        scale_factor =  60 / max_health
        if health > 0:
            bar_length = min(health * scale_factor,60)
        else:
            bar_length = 0
    
        canvas.draw_line((570, pos), (630, pos), 5, "Gray")
    
        canvas.draw_line((570, pos), (570 + bar_length, pos), 5, "Red")


class GunBar:
    def __init__(self):
        self.frame_index = [0,0]
        self.image = gunbr
        self._init_Image_dimension()

    def _init_Image_dimension(self):
        #usual image loading
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        self.frame_width = self.image.get_width() //9
        self.frame_height = self.image.get_height() 
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
    def draw(self, canvas):
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (self.frame_width,self.frame_height)
        canvas.draw_image(gunbr, source_centre,source_size,(130,600), (75, 75))
    

class Healthbar:
    def __init__(self):
        self.frame_index = [0,0]
        self.image = healthbr
        self._init_Image_dimension()

    def _init_Image_dimension(self):
        #usual image loading
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        self.frame_width = self.image.get_width() 
        self.frame_height = self.image.get_height() /4
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
    def draw(self, canvas):
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (192,64)
        canvas.draw_image(healthbr, source_centre,source_size,(550, 100), (75*3, 75))


class Wavecounter:
    def __init__(self):
        self.frame_index = [0,0]
        self.image= counter
        self._init_Image_dimension()

    def _init_Image_dimension(self):
        #usual image loading
        self.image_centre = (self.image.get_width()/2,self.image.get_height()/2)
        self.image_dims = (self.image.get_width(),self.image.get_height())

        
        self.frame_width = self.image.get_width() / 10
        self.frame_height = self.image.get_height() 
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
    
    def draw(self, canvas):
        source_centre = (self.frame_width*self.frame_index[0]+self.frame_centre_x,
                         self.frame_height*self.frame_index[1]+self.frame_centre_y)
        source_size = (64,64)
        canvas.draw_image(counter, source_centre, source_size, (130, 100), (75, 75))

