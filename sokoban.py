import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Define the window size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Sokoban")

# Function to load images with verification
def load_image(filename):
    if not os.path.exists(filename):
        print(f"Error: No file '{filename}' found in working directory '{os.getcwd()}'")
        pygame.quit()
        sys.exit()
    return pygame.image.load(filename)

# Load the images
tile_size = 50


# Charger les images avec la bonne taille
obstacle_image = pygame.transform.scale(load_image("obstacle.png"), (tile_size, tile_size))
empty_image = pygame.transform.scale(load_image("floor.png"), (tile_size, tile_size))
target_image = pygame.transform.scale(load_image("target.png"), (tile_size, tile_size))
box_image = pygame.transform.scale(load_image("box.png"), (tile_size, tile_size))
player_image = pygame.transform.scale(load_image("player.png"), (tile_size, tile_size))


# Define the tile size


# Define the game grid matrix
initial_grid = [
    [-1, -1, -1, -1, -1],
    [-1,  0,  2,  1, -1],
    [-1,  3,  0,  0, -1],
    [-1,  0,  0,  0, -1],
    [-1, -1, -1, -1, -1]
]

# Initial copy of the grid for resetting
grid = [row[:] for row in initial_grid]

# Movement history for undo
history = []

# Function to draw the grid
def draw_grid():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            x = col * tile_size
            y = row * tile_size
            if grid[row][col] == -1:
                screen.blit(obstacle_image, (x, y))
            elif grid[row][col] == 0:
                screen.blit(empty_image, (x, y))
            elif grid[row][col] == 1:
                screen.blit(target_image, (x, y))
            elif grid[row][col] == 2:
                screen.blit(box_image, (x, y))
            elif grid[row][col] == 3:
                screen.blit(player_image, (x, y))

# Function to find the player's position
def find_player():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 3:
                return row, col
    return None

# Function to move the player
def move_player(dx, dy):
    global grid
    player_pos = find_player()
    if player_pos:
        x, y = player_pos
        new_x, new_y = x + dx, y + dy
        if grid[new_x][new_y] in [0, 1]:  # Empty space or target
            history.append((x, y, new_x, new_y))
            grid[x][y], grid[new_x][new_y] = grid[new_x][new_y], grid[x][y]
        elif grid[new_x][new_y] == 2:  # Box
            new_box_x, new_box_y = new_x + dx, new_y + dy
            if grid[new_box_x][new_box_y] in [0, 1]:  # Move box to empty space or target
                history.append((x, y, new_x, new_y, new_box_x, new_box_y))
                grid[new_box_x][new_box_y], grid[new_x][new_y], grid[x][y] = grid[new_x][new_y], grid[x][y], 0

# Function to undo the last move
def undo_move():
    global grid
    if history:
        last_move = history.pop()
        if len(last_move) == 4:  # Player move
            x, y, new_x, new_y = last_move
            grid[x][y], grid[new_x][new_y] = grid[new_x][new_y], grid[x][y]
        elif len(last_move) == 6:  # Player move with box
            x, y, new_x, new_y, new_box_x, new_box_y = last_move
            grid[x][y], grid[new_x][new_y], grid[new_box_x][new_box_y] = grid[new_x][new_y], grid[new_box_x][new_box_y], 2

# Function to reset the game
def reset_game():
    global grid, history
    grid = [row[:] for row in initial_grid]
    history = []

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(-1, 0)
            elif event.key == pygame.K_DOWN:
                move_player(1, 0)
            elif event.key == pygame.K_LEFT:
                move_player(0, -1)
            elif event.key == pygame.K_RIGHT:
                move_player(0, 1)
            elif event.key == pygame.K_u:  # Undo move
                undo_move()
            elif event.key == pygame.K_r:  # Reset game
                reset_game()

    # Dessiner la grille du jeu
    screen.fill((255, 255, 255))
    draw_grid()

    # Mettre à jour l'affichage
    pygame.display.flip()
