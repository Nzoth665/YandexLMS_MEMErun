import pygame
import heapq
import math

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enemy Pathfinding with Obstacle Avoidance")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5


# Define the enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.path = []
        self.speed = 2

    def update(self):
        if self.path:
            target = self.path[0]
            self.move_towards(target)
            if self.rect.centerx == target[0] and self.rect.centery == target[1]:
                self.path.pop(0)  # Remove the target point once reached

    def move_towards(self, target):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            dx, dy = dx / distance, dy / distance  # Normalize direction
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed


# A* Pathfinding classes
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # Cost to get to this node
        self.h = 0  # Heuristic estimate from this node to the goal
        self.f = float('inf')  # Total cost (g + h)
        self.parent = None  # Parent node for path reconstruction

    def __lt__(self, other):
        return self.f < other.f  # For priority queue


# A* algorithm
def astar(start, goal, grid):
    open_list = []
    closed_list = set()

    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])

    start_node.g = 0
    start_node.f = start_node.g + heuristic(start_node, goal_node)
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if (current_node.x, current_node.y) == (goal_node.x, goal_node.y):
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        closed_list.add((current_node.x, current_node.y))

        for neighbor in neighbors(current_node, grid):
            if (neighbor.x, neighbor.y) in closed_list:
                continue

            tentative_g = current_node.g + 1  # Assumes cost of moving to a neighbor is always 1

            if tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal_node)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)

    return None  # No path found


def neighbors(node, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
    result = []

    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 0:
            result.append(Node(nx, ny))

    return result


def heuristic(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)  # Manhattan distance


# Create the grid (0 = walkable, 1 = blocked)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Add some obstacles
grid[5][5] = 1
grid[6][5] = 1
grid[7][5] = 1
grid[5][6] = 1
grid[5][7] = 1
grid[10][10] = 1
grid[11][10] = 1
grid[12][10] = 1

# Create player and enemy
player = Player()
enemy = Enemy(100, 100)

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the player's position
    player_position = (player.rect.centerx // GRID_SIZE, player.rect.centery // GRID_SIZE)

    # Calculate the path for the enemy to follow
    enemy_position = (enemy.rect.centerx // GRID_SIZE, enemy.rect.centery // GRID_SIZE)
    path = astar(enemy_position, player_position, grid)
    if path:
        enemy.path = path

    # Update all sprites
    all_sprites.update()

    # Draw everything
    screen.fill(WHITE)

    # Draw the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = BLACK if grid[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    # Draw the player and enemy
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
