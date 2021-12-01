import random
import sys
import pygame
from pygame.math import Vector2

pygame.init()
pygame.font.init()

# VARIABLES
WIDTH, HEIGHT = 400, 500
FPS = 60
SURF_WIDTH, SURF_HEIGHT = 100, 200
CELL_SIZE = 40
CELL_NUMBER = 15
MID_W, MID_H = (CELL_NUMBER * CELL_SIZE) / 2, (CELL_NUMBER * CELL_SIZE) / 2
WI, HE = CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE
TITLE = "SNAKE!"
PIXEL = 'SNAKE/8bit16.ttf'
click = False

# COLORS
GREEN = (175, 251, 70)
TILT = (102, 188, 196)
PURPLE = (161, 110, 196)
RED = (195, 12, 29)
TURQUOISE = (57, 199, 172)
GRASS_COLOR = (175, 243, 70)
BLACK = (0, 0, 0)
YELLOW = (250, 231, 1)
YELLOW_GRASS = (255, 213, 1)
WHITE = (255, 255, 255)
LIGHT_BLUE = (84, 175, 243)

# IMAGES
LOAD_APPLE = pygame.image.load('Graphics/frutas/small_apple.png')
APPLE = pygame.transform.scale(LOAD_APPLE, (CELL_SIZE, CELL_SIZE))

#BACKGROUND IMAGES
oropel_surface = pygame.image.load("Graphics/backgrounds/oropel.png")
oropel_surface = pygame.transform.scale(oropel_surface, (1026, 607))

grass_surface = pygame.image.load("Graphics/backgrounds/grass_texture.png")
grass_surface = pygame.transform.scale(grass_surface, (1026, 607))

LOAD_BANANA = pygame.image.load('Graphics/frutas/banana.png')
BANANA = pygame.transform.scale(LOAD_BANANA, (CELL_SIZE, CELL_SIZE))

#background music
backg_music = pygame.mixer.Sound("Sound/junglehjinx.mp3")
backg_music.set_volume(0.1)
backg_music.play(-1)

#more graphics
LOAD_CHERRY = pygame.image.load('Graphics/frutas/cherry.png')
CHERRY = pygame.transform.scale(LOAD_CHERRY, (CELL_SIZE, CELL_SIZE))

SNAKE_LOGO = pygame.image.load("Graphics/snake_logo.png")
SNAKE_LOGO = pygame.transform.scale(SNAKE_LOGO, (50, 50))

# DISPLAY
SCREEN = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))

# SOUND
pygame.display.set_caption(TITLE)
LOSE = pygame.mixer.Sound('Sound/lose.wav')

# TIME
CLOCK = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # 150 milliseconds

# STATE .
PLAYING, GAMEOVER = range(2)


