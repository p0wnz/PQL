import pygame,compent
def run(surface):
    running=True
    grid = compent.grid(surface,None,(720,520))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        surface.fill((255,255,255))
        grid.update()
        pygame.display.update()

    return running