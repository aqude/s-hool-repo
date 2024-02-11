import pygame
import numpy as np
import time
import random
import sys
pygame.init()

# Определение размеров окна
width, height = 1000, 1000
# Определение размера ячейки
cell_size = 10
# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)
survival_block = (0, 200, 0)

# Создание поля размером width x height
screen = pygame.display.set_mode((width, height))
# Задание заголовка окна
pygame.display.set_caption("Игра Жизнь")

# Создание пустой сетки
grid = np.zeros((width // cell_size, height // cell_size), dtype=int)

# Создание сетки плодородия
fertility_map = np.zeros((width // cell_size, height // cell_size), dtype=float)

# Функция для отрисовки сетки
def draw_grid():
    for i in range(0, width, cell_size):
        pygame.draw.line(screen, black, (i, 0), (i, height))
    for j in range(0, height, cell_size):
        pygame.draw.line(screen, black, (0, j), (width, j))

# Функция для обновления состояния клеток в следующем поколении
def update_grid():
    global grid, fertility_map
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = np.sum(grid[max(i-1, 0):min(i+2, grid.shape[0]), max(j-1, 0):min(j+2, grid.shape[1])]) - grid[i, j]
            fertility_bonus = fertility_map[i, j] 
            
            if grid[i, j] == 1:
                # Клетки "поедают" плодородие места
                fertility_map[i, j] = max(0, fertility_map[i, j] - 0.5)  # Уменьшаем плодородие, не позволяя уйти в отрицательное значение
                
                # Определяем условия выживания на основе плодородия
                min_neighbors_for_survival = 2 if fertility_bonus < 0.5 else 1
                max_neighbors_for_survival = 3
                if neighbors < min_neighbors_for_survival or neighbors > max_neighbors_for_survival:
                    new_grid[i, j] = 0
                    # Когда клетка исчезает, она "наполняет" почву на +0.5 энергии
                    fertility_map[i, j] = min(1, fertility_map[i, j] + 0.3)  # Увеличиваем плодородие, не превышая максимум в 1
            else:
                # Условия для рождения новой клетки
                required_neighbors_for_birth = 3 if fertility_bonus < 0.5 else 2
                if neighbors == required_neighbors_for_birth:
                    new_grid[i, j] = 1
                    # Клетка рождается, но не изменяет плодородие при рождении
                    
    grid = new_grid

def draw_fertility_map(screen, fertility_map, cell_size):
    """
    Отрисовывает плодородные участки поля в игре.
    """
    height, width = fertility_map.shape
    for i in range(height):
        for j in range(width):
            fertility_level = fertility_map[i, j]
            color = 255 - int(fertility_level * 255)
            pygame.draw.rect(screen, (color, color, color), (j * cell_size, i * cell_size, cell_size, cell_size))

# Функция для отрисовки текущего поколения клеток
def draw_cells():
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                pygame.draw.rect(screen, survival_block, (j*cell_size, i*cell_size, cell_size, cell_size))

def randomize_grid():
    for i in range(grid.shape[0]) :
        for j in range(grid.shape[1]) :
            grid[i, j] = random.choice([0,1])

def create_fertility_map(fertility_map):
    rows, cols = fertility_map.shape

    # Определяем количество строк, которые будут плодородными сверху и снизу
    fertile_rows = rows // 6

    infertile_center_start = rows // 2 - rows // cell_size  # Начало неплодородного центра
    infertile_center_end = rows // 2 + rows // cell_size  # Конец неплодородного центра

    for i in range(rows):
        for j in range(cols):
            if i < fertile_rows or i >= rows - fertile_rows:
                fertility_map[i, j] = 1.0  # Более высокое плодородие сверху и снизу
            elif infertile_center_start <= i <= infertile_center_end:
                fertility_map[i, j] = 0.1  # Самое низкое плодородие по центру
            else:
                fertility_map[i, j] = 0.5  # Базовое плодородие для остальных участков
                
    return fertility_map




fertility_map = create_fertility_map(fertility_map)
# randomize_grid()
# Основной игровой цикл
draw_fertility = False
running = True
pause = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause 
            elif event.key == pygame.K_SLASH:  # Проверка нажатия на '/'
                draw_fertility = not draw_fertility
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Получаем позицию мыши
            mouseX, mouseY = pygame.mouse.get_pos()
            # Переводим координаты мыши в индексы сетки
            gridX = mouseX // cell_size
            gridY = mouseY // cell_size
            # Изменяем состояние клетки на противоположное
            grid[gridY, gridX] = 1 if grid[gridY, gridX] == 0 else 0
            
    
    
    if not pause:  
        screen.fill(white)
        # draw_grid()
        # плодородность
        if draw_fertility:
            draw_fertility_map(screen, fertility_map, cell_size)
        # Отрисовка клеток
        draw_cells()
        # Обновление состояния клеток
        update_grid()
            # Обновление экрана
        pygame.display.flip()
            # Задержка между поколениями
        time.sleep(0.1)

    

