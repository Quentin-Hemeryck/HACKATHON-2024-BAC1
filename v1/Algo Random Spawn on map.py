import pygame as p
import random

p.init()

LARGEUR, HAUTEUR = 679, 676
surface = p.display.set_mode((LARGEUR, HAUTEUR))
p.display.set_caption("Game")

background = p.image.load("assets/map.png").convert_alpha()

class Monster:
    def __init__(self, images, speed, new_size=(100, 100)):
        self.images = [p.transform.scale(p.image.load(img).convert_alpha(), new_size) for img in images]
        self.speed = speed
        self.new_size = new_size
        self.x, self.y = self.random_position()
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_counter = 0

    def random_position(self):
        return random.randint(0, LARGEUR - self.new_size[0]), random.randint(0, HAUTEUR - self.new_size[1])

    def draw(self):
        frame = int(self.frame_counter) % len(self.images)
        surface.blit(self.images[frame], (self.x, self.y))
        self.frame_counter += self.animation_speed

    def update(self):
        self.x += random.choice([-1, 1]) * self.speed
        self.y += random.choice([-1, 1]) * self.speed
        self.x = max(0, min(self.x, LARGEUR - self.images[0].get_width()))
        self.y = max(0, min(self.y, HAUTEUR - self.images[0].get_height()))

lizard_frames = ["assets/big_demon_run_anim_f0.png", "assets/big_demon_run_anim_f1.png",
                 "assets/big_demon_run_anim_f2.png", "assets/big_demon_run_anim_f3.png"]
orc_frames = ["assets/ogre_run_anim_f0.png", "assets/ogre_run_anim_f1.png",
              "assets/ogre_run_anim_f2.png", "assets/ogre_run_anim_f3.png"]

lizard = Monster(lizard_frames, speed=2, new_size=(40, 80))
orc = Monster(orc_frames, speed=3, new_size=(50, 80))

running = True
clock = p.time.Clock()

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    surface.blit(background, (0,0))
    lizard.update()
    orc.update()
    lizard.draw()
    orc.draw()
    p.display.flip()
    clock.tick(60)

p.quit()
