import pygame
from pygame.locals import *
from sys import exit
from random import randint
import time

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    rand_col = (randint(0, 255), randint(0, 255), randint(0, 255))
    # 相当于上锁，让别的进程不会干扰我们,要记得解锁
    # screen.lock()    #很快你就会知道这两句lock和unlock的意思了
    for _ in range(100):
        rand_pos = (randint(0, 639), randint(0, 479))
        screen.set_at(rand_pos, rand_col)
    screen.unlock()
    time.sleep(1)

    pygame.display.update()