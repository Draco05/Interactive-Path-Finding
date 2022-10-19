import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60

WIDTH, HEIGHT = 400, 400
PIXEL_SIZE = 10
COLS, ROWS = WIDTH // PIXEL_SIZE, HEIGHT // PIXEL_SIZE
WIN = pygame.display.set_mode((COLS * PIXEL_SIZE, ROWS * PIXEL_SIZE))

directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # (delta-x, delta-y)

dist = [[0 for _ in range(COLS)] for __ in range(ROWS)]  # distance of the start to any point
checked = [[False for _ in range(COLS)] for __ in range(ROWS)]
prev = [[[] for _ in range(COLS)] for __ in range(ROWS)]  # path of the start to any point
blocked = [[False for _ in range(COLS)] for __ in range(ROWS)]


# Using BFS to calculate the distances
def calc_dist(x, y):
    queue = [(x, y)]
    checked[y][x] = True
    while len(queue) > 0:
        x2, y2 = queue.pop(0)
        for direction in directions:
            new_x = x2 + direction[0]
            new_y = y2 + direction[1]
            if new_y < 0 or new_x < 0 or new_y >= ROWS or new_x >= COLS:
                continue
            if checked[new_y][new_x] or blocked[new_y][new_x]:
                continue
            checked[new_y][new_x] = True
            queue.append((new_x, new_y))
            dist[new_y][new_x] = dist[y2][x2] + 1
            prev[new_y][new_x] = prev[y2][x2] + [[x2, y2]]


def draw(start_pos, end_pos):
    WIN.fill(BLACK)  # Background

    # Path
    for j, i in prev[end_pos[0]][end_pos[1]]:
        top_left = (j * PIXEL_SIZE, i * PIXEL_SIZE)
        pygame.draw.rect(WIN, BLUE, (top_left[0], top_left[1], PIXEL_SIZE, PIXEL_SIZE))

    # Edges
    pygame.draw.rect(WIN, GREEN, (start_pos[1] * PIXEL_SIZE, start_pos[0] * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    pygame.draw.rect(WIN, RED, (end_pos[1] * PIXEL_SIZE, end_pos[0] * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    # Blocked pixels
    for i in range(ROWS):
        for j in range(COLS):
            if blocked[i][j]:
                top_left = (j * PIXEL_SIZE, i * PIXEL_SIZE)
                pygame.draw.rect(WIN, WHITE, (top_left[0], top_left[1], PIXEL_SIZE, PIXEL_SIZE))


# Reset to default all arrays
def clear_vals():
    global dist, checked, prev
    dist = [[0 for _ in range(COLS)] for __ in range(ROWS)]
    checked = [[False for _ in range(COLS)] for __ in range(ROWS)]
    prev = [[[] for _ in range(COLS)] for __ in range(ROWS)]


def main():
    run = True
    start_pos = (ROWS - 1, 0)  # (y, x)
    end_pos = (0, COLS - 1)  # (y, x)
    clock = pygame.time.Clock()
    while run:
        draw(start_pos, end_pos)
        clock.tick(FPS)
        changed = False
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_pos = (pos[1] // PIXEL_SIZE, pos[0] // PIXEL_SIZE)
                    changed = True
                elif event.key == pygame.K_2:
                    end_pos = (pos[1] // PIXEL_SIZE, pos[0] // PIXEL_SIZE)
                    changed = True
            elif pygame.mouse.get_pressed()[0]:
                blocked[pos[1] // PIXEL_SIZE][pos[0] // PIXEL_SIZE] = True
                changed = True
            elif pygame.mouse.get_pressed()[2]:
                blocked[pos[1] // PIXEL_SIZE][pos[0] // PIXEL_SIZE] = False
                changed = True

        if changed:
            clear_vals()
            calc_dist(start_pos[1], start_pos[0])
            if not checked[end_pos[0]][end_pos[1]] or blocked[start_pos[0]][start_pos[1]]:
                print("Non reachable")
            else:
                print(dist[end_pos[0]][end_pos[1]])
        pygame.display.update()


main()
