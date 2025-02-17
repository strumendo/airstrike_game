import pygame
import os

def load_sound(filename):
    path = os.path.join("assets", filename)
    return pygame.mixer.Sound(path)


def load_image(filename, width=None, height=None):
    path = os.path.join("assets", filename)
    image = pygame.image.load(path).convert_alpha()
    if width and height:
        image = pygame.transform.scale(image, (width, height))
    return image