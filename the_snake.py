from random import choice, randint
import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (38, 46, 32)
POISON_COLOR = (148, 0, 211)

speed = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption(
    '"Змейка". Клавишами управления двигайте Змейку, она должна съесть яблоко.'
)
# По замечанию: остальная информация не помещается

clock = pygame.time.Clock()


class GameObject:
    """Основной класс для змейки и яблока."""

    def __init__(self, color=None):
        self.body_color = color
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self):
        """Метод должен определять, как объект будет
        отрисовываться на экране. По умолчанию — pass.
        """
        pass

    def draw_cell(self):
        """метод отрисовки единственного элемента"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Вычисляем случайное положение элемента."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Apple(GameObject):
    """Дочерний класс для отрисовки яблока."""

    def __init__(self):
        super().__init__(color=APPLE_COLOR)
        self.position = self.randomize_position()

    def draw(self):
        """Рисуем яблоко на экране."""
        self.draw_cell()


class Stone(GameObject):
    """Дочерний класс камней и вредной еды."""

    def __init__(self, color):
        super().__init__(color)
        self.quantity = 3
        self.positions = []
        self.general_position()

    def general_position(self):
        """Задаем случайное положение."""
        for i in range(0, self.quantity):
            list.append(self.positions, self.randomize_position())

    def draw(self):
        """Рисуем камни и вредную еду на экране."""
        for self.position in self.positions:
            self.draw_cell()


class Snake(GameObject):
    """Дочерний класс Змейка."""

    def __init__(self):
        super().__init__(color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет сегменты змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = head_x + direction_x * GRID_SIZE
        new_y = head_y + direction_y * GRID_SIZE

        # Проверка: Если змейка достигает края экрана,
        # то она появляется с противоположной стороны.
        if new_x >= SCREEN_WIDTH:
            new_x = new_x % SCREEN_WIDTH
        elif new_x < 0:
            new_x += SCREEN_WIDTH
        if new_y < 0:
            new_y += SCREEN_HEIGHT
        elif new_y >= SCREEN_HEIGHT:
            new_y = new_y % SCREEN_HEIGHT

        list.insert(self.positions, 0, (new_x, new_y))

        self.last = []
        while len(self.positions) > self.length:
            list.append(self.last, self.positions.pop())

    def draw(self):
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            self.draw_cell()

        self.position = self.positions[0]
        self.draw_cell()

        for last in self.last:
            last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Cбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, для изменения направление движения
    змейки и изменения скорости.
    """
    global speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_PAGEUP:
                speed += 1
            elif event.key == pygame.K_PAGEDOWN:
                speed = speed - 1 if speed > 1 else 1


def main():
    """Обработка нажатия клавиш, обновление движения змейки,
    проверка на поедание яблока и столкновения.
    """
    pygame.init()
    apple = Apple()
    snake = Snake()
    stone = Stone(color=STONE_COLOR)
    poison = Stone(color=POISON_COLOR)

    while True:
        clock.tick(speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            while (apple.position in snake.positions
                   or apple.position in stone.positions
                   or apple.position in poison.positions):
                apple.position = apple.randomize_position()

        if snake.positions[0] in poison.positions:
            snake.length -= 1
            list.remove(poison.positions, snake.positions[0])
            if snake.length < 1:
                snake.reset()

        # Проверка на столкновение с собой и с камнями:
        if (snake.positions[0] in snake.positions[1:]
                or snake.positions[0] in stone.positions):
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        apple.draw()
        stone.draw()
        poison.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
