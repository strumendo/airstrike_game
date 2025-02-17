import pygame
from src.player import Player
from src.enemy import Enemy
from src.powerup import PowerUp
from src.settings import WIDTH, HEIGHT, FPS, WHITE, BLACK, MENU_COLOR, BUTTON_COLOR
from src.utils import load_sound, load_image

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Meu Jogo Python")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.state = "menu"

        # Carrega recursos
        #self.background_music = load_sound("musica_fundo.mp3")
        #self.collision_sound = load_sound("colisao.wav")
        self.player_image = load_image("player.png", width=50, height=50)
        self.enemy_image = load_image("enemy.jpg", width=50, height=50)
        self.powerup_image = load_image("powerup.png", width=30, height=30)

        # Inicializa objetos
        self.player = Player(self.player_image)
        self.enemies = Enemy(self.enemy_image)
        self.powerups = PowerUp(self.powerup_image)

        # Toca música de fundo
        #self.background_music.play(-1)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if self.state == "menu":
                self.show_menu()
            elif self.state == "game":
                self.update()
                self.draw()
            elif self.state == "game_over":
                self.show_game_over()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key == pygame.K_SPACE:  # Inicia o jogo
                        self.state = "game"
                        self.reset_game()
                elif self.state == "game_over":
                    if event.key == pygame.K_SPACE:  # Volta ao menu
                        self.state = "menu"

    def update(self):
        self.player.update()
        self.spawn_enemies()
        self.spawn_powerups()
        self.move_enemies()
        self.move_powerups()
        self.check_collisions()

    def draw(self):
        self.screen.fill(WHITE)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

    def spawn_enemies(self):
        if pygame.time.get_ticks() % 60 == 0:  # Gera inimigos periodicamente
            enemy = Enemy(self.enemy_image)
            self.enemies.append(enemy)

    def spawn_powerups(self):
        if pygame.time.get_ticks() % 300 == 0:  # Gera power-ups periodicamente
            powerup = PowerUp(self.powerup_image)
            self.powerups.append(powerup)

    def move_enemies(self):
        for enemy in self.enemies[:]:  # Usamos [:] para iterar sobre uma cópia da lista
            enemy.update()
            if enemy.rect.y > HEIGHT:  # Remove inimigos que saíram da tela
                self.enemies.remove(enemy)
                self.score += 1  # Aumenta a pontuação

    def move_powerups(self):
        for powerup in self.powerups[:]:  # Usamos [:] para iterar sobre uma cópia da lista
            powerup.update()
            if powerup.rect.y > HEIGHT:  # Remove power-ups que saíram da tela
                self.powerups.remove(powerup)

    def check_collisions(self):
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                #self.collision_sound.play()
                self.running = False
            if enemy.rect.y > HEIGHT:
                self.enemies.remove(enemy)
                self.score += 1

        for powerup in self.powerups[:]:
            if self.player.rect.colliderect(powerup.rect):
                self.powerups.remove(powerup)
                self.player.speed += 1  # Aumenta a velocidade do jogador

    def draw_score(self):
        score_text = self.font.render(f"Pontuação: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def show_menu(self):
        self.screen.fill(MENU_COLOR)
        title_text = self.font.render("Meu Jogo Python", True, WHITE)
        start_text = self.font.render("Pressione ESPAÇO para começar", True, WHITE)
        self.screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        self.screen.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()

    def show_game_over(self):
        self.screen.fill(MENU_COLOR)
        game_over_text = self.font.render("Game Over!", True, WHITE)
        score_text = self.font.render(f"Pontuação: {self.score}", True, WHITE)
        restart_text = self.font.render("Pressione ESPAÇO para voltar ao menu", True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
        self.screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))
        self.screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))
        pygame.display.flip()

    def reset_game(self):
        self.score = 0
        self.player.rect.center = (WIDTH // 2, 500)
        self.enemies.clear()
        self.powerups.clear()