import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5  # Speed of the enemy bullets

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War Game")

# Load images
player_image = pygame.image.load("p1.png")  # Replace with your image path
player_image = pygame.transform.scale(player_image, (70, 70))  # Optional resize

bullet_image = pygame.Surface((5, 10))
bullet_image.fill(WHITE)

# Load background image
background_image = pygame.image.load("d2.png")  # Replace with your background image file path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize to screen size

background_image2 = pygame.image.load("S2.png")  # Replace with your background image file path
background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))  # Resize to screen size

# Load heart image for health
heart_image = pygame.image.load("h1.png")  # Replace with your heart image file path
heart_image = pygame.transform.scale(heart_image, (25, 25))  # Resize the heart to your desired size

bullet_sound = pygame.mixer.Sound("expl6.wav")  # Replace with your sound file path

bullet_image = pygame.image.load("bu1.png")  # Replace with your bullet image file path
bullet_image = pygame.transform.scale(bullet_image, (20, 25))  # Resize the image (adjust the size to fit your game)

enemy_bullet_image = pygame.image.load("bu2.png")  # Replace with your enemy bullet image file path
enemy_bullet_image = pygame.transform.scale(enemy_bullet_image, (20, 25))  # Resize the image (adjust the size to fit your game)

# Load background music
pygame.mixer.music.load("menu.ogg")  # Replace with your music file path
pygame.mixer.music.play(loops=-1, start=0.0)  # Play music in a loop
pygame.mixer.music.set_volume(0.2)  # Set music volume to 30%

enemy_bullet_sound = pygame.mixer.Sound("rocket.ogg")  # Replace with your sound file path

get_ready_sound = pygame.mixer.Sound("getready.ogg")  # Replace with your sound file path

enemy_hit_sound = pygame.mixer.Sound("mini_exp.mp3")  # Replace with your sound file path

enemy_destroyed_sound = pygame.mixer.Sound("rumble1.ogg")  # Replace with your sound file path



# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.health = 3  # Player health
        

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:  # Move up
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:  # Move down
            self.rect.y += PLAYER_SPEED

    def reduce_health(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()

# Load enemy image
enemy_image = pygame.image.load("p2.png")  # Replace with your enemy image file path
enemy_image = pygame.transform.scale(enemy_image, (50, 70))  # Resize to the desired size

# Enemy Bullet class (for enemy attacks)
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Bullet size
        self.image = enemy_bullet_image  # Use the enemy bullet image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calculate the direction to the player
        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2)**0.5
        self.velocity_x = dx / distance * ENEMY_BULLET_SPEED
        self.velocity_y = dy / distance * ENEMY_BULLET_SPEED

        enemy_bullet_sound.play()


    def update(self):
        # Move the bullet towards the player
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Remove the bullet if it goes out of bounds
        if self.rect.top > HEIGHT or self.rect.bottom < 0 or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

# Enemy class with random position
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image  # Set the image to the loaded enemy image
        # Set a random x position within the screen width and fixed y position at the top
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.shoot_delay = random.randint(600, 900)  # Increased range for random shooting delay (slower shooting)
        self.last_shot = pygame.time.get_ticks()  # Time of last shot

    def update(self):
        self.rect.y += ENEMY_SPEED  # Move the enemy down

        # Reinitialize position when the enemy goes off the screen
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH)  # Randomize x position when it goes off-screen
            self.rect.y = 0  # Reset y position to the top
        
        # Randomized shooting with a longer delay (less frequent)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            if random.random() < 0.2:  # 20% chance for an enemy to shoot
                self.shoot()
            self.last_shot = current_time  # Update the last shot time

    def shoot(self):
        # Enemy shoots a bullet toward the player
        enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, player.rect.centerx, player.rect.centery)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)

# Bullet class for player projectiles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Function to reset the game
def reset_game():
    global player, enemies, bullets, enemy_bullets, all_sprites, score, level
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    # Create initial enemies
    for _ in range(3):  # Reduced to 3 initial enemies
        enemy = Enemy()
        enemies.add(enemy)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)

    score = 0  # Reset score
    level = 1  # Reset level

# Function to display the main menu
def main_menu():
    screen.blit(background_image2, (0, 0))  # Draw the background image
    font = pygame.font.SysFont(None, 50)
    title_text = font.render("Space War Game", True, BLACK)
    start_text = font.render("Press Enter to Start", True, GREEN)
    exit_text = font.render("Press ESC to Exit", True, RED)

    # Draw title and start button
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()


# Function to display the home button
def draw_home_button():
    font = pygame.font.SysFont(None, 20)
    home_button = pygame.Rect(WIDTH - 55, HEIGHT - 583, 50, 20)
    pygame.draw.rect(screen, GREEN, home_button)
    home_text = font.render("Home", True, BLACK)
    screen.blit(home_text, (WIDTH - 50, HEIGHT - 580))

    return home_button

# Game setup
reset_game()

# Font for displaying score and level
font = pygame.font.SysFont(None, 30)

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type):
        super().__init__()
         # Load images for each power-up type
        if power_type == "health":
            self.image = pygame.image.load("h1.png")  # Replace with your image file
        elif power_type == "speed":
            self.image = pygame.image.load("s1.png")   # Replace with your image file
        elif power_type == "bullet":
            self.image = pygame.image.load("bu1.png")  # Replace with your image file

        # Resize the image if necessary
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize to fit your game

        self.rect = self.image.get_rect(center=(x, y))
        self.power_type = power_type  # Type of power-up

    def update(self):
        # Move the power-up down the screen
        self.rect.y += 3
        if self.rect.top > HEIGHT:  # Remove power-up if it goes off the screen
            self.kill()

