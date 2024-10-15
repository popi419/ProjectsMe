try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Vector import Vector
import random
import os

SPRITESHEET_PATH = os.path.join(os.getcwd(), "spritesheets")
WALL_SHEET_URL = os.path.join(SPRITESHEET_PATH, "glass_walls.png")
FLOOR_SHEET_URL = os.path.join(SPRITESHEET_PATH, "floor.png")

SOUND_FILE_PATH = os.path.join(os.getcwd(), "sounds")

WIDTH = 700
HEIGHT = 700
WALL = 2
WALL_COLOR = "blue"
LEVEL_GRID = [
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [4, 9, 9, 9, 9, 9, 9, 9, 9, 8],
    [5, 6, 6, 6, 6, 6, 6, 6, 6, 7]
]

INITIAL_FRAME_LEVEL = [0, 0]
INITIAL_FRAME_GLASS = [0, 0]

wall_image = simplegui.load_image('file:\\' + WALL_SHEET_URL)
floor_image = simplegui.load_image('file:\\' + FLOOR_SHEET_URL)

def get_dimension_width(image):
    width = image.get_width()
    return width

def get_dimension_height(image):
    height = image.get_height()
    return height

WALL_SHEET_WIDTH = get_dimension_width(wall_image)
WALL_SHEET_HEIGHT = get_dimension_height(wall_image)
FLOOR_SHEET_WIDTH = get_dimension_width(floor_image)
FLOOR_SHEET_HEIGHT = get_dimension_height(floor_image)

