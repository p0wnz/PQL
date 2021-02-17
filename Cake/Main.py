import pygame,grid
pygame.init()
pygame.display.set_caption("Table Viewer")
screen =pygame.display.set_mode((800,600))
running=True
while running:
    running = grid.run(screen)
pygame.quit()
quit()
