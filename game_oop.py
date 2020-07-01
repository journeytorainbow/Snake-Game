""" 객체지향 버전 """

import sys, pygame, random
from pygame.locals import *

pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
FPS = 8
fpsClock = pygame.time.Clock()

foods = []
bombs = []
x_box, y_box = 20, 20
x_length = width/x_box
y_length = height/y_box

LINE_COLOR = (64, 64, 64)
PINK = (232, 93, 244)
MINT = (88, 232, 220)
RED = (244, 19, 53)
WHITE = (255, 255, 255)
GREEN = (157, 201, 90)

Font1 = pygame.font.SysFont('Impact', 80)
Font2 = pygame.font.SysFont('Impact', 30)
Font3 = pygame.font.SysFont('Impact', 20)

class Snake:
    def __init__(self, pos):
        self.bodies = [pos]
    
    def move(self, key):
        xpos, ypos = self.bodies[0]
        if key == K_LEFT:
            xpos -= 1
        elif key == K_RIGHT:
            xpos += 1
        elif key == K_UP:
            ypos -= 1
        elif key == K_DOWN:
            ypos += 1
        head = (xpos, ypos)

        game_over = head in bombs or head in self.bodies or head[0] < 0 or head[1] < 0 or head[0] >= x_box or head[1] >= y_box

        self.bodies.insert(0, head)
        if head in foods:
            foods.remove(head)
            add_food(self)
        elif head in bombs:
            bombs.remove(head)
            self.bodies.pop()
        else:
            self.bodies.pop()
        
        return game_over

    def draw(self):
        for body in self.bodies:
            pygame.draw.rect(screen, MINT, Rect(body[0]*x_length, body[1]*y_length, x_length, y_length))

def add_food(snake):
    while True:
        pos = (random.randint(0, x_box - 1), random.randint(0, y_box - 1))
        if pos in foods or pos in snake.bodies:
            continue
        foods.append(pos)
        break

def add_bomb(snake):
    while True:
        pos = (random.randint(0, x_box - 1), random.randint(0, y_box - 1))
        if pos in bombs or pos in foods or pos in snake.bodies:
            continue
        bombs.append(pos)
        break

def playing_paint(snake, time_render):
    screen.fill(0)
    snake.draw()
    for food in foods:
        pygame.draw.ellipse(screen, PINK, Rect((food[0]*x_length, food[1]*y_length), (x_length, y_length)))
    for bomb in bombs:
        pygame.draw.ellipse(screen, GREEN, Rect((bomb[0]*x_length, bomb[1]*y_length), (x_length, y_length)))
    for xpos in range(20):
        pygame.draw.line(screen, LINE_COLOR, (xpos*x_length, 0), (xpos*x_length, height))        
    for ypos in range(20):
        pygame.draw.line(screen, LINE_COLOR, (0, ypos*y_length), (width, ypos*y_length))        
    
    textRect = time_render.get_rect()
    textRect.topright = (screen.get_width()-5, 5)
    screen.blit(time_render, textRect)
    pygame.display.flip()

def gameover_paint(msg1, msg2):
    textRect = msg1.get_rect(center=(width//2, height//2))
    screen.blit(msg1, textRect)
    textRect = msg2.get_rect(center=(width//2, height//2 + 50))
    screen.blit(msg2, textRect)
    pygame.display.flip()

def main():
    time_start = pygame.time.get_ticks()
    running = True
    key = K_DOWN
    snake = Snake((int(x_box/2), int(y_box/2)))
    num_food = 20
    num_bomb = 3
    for _ in range(num_food):
        add_food(snake)
    for _ in range(num_bomb):
        add_bomb(snake)
    while running:
        time_past = pygame.time.get_ticks() - time_start
        time_render = Font3.render(str(int((time_past)/60000)) + ":" + str(int((time_past)/1000%60)).zfill(2), True, WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_DOWN, K_RIGHT, K_LEFT):
                    key = event.key
        
        game_over = snake.move(key)
        if game_over:
            msg1 = Font1.render("Game Over!", True, RED)
            msg2 = Font2.render("Try again![press spacebar]", True, WHITE)
            running = False
        
        playing_paint(snake, time_render)
        fpsClock.tick(FPS)

    gameover_paint(msg1, msg2)
  
main()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            foods = []
            bombs = []
            main() # replay