class Floor:
    def __init__(self, grid):
        self.grid = grid
        self.grid_height = len(grid)
        self.grid_width = len(grid[0])
        self.cell_width = WIDTH // self.grid_width
        self.cell_height = HEIGHT // self.grid_height

        self._init_dimension()
        self.initial_frame = (0, 0)

    def _init_dimension(self):
        self.frame_width = FLOOR_SHEET_WIDTH / 1
        self.frame_height = FLOOR_SHEET_HEIGHT / 1
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def draw_floor(self, grid_x, grid_y, canvas):
        start_x = grid_x * self.cell_width
        end_x = start_x + self.cell_width
        centre_y = grid_y * self.cell_height + self.cell_height // 2

        source_center = (self.frame_width * self.initial_frame[0] + self.frame_centre_x,
                         self.frame_height * self.initial_frame[1] + self.frame_centre_y)

        source_size = (self.frame_width, self.frame_height)
        dest_center = ((start_x + end_x) // 2, centre_y)
        dest_size = (self.cell_width, self.cell_height)

        canvas.draw_image(floor_image, source_center, source_size, dest_center, dest_size)

    def draw(self, canvas):
        for grid_y in range(self.grid_height):
            for grid_x in range(self.grid_width):
                    self.draw_floor(grid_x, grid_y, canvas)

class Level:
    def __init__(self, grid, broken):
        self.grid = grid
        self.grid_height = len(grid)
        self.grid_width = len(grid[0])
        self.cell_width = WIDTH // self.grid_width
        self.cell_height = HEIGHT // self.grid_height
        self.broken = broken

        self._init_dimension()
        # record which part of the wall has been hit
        self.hit_count = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        # record which part of the wall has broken (1: broken, 0: not broken)
        self.sound_effect = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def try_hit(self, pos):
        grid_x = int(pos.x // self.cell_width)
        grid_y = int(pos.y // self.cell_height)
        hit = 0
        if self.is_wall(grid_x, grid_y):
            self.hit_count[grid_x][grid_y] += (1/15)
            # if hit_count is larger or equal to 3, break it
            if self.hit_count[grid_y][grid_x] >= 3:
                grid = self.grid[grid_y][grid_x]
                grid = 0
                return True
        else:
            return False

    def hit(self, pos):
        grid_x = int(pos.x // self.cell_width)
        grid_y = int(pos.y // self.cell_height)
        return self.is_wall(grid_x, grid_y)

    def is_wall(self, grid_x, grid_y):
        if grid_x < 0 or grid_x >= self.grid_width or grid_y < 0 or grid_y >= self.grid_height:
            return False
        # checking if it's wall, floor or corner
        # if it's wall it's divisible by 2 according to the LEVEL_GRID
        return self.grid[grid_y][grid_x] % 2 == 0

    def _init_dimension(self):
        self.frame_width = 64
        self.frame_height = 64
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    # associating the grid of the sprite image with the wall grid
    def _init_frames(self, grid_x, grid_y):
        global INITIAL_FRAME_LEVEL
        if self.grid[grid_y][grid_x] == 1:
            INITIAL_FRAME_LEVEL = [0, 0]
        elif self.grid[grid_y][grid_x] == 2:
            INITIAL_FRAME_LEVEL = [1, 0]
        elif self.grid[grid_y][grid_x] == 3:
            INITIAL_FRAME_LEVEL = [2, 0]
        elif self.grid[grid_y][grid_x] == 4:
            INITIAL_FRAME_LEVEL = [0, 1]
        elif self.grid[grid_y][grid_x] == 5:
            INITIAL_FRAME_LEVEL = [0, 2]
        elif self.grid[grid_y][grid_x] == 6:
            INITIAL_FRAME_LEVEL = [1, 2]
        elif self.grid[grid_y][grid_x] == 7:
            INITIAL_FRAME_LEVEL = [2, 2]
        elif self.grid[grid_y][grid_x] == 8:
            INITIAL_FRAME_LEVEL = [2, 1]
        elif self.grid[grid_y][grid_x] == 9:
            INITIAL_FRAME_LEVEL = [1, 1]

    def draw_cell(self, grid_x, grid_y, canvas):
        self._init_frames(grid_x, grid_y)

        if self.hit_count[grid_x][grid_y] < 3:
            start_x = grid_x * self.cell_width
            end_x = start_x + self.cell_width
            centre_y = grid_y * self.cell_height + self.cell_height // 2

            source_center = (self.frame_width * INITIAL_FRAME_LEVEL[0] + self.frame_centre_x,
                             self.frame_height * INITIAL_FRAME_LEVEL[1] + self.frame_centre_y)

            source_size = (self.frame_width, self.frame_height)
            dest_center = ((start_x + end_x) // 2, centre_y)
            dest_size = (self.cell_width, self.cell_height)

            canvas.draw_image(wall_image, source_center, source_size, dest_center, dest_size)
        # if the hit on the wall is more than 3, break it
        elif self.hit_count[grid_x][grid_y] >= 3:
            self.broken.draw_cell(grid_x, grid_y, canvas)
            if self.sound_effect[grid_x][grid_y] == 0:
                # if 0, not broken yet so make a sound
                self.broken.setSound()
                # update the wall to be broken and already made a sound
                # so that it won't make sound next time
                self.sound_effect[grid_x][grid_y] = 1

    def draw(self, canvas):
        for grid_y in range(self.grid_height):
            for grid_x in range(self.grid_width):
                self.draw_cell(grid_x, grid_y, canvas)

class BrokenGlass:
    def __init__(self, grid):
        self.grid = grid
        self.grid_height = len(grid)
        self.grid_width = len(grid[0])
        self.cell_width = WIDTH // self.grid_width
        self.cell_height = HEIGHT // self.grid_height

        sound_path = os.path.join(SOUND_FILE_PATH, 'Smashing_Glass.ogg')
        self.sound = simplegui._load_local_sound(sound_path)

        self._init_dimension()

    def setSound(self):
        self.sound.set_volume(0.1)
        self.sound.rewind()
        self.sound.play()

    def _init_dimension(self):
        self.frame_width = 64
        self.frame_height = 64
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    # associating the grid of the sprite image with the wall grid
    def _init_frames(self, grid_x, grid_y):
        global INITIAL_FRAME_GLASS
        if self.grid[grid_y][grid_x] == 1:
            INITIAL_FRAME_GLASS = [3, 0]
        elif self.grid[grid_y][grid_x] == 2:
            INITIAL_FRAME_GLASS = [4, 0]
        elif self.grid[grid_y][grid_x] == 3:
            INITIAL_FRAME_GLASS = [5, 0]
        elif self.grid[grid_y][grid_x] == 4:
            INITIAL_FRAME_GLASS = [3, 1]
        elif self.grid[grid_y][grid_x] == 5:
            INITIAL_FRAME_GLASS = [3, 2]
        elif self.grid[grid_y][grid_x] == 6:
            INITIAL_FRAME_GLASS = [4, 2]
        elif self.grid[grid_y][grid_x] == 7:
            INITIAL_FRAME_GLASS = [5, 2]
        elif self.grid[grid_y][grid_x] == 8:
            INITIAL_FRAME_GLASS = [5, 1]
        elif self.grid[grid_y][grid_x] == 9:
            INITIAL_FRAME_GLASS = [1, 1]

    def draw_cell(self, grid_x, grid_y, canvas):
        self._init_frames(grid_x, grid_y)
        start_x = grid_x * self.cell_width
        end_x = start_x + self.cell_width
        centre_y = grid_y * self.cell_height + self.cell_height // 2

        source_center = (self.frame_width * INITIAL_FRAME_GLASS[0] + self.frame_centre_x,
                         self.frame_height * INITIAL_FRAME_GLASS[1] + self.frame_centre_y)

        source_size = (self.frame_width, self.frame_height)
        dest_center = ((start_x + end_x) // 2, centre_y)
        dest_size = (self.cell_width, self.cell_height)

        canvas.draw_image(wall_image, source_center, source_size, dest_center, dest_size)
