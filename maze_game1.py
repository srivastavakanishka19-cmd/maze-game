import pygame
import random

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 4
ENEMY_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 50, 50)     # Enemy
BLUE = (50, 150, 255)   # Player
GOLD = (255, 215, 0)    # Collectible
GREEN = (50, 255, 50)   # Exit

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.score = 0

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]: dx = PLAYER_SPEED
        if keys[pygame.K_UP]: dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN]: dy = PLAYER_SPEED

        # Move horizontally and check collisions
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left
                if dx < 0: self.rect.left = wall.rect.right

        # Move vertically and check collisions
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                if dy < 0: self.rect.top = wall.rect.bottom

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.move_counter = 0

    def update(self, walls):
        self.rect.x += self.direction[0] * ENEMY_SPEED
        self.rect.y += self.direction[1] * ENEMY_SPEED
        
        # Change direction if hit wall or every 60 frames
        hit_wall = any(self.rect.colliderect(w.rect) for w in walls)
        self.move_counter += 1
        
        if hit_wall or self.move_counter > 60:
            if hit_wall: # Back up slightly
                self.rect.x -= self.direction[0] * ENEMY_SPEED
                self.rect.y -= self.direction[1] * ENEMY_SPEED
            self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            self.move_counter = 0

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GOLD, (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Stealth Mission")
    clock = pygame.time.Clock()

    # Create Groups
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    # Build a simple level layout
    layout = [
        "WWWWWWWWWWWWWWWWWWWW",
        "W P      W        EW",
        "W   WW   W   WW    W",
        "W   W        W     W",
        "W      C     W  C  W",
        "W   WWWWWW   WWWW  W",
        "W   W        W     W",
        "W C      C         W",
        "WWWWWWWWWWWWWWWWWWWW",
    ]

    for row_idx, row in enumerate(layout):
        for col_idx, char in enumerate(row):
            x, y = col_idx * 40, row_idx * 40
            if char == "W":
                w = Wall(x, y, 40, 40)
                walls.add(w)
                all_sprites.add(w)
            elif char == "P":
                player = Player(x, y)
                all_sprites.add(player)
            elif char == "C":
                c = Coin(x+20, y+20)
                coins.add(c)
                all_sprites.add(c)
            elif char == "E": # Exit
                exit_rect = pygame.Rect(x, y, 40, 40)

    # Spawn 3 Enemies
    for _ in range(3):
        en = Enemy(random.randint(200, 600), random.randint(100, 300))
        enemies.add(en)
        all_sprites.add(en)

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Update
        player.update(walls)
        enemies.update(walls)

        # Collisions
        if pygame.sprite.spritecollide(player, coins, True):
            player.score += 1
            print(f"Data Collected: {player.score}")

        if pygame.sprite.spritecollide(player, enemies, False):
            print("CAUGHT BY MALWARE! Game Over.")
            running = False

        # 3. Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Draw exit
        color = GREEN if not coins else RED
        pygame.draw.rect(screen, color, exit_rect, 2)

        if not coins and player.rect.colliderect(exit_rect):
            print("System Secured! You Win!")
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()