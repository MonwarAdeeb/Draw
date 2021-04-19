try:
    import pygame
except:
    import install_requirements
    import pygame
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import grid_module
from grid_module import colorPallet
from grid_module import pixelArt
from grid_module import menu
from grid_module import grid
import sys
import time

sys.setrecursionlimit(1000000)

pygame.init()  # initalize pygame
paintBrush = pygame.image.load("Paintbrush.png")
currentVersion = 1.1

# Set defaults for our screen size and rows and columns
rows = 50
cols = 50
wid = 600
heigh = 600

checked = []


def fill(spot, grid, color, c):
    if spot.color != c:
        pass
    else:
        spot.click(grid.screen, color)
        pygame.display.update()

        i = spot.col  # the var i is responsible for denoting the current col value in the grid
        j = spot.row  # the var j is responsible for denoting the current row value in the grid

        # Horizontal and vertical neighbors
        if i < cols-1:  # Right
            fill(grid.getGrid()[i + 1][j], grid, color, c)
        if i > 0:  # Left
            fill(grid.getGrid()[i - 1][j], grid, color, c)
        if j < rows-1:  # Up
            fill(grid.getGrid()[i][j + 1], grid, color, c)
        if j > 0:  # Down
            fill(grid.getGrid()[i][j - 1], grid, color, c)
