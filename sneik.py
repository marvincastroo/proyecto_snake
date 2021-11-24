import random
import sys
import pygame
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
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
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        SCREEN.blit(APPLE, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


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


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

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

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER \
                or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = GAME_FONT.render(score_text, True, BLACK)
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = APPLE.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 6, apple_rect.height)
        pygame.draw.rect(SCREEN, GREEN, bg_rect)
        SCREEN.blit(score_surface, score_rect)
        SCREEN.blit(APPLE, apple_rect)
        pygame.draw.rect(SCREEN, BLACK, bg_rect, 2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption('SNAKE')

# VARIABLES
WIDTH, HEIGHT = 400, 500
FPS = 60
SURF_WIDTH, SURF_HEIGHT = 100, 200
CELL_SIZE = 40
CELL_NUMBER = 15

# COLORS
GREEN = (175, 251, 70)
TILT = (102, 188, 196)
PURPLE = (161, 110, 196)
RED = (195, 12, 29)
TURQUOISE = (57, 199, 172)
GRASS_COLOR = (175, 243, 70)
BLACK = (0, 0, 0)

# IMPORTED IMAGE
LOAD_APPLE = pygame.image.load('Graphics/small_apple.png')
APPLE = pygame.transform.scale(LOAD_APPLE, (CELL_SIZE, CELL_SIZE))

# FONT
GAME_FONT = pygame.font.Font('SNAKE/DinoTopia.ttf', 28)

# DISPLAY
SCREEN = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))

# TIME
CLOCK = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # 150 milliseconds

# CALLING MAIN FUNCTION
main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
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
    SCREEN.fill(GREEN)
    main_game.draw_elements()
    pygame.display.update()
    CLOCK.tick(FPS)
