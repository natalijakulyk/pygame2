import pygame
import sys

# Инициализация Pygame
pygame.init()

# Устанавливаем параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Визуализация движения данных")

# Основной цвет фона
BACKGROUND_COLOR = (30, 30, 30)

# Начальная скорость движения данных
speed = 5

# Функция для рисования компонентов на экране (процессор и память)
def draw_components():
    # Рисуем процессор (CPU)
    pygame.draw.rect(screen, (100, 200, 100), (50, 250, 150, 100))  # Зеленый прямоугольник
    font = pygame.font.SysFont(None, 30)
    cpu_label = font.render("Procesor", True, (255, 255, 255))
    screen.blit(cpu_label, (60, 260))

    # Рисуем память (RAM)
    pygame.draw.rect(screen, (200, 100, 100), (600, 250, 150, 100))  # Красный прямоугольник
    memory_label = font.render("Paměť", True, (255, 255, 255))
    screen.blit(memory_label, (630, 260))

    # Линия, которая соединяет процессор и память
    pygame.draw.line(screen, (255, 255, 255), (200, 300), (600, 300), 5)  # Белая линия

# Функция для анимации перемещения данных
def move_data(data_pos, direction):
    if direction == "to_memory":
        data_pos[0] += speed  # Перемещаем данные вправо
        if data_pos[0] >= 600:  # Если данные дошли до памяти, меняем направление
            direction = "to_cpu"
    elif direction == "to_cpu":
        data_pos[0] -= speed  # Перемещаем данные влево
        if data_pos[0] <= 200:  # Если данные дошли до процессора, меняем направление
            direction = "to_memory"
    return data_pos, direction

# Функция для обработки событий (изменение скорости)
def handle_events():
    global speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Закрытие окна
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Увеличиваем скорость
                speed += 1
            elif event.key == pygame.K_DOWN:  # Уменьшаем скорость
                speed = max(1, speed - 1)  # Не даем скорости стать меньше 1

# Главная функция программы
def main():
    global speed
    clock = pygame.time.Clock()
    data_pos = [200, 300]  # Начальная позиция данных
    direction = "to_memory"  # Направление движения данных

    while True:
        handle_events()  # Обрабатываем события (клавиши)

        screen.fill(BACKGROUND_COLOR)  # Заполнение фона

        draw_components()  # Рисуем процессор и память

        # Двигаем данные с текущей скоростью
        data_pos, direction = move_data(data_pos, direction)

        # Рисуем данные как круг
        pygame.draw.circle(screen, (100, 100, 255), data_pos, 10)  # Синий круг (данные)

        pygame.display.flip()  # Обновление экрана
        clock.tick(60)  # Ограничение частоты обновлений (60 кадров в секунду)

# Здесь должна быть правильная проверка
if __name__ == "__main__":
    main()
