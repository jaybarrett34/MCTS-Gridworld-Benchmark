def print_grid(env, path=[]):
    grid_size = int(env.observation_space.n ** 0.5)
    desc = env.unwrapped.desc 
    grid = [[desc[row][col].decode('utf-8') for col in range(grid_size)] for row in range(grid_size)]

    for state in path:
        row = state // grid_size
        col = state % grid_size
        grid[row][col] = f"\033[92mP[{state}]\033[0m" 

    grid[0][0] = f"\033[94mS[0]\033[0m"  
    grid[grid_size - 1][grid_size - 1] = f"\033[91mG[{(grid_size * grid_size) - 1}]\033[0m"  

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col][0] not in 'PSG': 
                state_number = row * grid_size + col
                if grid[row][col] == 'F':
                    grid[row][col] = f"\033[96mF[{state_number}]\033[0m"  
                elif grid[row][col] == 'H':
                    grid[row][col] = f"\033[93mH[{state_number}]\033[0m" 

    for row in grid:
        print(' '.join(row))
    print()

