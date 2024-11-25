import pygame
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hra Hadač")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Параметры змейки
block_size = 20
snake_speed = 2 # Еще медленнее змейка

# Шрифт для отображения текста
font_style = pygame.font.SysFont("bahnschrift", 25)

# Функция для отображения текста
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# Функция для рисования змейки
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Главная функция игры
def gameLoop():
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Генерация яблока
    foodx = round(random.randrange(0, WIDTH - block_size) / block_size) * block_size
    foody = round(random.randrange(0, HEIGHT - block_size) / block_size) * block_size

    # Основной цикл игры
    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Prohrál jsi! Stiskni Q pro quit nebo C pro novou hru", RED)
            pygame.display.update()

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Проверка на выход за границы экрана
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        # Рисуем яблоко
        pygame.draw.rect(screen, RED, [foodx, foody, block_size, block_size])

        # Добавляем голову змейки
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Столкновение змейки с собой
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(block_size, snake_List)

        pygame.display.update()

        # Проверка на съедание яблока
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - block_size) / block_size) * block_size
            foody = round(random.randrange(0, HEIGHT - block_size) / block_size) * block_size
            Length_of_snake += 1

        # Задержка для скорости игры
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
