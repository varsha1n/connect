import pygame

pygame.init()

screen=pygame.display.set_mode((600,400))
pygame.display.set_caption("wordle")
icon=pygame.image.load('letter-w.png')
pygame.display.set_icon(icon)
#game loop
running=True
while running:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False