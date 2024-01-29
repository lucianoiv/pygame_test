import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Test Game!")
blue = (0, 0, 255)
fps = 60
speed = 5
enemy_speed = 2
character_width, character_height = 65, 65
enemy_width, enemy_height = 50, 50

menu_background = pygame.image.load(os.path.join('Assets', 'menu_backgroun.png'))

background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Space Bg 1.png')), (WIDTH, HEIGHT))
background_earth = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'earth.png')), (200, 400))
main_character = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'tiny_ship1.png')), (character_width, character_width))
enemy_character = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'tiny_ship5.png')), (enemy_width,enemy_height)), 180)
ship_hit = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'hit.png')), (50, 50))

bullet_fire = pygame.mixer.Sound(os.path.join('Assets', 'blaster.wav'))
collision = pygame.mixer.Sound(os.path.join('Assets', 'impact.wav'))

bullet_speed = 10
max_bullets = 5
hero_hit = pygame.USEREVENT + 1
enemy_hit = pygame.USEREVENT + 2

# SPAWN OBJECTS WINDOW

def draw(hero, enemy, hero_bullets, enemies):
    
    WIN.blit(background, (0,0))
    WIN.blit(background_earth, (300,0))
    WIN.blit(main_character, (hero.x, hero.y))
    WIN.blit(enemy_character, (enemy.x, enemy.y))
    
    
    
    for bullet in hero_bullets:
        pygame.draw.rect(WIN, (0,255,0), bullet)
    
    pygame.display.update()
        

    
# BULLETS FUNCTION
    
def handle_bullets(hero_bullets, enemy_bullets, hero, enemy):
    for bullet in hero_bullets:
        bullet.y -= bullet_speed 
        if enemy.colliderect(bullet):
            hero_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(enemy_hit))
        elif bullet.y < 0:
            hero_bullets.remove(bullet)
            
    for bullet in enemy_bullets:
        bullet.y += bullet_speed 
        if hero.colliderect(bullet):
            enemy_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(hero_hit))
        elif enemy_bullets.y > HEIGHT:
            enemy_bullets.remove(bullet)
    
# GAME

def main():
    enemy = pygame.Rect(random.randrange(0,WIDTH),100,enemy_width,enemy_height) # (x position, y position, width, height)
    hero = pygame.Rect(230,420,character_width,character_height)
    
    hero_bullets = []
    enemy_bullets = []
    
    enemies = []

    #hero_lives = 3
        
    clock = pygame.time.Clock()
    run = True
    while run:
                
        enemy.y += enemy_speed
        
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(hero_bullets) < max_bullets:
                    bullet = pygame.Rect(hero.x + character_height // 2, hero.y , 5 , 15)
                    hero_bullets.append(bullet)
                    
                    bullet_fire.play()
                
            if event.type == enemy_hit:
                collision.play()
        
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_LEFT] and hero.x - speed > 0: #LEFT + check border
            hero.x -= speed
        if keys_pressed[pygame.K_RIGHT] and hero.x - speed < 425: #RIGHT + check border
            hero.x += speed
        if keys_pressed[pygame.K_UP] and hero.y - speed > 0: #UP + check border
            hero.y -= speed
        if keys_pressed[pygame.K_DOWN] and hero.y - speed < 425: #DOWN + check border
            hero.y += speed

        
        handle_bullets(hero_bullets,enemy_bullets,hero,enemy)
        draw(hero, enemy, hero_bullets, enemies)
    
    pygame.quit()

# MAIN MENU
    
def main_menu():
        title_font = pygame.font.SysFont("comicsans", 30)
        run = True
        while run:
            WIN.blit(menu_background , (0,0))
            title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
            WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 200))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
        pygame.quit()

main_menu()


