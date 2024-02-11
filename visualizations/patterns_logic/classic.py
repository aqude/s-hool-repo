def update_grid():
    global grid
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # Подсчет числа соседей для каждой клетки
            neighbors = np.sum(grid[max(i-1, 0):min(i+2, grid.shape[0]), max(j-1, 0):min(j+2, grid.shape[1])]) - grid[i, j]
            # Применение правил игры "Жизнь"
            if grid[i, j] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and neighbors == 3:
                new_grid[i, j] = 1
    grid = new_grid