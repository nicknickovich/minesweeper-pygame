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

game_over = False

game_grid = GameGrid(DISPLAY_SURFACE)
game_grid.setup_game_grid()

while True:
    DISPLAY_SURFACE.fill(settings.BLACK)
    
    # get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if game_over and event.key == K_SPACE or event.key == K_RETURN:
                game_over = False
                game_grid.reset_grid()
        
        if not game_over:
            if event.type == MOUSEBUTTONDOWN:
                for row in game_grid.tiles_map:
                    for tile in row:
                        if (mouse_x > tile.x and mouse_x < tile.x + tile.TILE_SIZE
                                and mouse_y > tile.y and mouse_y < tile.y + tile.TILE_SIZE):
                            if pygame.mouse.get_pressed()[0] and tile.state == "closed":
                                game_grid.open_around_blanks(tile)
                                tile.state = "open"
                                if tile.type == "bomb":
                                    game_over = True
                                    game_grid.reveal_all_bombs()
                            elif pygame.mouse.get_pressed()[2]:
                                if tile.state == "closed":
                                    tile.state = "flag"
                                elif tile.state == "flag":
                                    tile.state = "closed"
                        
    game_grid.draw_grid()
    pygame.display.update()
    fps_clock.tick(settings.FPS)
