'''Too Much Sun! is a 2D wave-based game. Armed with a pool noodle and aloe vera, the player must \
cool down waves of sunburnt people who are acting strangely due to staying in the sun too long.'''

import pygame, sys, random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Too Much Sun!")
clock = pygame.time.Clock()

# background music
music_list = ["invasive_idiot.wav", "luminous_lamb.wav", "peckish_pumpkin.wav", "radical_robot.wav"] # music by BobThePilot on youtube.com
music = random.choice(music_list)
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
print("Music:", music, "by BobThePilot on youtube.com")

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
player_health = 100
score = 0
ouch = pygame.mixer.Sound("ouch.wav") # sound by OwlStorm on freesound.org

# font vars
font = pygame.font.Font(None, 27)
dark = (0, 0, 0)

# if player is no longer alive
def restart():
    global player_health
    global aloe
    print_text(font, 250, 300, "Game over...", dark)
    print_text(font, 250, 330, "Press R to restart.", dark)
    waiting = True
    pygame.display.flip()
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    waiting = False
                    player_health = 100
                    aloe = 20
                elif event.key == K_ESCAPE:
                    sys.exit()
                else:
                    waiting = True

# aloe vars
droplets = []
aloe = 20
last_shot_time = 0
shot_cooldown = 400 
aloe_splash = pygame.mixer.Sound("splash.wav")  # sound by rombart on freesound.org

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
enemies_needed = 10 # constant (sorta)
enemies_remaining = enemies_needed  # how many still need to be spawned
enemies_helped = 0  # how many you've helped
wave_alarm = pygame.mixer.Sound("beep.wav") # sound by Greencouch on freesound.org

# menu/controls func
def show_menu():
    screen.fill((135, 206, 250))
    pygame.draw.rect(screen, (255, 255, 153), (0, 500, 800, 100))

    print_text(font, 250, 100, "Too Much Sun!", (0, 0, 0))
    print_text(font, 250, 220, "Use A/D to move left/right", dark)
    print_text(font, 250, 250, "Left Click - Swing Pool Noodle", dark)
    print_text(font, 250, 280, "Right Click - Spray Aloe", dark)
    print_text(font, 250, 310, "Help sunburnt people and survive!", dark)
    print_text(font, 250, 360, "Press ENTER to start...", dark)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False
                if event.key == K_ESCAPE:
                    sys.exit()
             
show_menu()
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

            # right click - shoot aloe
            elif event.button == 3:
                current_time = pygame.time.get_ticks()
                if aloe >= 1 and current_time - last_shot_time >= shot_cooldown:
                    # Rabbid76 on Stack Overflow
                    start_pos = pygame.Vector2(player_rect.center)
                    target = pygame.Vector2(mouse_pos)
                    direction = (target - start_pos).normalize()

                    # create droplet
                    droplet = pygame.Rect(start_pos.x, start_pos.y, 10, 5)
                    droplets.append((droplet, direction))

                    # use one aloe and reset cooldown timer
                    aloe -= 1
                    last_shot_time = current_time

                    # play aloe splash sound
                    aloe_splash.play()

        # handle quit
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
    
    # draw aloe amount, health, wave, score
    print_text(font, 40, 80, "Aloe: " + str(aloe), dark)
    print_text(font, 650, 80, "Health: " + str(player_health), dark)
    print_text(font, 670, 540, "Wave: " + str(wave), dark)
    print_text(font, 350, 80, "Score: " + str(score), dark)

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

    # aloe logic
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
                score += 10
                if random.random() < 0.1:
                    # 10% chance to restore 2 aloe
                    aloe = min(aloe + 2, 20)  # cap at max aloe
                break

        if rect.right < 0 or rect.left > 800 or rect.bottom < 0 or rect.top > 600:
            droplets.remove(d)
        else:
            pygame.draw.rect(screen, (210, 255, 220), rect)

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
            enemies_helped += 1
            score += 10
            ouch.play()
            player_health -= 20
            if player_health <= 0:
                # force health display and refresh screen
                screen.fill((135, 206, 250))
                pygame.draw.rect(screen, (255, 255, 153), (0, 500, 800, 100))
                screen.blit(player_img, player_rect)
                print_text(font, 650, 80, "Health: 0", dark)
                print_text(font, 40, 80, "Aloe: " + str(aloe), dark)
                print_text(font, 670, 540, "Wave: " + str(wave), dark)
                print_text(font, 350, 80, "Score: " + str(score), dark)
                pygame.display.flip()
                restart()
        if noodle_active and noodle_rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            enemies_helped += 1
            score += 10
            if random.random() < 0.1:
                # 10% chance to restore 2 aloe
                aloe = min(aloe + 2, 20)  # cap at max aloe
                
    # check if new wave should begin
    if enemies_helped >= enemies_needed:
        score += 50
        wave += 1
        wave_alarm.play()
        enemy_spawn_delay = max(300, enemy_spawn_delay - 300)

        # reset
        enemies_needed = 10 + wave * 2
        enemies_remaining = enemies_needed
        enemies_helped = 0
        
    pygame.display.flip()
    clock.tick(60)
