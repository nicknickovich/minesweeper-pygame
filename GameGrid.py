import pygame, random
from Settings import Settings
from Tile import Tile

class GameGrid(Settings):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.tiles_map = []


    def setup_game_grid(self):
        self.generate_grid()
        self.place_bombs()
        self.place_numbers()

    def reset_grid(self):
        self.tiles_map = []
        self.setup_game_grid()
        
    # generate grid with empty tile objects
    def generate_grid(self):
        for y in range(self.NUM_ROWS):
            self.tiles_map.append([])
            for x in range(self.NUM_COLS):
                self.tiles_map[y].append(Tile(self.screen,
                    x * self.TILE_SIZE + self.OFFSET_LEFT, 
                    y * self.TILE_SIZE + self.OFFSET_TOP,
                    x, y))

    # generate random bomb locations and place them on the grid
    def place_bombs(self):
        flat_list = []
        for row in self.tiles_map:
            for item in row:
                flat_list.append(item)
        bombs = random.sample(flat_list, self.NUM_BOMBS)
        for tile in bombs:
            self.tiles_map[tile.pos_y][tile.pos_x].type = "bomb"

    # generate numbers of the tiles depending on the amount of bombs around
    def place_numbers(self):
        for row in self.tiles_map:
            for tile in row:
                if tile.type != "bomb":
                    bomb_count = 0
                    x = tile.pos_x
                    y = tile.pos_y
                
                    if 0 <= x < 9 and 0 <= y < 9:
                        bomb_count += self.check_bomb(y+1, x+1)
                    if 0 < x <= 9 and 0 <= y < 9:
                        bomb_count += self.check_bomb(y+1, x-1)
                    if 0 <= x < 9 and 0 < y <= 9:
                        bomb_count += self.check_bomb(y-1, x+1)
                    if 0 < x <= 9 and 0 < y <= 9:
                        bomb_count += self.check_bomb(y-1, x-1)
                    if x > 0:
                        bomb_count += self.check_bomb(y, x-1)
                    if x < 9:
                        bomb_count += self.check_bomb(y, x+1)
                    if y > 0:
                        bomb_count += self.check_bomb(y-1, x)
                    if y < 9:
                        bomb_count += self.check_bomb(y+1, x)
                    self.tiles_map[y][x].type = "tile" + str(bomb_count)
                        
                        
    def check_bomb(self, y, x):
        if self.tiles_map[y][x].type == "bomb":
            return 1
        return 0

    def draw_grid(self):
        for row in self.tiles_map:
            for tile in row:
                tile.draw_tile()

    def open_around_blanks(self, tile):
        if tile.state == "closed" and tile.type == "tile0":
            x = tile.pos_x
            y = tile.pos_y
            self.tiles_map[y][x].state = "open"
            if 0 <= x < 9 and 0 <= y < 9:
                self.set_open_and_go_deeper(y+1, x+1)
            if 0 < x <= 9 and 0 <= y < 9:
                self.set_open_and_go_deeper(y+1, x-1)
            if 0 <= x < 9 and 0 < y <= 9:
                self.set_open_and_go_deeper(y-1, x+1)
            if 0 < x <= 9 and 0 < y <= 9:
                self.set_open_and_go_deeper(y-1, x-1)
            if x > 0:
                self.set_open_and_go_deeper(y, x-1)
            if x < 9:
                self.set_open_and_go_deeper(y, x+1)
            if y > 0:
                self.set_open_and_go_deeper(y-1, x)
            if y < 9:
                self.set_open_and_go_deeper(y+1, x)

    def set_open_and_go_deeper(self, y, x):
        if self.tiles_map[y][x].state == "closed":
            self.open_around_blanks(self.tiles_map[y][x])
            self.tiles_map[y][x].state = "open"
            
    def reveal_all_bombs(self):
        for row in self.tiles_map:
            for tile in row:
                if tile.type == "bomb":
                    tile.state = "open"