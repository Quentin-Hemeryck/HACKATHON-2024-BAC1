import pygame as p
import sys
from button import Button
import random
from pause_menu import pause_menu


# Initialisation de Pygame
p.init()

# Définition des dimensions de l'écran
SCREEN_WIDTH = 679
SCREEN_HEIGHT = 676

# Création de la fenêtre d'affichage
SCREEN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption("Menu")

# Chargement et mise à l'échelle de l'image de fond
BG = p.image.load("assets/Background.png")
BG = p.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Fonction pour obtenir la police de caractères adaptée
def get_font(size):
    font_size = int(size * SCREEN_WIDTH / 1920)
    return p.font.Font("assets/font.ttf", font_size)

# Fonction pour afficher l'écran de jeu
def play():
    running = True
    while running:
        PLAY_MOUSE_POS = p.mouse.get_pos()
        SCREEN.fill("black")

        # Utiliser exec() pour exécuter main.py
        exec(open("Algo Random Spawn on map.py").read())

        # Si vous voulez toujours afficher quelque chose après avoir exécuté main.py, vous pouvez le faire ici

        # Exemple : Afficher un texte
        PLAY_TEXT = get_font(45).render("Returned from main.py", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Exemple : Afficher un bouton pour revenir en arrière
        PLAY_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.68),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

# Fonction pour afficher le menu principal
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = p.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.15))

        PLAY_BUTTON = Button(image=p.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.36),
                             text_input="CLASSIC MODE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=p.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.54),
                                text_input="TIME TRIAL MODE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=p.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.72),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    sys.exit()

        p.display.update()

# Lancement du menu principal
main_menu()
