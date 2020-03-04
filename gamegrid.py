import pygame, random
from settings import Settings
from tile import Tile


class GameGrid(Settings):
    """All functionality of game grid:
    - setup;
    - game functions;
    - drawing functions;
    """
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        # All tiles in a list:
        self.tiles_map = []
        # Current number of flags:
        self.num_flags = 0
        self.game_over = False
        self.won = False

    # ====================================
    # METHODS FOR SETTING UP THE GAME GRID
    # ====================================

    def setup_game_grid(self):
        """Set up new game grid."""
        self.generate_grid()
        self.place_bombs()
        self.place_numbers()

    def reset_grid(self):
        """Discard existing grid and generate new one."""
        self.tiles_map = []
        self.setup_game_grid()
        self.num_flags = 0
        self.game_over = False
        self.won = False
        
    def generate_grid(self):
        """Generate a grid with empty tile objects."""
        for y in range(self.NUM_ROWS):
            self.tiles_map.append([])
            for x in range(self.NUM_COLS):
                self.tiles_map[y].append(Tile(
                    self.screen,
                    x * self.TILE_SIZE + self.OFFSET_LEFT, 
                    y * self.TILE_SIZE + self.OFFSET_TOP,
                    x, y
                ))

    def place_bombs(self):
        """Generate random bomb locations and place them on the grid."""
        flat_list = []
        for row in self.tiles_map:
            for item in row:
                flat_list.append(item)
        bombs = random.sample(flat_list, self.NUM_BOMBS)
        for tile in bombs:
            self.tiles_map[tile.pos_y][tile.pos_x].type = "bomb"

    def place_numbers(self):
        """Generate numbers of the tiles depending on 
        the amount of bombs around them.
        """
        for row in self.tiles_map:
            for tile in row:
                if tile.type != "bomb":
                    bomb_count = 0
                    x = tile.pos_x
                    y = tile.pos_y
                
                    if x < 9 and y < 9:
                        bomb_count += self.check_bomb(y+1, x+1)
                    if 0 < x and y < 9:
                        bomb_count += self.check_bomb(y+1, x-1)
                    if x < 9 and 0 < y:
                        bomb_count += self.check_bomb(y-1, x+1)
                    if 0 < x and 0 < y:
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
        """Check if tile type is a bomb."""
        if self.tiles_map[y][x].type == "bomb":
            return 1
        return 0

    # =================================
    # METHODS FOR IN-GAME FUNCTIONALITY    
    # =================================          
    
    def open_around_blanks(self, tile):
        """Open the area around blank tiles recursively."""
        if tile.state == "closed" and tile.type == "tile0":
            x = tile.pos_x
            y = tile.pos_y
            self.tiles_map[y][x].state = "open"
            if x < 9 and y < 9:
                self.set_open_and_go_deeper(y+1, x+1)
            if 0 < x and y < 9:
                self.set_open_and_go_deeper(y+1, x-1)
            if x < 9 and 0 < y:
                self.set_open_and_go_deeper(y-1, x+1)
            if 0 < x and 0 < y:
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
        """Helper function for recursive opening of blank tiles.
        Set tile state to open and call 'open_around_blanks'.
        """
        if self.tiles_map[y][x].state == "closed":
            self.open_around_blanks(self.tiles_map[y][x])
            self.tiles_map[y][x].state = "open"
            
    def reveal_all_bombs(self):
        """Show all bombs on the grid."""
        for row in self.tiles_map:
            for tile in row:
                if tile.type == "bomb":
                    tile.state = "open"

    def show_all_bombs_as_flags(self):
        """Show all bombs on the grid as flags."""
        for row in self.tiles_map:
            for tile in row:
                if tile.type == "bomb":
                    tile.state = "flag"

    def check_win(self):
        """Determine if the game is won."""
        open_tiles = []
        for row in self.tiles_map:
            for tile in row:
                if tile.type != "bomb" and tile.state == "open":
                    open_tiles.append(tile)
        if len(open_tiles) == self.NUM_ROWS * self.NUM_COLS - self.NUM_BOMBS:
            self.won = True

    # ===================
    # METHODS FOR DRAWING
    # ===================

    def draw_game(self):
        """Draw the whole game."""
        self.draw_grid()
        self.draw_legend()

    def draw_grid(self):
        """Draw game grid."""
        for row in self.tiles_map:
            for tile in row:
                tile.draw_tile()

    def draw_legend(self):
        """Display the number of bombs on the grid and 
        current number of flags.
        """
        font = pygame.font.SysFont(None, 32)
        bomb_text = font.render(
            "Bombs:" + str(self.NUM_BOMBS), True, self.WHITE
        )
        self.screen.blit(bomb_text, (50, 150))

        font = pygame.font.SysFont(None, 32)
        flag_text = font.render(
            "Flags:" + str(self.num_flags), True, self.WHITE
        )
        self.screen.blit(flag_text, (50, 200))

    def draw_win_lose_message(self, message, text_color):
        """Draw a message at the top of the window."""
        font = pygame.font.SysFont(None, 64)
        text = font.render(message, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 10)
        self.screen.blit(text, text_rect)
        self.draw_press_button_msg()

    def draw_game_over(self):
        """Draw a message for game over state."""
        self.draw_win_lose_message("GAME OVER", self.RED)
    
    def draw_win(self):
        """Draw a message for win state."""
        self.draw_win_lose_message("YOU WIN", self.GREEN)

    def draw_press_button_msg(self):
        """Draw a message at the bottom of the window."""
        font = pygame.font.SysFont(None, 48)
        text = font.render(
            "press space or enter to play again", True, self.WHITE
        )
        text_rect = text.get_rect()
        text_rect.center = (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 9 / 10)
        self.screen.blit(text, text_rect)