class Snake:
    # se cargan las texturas de la serpiente, se usan los vectores para dar la posicion de cada "bloque"
    # de la serpiente
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # HEAD
        self.head_up = pygame.image.load('Graphics/skin1/head_up2.png')
        self.head_down = pygame.image.load('Graphics/skin1/head_down2.png')
        self.head_right = pygame.image.load('Graphics/skin1/head_right2.png')
        self.head_left = pygame.image.load('Graphics/skin1/head_left2.png')

        # TAIL
        self.tail_up = pygame.image.load('Graphics/skin1/tail_up2.png')
        self.tail_down = pygame.image.load('Graphics/skin1/tail_down2.png')
        self.tail_right = pygame.image.load('Graphics/skin1/tail_right2.png')
        self.tail_left = pygame.image.load('Graphics/skin1/tail_left2.png')

        # VERTICAL AND HORIZONTAL .
        self.body_horizontal = pygame.image.load('Graphics/skin1/body_horizontal2.png')
        self.body_vertical = pygame.image.load('Graphics/skin1/body_vertical2.png')

        # CORNERS
        self.body_tr = pygame.image.load('Graphics/skin1/body_tr2.png')
        self.body_tl = pygame.image.load('Graphics/skin1/body_tl2.png')
        self.body_br = pygame.image.load('Graphics/skin1/body_br2.png')
        self.body_bl = pygame.image.load('Graphics/skin1/body_bl2.png')

        # SOUND .
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        self.crunch_sound.set_volume(0.2)

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            if index == 0:
                SCREEN.blit(self.update_head_graphics(), block_rect)
            elif index == len(self.body) - 1:
                SCREEN.blit(self.update_tail_graphics(), block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    SCREEN.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    SCREEN.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 \
                            or previous_block.y == -1 and next_block.x == -1:
                        SCREEN.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 \
                            or previous_block.y == 1 and next_block.x == -1:
                        SCREEN.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 \
                            or previous_block.y == -1 and next_block.x == 1:
                        SCREEN.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 \
                            or previous_block.y == 1 and next_block.x == 1:
                        SCREEN.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            return self.head_left
        elif head_relation == Vector2(-1, 0):
            return self.head_right
        elif head_relation == Vector2(0, 1):
            return self.head_up
        elif head_relation == Vector2(0, -1):
            return self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            return self.tail_left
        elif tail_relation == Vector2(-1, 0):
            return self.tail_right
        elif tail_relation == Vector2(0, 1):
            return self.tail_up
        elif tail_relation == Vector2(0, -1):
            return self.tail_down

    def move_snake(self):
        if self.new_block is True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, fruit_choice):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        SCREEN.blit(fruit_choice, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


# clase que se encarga de todas las funcionalidades del menú que aparece al inicio del juego
class Menu:
    # se cargan algunos assets necesarios
    def __init__(self):
        self.running = True
        self.menu_font = 'SNAKE/pixel_font.ttf'
        self.white_screen = SCREEN.fill(WHITE)
        self.click_sound = pygame.mixer.Sound('Sound/click.wav')
        self.click_sound.set_volume(0.1)
        self.play_sound = pygame.mixer.Sound('Sound/play.wav')
        self.play_sound.set_volume(0.1)
        self.played = True
        self.key_esc = True

    # método que se usa para facilitar la impresión de texto, parametrosÑ
    # text: texto a hacer display
    # size: tamaño de letra
    # x, y: posiciones en x, y, respectivamente
    # color: no sé
    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.menu_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        SCREEN.blit(text_surface, text_rect)

    def force_to_game(self):
        correr_juego = True
        print("force to game")
        return correr_juego

    # método que se encarga de generar los 3 botones, y  obtener input del usuario.
    def menu_screen(self):
        oropel_rect = oropel_surface.get_rect(center = (350,300))
        click = ""
        while self.running is True:
            SCREEN.fill(BLACK)
            SCREEN.blit(oropel_surface, oropel_rect)
            self.draw_text("SNAKE!", 60, WI / 2, HE / 4, WHITE)
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(200, 225, 200, 50)
            button_2 = pygame.Rect(200, 325, 200, 50)
            button_3 = pygame.Rect(200, 425, 200, 50)

            pygame.draw.rect(SCREEN, WHITE, button_1)
            self.draw_text('JUGAR', 25, 200 + 100, 225 + 25, RED)
            pygame.draw.rect(SCREEN, WHITE, button_2)
            self.draw_text('PUNTAJES', 24, 200 + 100, 325 + 25, RED)
            pygame.draw.rect(SCREEN, WHITE, button_3)
            self.draw_text('OPCIONES', 24, 200 + 100, 425 + 25, RED)

            if button_1.collidepoint((mx, my)):
                SNAKE_LOGO_rect = SNAKE_LOGO.get_rect(midbottom=(175, 270))
                SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_rect)
                pygame.display.update()
                if click:
                    self.play_sound.play()
                    self.running = False

                    self.force_to_game()
                    return 1

            elif button_2.collidepoint((mx, my)):
                SNAKE_LOGO_rect = SNAKE_LOGO.get_rect(midbottom=(175, 370))
                SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_rect)
                pygame.display.update()
                if click:
                    self.click_sound.play()
                    highscores = Highscores()
                    highscores.scores_in_display()
                    # return 2

            if button_3.collidepoint((mx, my)):
                SNAKE_LOGO_rect = SNAKE_LOGO.get_rect(midbottom=(175, 470))
                SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_rect)
                pygame.display.update()
                if click:
                    self.click_sound.play()
                    options = Options()
                    options.options_screen()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()

