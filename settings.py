import numpy as np
import math

#GAME constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
CENTER = np.array([WIDTH/2, HEIGHT/2])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)

pi = math.pi