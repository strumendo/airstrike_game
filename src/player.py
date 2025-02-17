import pygame
from src.settings import WIDTH, PLAYER_SPEED

class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 500)
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)