'''Too Much Sun! is a 2D wave-based game. Armed with a pool noodle and water gun, the player must \
cool down waves of sunburnt people who are acting strangely due to staying in the sun too long.'''

import pygame, sys, random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Too Much Sun!")
clock = pygame.time.Clock()

# background music
#pygame.mixer.music.load("atomic_apple_juice.wav") # music by BobThePilot on youtube.com
#pygame.mixer.music.set_volume(0.4)
#pygame.mixer.music.play(-1)

# func to print text to screen
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))
    
# class for sunburnt little guys
class Enemy(object):
    def __init__(self, x, direction):
        self.image = pygame.image.load("sunburnt_guy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 440
        self.speed = random.randint(1, 2)
        self.direction = direction
    
    def move(self):
        self.rect.x += self.direction * self.speed

# load player & vars
player_img = pygame.image.load("player.png").convert_alpha()
player_rect = player_img.get_rect()
player_rect.x = 350
player_rect.y = 440
font = pygame.font.Font(None, 27)
player_health = 100
ouch = pygame.mixer.Sound("ouch.wav") # sound by OwlStorm on freesound.org

# if player is no longer alive
def restart():
    global player_health
    global water
    print_text(font, 400, 300, "Game over...")
    print_text(font, 400, 330, "Press R to restart.")
    waiting = True
    pygame.display.flip()
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_r:
                    waiting = False
                    player_health = 100
                    water = 20
                elif event.key == K_ESCAPE:
                    sys.exit()
                else:
                    waiting = True

# water gun vars
droplets = []
water = 20
last_shot_time = 0
shot_cooldown = 400 
water_splash = pygame.mixer.Sound("splash.wav")  # sound by rombart on freesound.org

# enemy vars
enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 4000

# pool noodle vars
noodle_active = False
last_noodle_time = 0
noodle_timer = 0
noodle_cooldown = 300 
facing_right = True  # updated based on mouse position
bonk = pygame.mixer.Sound("plop.wav") # sound by Squirrel_404 on freesound.org

# wave vars
wave = 1
enemies_needed = 10
enemies_remaining = enemies_needed  # how many still need to be spawned
enemies_helped = 0  # how many you've helped

done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        # handle mouse buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # left click - pool noodle swing
            if event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - last_noodle_time >= noodle_cooldown:
                    noodle_active = True
                    noodle_timer = 10  # frames the swing lasts
                    facing_right = mouse_pos[0] > player_rect.centerx
                    
                    # reset cooldown timer
                    last_noodle_time = current_time
                    
                    # play bonk sound
                    bonk.play()

            # right click - shoot water gun
            elif event.button == 3:
                current_time = pygame.time.get_ticks()
                if water >= 1 and current_time - last_shot_time >= shot_cooldown:
                    start_pos = pygame.Vector2(player_rect.center)
                    target = pygame.Vector2(mouse_pos)
                    direction = (target - start_pos).normalize()

                    # create droplet
                    droplet = pygame.Rect(start_pos.x, start_pos.y, 10, 5)
                    droplets.append((droplet, direction))

                    # use one water and reset cooldown timer
                    water -= 1
                    last_shot_time = current_time

                    # play water splash sound
                    water_splash.play()

        # handle key presses
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

    # movement
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        player_rect.x -= 5
    if keys[K_d]:
        player_rect.x += 5

    # keep the player on the screen
    player_rect.x = max(0, min(player_rect.x, 800 - player_rect.width))

    # handle pool noodle logic    
    if noodle_active:
        noodle_timer -= 1
        if noodle_timer <= 0:
            noodle_active = False

    # draw sky and sand
    screen.fill((135, 206, 250))
    pygame.draw.rect(screen, (255, 255, 153), (0, 500, 800, 100))
    
    # draw water amount, health, wave
    print_text(font, 40, 60, "Water: " + str(water))
    print_text(font, 650, 60, "Health: " + str(player_health))
    print_text(font, 350, 60, "Wave: " + str(wave))

    # draw player
    screen.blit(player_img, player_rect)
    
    # enemy spawn logic
    enemy_spawn_timer += clock.get_time()
    if enemies_remaining > 0 and enemy_spawn_timer >= enemy_spawn_delay:
        side = random.choice(["left", "right"])
        if side == "left":
            enemies.append(Enemy(-96, 1))
        elif side == "right":
            enemies.append(Enemy(800, -1))
        enemy_spawn_timer = 0
        enemies_remaining -= 1

    # water gun logic
    for d in droplets[:]:
        rect, direction = d
        rect.x += direction.x * 10
        rect.y += direction.y * 10
        
        # check for collisions droplet
        for enemy in enemies[:]:
            if rect.colliderect(enemy.rect):
                droplets.remove(d)
                enemies.remove(enemy)
                enemies_helped += 1
                if random.random() < 0.05:
                    # 20% chance to restore 5 water
                    water = min(water + 2, 20)  # cap at max water
                break

        if rect.right < 0 or rect.left > 800 or rect.bottom < 0 or rect.top > 600:
            droplets.remove(d)
        else:
            pygame.draw.rect(screen, (222, 244, 252), rect)

    # draw pool noodle
    if noodle_active:
        if facing_right:
            noodle_rect = pygame.Rect(player_rect.right, player_rect.y + 40, 40, 10)
        else:
            noodle_rect = pygame.Rect(player_rect.left - 40, player_rect.y + 40, 40, 10)

        pygame.draw.rect(screen, (0, 255, 0), noodle_rect)
        
    # draw and move enemies
    for enemy in enemies[:]:
        enemy.move()
        screen.blit(enemy.image, enemy.rect)
        
        # check for collisions player, noodle
        if enemy.rect.colliderect(player_rect):
            enemies.remove(enemy)
            ouch.play()
            player_health -= 20
            if player_health <= 0:
                # force health display and refresh screen
                screen.fill((135, 206, 250))
                pygame.draw.rect(screen, (255, 255, 153), (0, 500, 800, 100))
                screen.blit(player_img, player_rect)
                print_text(font, 40, 60, "Water: " + str(water))
                print_text(font, 650, 60, "Health: 0")
                pygame.display.flip()
                restart()
        if noodle_active and noodle_rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            enemies_helped += 1
            if random.random() < 0.05:
                # 20% chance to restore 5 water
                water = min(water + 2, 20)  # cap at max water
                
    if enemies_helped >= enemies_needed:
        wave += 1
        enemies_needed = 10 + wave * 2
        enemies_remaining = enemies_needed
        enemies_helped = 0
        enemy_spawn_delay = max(500, enemy_spawn_delay - 200)
            
    pygame.display.flip()
    clock.tick(60)
