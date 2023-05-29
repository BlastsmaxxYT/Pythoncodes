import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BlastsMaxx Shooting Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)

    def update(self):
        # Move the player with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Keep the player within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 3)

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create enemy objects
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display name
    font = pygame.font.Font(None, 36)
    text = font.render("BlastsMaxx", True, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 10))

    pygame.display.flip()

# Quit the game
pygame.quit()
