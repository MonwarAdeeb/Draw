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

    # This will draw the lines to create the grid, this is done so by simply creating overlapping boxes
    def drawGrid(self, lineColor=(0, 0, 0)):
        x = self.startx
        y = self.starty

        for i in range(self.cols):
            y = self.starty + self.height
            if i > 0:
                x += (self.width / self.cols)
            for j in range(self.rows):
                y -= self.height / self.rows
                pygame.draw.rect(
                    self.screen, (0, 0, 0), (x, y, self.width / self.cols, self.height / self.rows), 1)

    def clicked(self, pos):  # Return the position in the grid that user clicked on
        try:
            t = pos[0]
            w = pos[1]
            g1 = int((t - self.startx) / self.grid[0][0].w)
            g2 = int((w - self.starty) / self.grid[0][0].h)
