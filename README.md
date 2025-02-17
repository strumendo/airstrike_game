
Para organizar o código do jogo de maneira estrutural em pastas, vamos seguir boas práticas de desenvolvimento de software. Isso inclui separar o código em módulos e pastas, como:

1. **`main.py`**: Arquivo principal que inicia o jogo.
2. **`assets/`**: Pasta para armazenar recursos como imagens, sons e fontes.
3. **`src/`**: Pasta para o código-fonte do jogo, dividido em módulos.
   - **`game.py`**: Lógica principal do jogo.
   - **`player.py`**: Classe do jogador.
   - **`enemy.py`**: Classe dos inimigos.
   - **`powerup.py`**: Classe dos power-ups.
   - **`settings.py`**: Configurações do jogo (cores, tamanhos, etc.).
   - **`utils.py`**: Funções utilitárias (ex: carregar imagens, sons).

Aqui está como você pode estruturar o projeto:

---

### Estrutura de Pastas

```
meu_jogo_python/
├── assets/
│   ├── musica_fundo.mp3
│   ├── colisao.wav
│   ├── player.png
│   ├── enemy.png
│   └── powerup.png
├── src/
│   ├── game.py
│   ├── player.py
│   ├── enemy.py
│   ├── powerup.py
│   ├── settings.py
│   └── utils.py
└── main.py
```

---
### Instalar o Pygame
Primeiro, você precisa instalar a biblioteca Pygame. Se ainda não a tem, use o pip para instalar:

```bash
pip install pygame
```

ou

```bash
pip install requirements.txt
```

---

### Código Organizado

#### 1. **`main.py`**
Arquivo principal que inicia o jogo.

```python
from src.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
```

---

#### 2. **`src/game.py`**
Lógica principal do jogo.

```python
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
        self.state = "menu"  # Estado inicial: menu

        # Carrega recursos
        self.background_music = load_sound("musica_fundo.mp3")
        self.collision_sound = load_sound("colisao.wav")
        self.player_image = load_image("player.png", width=50, height=50)
        self.enemy_image = load_image("enemy.png", width=50, height=50)
        self.powerup_image = load_image("powerup.png", width=30, height=30)

        # Inicializa objetos
        self.player = Player(self.player_image)
        self.enemies = []
        self.powerups = []

        # Toca música de fundo
        self.background_music.play(-1)

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
            self.enemies.append(Enemy(self.enemy_image))

    def spawn_powerups(self):
        if pygame.time.get_ticks() % 300 == 0:  # Gera power-ups periodicamente
            self.powerups.append(PowerUp(self.powerup_image))

    def check_collisions(self):
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                self.collision_sound.play()
                self.state = "game_over"
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
```

---

#### 3. **`src/player.py`**
Classe do jogador.

```python
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
```

---

#### 4. **`src/enemy.py`**
Classe dos inimigos.

```python
import pygame
import random
from src.settings import WIDTH, ENEMY_SPEED

class Enemy:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
```

---

#### 5. **`src/powerup.py`**
Classe dos power-ups.

```python
import pygame
import random
from src.settings import WIDTH, POWERUP_SPEED

class PowerUp:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = POWERUP_SPEED

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
```

---

#### 6. **`src/settings.py`**
Configurações do jogo.

```python
# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MENU_COLOR = (30, 30, 30)  # Cor de fundo do menu
BUTTON_COLOR = (70, 70, 70)  # Cor dos botões (se necessário)

# Tela
WIDTH = 800
HEIGHT = 600
FPS = 60

# Velocidades
PLAYER_SPEED = 5
ENEMY_SPEED = 3
POWERUP_SPEED = 2
```

---

#### 7. **`src/utils.py`**
Funções utilitárias.

```python
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
```

---

### Como Executar
1. Crie a estrutura de pastas e arquivos conforme descrito.
2. Coloque os recursos (imagens, sons) na pasta `assets/`.
3. Execute o arquivo `main.py`:

```bash
python main.py
```

---

### Benefícios dessa Estrutura
- **Organização:** O código fica modular e fácil de manter.
- **Reutilização:** Classes como `Player`, `Enemy` e `PowerUp` podem ser reutilizadas em outros projetos.
- **Escalabilidade:** Adicionar novos recursos (ex: novos tipos de inimigos) é mais simples.