import pygame
import random

# Inicializace Pygame
pygame.init()

# Rozměry okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulátor procesoru")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

# Písmo
FONT = pygame.font.SysFont("Arial", 24)
LARGE_FONT = pygame.font.SysFont("Arial", 40)

# Časovače a nastavení
FPS = 60
TASK_INTERVAL = 2000  # Interval pro vytváření úkolů (ms)
TASK_TIME = 3000      # Doba trvání úkolu (ms)
PENALTY_TIME = 2000   # Doba zobrazení trestu (ms)

# Seznam úkolů
tasks = []

# Efekty
click_effects = []
penalty_message = None

# Třída pro úkol
class Task:
    def __init__(self, x, y, task_id):
        self.rect = pygame.Rect(x, y, 120, 40)
        self.time_created = pygame.time.get_ticks()
        self.task_id = task_id
        self.color = BLUE
        self.animation_scale = 0.0  # Pro animaci zvětšení

    def draw(self, screen):
        # Animace zvětšování úkolu
        if self.animation_scale < 1.0:
            self.animation_scale += 0.05
        scaled_rect = self.rect.inflate(
            self.rect.width * (self.animation_scale - 1),
            self.rect.height * (self.animation_scale - 1),
        )
        pygame.draw.rect(screen, self.color, scaled_rect)
        pygame.draw.rect(screen, BLACK, scaled_rect, 2)
        text = FONT.render(f"Úkol {self.task_id}", True, WHITE)
        screen.blit(text, (scaled_rect.x + 10, scaled_rect.y + 10))

    def is_expired(self):
        return pygame.time.get_ticks() - self.time_created > TASK_TIME

# Hlavní herní smyčka
def main():
    global penalty_message
    clock = pygame.time.Clock()
    running = True
    last_task_time = pygame.time.get_ticks()
    score = 0
    task_counter = 1

    while running:
        screen.fill(GRAY)

        # Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for task in tasks[:]:
                    if task.rect.collidepoint(event.pos):
                        tasks.remove(task)
                        score += 1
                        # Přidání efektu kliknutí
                        click_effects.append({"pos": event.pos, "radius": 5, "color": GREEN})

        # Vytváření nového úkolu
        current_time = pygame.time.get_ticks()
        if current_time - last_task_time > TASK_INTERVAL:
            x = random.randint(50, WIDTH - 170)
            y = random.randint(50, HEIGHT - 90)
            tasks.append(Task(x, y, task_counter))
            task_counter += 1
            last_task_time = current_time

        # Aktualizace a zobrazení úkolů
        for task in tasks[:]:
            if task.is_expired():
                tasks.remove(task)
                # Zobrazení trestu za zmeškaný úkol a odečtení bodu
                penalty_message = {"text": "Trest za zmeškaný úkol!", "time": current_time}
                score -= 1  # Odečítáme jeden bod za zmeškaný úkol
            else:
                task.draw(screen)

        # Zobrazení efektu kliknutí
        for effect in click_effects[:]:
            pygame.draw.circle(screen, effect["color"], effect["pos"], effect["radius"])
            effect["radius"] += 5
            effect["color"] = (
                max(0, effect["color"][0] - 10),
                max(0, effect["color"][1] - 10),
                max(0, effect["color"][2] - 10),
            )
            if effect["radius"] > 30:
                click_effects.remove(effect)

        # Zobrazení trestného sdělení
        if penalty_message:
            time_since_penalty = current_time - penalty_message["time"]
            if time_since_penalty < PENALTY_TIME:
                penalty_text = LARGE_FONT.render(penalty_message["text"], True, RED)
                screen.blit(penalty_text, (WIDTH // 2 - penalty_text.get_width() // 2, HEIGHT // 2 - 30))
            else:
                penalty_message = None

        # Zobrazení skóre
        score_text = FONT.render(f"Skóre: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__== "__main__":
    main()
