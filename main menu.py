import pygame
import sys
from button import Button

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de l'écran
SCREEN_WIDTH = 679
SCREEN_HEIGHT = 676

# Création de la fenêtre d'affichage
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Chargement et mise à l'échelle de l'image de fond
BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonction pour obtenir la police de caractères adaptée
def get_font(size):
    font_size = int(size * SCREEN_WIDTH / 1920)
    return pygame.font.Font("assets/font.ttf", font_size)

# Fonction pour afficher l'écran de jeu
def play():
    running = True
    while running:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.68),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


# Fonction pour afficher le menu principal
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.15))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.36),
                             text_input="CLASSIC MODE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.54),
                                text_input="TIME TRIAL MODE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.72),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Lancement du menu principal
main_menu()
