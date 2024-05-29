from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки было 20, но я не успеваю, поэтому:
SPEED = 3

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной класс для змейки и яблока."""

    # инициализирует базовые атрибуты объекта
    def __init__(self, color=None):
        # цвет объекта. Он не задаётся конкретно в классе
        self.body_color = color
        # позиция объекта на игровом поле. В данном
        # случае она инициализируется как центральная точка экрана.
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self):
        """Метод должен определять, как объект будет
        отрисовываться на экране. По умолчанию — pass.
        """
        pass


class Apple(GameObject):
    """Дочерний класс для отрисовки яблока."""

    def __init__(self):
        super().__init__(color=APPLE_COLOR)
        # задаем случайное положение яблока
        self.randomize_position()

    def randomize_position(self):
        """Вычисляем случайное положение яблока."""
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )

    def draw(self):
        """Рисуем яблоко на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс Змейка."""

    # Инициализирует начальное состояние змейки.
    def __init__(self):
        self.length = 1
        # При запуске игры змейка сразу же начинает движение вправо.
        self.direction = RIGHT
        # Следующее направление движения, которое будет применено после
        # обработки нажатия клавиши. По умолчанию задать None.
        self.next_direction = None
        # Последняя клетка змейки (хвост). По умолчанию задать None.
        self.last = None
        super().__init__(color=SNAKE_COLOR)
        # Список (все сегменты тела змейки). Начальная позиция — центр экрана.
        self.positions = [(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )]

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
        # Берем позицию головы.
        head_position = self.get_head_position()
        # Вычисляем новую позицию
        if self.direction == UP:
            # Если вверх, то измененяем по y -.
            new_x, new_y = head_position[0], head_position[1] - GRID_SIZE
        elif self.direction == RIGHT:
            # Если вправо, то измененяем по х +.
            new_x, new_y = head_position[0] + GRID_SIZE, head_position[1]
        elif self.direction == DOWN:
            # Если вниз, то измененяем по y +.
            new_x, new_y = head_position[0], head_position[1] + GRID_SIZE
        elif self.direction == LEFT:
            # Если влево, то измененяем по х -.
            new_x, new_y = head_position[0] - GRID_SIZE, head_position[1]

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

        # Создаем кортеж с новыми координатами головы.
        new_position = (new_x, new_y)

        # Проверка на столкновение с собой:
        self.reset() if new_position in self.positions else list.insert(
            self.positions, 0, new_position)

        # Проверка: если длина змейки не изменилась,
        if len(self.positions) > self.length:
            # удаляем последний элемент списка
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка тела змейка."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        # получаем координаты
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        # рисуем квадрат
        pygame.draw.rect(screen, self.body_color, head_rect)
        # рисуем ободок квадрата
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Cбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )]
        all_direction = [UP, DOWN, LEFT, RIGHT]
        # Случайный выбор направления
        self.direction = choice(all_direction)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, для изменения направление движения
    змейки.
    """
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


def main():
    """Обработка нажатия клавиш, обновление движения змейки,
    проверка на поедание яблока.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        # Смотрим нажатие клавиш.
        handle_keys(snake)
        # Обновим направление движения змейки.
        snake.update_direction()
        # Двигаем змейку, изменяем список.
        snake.move()
        # Если змейка съела яблоко, то ...
        if snake.positions[0] == apple.position:
            # ...увеличьте длину змейки
            snake.length += 1
            # и переместите яблоко.
            apple.randomize_position()
        # Отрисовывайте змейку и яблоко.
        apple.draw()
        snake.draw()
        # Обновляйте экран.
        pygame.display.update()


if __name__ == '__main__':
    main()
