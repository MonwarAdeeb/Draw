import pygame
pygame.init()

# Main abstract class (parent)
# This class is capable of creating a grid containing different rows and different columns, bases upon those arguments it
# will automatically alter the pixel size. To display the grid simply call ____.drawGrid(). To find the item in the grid
# that was clicked on call ____.clicked().


class grid(object):
    def __init__(self, win, width, height, cols, rows, showGrid=False, startx=0, starty=0, bg=(255, 255, 255)):
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.bg = bg
        self.startx = startx
        self.starty = starty
        self.lineThick = 1
        self.showGrid = showGrid  # If we should show the black outline
        self.isSelected = None
        self.grid = None

        self.screen = win
        pygame.display.update()

    def getGrid(self):
        return self.grid  # Return the grid list
