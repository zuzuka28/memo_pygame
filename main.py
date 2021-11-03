import pygame
from memo import memo_game

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
memo_scr = memo_game(screen)
running = True
is_clicked = False
mouse_pos = [-1, -1]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_clicked = True
            mouse_pos = [event.pos[0], event.pos[1]]
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = [-1, -1]
            is_clicked = False


    memo_scr.update(is_clicked, mouse_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
