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


# Saves the current project into a text file that contains the size of the screen, if the gird is showing and all the colors of all the pixels
def save(cols, rows, show, grid, path):
    if len(path) >= 4:  # This just makes sure we have .txt at the end of our file selection
        if path[-4:] != '.txt':
            path = path + '.txt'
    else:
        path = path + '.txt'

    # Overwrite the current file, or if it doesn't exist create a new one
    file = open(path, 'w')
    file.write(str(cols) + ' ' + str(rows) + ' ' + str(show) + '\n')

    for pixel in grid:
        for p in pixel:  # For every pixel write the color in the text file
            wr = str(p.color[0]) + ',' + \
                str(p.color[1]) + ',' + str(p.color[2])
            file.write(wr + '\n')
    file.write(str(currentVersion))

    file.close()
    name = path.split("/")
    changeCaption(name[-1])


# Opens the file from the given path and displays it to the screen
def openFile(path):
    global grid

    file = open(path, 'r')
    f = file.readlines()
    if f[-1] == str(currentVersion):

        dimensions = f[0].split()  # Dimesnions for the rows and cols
        columns = int(dimensions[0])
        rows = int(dimensions[1])

        # If the show grid attribute at the end of our dimensions line is 0 then don't show grid
        if dimensions[2] == '0':
            v = False
        else:
            v = True
        # Redraw the grid, tool bars, menu bars etc.
        initalize(columns, rows, v)
        name = path.split("/")
        changeCaption(name[-1])

        line = 0
        for i in range(columns):  # For every pixel, read the color and format it into a tuple
            for j in range(rows):
                line += 1
                nColor = []
                for char in f[line].strip().split(','):
                    nColor.append(int(char))

                # Show the color on the grid
                grid.getGrid()[i][j].show(win, tuple(nColor), 0)
