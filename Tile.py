from settings import Settings


class Tile(Settings):
    """Single tile with its position on display and on the grid.
    Created with default 'blank' type and 'closed' state.
    """
    def __init__(self, screen, x, y, pos_x, pos_y):
        super().__init__()
        # tile position in pixels
        self.x = x
        self.y = y
        # tile position on the grid
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.screen = screen
        self.type = "tile0"
        self.state = "closed"

    def draw_tile(self):
        """Draw tile depending on its state and type."""
        if self.state == "open":
            if self.type == "bomb":
                self.screen.blit(self.bomb_tile, (self.x, self.y))
            else:
                self.screen.blit(getattr(self, self.type), (self.x, self.y))
        elif self.state == "flag":
            self.screen.blit(self.flag_tile, (self.x, self.y))
        else:
            self.screen.blit(self.closed_tile, (self.x, self.y))
