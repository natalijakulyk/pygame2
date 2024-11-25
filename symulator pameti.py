import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симулятор памяти")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Шрифт
FONT = pygame.font.SysFont("Arial", 36)

# Размер карточек и их количество
CARD_WIDTH, CARD_HEIGHT = 100, 150
GRID_COLS, GRID_ROWS = 4, 4  # 16 карточек (8 пар)
SPACING = 20

# Время отображения выбранной карточки
SHOW_CARD_TIME = 1000  # мс

# Создание набора карточек
def create_card_deck():
    total_pairs = (GRID_COLS * GRID_ROWS) // 2
    deck = list(range(total_pairs)) * 2
    random.shuffle(deck)
    return deck

# Координаты карточек на экране
def calculate_card_positions():
    positions = []
    start_x = (WIDTH - (GRID_COLS * CARD_WIDTH + (GRID_COLS - 1) * SPACING)) // 2
    start_y = (HEIGHT - (GRID_ROWS * CARD_HEIGHT + (GRID_ROWS - 1) * SPACING)) // 2
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = start_x + col * (CARD_WIDTH + SPACING)
            y = start_y + row * (CARD_HEIGHT + SPACING)
            positions.append((x, y))
    return positions

# Класс карточки
class Card:
    def __init__(self, value, rect):
        self.value = value
        self.rect = rect
        self.is_matched = False
        self.is_revealed = False

    def draw(self, screen):
        if self.is_matched or self.is_revealed:
            pygame.draw.rect(screen, WHITE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)
            text = FONT.render(str(self.value), True, BLACK)
            screen.blit(text, (self.rect.x + (CARD_WIDTH - text.get_width()) // 2,
                               self.rect.y + (CARD_HEIGHT - text.get_height()) // 2))
        else:
            pygame.draw.rect(screen, BLUE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    running = True

    # Создание карточек
    deck = create_card_deck()
    positions = calculate_card_positions()
    cards = [Card(value, pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)) for value, (x, y) in zip(deck, positions)]

    # Параметры игры
    first_card = None
    second_card = None
    last_reveal_time = 0
    matches_found = 0
    total_matches = len(deck) // 2

    while running:
        screen.fill(GRAY)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if first_card is None or second_card is None:
                    for card in cards:
                        if card.rect.collidepoint(event.pos) and not card.is_revealed and not card.is_matched:
                            card.is_revealed = True
                            if first_card is None:
                                first_card = card
                            elif second_card is None:
                                second_card = card

        # Логика проверки совпадений
        if first_card and second_card:
            if pygame.time.get_ticks() - last_reveal_time > SHOW_CARD_TIME:
                if first_card.value == second_card.value:
                    first_card.is_matched = True
                    second_card.is_matched = True
                    matches_found += 1
                else:
                    first_card.is_revealed = False
                    second_card.is_revealed = False
                first_card = None
                second_card = None

        # Отображение карточек
        for card in cards:
            card.draw(screen)

        # Проверка окончания игры
        if matches_found == total_matches:
            win_text = FONT.render("Jsi winner!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

        # Таймер для обработки задержки открытия пары
        if first_card and second_card and last_reveal_time == 0:
            last_reveal_time = pygame.time.get_ticks()

    pygame.quit()

if __name__ == "__main__":
    main()
