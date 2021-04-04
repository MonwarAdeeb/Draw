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

            self.selected = self.grid[g1][g2]

            return self.grid[g1][g2]

        except IndexError:  # If we run into an index error that means that the user did not click on a position in the grid
            return False

    def isSelected(self):  # Return the currently selected object
        return self.selected


# This is the concrete class used to draw pixels in a grid
# The draw grid function in this class uses polymorphism to create a grid
# full of pixel objects. It still contains the methods from the aboce class
# has its own specific clearGrid(). Using ____.clearGrid() will simply set the color
# to the original background color.
class pixelArt(grid):
    def drawGrid(self):
        self.grid = []
        # Create pixels in the grid
        for i in range(self.cols):
            self.grid.append([])
            for j in range(self.rows):
                self.grid[i].append(pixel(i, j, self.width, self.height, self.cols,
                                          self.rows, self.startx, self.starty, self.showGrid))
                self.grid[i][j].show(
                    self.screen, (255, 255, 255), self.lineThick)
                if self.showGrid:
                    self.grid[i][j].show(
                        self.screen, (0, 0, 0), 1, False, True)
