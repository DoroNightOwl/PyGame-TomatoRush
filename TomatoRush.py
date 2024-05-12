#IMPORT LIBRARIES AND MODULES
import pygame, time, math, os, random, sys
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
#CONSTANTS
WINDOW_SIZE = (1280,720)
WINDOW_FACTOR = 4
GAME_TITLE = "Tomato Rush"
GAME_SCREEN_SIZE = (320,180)
MAX_FPS = 60
lT = time.time()
dT = time.time()
BACKGROUND_COLOR = (161,148,140)
#HEALTH
HEALTH_COLOR = (237,43,37)
#WINDOW INITIALIZATION
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(GAME_TITLE)
game_surface = pygame.Surface(GAME_SCREEN_SIZE)
clock = pygame.time.Clock()
#CLASSES
class staticObject:
    def __init__(self,image,position):
        self.texture = pygame.image.load(image).convert_alpha()
        self.rect = self.texture.get_rect(topleft=position)
class hostileObject:
    def __init__(self,image,image2,position):
        self.texture = pygame.image.load(image).convert_alpha()
        self.texture2 = pygame.image.load(image2).convert_alpha()
        self.rect = self.texture.get_rect(topleft=position)
        self.posX = self.rect.x
        self.posY = self.rect.y
        self.lastX = self.posX
        self.lastY = self.posY
        self.movement = True
        self.explode = False
        self.explodeTime = None 
class playableCharacter:
    def __init__(self,image,position):
        self.texture = pygame.image.load(image).convert_alpha()
        self.rect = self.texture.get_rect(topleft=position)
        self.posX = self.rect.x
        self.posY = self.rect.y
        self.lastX = self.posX
        self.lastY = self.posY
        self.INITIAL_SPEED = 40
        self.speed = self.INITIAL_SPEED
    def move(self,speed,dT):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] == True and keys[pygame.K_a] == False and keys[pygame.K_s] == False and keys[pygame.K_d] == False :
            self.posY -= speed*dT
        if keys[pygame.K_w] == False and keys[pygame.K_a] == True and keys[pygame.K_s] == False and keys[pygame.K_d] == False :
            self.posX -= speed*dT
        if keys[pygame.K_w] == False and keys[pygame.K_a] == False and keys[pygame.K_s] == True and keys[pygame.K_d] == False :
            self.posY += speed*dT
        if keys[pygame.K_w] == False and keys[pygame.K_a] == False and keys[pygame.K_s] == False and keys[pygame.K_d] == True :
            self.posX += speed*dT
        diagonal_speed = math.sqrt(speed*speed/2)
        if keys[pygame.K_w] == True and keys[pygame.K_a] == True and keys[pygame.K_s] == False and keys[pygame.K_d] == False :
            self.posX -= diagonal_speed*dT
            self.posY -= diagonal_speed*dT
        if keys[pygame.K_w] == True and keys[pygame.K_a] == False and keys[pygame.K_s] == False and keys[pygame.K_d] == True :
            self.posX += diagonal_speed*dT
            self.posY -= diagonal_speed*dT
        if keys[pygame.K_w] == False and keys[pygame.K_a] == True and keys[pygame.K_s] == True and keys[pygame.K_d] == False :
            self.posX -= diagonal_speed*dT
            self.posY += diagonal_speed*dT
        if keys[pygame.K_w] == False and keys[pygame.K_a] == False and keys[pygame.K_s] == True and keys[pygame.K_d] == True :
            self.posX += diagonal_speed*dT
            self.posY += diagonal_speed*dT
        self.rect.x = self.posX
        self.rect.y = self.posY
    def take_last_pos(self):
        self.lastX = self.posX
        self.lastY = self.posY
    def keep_margins(self):
        if self.rect.x < 0 :
            self.posX = self.lastX
            self.rect.x = self.posX
        if self.rect.x+self.rect.width > 320 :
            self.posX = self.lastX
            self.rect.x = self.posX
        if self.rect.y < 0 :
            self.posY = self.lastY
            self.rect.y = self.posY
        if self.rect.y+self.rect.height > 180 :
            self.posY = self.lastY
            self.rect.y = self.posY
    def player_collision(self):
        for i in range(len(enemy_list)):
            if player.rect.colliderect(enemy_list[i]):
                self.posX = self.lastX
                self.posY = self.lastY
                self.rect.x = self.posX
                self.rect.y = self.posY
                updating_health_bar()
