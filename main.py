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
