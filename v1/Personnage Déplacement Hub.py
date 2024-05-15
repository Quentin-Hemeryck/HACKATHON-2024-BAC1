import pygame as p

p.init()


LARGEUR, HAUTEUR = 679, 676
surface = p.display.set_mode((LARGEUR, HAUTEUR))
p.display.set_caption("hadesLikeGaming")
background = p.image.load("assets/map.png").convert_alpha()
surface.blit(background, (0,0))

class Asset:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        surface.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.images = images
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 5
        self.speed = 200

    def draw(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_counter = 0
        image = self.images[self.current_frame]
        surface.blit(image, (self.x, self.y))

    def update(self, dt):
        keys = p.key.get_pressed()
        if keys[p.K_q]:
            self.x -= self.speed * dt
        if keys[p.K_d]:
            self.x += self.speed * dt
        if keys[p.K_z]:
            self.y -= self.speed * dt
        if keys[p.K_s]:
            self.y += self.speed * dt


player_images = [p.transform.scale(p.image.load(f"assets/elf_f_run_anim_f{i}.png").convert_alpha(), (40, 70)) for i in range(4)]
player = Player(100, 100, player_images)


center_asset_image = p.image.load("assets/tapisTrappeur.png").convert_alpha()
top_right_asset_image = p.image.load("assets/library.png").convert_alpha()
top_right_asset_image = p.transform.scale(top_right_asset_image, (85, 85))
door_image = p.image.load("assets/Door.png").convert_alpha()
door_image = p.transform.scale(door_image, (90, 85))

center_x = (LARGEUR - center_asset_image.get_width()) // 2
center_y = (HAUTEUR - center_asset_image.get_height()) // 2
top_right_x = 583
top_right_y = 0
door_x = 300
door_y = -35


center_asset = Asset(center_x, center_y, center_asset_image)
top_right_asset = Asset(top_right_x, top_right_y, top_right_asset_image)
top_center_door = Asset(door_x, door_y, door_image)

running = True
FPS = 60
clock = p.time.Clock()

while running:
    dt = clock.tick(FPS) / 1000

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    surface.blit(background, (0,0))
    center_asset.draw()
    top_right_asset.draw()
    top_center_door.draw()
    player.update(dt)
    player.draw()
    p.display.flip()

p.quit()