#FUNCTIONS
#---->CACHE FUNCTION
def resource_path(relative_path): 
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)
#---->ENEMY SPAWN
MAX_SPAWN_RATE = 0.75
spawn_rate = MAX_SPAWN_RATE
next_spawn = None
def enemy_spawn(spawn_rate):
    global next_spawn
    if next_spawn == None : next_spawn = time.time() + spawn_rate
    random_x = random.randint(0,320)
    random_y = random.randint(0,180)
    collision_counter = 0
    if player.rect.collidepoint(random_x,random_y) : collision_counter += 1
    if player.rect.collidepoint(random_x+player.rect.width,random_y): collision_counter += 1
    if player.rect.collidepoint(random_x,random_y+player.rect.height) : collision_counter += 1
    if player.rect.collidepoint(random_x+player.rect.width,random_y+player.rect.height) : collision_counter += 1
    for i in range(len(enemy_list)):
        if enemy_list[i].rect.collidepoint(random_x,random_y) : collision_counter += 1
        if enemy_list[i].rect.collidepoint(random_x+player.rect.width,random_y): collision_counter += 1
        if enemy_list[i].rect.collidepoint(random_x,random_y+player.rect.height) : collision_counter += 1
        if enemy_list[i].rect.collidepoint(random_x+player.rect.width,random_y+player.rect.height) : collision_counter += 1
    if collision_counter == 0 :
        if  time.time() > next_spawn :
            next_spawn = time.time() + spawn_rate
            enemy_list.append(hostileObject(resource_path("assets\\enemy.png"),resource_path("assets\\enemyDeath.png"),(random_x,random_y)))
#---->BLITTING ENEMIES
def blit_enemy_list():
    for i in range(len(enemy_list)):
        game_surface.blit(enemy_list[i].texture,enemy_list[i].rect)
#---->ENEMIES FOLLOW THE PLAYER
MIN_ENEMY_SPEED = 20
enemy_speed = MIN_ENEMY_SPEED
def enemy_follow_player(enemy_speed,dT):
    global enemy_list
    for i in range(len(enemy_list)):
        if enemy_list[i].movement == True :
            enemy_diagonal_speed = math.sqrt(enemy_speed*enemy_speed/2)
            if enemy_list[i].rect.x < player.rect.x and enemy_list[i].rect.y == player.rect.y :
                enemy_list[i].posX += enemy_speed * dT
                enemy_list[i].rect.x = enemy_list[i].posX
            if enemy_list[i].rect.x > player.rect.x and enemy_list[i].rect.y == player.rect.y :
                enemy_list[i].posX -= enemy_speed * dT
                enemy_list[i].rect.x = enemy_list[i].posX
            if enemy_list[i].rect.y < player.rect.y and enemy_list[i].rect.x == player.rect.x :
                enemy_list[i].posY += enemy_speed * dT
                enemy_list[i].rect.y = enemy_list[i].posY
            if enemy_list[i].rect.y > player.rect.y and enemy_list[i].rect.x == player.rect.x :
                enemy_list[i].posY -= enemy_speed * dT
                enemy_list[i].rect.y = enemy_list[i].posY
            if enemy_list[i].rect.x < player.rect.x and enemy_list[i].rect.y < player.rect.y :
                enemy_list[i].posX += enemy_diagonal_speed*dT
                enemy_list[i].posY += enemy_diagonal_speed*dT
                enemy_list[i].rect.x = enemy_list[i].posX
                enemy_list[i].rect.y = enemy_list[i].posY
            if enemy_list[i].rect.x > player.rect.x and enemy_list[i].rect.y < player.rect.y :
                enemy_list[i].posX -= enemy_diagonal_speed*dT
                enemy_list[i].posY += enemy_diagonal_speed*dT
                enemy_list[i].rect.x = enemy_list[i].posX
                enemy_list[i].rect.y = enemy_list[i].posY
            if enemy_list[i].rect.x > player.rect.x and enemy_list[i].rect.y > player.rect.y :
                enemy_list[i].posX -= enemy_diagonal_speed*dT
                enemy_list[i].posY -= enemy_diagonal_speed*dT
                enemy_list[i].rect.x = enemy_list[i].posX
                enemy_list[i].rect.y = enemy_list[i].posY
            if enemy_list[i].rect.x < player.rect.x and enemy_list[i].rect.y > player.rect.y :
                enemy_list[i].posX += enemy_diagonal_speed*dT
                enemy_list[i].posY -= enemy_diagonal_speed*dT
                enemy_list[i].rect.x = enemy_list[i].posX
                enemy_list[i].rect.y = enemy_list[i].posY
