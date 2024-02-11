def update_grid():
    global grid
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # Подсчет числа соседей для каждой клетки
            neighbors = np.sum(grid[max(i-1, 0):min(i+2, grid.shape[0]), max(j-1, 0):min(j+2, grid.shape[1])]) - grid[i, j]
            fertility_bonus = fertility_map[i, j] 
            if grid[i, j] == 1:
                # Клетки на более плодородных участках могут выжить даже при одном соседе
                min_neighbors_for_survival = 2 if fertility_bonus < 0.5 else 1
                max_neighbors_for_survival = 3
                if neighbors < min_neighbors_for_survival or neighbors > max_neighbors_for_survival:
                    new_grid[i, j] = 0
            else:
                # Плодородные участки могут уменьшить необходимое количество соседей для рождения новой клетки
                required_neighbors_for_birth = 3 if fertility_bonus < 0.5 else 2
                if neighbors == required_neighbors_for_birth:
                    new_grid[i, j] = 1


def update_grid():
    global grid, fertility_map
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = np.sum(grid[max(i-1, 0):min(i+2, grid.shape[0]), max(j-1, 0):min(j+2, grid.shape[1])]) - grid[i, j]
            fertility_bonus = fertility_map[i, j] 
            
            if grid[i, j] == 1:
                # Клетки "поедают" плодородие места
                fertility_map[i, j] = max(0, fertility_map[i, j] - 0.3)  # Уменьшаем плодородие, не позволяя уйти в отрицательное значение
                
                # Определяем условия выживания на основе плодородия
                min_neighbors_for_survival = 2 if fertility_bonus < 0.5 else 1
                max_neighbors_for_survival = 3
                if neighbors < min_neighbors_for_survival or neighbors > max_neighbors_for_survival:
                    new_grid[i, j] = 0
                    # Когда клетка исчезает, она "наполняет" почву на +0.5 энергии
                    fertility_map[i, j] = min(1, fertility_map[i, j] + 0.5)  # Увеличиваем плодородие, не превышая максимум в 1
            else:
                # Условия для рождения новой клетки
                required_neighbors_for_birth = 3 if fertility_bonus < 0.5 else 2
                if neighbors == required_neighbors_for_birth:
                    new_grid[i, j] = 1
                    # Клетка рождается, но не изменяет плодородие при рождении
                    
    grid = new_grid
