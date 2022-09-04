import pygame
import os
import time
from button import Button

os.chdir("C:/Users/William/Documents/Clement/Python/Sudoku")

WIN = pygame.display.set_mode((520,650))
pygame.display.set_caption("Sudoku")
pygame.font.init()

def pause(win, play):
    def draw_empty_grid():
        gap = 520 / 9
        for i in range(10):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (520, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, 520), thick)

    resume_img = pygame.image.load(os.path.join('images','resume.png'))
    resume_button = Button(520-40,530, resume_img, 0.7)
    run = True
    fnt = pygame.font.SysFont("comicsans", 20)
    while run:
        win.fill((255,255,255))
        draw_empty_grid()
        if resume_button.get_clicked():
            return time.time() - play
        resume_button.draw(win)
        sec = play % 60
        minute = play // 60
        hour = minute // 60
        text = fnt.render("Time: {:02d}:{:02d}:{:02d}".format(hour, minute, sec), 1, (0,0,0))
        win.blit(text, (520 - 150, 610))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.display.update()


    