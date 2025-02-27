import pygame
import sys
import random


WIDTH, HEIGHT = 1200, 800
BLOCK_SIZE = 30
WALL_BLOCKS = 2
SNAKE_ICON = "snake.jpg"
GAME_TITLE = "Snake"
INITIAL_GAME_SPEED = 6
INITIAL_APPLES = 5
BACKGROUND_COLOR = (128, 64, 48)
INITIAL_SNAKE_LENGHT = 10
SIZE_X = WIDTH // BLOCK_SIZE - WALL_BLOCKS * 2
SIZE_Y = HEIGHT // BLOCK_SIZE - WALL_BLOCKS * 2
APPLE_COLOR = (191, 31, 31)
APPLE_RADIUS = BLOCK_SIZE // 4
SNAKE_RADIUS = BLOCK_SIZE // 4
SNAKE_COLOR = (31, 191, 31)
WALL_COLOR = (31, 31, 31)
TEXT_COLOR = (255, 255, 255)

def main():
    screen, clock = initialize_pygame()
    game_state = initialize_game_state()
    while game_state["program_running"]:
        clock.tick(game_state['game_speed'])
        events = get_events()
        update_game_state(events, game_state)
        update_screen(screen, game_state)
    perform_shutdown()



def initialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    icon = pygame.image.load(SNAKE_ICON)
    pygame.display.set_icon(icon)
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    return screen, clock

def initialize_game_state():
    game_state = {
        "program_running": True,
        "game_running": False,
        "game_speed": INITIAL_GAME_SPEED,
        "game_paused": False,
        'score': 0
    }
    return game_state
def perform_shutdown():
    pygame.quit()
    sys.exit()

def get_events():
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.append("quit")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                events.append('up')
            elif event.key == pygame.K_DOWN:
                events.append('down')
            elif event.key == pygame.K_LEFT:
                events.append('left')
            elif event.key == pygame.K_RIGHT:
                events.append('right')
            elif event.key == pygame.K_SPACE:
                events.append('space')
            elif event.key == pygame.K_RETURN:
                events.append('enter')
            elif event.key == pygame.K_ESCAPE:
                events.append('escape')
    return events

def update_game_state(events, game_state):
    check_key_presses(events, game_state)
    if game_state['game_running'] and not game_state['game_paused']:
        move_snake(game_state)
        check_collisions(game_state)
        check_apple_consumption(game_state)

def move_snake(game_state):
    x = game_state['snake'][0][0] + game_state['direction'][0]
    y = game_state['snake'][0][1] + game_state['direction'][1]
    game_state['snake'].insert(0, (x, y))

def check_collisions(game_state):
    x, y = game_state['snake'][0]
    if (
        x < 0 or y < 0 or x >= SIZE_X or y >= SIZE_Y or
        len(game_state['snake']) > len(set(game_state['snake']))
    ):
        game_state['game_running'] = False


def check_apple_consumption(game_state):
    apples_eaten = 0
    for apple in game_state['apples']:
        if apple == game_state['snake'][0]:
            game_state['apples'].remove(apple)
            place_apples(1, game_state)
            game_state['score'] += 1
            apples_eaten += 1
            game_state['game_speed'] = round(game_state["game_speed"] * 1)
    if apples_eaten == 0:
        game_state['snake'].pop()


def check_key_presses(events, game_state):
    if 'quit' in events:
        game_state['program_running'] = False
    elif not game_state['game_running']:
        if 'escape' in events:
            game_state['program_running'] = False
        elif 'enter' in events:
            initialize_new_game(game_state)
            game_state['game_running'] = True
    elif game_state['game_paused']:
        if 'escape' in events:
            game_state['game_running'] = False
        elif 'space' in events:
            game_state['game_paused'] = False
        elif "enter" in events:
            game_state['game_running'] = True
            initialize_new_game(game_state)
    else:
        if 'escape' in events or 'space' in events:
            game_state['game_paused'] = True
        if 'up' in events:
            game_state['direction'] = (0, -1)
        if 'down' in events:
            game_state['direction'] = (0, 1)
        if 'left' in events:
            game_state['direction'] = (-1, 0)
        if 'right' in events:
            game_state['direction'] = (1, 0)

def update_screen(screen, game_state):
    screen.fill(BACKGROUND_COLOR)
    if not game_state['game_running']:
        print_new_game_message(screen)
    elif game_state['game_paused']:
        print_game_paused_message(screen)
    else:
        draw_apples(screen, game_state['apples'])
        draw_snake(screen, game_state['snake'])
    draw_walls(screen)
    print_score(screen, game_state['score'])
    pygame.display.flip()

def draw_walls(screen):
    wall_size = WALL_BLOCKS * BLOCK_SIZE
    pygame.draw.rect(screen, WALL_COLOR, ((0, 0), (WIDTH, wall_size)))
    pygame.draw.rect(screen, WALL_COLOR, ((0,0), (wall_size, HEIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, ((0, HEIGHT - wall_size), (WIDTH, HEIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, ((WIDTH - wall_size, 0), (WIDTH, HEIGHT)))
def print_score(screen, score):
    ...
def print_game_paused_message(screen):
    font = pygame.font.SysFont('Courier New', 50, bold=True)
    message1 = "Press ENTER to start new game"
    message2 = "Press SPACE to continue"
    text1 = font.render(message1, True, TEXT_COLOR)
    text2 = font.render(message2, True, TEXT_COLOR)
    text_rect1 = text1.get_rect()
    text_rect2 = text2.get_rect()
    text_rect1.center = (WIDTH // 2, HEIGHT // 2 - 50)
    text_rect2.center = (WIDTH // 2, HEIGHT // 2 + 50)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
def draw_snake(screen, snake):
    for segment in snake:
        x = segment[0] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        y = segment[1] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        rect = ((x, y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, rect, border_radius= SNAKE_RADIUS)

def initialize_new_game(game_state):
    game_state['snake'] = []
    place_snake(INITIAL_SNAKE_LENGHT, game_state)
    game_state['apples'] = []
    place_apples(INITIAL_APPLES, game_state)
    game_state ['direction'] = (1, 0)
    game_state['game_paused'] = False
    game_state['game_score'] = 0
    game_state['game_speed'] = INITIAL_GAME_SPEED


def place_apples(apples, game_state):
    for i in range(apples):
        x = random.randint(0, SIZE_X - 1)
        y = random.randint(0, SIZE_Y - 1)
        while(x, y) in game_state['apples'] or (x, y) in game_state['snake']:
            x = random.randint(0, SIZE_X - 1)
            y = random.randint(0, SIZE_Y - 1)
        game_state['apples'].append((x, y))


def draw_apples(screen, apples):
    for apple in apples:
        x = apple[0] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        y = apple[1] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        rect = ((x, y), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, APPLE_COLOR, rect, border_radius= APPLE_RADIUS)

def print_new_game_message(screen):
    font = pygame.font.SysFont('Courier New', 50, bold=True)
    message = "Press ENTER to start new game"
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)

def place_snake(lenght, game_state):
    x = SIZE_X // 2
    y = SIZE_Y // 2
    game_state['snake'].append((x, y))
    for i in range(1, lenght):
        game_state['snake'].append((x - i, y))


def print_score(screen, score):
    font = pygame.font.SysFont('Courier New', 24, bold = True)
    text = font.render(f"Score: {score}", True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (WALL_BLOCKS * BLOCK_SIZE, 0)
    screen.blit(text, text_rect)
main()




