# an attempt to replicate classic minesweeper game using pygame
# author: Nick Poberezhnyk 
# email: nick.poberezhnyk@gmail.com
# images from opengameart.org

import pygame, sys, random
from pygame.locals import *
from Settings import Settings
from GameGrid import GameGrid
pygame.init()

def main():
    settings = Settings()

    # clock that sets the amount of frames per second
    fps_clock = pygame.time.Clock()

    # set title for the game window
    pygame.display.set_caption("Minesweeper")

    # create display surface on which everithing is drawn
    DISPLAY_SURFACE = pygame.display.set_mode((settings.WINDOW_WIDTH, 
                                                settings.WINDOW_HEIGHT))

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
                if (game_grid.game_over or game_grid.won 
                        and event.key == K_SPACE or event.key == K_RETURN):
                    game_grid.reset_grid()
            
            if not game_grid.game_over and not game_grid.won:
                if event.type == MOUSEBUTTONDOWN:
                    for row in game_grid.tiles_map:
                        for tile in row:
                            # check if mouse is over the tile
                            if (mouse_x > tile.x and mouse_x < tile.x + tile.TILE_SIZE
                                    and mouse_y > tile.y and mouse_y < tile.y + tile.TILE_SIZE):
                                # handle left click
                                if pygame.mouse.get_pressed()[0] and tile.state == "closed":
                                    game_grid.open_around_blanks(tile)
                                    tile.state = "open"
                                    if tile.type == "bomb":
                                        game_grid.game_over = True
                                        game_grid.reveal_all_bombs()
                                # handle right click
                                elif pygame.mouse.get_pressed()[2]:
                                    if tile.state == "closed":
                                        tile.state = "flag"
                                        game_grid.num_flags += 1
                                    elif tile.state == "flag":
                                        tile.state = "closed"
                                        game_grid.num_flags -= 1
        game_grid.check_win()

        game_grid.draw_game()

        if game_grid.game_over:
            game_grid.draw_game_over()
        elif game_grid.won:
            game_grid.draw_win()

        pygame.display.update()
        fps_clock.tick(settings.FPS)

if __name__ == "__main__":
    main()