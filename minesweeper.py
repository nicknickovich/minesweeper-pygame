# an attempt to replicate classic minesweeper game
# using pygame
# author: Nick Poberezhnyk 
# email: nick.poberezhnyk@gmail.com

import pygame, sys, random
from pygame.locals import *
from Settings import Settings
from GameGrid import GameGrid
pygame.init()

settings = Settings()

# clock that sets the amount of frames per second
fps_clock = pygame.time.Clock()

# set title for the game window
pygame.display.set_caption("Minesweeper")

# create display surface on which everithing is drawn
DISPLAY_SURFACE = pygame.display.set_mode((settings.WINDOW_WIDTH, 
                                            settings.WINDOW_HEIGHT))

game_grid = GameGrid(DISPLAY_SURFACE)
game_grid.generate_grid()
game_grid.place_bombs()
game_grid.place_numbers()

last_tile = None

def display_debug(tile):
    if tile:
        font = pygame.font.SysFont(None, 48)
        text = font.render(", ".join([str(tile.x), str(tile.y), str(tile.pos_x), str(tile.pos_y), tile.type]), True, settings.WHITE)
        text_rect = text.get_rect()
        text_rect.center = ((settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT / 12 * 11))
        DISPLAY_SURFACE.blit(text, text_rect)



while True:
    DISPLAY_SURFACE.fill(settings.BLACK)
    
    # get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            for tile in game_grid.tiles_map:
                if (mouse_x > tile.x and mouse_x < tile.x + tile.TILE_SIZE
                        and mouse_y > tile.y and mouse_y < tile.y + tile.TILE_SIZE):
                    last_tile = tile

    display_debug(last_tile)
    game_grid.draw_grid()
    pygame.display.update()
    fps_clock.tick(settings.FPS)
