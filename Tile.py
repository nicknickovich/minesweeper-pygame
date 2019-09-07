from Settings import Settings
class Tile(Settings):
    def __init__(self, screen, x, y, pos_x, pos_y):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = "tile0"
        self.state = True

    def draw_tile(self):
        if self.state:
            if self.type == "bomb":
                self.screen.blit(self.bomb_tile, (self.x, self.y))
            else:
                self.screen.blit(getattr(self, "tile" + str(self.type)), (self.x, self.y))
        else:
            self.screen.blit(self.closed_tile, (self.x, self.y))
