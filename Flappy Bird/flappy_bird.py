import pygame,sys,time
from os import walk
from random import choice,randint

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.import_assests()
        self.frame_index = 0
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center = (50,256))
        self.gravity = 0.35 

        # float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0,0) 
        self.speed = 100 

        self.rotation = 0
        self.rotation_speed = 100

    def import_assests(self):
        self.animations = []
        for _,_,bird_name in walk("bird"):
             for file_name in bird_name:
                surf = pygame.image.load(f"bird/{file_name}").convert_alpha()
                self.animations.append(surf)
    
    def animate(self):
       self.frame_index += 15 * dt 
       if self.frame_index > 3:
            self.frame_index = 0
       self.bird_surf = self.animations[int(self.frame_index)] # the surface to be rotated, to prevent self.image from losing quality and crashing the game
       self.rotation += self.rotation_speed * dt 
       self.image = pygame.transform.rotozoom(self.bird_surf,-self.rotation,1)

    def collision(self):
        global game_active
        if pygame.sprite.spritecollide(self,collision_sprites,False) or self.rect.top <= -100 or self.rect.bottom >= 450:
            game_active = False
            pygame.mixer.Sound("sounds/sfx_hit.wav").play()

    def move(self):
        keys = pygame.key.get_pressed()
        self.direction.y += self.gravity 
        
        if keys[pygame.K_SPACE]:
            self.direction.y = 0 # to reset the gravity and focus on the upward movement of the bird
            self.direction.y = -3.5
            self.rotation = 0
            self.rotation = -40
            
    def update(self):
        self.animate()
        #self.rotate()
        self.move()
        self.pos.y += self.direction.y * self.speed * dt 
        self.rect.y = round(self.pos.y) 
        self.collision()

class BottomPipe(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("assets/pipe-green.png").convert_alpha()
        if pos[1] < 0:
            self.image = pygame.transform.flip(self.image,False,True)
        
        self.rect = self.image.get_rect(midtop = pos)

        # float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(-1,0)
        self.speed = 175

    def move(self):
        self.pos.x += self.direction.x * self.speed * dt 
        self.rect.centerx = round(self.pos.x)

    def pipe_score(self):
        global score,can_score
        if 50 < self.rect.centerx < 55 and can_score:
            score += 1
            can_score = False
            pygame.mixer.Sound("sounds/sfx_point.wav").play()
        if self.rect.centerx < 45:
            can_score = True

    def update(self):
        self.move()
        self.pipe_score()
        if self.rect.left <= -100:
            self.kill()
        if not game_active: 
            self.kill()

class TopPipe(BottomPipe):
    def __init__(self,pos,groups):
        super().__init__(pos,groups)

class Floor:
    def __init__(self):
        self.floor_surf = pygame.image.load("assets/base.png").convert()
        self.floor_x_pos = 0

    def display(self):
        if self.floor_x_pos <= -288:
            self.floor_x_pos = 0

        self.floor_x_pos -= 2.5
        display_surf.blit(self.floor_surf,(self.floor_x_pos,450))
        display_surf.blit(self.floor_surf,(self.floor_x_pos + 288,450))

class Score:
    def __init__(self):
        self.font = pygame.font.Font("04B_19.ttf",20)

    def display_score(self,game_status):
        if game_status == "playing":
            score_surf = self.font.render(f"{score}",True,"white")
            score_rect = score_surf.get_rect(center = (144,50))
            display_surf.blit(score_surf,score_rect)
        if game_status == "game over":
            score_surf = self.font.render(f"Score: {score}",True,"white")
            score_rect = score_surf.get_rect(center = (144,50))
            display_surf.blit(score_surf,score_rect)

            high_score_surf = self.font.render(f'High score: {int(high_score)}',True,"white")
            high_score_rect = high_score_surf.get_rect(center = (144,420))
            display_surf.blit(high_score_surf,high_score_rect)


pygame.init()
pygame.mixer.init()
WIDTH,HEIGHT = 288,512
display_surf = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Birdy")
clock = pygame.time.Clock()
game_active = True

# import background, title
bg_surf = pygame.image.load("assets/background-day.png").convert()
title_surf = pygame.image.load("assets/message.png").convert_alpha()
title_rect = title_surf.get_rect(center = (WIDTH/2,HEIGHT/2))

# import floor
floor = Floor()

# sprite groups
all_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()

# sprite creation
player = Player(all_sprites)

# pipe timer
pipe_timer = pygame.event.custom_type()
pygame.time.set_timer(pipe_timer,900)

# score
score = 0
high_score = 0
can_score = True
score_prompt = Score()

previous_time = time.time()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pipe_timer and game_active:
            height = choice([200,210,225,250,275,300,310,325,350,375,400])
            BottomPipe((350,height),[all_sprites,collision_sprites])
            TopPipe((350,height - randint(430,450)),[all_sprites,collision_sprites])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active:
            pygame.mixer.Sound("sounds/sfx_wing.wav").play() # i play the sound here since when i play this sound in the input function of my Player class it sounds different
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_active:
            player.direction.y = 0 # reset the upward movement
            player.rect.center = (50,256)
            player.pos =  pygame.math.Vector2(player.rect.center)
            game_active = True
            score = 0
            player.rotation = 0
            can_score = True

    clock.tick(60)

    # delta time
    dt = time.time() - previous_time
    previous_time = time.time() 

    # background
    display_surf.blit(bg_surf,(0,0))

    if game_active:
        # update
        all_sprites.update()

        # draw
        all_sprites.draw(display_surf)

        # score
        score_prompt.display_score("playing")
    else:
        if score > high_score: high_score = score
        display_surf.blit(title_surf,title_rect)
        score_prompt.display_score("game over")
    

    # floor
    floor.display()
    


    # update frame
    pygame.display.update()
