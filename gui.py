"""
GUI for displaying a Sudoku Grid
"""
import math
import pygame

class Square:
    """
    A single square within the Sudoku grid
    """

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.possibles = {x+1 for x in range(9)}
        self.value = 0
        self.selected = False
        self.rect = pygame.Rect(self.center_pos(self.x) - self.grid.scale/2,
                                self.center_pos(self.y) - self.grid.scale/2,
                                self.grid.scale,
                                self.grid.scale)

    def center_pos(self, x_or_y):
        """Given the x or y position of this square, returns the coordinates"""
        grid_widths = (x_or_y + 0.5) * (self.grid.scale + self.grid.grid_width)
        break_widths = math.floor(x_or_y/3) * self.grid.grid_break
        return grid_widths+break_widths

    def erase(self):
        """ Erases the current square in the grid """
        if self.selected:
            col = self.grid.sel_bg
        else:
            col = self.grid.col_bg
        pygame.draw.rect(self.grid.screen, col, self.rect, 0)

    def draw_pos(self):
        """ Add text for all possibles """
        for pos in self.possibles:
            # rel_x and y used to position the possible relatiev to the cell center
            rel_x = ((pos - 1) % 3 - 1) * self.grid.scale / 3
            rel_y = ((pos - 1) // 3 - 1) * self.grid.scale / 3

            text = self.grid.poss_font.render(str(pos), False, (150, 150, 150))
            text_rec = text.get_rect(center=(self.center_pos(self.x) + rel_x,
                                             self.center_pos(self.y) + rel_y))
            self.grid.screen.blit(text, (text_rec))

    def draw_val(self):
        """ Adds text for known value """
        text = self.grid.vals_font.render(str(self.value), False, (0, 0, 0))
        # Use text rectangle to always center the text
        text_rec = text.get_rect(center=(self.center_pos(self.x), self.center_pos(self.y)))
        self.grid.screen.blit(text, (text_rec))

    def draw(self):
        """Draws the value or possibles for this square"""
        if self.value != 0:
            self.draw_val()
        else:
            self.draw_pos()

class Grid:
    """
    Grid containing the 9x9 Squares
    """

    def show_grid(self):
        """ Displays all possibles and values in the grid"""
        #pygame.init()
        for square in self.squaredict.values():
            square.erase()
            square.draw()
        pygame.display.update()

    def __init__(self):
        self.scale = 70
        self.grid_width = 2
        self.grid_break = 5
        self.col_bg = (255, 255, 255)
        self.sel_bg = (200, 200, 255)

        pygame.font.init()
        self.poss_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.vals_font = pygame.font.SysFont('Comic Sans MS', 70)

        self.squaredict = {(x, y):Square(x, y, self)
                           for x in range(9)
                           for y in range(9)}
        self.screen = pygame.display.set_mode((9*(self.scale+self.grid_width)+2*self.grid_break,
                                               9*(self.scale+self.grid_width)+2*self.grid_break))

    def clicked_square(self, point):
        """ Returns the clicked square when given x,y within the rectangle """
        for square in self.squaredict.values():
            if square.rect.collidepoint(point):
                return square
        return None

    def deselect_squares(self):
        """ Deselects all squares, usually before selecting a new one"""
        for square in self.squaredict.values():
            square.selected = False

def eventloop(grid):
    """ Main eventloop for detecting user interaction with pygame"""
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                square = grid.clicked_square(pos)
                if square is None:
                    break
                grid.deselect_squares()
                square.selected = True
                grid.show_grid()

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
def main():
    """
    Main function
    """
    grid = Grid()
    grid.squaredict[(3, 4)].value = 5
    grid.show_grid()
    eventloop(grid)

if __name__ == '__main__':
    main()
