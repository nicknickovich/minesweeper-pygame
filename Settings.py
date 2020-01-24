import pygame


class Settings:
    """All settings for the game in one class."""
    def __init__(self):
        # Game window settings.
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        self.NUM_BOMBS = 15

        # Colors.
        self.BLACK = 0, 0, 0
        self.WHITE = 255, 255, 255
        self.RED = 255, 0, 0
        self.GREEN = 0, 255, 0

        # Grid settings.
        self.OFFSET_LEFT = 200
        self.OFFSET_TOP = 100
        self.TILE_SIZE = 40
        self.NUM_ROWS = 10
        self.NUM_COLS = 10

        # Tiles settings.
        self.SCALING_FACTOR = 40 / 62 
        # Pictures for numbers, named tile0-tile8.
        for i in range(9):
            setattr(self, "tile" + str(i), self.resize_img(
                pygame.image.load("images/" + str(i) + ".png"
            )))
        self.closed_tile = self.resize_img(
            pygame.image.load("images/closed.png")
        )
        self.bomb_tile = self.resize_img(pygame.image.load("images/bomb.png"))
        self.flag_tile = self.resize_img(pygame.image.load("images/flag.png"))

        # FPS for clock.
        self.FPS = 60

    def resize_img(self, image):
        """Resize image according to the scaling factor."""
        image_rect = image.get_rect()
        return pygame.transform.scale(image, 
            (int(image_rect.width * self.SCALING_FACTOR), 
                int(image_rect.height * self.SCALING_FACTOR)))