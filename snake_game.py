import random
import sys
import pygame
from pygame.math import Vector2
from settings import *

pygame.init()

# IMAGES
LOAD_APPLE = pygame.image.load('Graphics/small_apple.png')
APPLE = pygame.transform.scale(LOAD_APPLE, (CELL_SIZE, CELL_SIZE))

LOAD_CHERRY = pygame.image.load('Graphics/cherry.png')
CHERRY = pygame.transform.scale(LOAD_CHERRY, (CELL_SIZE, CELL_SIZE))

# DISPLAY
SCREEN = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))

# SOUND
MUSIC = pygame.mixer.Sound('Sound/Solve-The-Puzzle.wav')
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.display.set_caption(TITLE)
LOSE = pygame.mixer.Sound('Sound/lose.wav')

# TIME
CLOCK = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # 150 milliseconds


class Snake:
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # HEAD
        self.head_up = pygame.image.load('Graphics/head_up.png')
        self.head_down = pygame.image.load('Graphics/head_down.png')
        self.head_right = pygame.image.load('Graphics/head_right.png')
        self.head_left = pygame.image.load('Graphics/head_left.png')

        # TAIL
        self.tail_up = pygame.image.load('Graphics/tail_up.png')
        self.tail_down = pygame.image.load('Graphics/tail_down.png')
        self.tail_right = pygame.image.load('Graphics/tail_right.png')
        self.tail_left = pygame.image.load('Graphics/tail_left.png')

        # VERTICAL AND HORIZONTAL
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png')
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png')

        # CORNERS
        self.body_tr = pygame.image.load('Graphics/body_tr.png')
        self.body_tl = pygame.image.load('Graphics/body_tl.png')
        self.body_br = pygame.image.load('Graphics/body_br.png')
        self.body_bl = pygame.image.load('Graphics/body_bl.png')

        # SOUND
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

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

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        SCREEN.blit(CHERRY, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.running = True
        self.GAME_FONT = pygame.font.match_font(FONT_NAME)
        self.lose_sound = pygame.mixer.Sound('Sound/lose.wav')

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def show_go_screen(self):
        # game over/continue
        key = pygame.event.get()
        score_text = len(self.snake.body) - 3
        SCREEN.fill(LIGHT_BLUE)
        self.draw_text("GAME OVER", 60, WI / 2, HE / 4, WHITE)
        self.draw_text("Score: " + str(score_text), 30, WI / 2, HE / 2, WHITE)
        self.draw_text("Press a key to play again", 30, WI / 2, HE * 3 / 4, WHITE)
        pygame.display.update()
        self.wait_for_key(key)

    def draw_elements(self):
        draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def game_over(self):
        self.snake.reset()
        print('game over')

    def wait_for_key(self, events_key):
        for event_key in events_key:
            if event_key.type == pygame.KEYUP:
                self.running = True

    def check_fail(self):
        # key = pygame.event.get()
        dead = False
        if not 0 <= self.snake.body[0].x < CELL_NUMBER \
                or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            # self.show_go_screen(key)
            dead = True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                # self.show_go_screen(key)
                dead = True
        if dead is True:
            self.game_over()

    def draw(self):
        # Game Loop - draw
        score_text = str(len(self.snake.body) - 3)
        self.draw_text(str(score_text), 40, WI / 2, 15, WHITE)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.GAME_FONT, size)
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


# CALLING MAIN FUNCTION
main_game = Main()

while main_game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            motion()
    SCREEN.fill(GREEN)
    main_game.draw_elements()
    # main_game.show_go_screen(key)
    pygame.display.update()
    CLOCK.tick(FPS)