# clase que se encarga de la pestaña de Highscores en el menú
class Highscores:
    def __init__(self):
        self.running = True
        self.runningHS = True
        self.GAME_FONT = "SNAKE/pixel_font.ttf"
        self.white_screen = SCREEN.fill(WHITE)
        self.menu_class = Menu()

    # método que facilita la impresión de texto
    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.GAME_FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        SCREEN.blit(text_surface, text_rect)

    # método que se encarga de acceder al archivo de Scores, leer la información en él y hacer
    # display de los highscores en la pantalla.
    def scores_in_display(self):
        lista_highscores = []
        text_file_location = "Scores/Scores.txt"
        file = open(text_file_location)
        for linea in file:
            lista_highscores = linea.split(",")
            if len(lista_highscores) != 0:
                lista_highscores.pop()
        print(lista_highscores)

        for i in range(0, (len(lista_highscores))):
            lista_highscores[i] = int(lista_highscores[i])

        file.close()
        lista_highscores.sort(reverse=True)


        while self.runningHS is True:
            SCREEN.fill(WHITE)
            self.draw_text("HIGHSCORES ", 40, WI / 2, HE / 4, BLACK)
            if len(lista_highscores) == 0:
                self.draw_text("No hay ningún puntaje", 20, WI / 2, 250, BLACK)
            elif len(lista_highscores) == 1:
                self.draw_text("El puntaje más alto: ", 20, WI / 2, 250, BLACK)
                self.draw_text(("1. Score: " + str(lista_highscores[0])), 20, WI / 2, 300, BLACK)
            elif len(lista_highscores) == 2:
                self.draw_text("Los dos puntajes más altos:", 20, WI / 2, 250, BLACK)
                self.draw_text(("1. Score: " + str(lista_highscores[0])), 20, WI / 2, 300, BLACK)
                self.draw_text(("2. Score: " + str(lista_highscores[1])), 20, WI / 2, 350, BLACK)
            elif len(lista_highscores) > 2:
                self.draw_text("Los tres puntajes más altos:", 20, WI / 2, 250, BLACK)
                self.draw_text(("1. Score: " + str(lista_highscores[0])), 20, WI / 2, 300, BLACK)
                self.draw_text(("2. Score: " + str(lista_highscores[1])), 20, WI / 2, 350, BLACK)
                self.draw_text(("3. Score: " + str(lista_highscores[2])), 20, WI / 2, 400, BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.runningHS = False
                        Menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
        if self.runningHS is False:
            menu = Menu()
            menu.menu_screen()
            self.menu_class = 0

# clase que se encarga de la ventana de opciones en el menú
class Options:
    def __init__(self):
        self.cherry = pygame.transform.scale(LOAD_CHERRY, (CELL_SIZE, CELL_SIZE))
        self.apple = pygame.transform.scale(LOAD_APPLE, (CELL_SIZE, CELL_SIZE))
        self.banana = pygame.transform.scale(LOAD_APPLE, (CELL_SIZE, CELL_SIZE))
        self.running = True
        self.click_sound = pygame.mixer.Sound('Sound/click.wav')
        self.click_sound.set_volume(0.1)
        self.fruit = Fruit()
        self.options_font = 'SNAKE/pixel_font.ttf'
        self.main = Main()
        self.menu = Menu()
        self.music_on = True

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.options_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        SCREEN.blit(text_surface, text_rect)

    # metodo  que imprime los botones y detecta el input del usuario
    def options_screen(self):
        click = ""
        music_on = ""
        while self.running is True:
            SCREEN.fill(BLACK)
            self.draw_text("música:", 20, 100, HE / 4, WHITE)

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(180, 130, 50, 40)
            button_2 = pygame.Rect(300, 130, 50, 40)
            button_3 = pygame.Rect(20, 210, 320, 40)


            pygame.draw.rect(SCREEN, WHITE, button_1)
            pygame.draw.rect(SCREEN, WHITE, button_2)
            pygame.draw.rect(SCREEN, WHITE, button_3)
            self.draw_text('SI', 20, 205 ,150 , RED)
            self.draw_text('NO', 20, 325, 150, RED)
            self.draw_text("Borrar puntajes", 20, 180, 230, RED)

            if button_1.collidepoint((mx, my)):
                SNAKE_LOGO_rect = SNAKE_LOGO.get_rect(midbottom=(255, 170))
                SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_rect)
                if click:

                    self.click_sound.play()
                    #self.running = False
                    if music_on == False:
                        backg_music.play(-1)
                        self.running = False


            if button_2.collidepoint((mx, my)):
                SNAKE_LOGO_rect = SNAKE_LOGO.get_rect(midbottom=(375, 170))
                SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_rect)
                if click:
                    self.click_sound.play()
                    #self.running = False
                    backg_music.stop()
                    music_on = False
                    self.running = False

            if button_3.collidepoint((mx, my)):
                SNAKE_LOGO_rect = SNAKE_LOGO.get_rect(midbottom=(365, 250))
                SCREEN.blit(SNAKE_LOGO, SNAKE_LOGO_rect)
                if click:
                    file = open("Scores/Scores.txt", "r+")
                    file.truncate(0)
                    file.close()
                    self.click_sound.play()
                    self.running = False




            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Menu()
                        self.running = False
                        pygame.display.update()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()