# Function to spawn a power-up
def spawn_power_up():
    # Randomly choose a power-up type
    power_type = random.choice(["health", "speed", "bullet"])
    # Random position
    x = random.randint(50, WIDTH - 50)
    power_up = PowerUp(x, 0, power_type)
    all_sprites.add(power_up)
    power_ups.add(power_up)

# Update the Player class to handle power-ups
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.health = 3  # Player health
        self.speed = PLAYER_SPEED  # Default speed
        self.is_firing_fast = False  # Flag for rapid fire

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:  # Move up
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:  # Move down
            self.rect.y += self.speed

        # Handle rapid fire (if enabled)
        if self.is_firing_fast:
            if keys[pygame.K_SPACE]:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                bullet_sound.play()

    def reduce_health(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def apply_power_up(self, power_type):
        if power_type == "health" and self.health < 3:  # Increase health
            self.health += 1
        elif power_type == "speed":  # Increase speed
            self.speed = PLAYER_SPEED * 1.5  # Increase speed by 1.5x
        elif power_type == "bullet":  # Enable rapid fire
            self.is_firing_fast = True

    def reset_speed(self):
        self.speed = PLAYER_SPEED

# Game setup for power-ups
power_ups = pygame.sprite.Group()

# Update the main game loop to spawn power-ups periodically
spawn_timer = pygame.time.get_ticks()  # Timer for spawning power-ups
power_up_interval = 5000  # 5 seconds interval to spawn power-up

# Main game loop
running = True
clock = pygame.time.Clock()
game_over = False
in_menu = True
get_ready_playing = False  # Flag to check if "get ready" is playing

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if in_menu:
                if event.key == pygame.K_RETURN:  # Start the game on Enter key press
                    get_ready_sound.play()  # Play the "get ready" sound
                    get_ready_playing = True  # Set the flag to True
                    pygame.time.delay(1000)  # Wait for 1 second
                    reset_game()
                    in_menu = False
                elif event.key == pygame.K_ESCAPE:  # Exit the game on ESC key press
                    running = False
            else:
                if event.key == pygame.K_SPACE and not game_over:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    bullet_sound.play()
                if event.key == pygame.K_r and game_over:  # Retry game on 'R' key
                    reset_game()
                    game_over = False
                if event.key == pygame.K_h:  # Go to home on 'H' key
                    in_menu = True
                    game_over = False
                    reset_game()

    # Game logic if not in the main menu
    if not in_menu:
        all_sprites.update()

        # Spawn power-ups periodically
        if pygame.time.get_ticks() - spawn_timer > power_up_interval:
            spawn_power_up()
            spawn_timer = pygame.time.get_ticks()  # Reset the spawn timer

        # Check for collisions with power-ups
        for power_up in power_ups:
            if pygame.sprite.collide_rect(power_up, player):
                player.apply_power_up(power_up.power_type)  # Apply the power-up
                power_up.kill()  # Remove the power-up from the screen

        # Check for collisions with enemy bullets
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(bullet, player):
                bullet.kill()  # Remove the bullet
                enemy_destroyed_sound.play()  # Play the sound when an enemy is destroyed
                player.reduce_health()  # Reduce health of the player
                enemy_hit_sound.play()  # Play the enemy hit sound when the player is hit

        # Check for collisions between player bullets and enemies
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy in hit_enemies:
                bullet.kill()
                enemy_destroyed_sound.play()  # Play the sound when an enemy is destroyed
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                score += 5  # Increment score when an enemy is defeated

        # Reset player speed after some time (for example, after 5 seconds)
        if player.is_firing_fast:
            if pygame.time.get_ticks() - spawn_timer > 4000:  # If 5 seconds have passed
                player.is_firing_fast = False
                player.reset_speed()  # Reset player speed

        # Check if player is dead
        if player.health <= 0 and not game_over:
            game_over = True

   # Check if score reaches 200 to move to Level 2
        if score >= 500 and level == 1:
            level = 2
            ENEMY_SPEED = 2  # Increase the enemy speed for level 2
            for _ in range(3):  # Add more enemies at level 2
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

        # Check if score reaches 250 to move to Level 3
        if score >= 1000 and level == 2:
            level = 3
            ENEMY_SPEED = 2  # Increase the enemy speed for level 3
            for _ in range(4):  # Add more enemies at level 3
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)


        # Draw everything
        screen.fill(BLACK)  # Clear the screen before drawing the new frame
        screen.blit(background_image, (0, 0))  # Draw the background image
        all_sprites.draw(screen)

        # Display health as heart images
        for i in range(player.health):
            screen.blit(heart_image, (5 + i * 35, 2))  # 35 is the spacing between hearts

        # Display score and level
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, RED)
        screen.blit(score_text, (10, 40))
        screen.blit(level_text, (10, 70))  # Display the level

        # End game if health is 0
        if game_over:
            game_over_text = font.render("GAME OVER - Press R to Retry or H to Home", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))

        # Draw Home button
        home_button = draw_home_button()

        # Handle clicking on the Home button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if home_button.collidepoint(event.pos):
                in_menu = True
                game_over = False
                reset_game()

    else:
        # Display the main menu
        main_menu()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
