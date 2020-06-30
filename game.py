""" 함수 버전 """

import sys, pygame, random
from pygame.locals import *

pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))

x_box, y_box = 20, 20
x_length = width/x_box 
y_length = height/y_box 

FPS = 7
fpsClock = pygame.time.Clock()

LINE_COLOR = (64, 64, 64)
PINK = (232, 93, 244)
MINT = (88, 232, 220)
RED = (244, 19, 53)
WHITE = (255, 255, 255)

foods = []
snake = []

# 먹이 추가
def add_food():
    while True:
        pos = (random.randint(0, x_box - 1), random.randint(0, y_box - 1))
        if pos in foods or pos in snake:
            continue
        foods.append(pos)
        break

# 먹이 이동 
def move_food(pos):
    foods.remove(pos)
    add_food()

# 게임 화면 그리기
def playing_paint():
    screen.fill(0)
    # 눈금 그리기
    for xpos in range(x_box):
        pygame.draw.line(screen, LINE_COLOR, (xpos*(x_length), 0), (xpos*(x_length), height))
    for ypos in range(y_box):
        pygame.draw.line(screen, LINE_COLOR, (0, ypos*y_length), (width, ypos*y_length))
    # 먹이 그리기
    for food in foods:
        pygame.draw.ellipse(screen, PINK, Rect((food[0]*x_length, food[1]*y_length), (x_length, y_length)))
    # 뱀 몸통 그리기
    for body in snake:
        pygame.draw.rect(screen, MINT, Rect((body[0]*x_length, body[1]*y_length), (x_length, y_length)))
    pygame.display.flip()

# 게임 오버 화면 그리기
def gameover_paint(msg1, msg2):
        textRect = msg1.get_rect(center=(width//2, height//2))
        screen.blit(msg1, textRect)
        textRect = msg2.get_rect(center=(width//2, height//2 + 50))
        screen.blit(msg2, textRect)
        pygame.display.flip()

# 메인 루틴
def main():
    Font1 = pygame.font.SysFont('Impact', 80)
    Font2 = pygame.font.SysFont('Impact', 30)
    key = K_DOWN
    msg = None
    running = True
    num_food = 10
    snake.append((int(x_box/2), int(y_box/2)))
    for _ in range(num_food):
        add_food()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                    key = event.key 
        
        if key == K_LEFT:
            head = (snake[0][0] - 1, snake[0][1])
        elif key == K_RIGHT:
            head = (snake[0][0] + 1, snake[0][1])
        elif key == K_UP:
            head = (snake[0][0], snake[0][1] - 1)
        elif key == K_DOWN:
            head = (snake[0][0], snake[0][1] + 1)
        
        if head in snake or head[0] < 0 or head[1] < 0 or head[0] > x_box - 1 or head[1] > y_box - 1:
            msg1 = Font1.render("Game Over!", True, RED)
            msg2 = Font2.render("Try again![press spacebar]", True, WHITE)
            running = False

        snake.insert(0, head)
        if head in foods:
            move_food(head)
        else:
            snake.pop()

        playing_paint()
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
            snake = []
            main() # replay