#---->GETTING THE ENEMIES LAST POSITIONS
def enemy_last_pos():
    for i in range(len(enemy_list)):
        enemy_list[i].lastX = enemy_list[i].posX
        enemy_list[i].lastY = enemy_list[i].posY
#---->CHECKS COLLISION WITH PLAYER AND DOES DAMAGE
def enemy_collision():
    for i in range(len(enemy_list)):
        for j in range(len(enemy_list)):
            if i==j : pass
            else:
                if enemy_list[i].rect.colliderect(enemy_list[j].rect):
                    enemy_list[i].posX = enemy_list[i].lastX
                    enemy_list[i].posY = enemy_list[i].lastY
                    enemy_list[i].rect.x = enemy_list[i].posX
                    enemy_list[i].rect.y = enemy_list[i].posY
                if enemy_list[i].rect.colliderect(player.rect):
                    enemy_list[i].posX = enemy_list[i].lastX
                    enemy_list[i].posY = enemy_list[i].lastY
                    enemy_list[i].rect.x = enemy_list[i].posX
                    enemy_list[i].rect.y = enemy_list[i].posY
                    updating_health_bar()
#---->HEALTH FUNCTION AND VARIABLES
MAX_HEALTH = 500
HEALTH_COLOR = (237,43,37)
HEALTH_BAR_SIZE = 56
current_health = MAX_HEALTH
health_bar_fill = 56
def updating_health_bar():
    global health_fill
    global health_bar_fill
    global run_game
    global return_to_main_menu_timer
    health_bar_fill -= HEALTH_BAR_SIZE/MAX_HEALTH
    health_fill = pygame.Surface((health_bar_fill,8))
    if health_bar_fill <= 2 :
        run_game = False
        if return_to_main_menu_timer == None :
            return_to_main_menu_timer = time.time() + 3
#---->DISPLAYS GAMEOVER AND RESETS THE GAME
run_game = True
return_to_main_menu_timer = None
def set_gameover():
    global health_bar_fill
    global run_game
    global return_to_main_menu_timer
    global main_menu_on
    global level_one_on
    global enemy_list
    global SCORE
    global enemy_speed
    global spawn_rate
    if run_game == False :
        window.blit(gameover_text,gameover_text_rect)
        if return_to_main_menu_timer == None :
            return_to_main_menu_timer = time.time() + 3
        if time.time() > return_to_main_menu_timer :
            #GOING BACK TO MAIN MENU
            main_menu_on = True
            level_one_on = False
            enemy_list = []
            #RESETTING PLAYER POSITION
            player.posX = 160-10
            player.posY = 90-10
            player.rect.x = player.posX
            player.rect.y = player.posY
            player.speed = player.INITIAL_SPEED
            #RESETTING SCORE AND HEALTH
            SCORE = 0
            health_bar_fill = HEALTH_BAR_SIZE
            run_game = True
            #RESETTING THE ENEMY STRENGTH
            return_to_main_menu_timer = None
            enemy_speed = MIN_ENEMY_SPEED
            spawn_rate = MAX_SPAWN_RATE
            pygame.mixer.music.play(-1)
            
#---->DESTROYS THE ENEMY ON CLICK
SCORE = 0
def destroy_enemy():
    global SCORE
    for i in range(len(enemy_list)):
        if enemy_list[i].rect.collidepoint(mouse_x,mouse_y) and mouse_click == True :
            enemy_list[i].explode = True
            enemy_list[i].explodeTime = time.time() + 0.5
            enemy_list[i].movement = False
            enemy_list[i].texture = enemy_list[i].texture2
        if enemy_list[i].explode == True :
            if time.time() > enemy_list[i].explodeTime :
                #---->UPON DESTRUCTION SCORE INCREASES AND ENEMIES GET STRONGER
                del enemy_list[i]
                SCORE += 1
                player.speed += 0.025
                make_enemies_stronger()
                break
