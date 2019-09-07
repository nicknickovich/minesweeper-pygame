import pygame, random
from Settings import Settings
from Tile import Tile

class GameGrid(Settings):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.tiles_map = []

    def generate_grid(self):
        for y in range(self.NUM_ROWS):
            self.tiles_map.append([])
            for x in range(self.NUM_COLS):
                self.tiles_map[y].append(Tile(self.screen,
                    x * self.TILE_SIZE + self.OFFSET_LEFT, 
                    y * self.TILE_SIZE + self.OFFSET_TOP,
                    x, y))

    def place_bombs(self):
        flat_list = []
        for row in self.tiles_map:
            for item in row:
                flat_list.append(item)
        bombs = random.sample(flat_list, 20)
        for tile in bombs:
            self.tiles_map[tile.pos_y][tile.pos_x].type = "bomb"

    def place_numbers(self):
        for row in self.tiles_map:
            for tile in row:
                if tile.type != "bomb":
                    bomb_count = 0
                    x = tile.pos_x
                    y = tile.pos_y
                
                    if 0 <= x < 9 and 0 <= y < 9:
                        bomb_count += self.check_bomb(y, x+1)
                        bomb_count += self.check_bomb(y+1, x)
                        bomb_count += self.check_bomb(y+1, x+1)
                    if 0 < x <= 9 and 0 <= y < 9:
                        bomb_count += self.check_bomb(y, x-1)
                        bomb_count += self.check_bomb(y+1, x-1)
                    if 0 <= x < 9 and 0 < y <= 9:
                        bomb_count += self.check_bomb(y-1, x)
                        bomb_count += self.check_bomb(y-1, x+1)
                    if 0 < x <= 9 and 0 < y <= 9:
                        bomb_count += self.check_bomb(y-1, x-1)
                    self.tiles_map[y][x].type = bomb_count

                        

    def check_bomb(self, y, x):
        if self.tiles_map[y][x].type == "bomb":
            return 1
        return 0

    def draw_grid(self):
        for row in self.tiles_map:
            for tile in row:
                tile.draw_tile()