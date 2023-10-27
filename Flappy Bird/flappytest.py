import pygame,sys,time

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load("Flappy Bird/bird/bluebird-upflap.png")
        self.rect = self.image.get_rect(center = (600,300))
        self.gravity = 0.20

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 200

    def update(self):
        self.direction.y += self.gravity
        self.pos.y = self.direction.y * self.speed * dt 
        self.rect.centery = round(self.pos.y)

pygame.init()
display_surf = pygame.display.set_mode((1200,600))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

player = Player(all_sprites)

previous_time = time.time()

# game loop 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = time.time() - previous_time
    previous_time = time.time()

    display_surf.fill("black")

    all_sprites.update()

    all_sprites.draw(display_surf)

    clock.tick(60)

    pygame.display.update()