class Main:
    def __init__(self):
        self.high_score = 0
        self.HS = False
        self.snake = Snake()
        self.fruit = Fruit()
        self.running = True
        self.lose_sound = pygame.mixer.Sound('Sound/lose.wav')
        self.lose_sound.set_volume(0.1)
        self.dead = True
        self.currentState = PLAYING
        self.play_sound = pygame.mixer.Sound('Sound/play.wav')
        self.play_sound.set_volume(0.1)
        self.game_font = 'SNAKE/pixel_font.ttf'
        self.menu = False
        self.options = Options

    def update(self):
        if not self.dead:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
        if self.menu is True:
            main_menu = Menu()
            main_menu.menu_screen()

    def checkReset(self, events):
        for event in events:
            if event.type == pygame.KEYUP:
                self.currentState = PLAYING
                self.snake.reset()
                self.dead = True
                self.play_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu = True
            if self.menu is True:
                self.menu = False
                self.dead = True
                main_menu = Menu()
                main_menu.menu_screen()

    def play_go_sound(self):
        self.lose_sound.play()

    def show_go_screen(self):
        # game over/continue
        score_text = len(self.snake.body) - 3
        SCREEN.fill(BLACK)
        if score_text > self.high_score:
            self.high_score = score_text
            self.HS = True
            ruta = "Scores/Scores.txt"
            file = open(ruta, "a")
            file.write(str(score_text) + ",")
            file.close()
        elif score_text < self.high_score:
            self.HS = False
        self.draw_text("GAME OVER", 50, WI / 2, HE / 3, WHITE)
        self.draw_text("Puntaje: " + str(score_text), 20, WI / 2, HE / 2 - 25, WHITE)
        self.draw_text("Presione cualquier tecla para jugar de nuevo", 13, WI / 2, HE * 3 / 4, WHITE)
        self.draw_text("o ESC para ir al menú", 20, WI / 2, HE * 3 / 4 + 25, WHITE)
        self.draw_text("Puntaje máximo: " + str(self.high_score), 20, WI / 2, HE / 2 + 28, WHITE)
        if self.HS is True:
                self.draw_text("NUEVO PUNTAJE MÁXIMO!!", 25, WI / 2, HE / 2 + 85, RED)

    def draw_elements(self):
        self.snake.draw_snake()
        self.draw()
        self.fruit.draw_fruit(BANANA)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def game_over(self):
        self.currentState = GAMEOVER

    def wait_for_key(self, events_key):
        for event_key in events_key:
            if event_key.type == pygame.KEYUP:
                self.dead = False
            if event_key.type == pygame.K_ESCAPE:
                return 1

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER \
                or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.dead = True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.dead = True

        if self.dead:
            self.game_over()
            self.play_go_sound()

    def draw(self):
        # draw score
        score_text = str(len(self.snake.body) - 3)
        self.draw_text(str(score_text), 25, WI / 2, 15, WHITE)

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.game_font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        SCREEN.blit(text_surface, text_rect)


def draw_grass():
    for row in range(CELL_NUMBER):
        if row % 2 == 0:
            for col in range(CELL_NUMBER):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(SCREEN, GRASS_COLOR, grass_rect)
        else:
            for col in range(CELL_NUMBER):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(SCREEN, GRASS_COLOR, grass_rect)


def motion():
    if event.key == pygame.K_UP:
        if main_game.snake.direction.y != 1:
            main_game.snake.direction = Vector2(0, -1)
    if event.key == pygame.K_DOWN:
        if main_game.snake.direction.y != -1:
            main_game.snake.direction = Vector2(0, 1)
    if event.key == pygame.K_LEFT:
        if main_game.snake.direction.x != 1:
            main_game.snake.direction = Vector2(-1, 0)
    if event.key == pygame.K_RIGHT:
        if main_game.snake.direction.x != -1:
            main_game.snake.direction = Vector2(1, 0)


menu = Menu()
correr_juego = False
correr_highscores = False
highscores = Highscores()
options = Options()

if menu.menu_screen() == 1:
    main_game = Main()
    print("si")
    correr_juego = True

while correr_juego:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            motion()



    SCREEN.fill(BLACK)
    grass_rect = grass_surface.get_rect(center=(350, 300))
    SCREEN.blit(grass_surface, grass_rect)
    if main_game.currentState == PLAYING:
        main_game.wait_for_key(events)
        main_game.draw_elements()
    elif main_game.currentState == GAMEOVER:
        main_game.checkReset(events)
        main_game.show_go_screen()

    pygame.display.flip()
    CLOCK.tick(FPS)