#---->MAKES ENEMIES STRONKKKER
speed_growth = 0.075
spawn_rate_growth = 0.0005
def make_enemies_stronger():
    global spawn_rate
    global enemy_speed
    spawn_rate -= spawn_rate_growth
    enemy_speed += speed_growth
#SCENES
main_menu_on = True
def main_menu():
    game_surface.blit(background_mainmenu.texture,background_mainmenu.rect)
    game_surface.blit(play_button.texture,play_button.rect)
    window.blit(pygame.transform.scale(game_surface,WINDOW_SIZE),(0,0))
level_one_on = False
def level_one():
    set_gameover()
    if run_game == True :
        #---->BLITTING OBJECTS ON THE SCREEN
        game_surface.blit(background.texture,background.rect)
        game_surface.blit(player.texture,player.rect)
        blit_enemy_list()
        health_fill = pygame.Surface((health_bar_fill,8))
        health_fill.fill(HEALTH_COLOR)
        game_surface.blit(health_bar,health_bar_rect)
        game_surface.blit(health_fill,health_fill_rect)
        #---->CALLING GAMEPLAY FUNCTIONS
        player.take_last_pos()
        enemy_last_pos()
        player.move(player.speed,dT)
        player.keep_margins()
        player.player_collision()
        enemy_spawn(spawn_rate)
        enemy_follow_player(enemy_speed,dT)
        enemy_collision()
        destroy_enemy()
        #---->SHOWING THE SCORE
        score_msg = "SCORE : " + str(SCORE)
        score_text = font_one.render(score_msg,False,"white")
        score_text_rect = score_text.get_rect(topleft=(60,100))
        #---->DRAWING EVERYTHING IN WINDOW
        window.blit(pygame.transform.scale(game_surface,WINDOW_SIZE),(0,0))
        window.blit(score_text,score_text_rect)
#OBJECT GENERATION
player = playableCharacter(resource_path("assets\\player.png"),(160-10,90-10))
background = staticObject(resource_path("assets\\background.png"),(0,0))
background_mainmenu = staticObject(resource_path("assets\\backgroundMainMenu.png"),(0,0))
background_mainmenu.texture = pygame.transform.scale_by(background_mainmenu.texture,2)
background_mainmenu.rect = background_mainmenu.texture.get_rect(topleft=(0,0))
play_button = staticObject(resource_path("assets\\playButton.png"),(160-50,90-22))
play_button.texture = pygame.transform.scale_by(play_button.texture,2)
play_button.rect = play_button.texture.get_rect(topleft=(160-50,90-22))
enemy_list = []
game_icon = pygame.image.load(resource_path("assets\\icon2.ico")).convert_alpha()
pygame.display.set_icon(game_icon)
#---->MUSIC PLAY
pygame.mixer.music.load(resource_path("assets\\game_music.wav"))
pygame.mixer.music.play(-1)
#---->FONTS
font_one = pygame.font.Font(resource_path("assets\\PixCon.ttf"),24)
font_two = pygame.font.Font(resource_path("assets\\PixCon.ttf"),96)
#---->HEALTH BAR
health_bar = pygame.Surface((60,12))
health_bar.fill("white")
health_bar_rect = health_bar.get_rect(topleft=(10,10))
health_fill = pygame.Surface((56,8))
health_fill.fill(HEALTH_COLOR)
health_fill_rect = health_bar.get_rect(topleft=(12,12))
#---->GAMEOVER TEXT
gameover_msg = "GAME OVER!"
gameover_text = font_two.render(gameover_msg,False,"white")
gameover_text_rect = gameover_text.get_rect(center=(1280/2,720/2))
#GAME MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and play_button.rect.collidepoint((mouse_x,mouse_y)) and  main_menu_on == True :
            main_menu_on = False
            level_one_on = True
    #---->GET MOUSE COORDINATES
    mouse_click = pygame.mouse.get_pressed()
    mouse_click = mouse_click[0]
    mouse_pos = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse_pos[0]/WINDOW_FACTOR, mouse_pos[1]/WINDOW_FACTOR
    #---->SCENES
    if main_menu_on : main_menu()
    if level_one_on : level_one()
    #---->DELTATIME
    dT = time.time()-lT
    lT = time.time()
    clock.tick(MAX_FPS)
    pygame.display.update()
#END OF PROGRAM
