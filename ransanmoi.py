import pygame
import random
import os

# Xóa màn hình
os.system('cls')

# Thiết lập kích thước cửa sổ
WIDTH = 800
HEIGHT = 600

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rắn săn mồi")

clock = pygame.time.Clock()

# Thiết lập các biến cho rắn và mồi
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_size = 15
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_size = 10

# Thiết lập các biến cho hướng di chuyển ban đầu
direction = 'RIGHT'
change_to = direction

# Thiết lập biến đếm điểm và điểm cao nhất
score = 0
high_score = 0

# Khởi tạo danh sách obstacles
obstacles = []

# Hàm để hiển thị rắn và mồi lên màn hình
def show_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, WHITE, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

def show_food():
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], food_size, food_size))

def show_score():
    font = pygame.font.Font(None, 24)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (10, 30))

def show_game_over():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Ban Da Thua ", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)

    restart_text = font.render("Nhan Enter đe choi lai", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

def create_obstacles():
    # Xóa các vị trí cũ của tường chặn
    obstacles.clear()
    
    # Tạo ra các vị trí mới cho tường chặn
    for _ in range(6):  # Số lượng tường chặn (có thể điều chỉnh)
        obstacle_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        obstacles.append(obstacle_pos)

def show_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, pygame.Rect(obstacle[0], obstacle[1], snake_size, snake_size))

# Hàm để chạy trò chơi
def run_game():
    global direction, change_to, snake_pos, food_pos, score, high_score  # Thêm khai báo global
    running = True
    game_over = False

    # Thời gian để thay đổi vị trí các tường chặn (3 giây)
    obstacle_timer = pygame.time.get_ticks() + 3000

    while running:
        while game_over:
            screen.fill(BLACK)
            show_game_over()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Reset trạng thái trò chơi khi nhấn Enter
                        snake_pos = [[100, 50], [90, 50], [80, 50]]
                        direction = 'RIGHT'
                        change_to = direction
                        food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
                        score = 0
                        game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Cập nhật hướng di chuyển của rắn
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Tạo phần tử mới cho đầu rắn
        new_head = [snake_pos[0][0], snake_pos[0][1]]

        # Cập nhật vị trí của đầu rắn
        if direction == 'UP':
            new_head[1] -= 10
        elif direction == 'DOWN':
            new_head[1] += 10
        elif direction == 'LEFT':
            new_head[0] -= 10
        elif direction == 'RIGHT':
            new_head[0] += 10

        # Thêm đầu rắn vào vị trí mới
        snake_pos.insert(0, new_head)

        # Kiểm tra nếu rắn ăn mồi
        if snake_pos[0] == food_pos:
            # Tăng độ dài của rắn
            snake_pos.append([0, 0])
            score += 1

            # Cập nhật điểm cao nhất
            if score > high_score:
                high_score = score

            # Tạo mồi mới
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        else:
            # Xóa phần tử cuối cùng của rắn
            snake_pos.pop()

        # Kiểm tra nếu rắn chạm vào cạnh màn hình hoặc chính nó
        if snake_pos[0][0] >= WIDTH or snake_pos[0][0] < 0 or snake_pos[0][1] >= HEIGHT or snake_pos[0][1] < 0:
            game_over = True
        for block in snake_pos[1:]:
            if snake_pos[0] == block:
                game_over = True

        # Kiểm tra thời gian để thay đổi vị trí của các tường chặn
        if pygame.time.get_ticks() >= obstacle_timer:
            create_obstacles()
            obstacle_timer = pygame.time.get_ticks() + 3000  # Cập nhật thời gian cho lần thay đổi tiếp theo

        # Hiển thị các phần tử lên màn hình
        screen.fill(BLACK)
        show_snake(snake_pos)
        show_food()
        show_obstacles()  # Hiển thị các tường chặn
        show_score()

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()

# Gọi hàm run_game()
run_game()
