import pygame

pygame.init()

window_width = 800
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))
screen_colour = (0, 0, 0)

x = window_width / 4
y = window_height / 4

box_width = window_width / 6
box_height = window_height / 6

cubes = [
    [x + (0 * box_width), y + (0 * box_height)], [x + (1 * box_width), y + (0 * box_height)],
    [x + (2 * box_width), y + (0 * box_height)],
    [x + (0 * box_width), y + (1 * box_height)], [x + (1 * box_width), y + (1 * box_height)],
    [x + (2 * box_width), y + (1 * box_height)],
    [x + (0 * box_width), y + (2 * box_height)], [x + (1 * box_width), y + (2 * box_height)],
    [x + (2 * box_width), y + (2 * box_height)]
]


def check_collision(cube):
    x, y = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]
    if x > cube[0] and x < cube[0] + box_width and y > cube[1] and y < cube[1] + box_height and pressed:
        return True
    else:
        return False


def draw_text(text, x, y, colour, size):
    font = pygame.font.SysFont("Comic Sans MS", size)
    text_surface = font.render(text, False, colour)
    screen.blit(text_surface, (x, y))


def win_check(board, marker):
    return ((board[0] == board[1] == board[2] == marker) or (board[3] == board[4] == board[5] == marker) or
            (board[6] == board[7] == board[8] == marker) or (board[0] == board[3] == board[6] == marker) or
            (board[1] == board[4] == board[7] == marker) or (board[2] == board[5] == board[8] == marker) or
            (board[0] == board[4] == board[8] == marker) or (board[2] == board[4] == board[6] == marker))


board_layout = [None] * 9



class Red_button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.window_open_time = pygame.time.get_ticks()
        self.orig_image = pygame.image.load("images/button.png")
        self.image = self.orig_image
        self.size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (self.size[0] / 9, self.size[1] / 9))
        self.size = self.image.get_rect().size
        self.rect = self.image.get_rect()
        self.rect.center = (400, 650)
        self.restart = False

    def update(self):
        global board_layout
        if (self.rect.x < pygame.mouse.get_pos()[0] < self.rect.x + self.size[0]) and \
                self.rect.y < pygame.mouse.get_pos()[1] < self.rect.y + self.size[1]:
            old_pos = self.rect.center
            self.image = self.orig_image
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / 7, self.size[1] / 7))
            self.size = self.image.get_rect().size
            self.rect = self.image.get_rect()
            self.rect.center = old_pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.restart = False
                board_layout = [None] * 9
                

        else:
            old_pos = self.rect.center
            self.image = self.orig_image
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / 9, self.size[1] / 9))
            self.size = self.image.get_rect().size
            self.rect = self.image.get_rect()
            self.rect.center = old_pos


class Shape(pygame.sprite.Sprite):
    next_shape = 'X'

    def __init__(self, where, index):
        pygame.sprite.Sprite.__init__(self)
        self.where = where
        if Shape.next_shape == '0':
            self.scale = 8
            self.image = pygame.image.load("images/circle.png")
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / self.scale, self.size[1] / self.scale))
            Shape.next_shape = 'X'
            board_layout[index] = '0'
            self.rect = self.image.get_rect()
            self.rect.x = self.where[0] + 3
            self.rect.y = self.where[1] + 1
        elif Shape.next_shape == 'X':
            self.scale = 2.7
            self.image = pygame.image.load("images/cross.png")
            self.size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (self.size[0] / self.scale, self.size[1] / self.scale))
            Shape.next_shape = '0'
            board_layout[index] = 'X'
            self.rect = self.image.get_rect()
            self.rect.x = self.where[0]
            self.rect.y = self.where[1]


shape_group = pygame.sprite.Group()


button_group = pygame.sprite.Group()
red_button = Red_button()
button_group.add(red_button)

while True:
    screen.fill(screen_colour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()

    if red_button.restart:
        # screen.fill(screen_colour)
        button_group.update()
        button_group.draw(screen)
        for sprite in shape_group:
            sprite.kill()


    if not red_button.restart:
        # screen.fill(screen_colour)

        pygame.draw.rect(screen, (255, 0, 255), (cubes[0][0], cubes[0][1], box_width * 3, box_height * 3))
        pygame.draw.line(screen, (255, 255, 255), (cubes[1]), (cubes[7][0], cubes[7][1] + box_height))
        pygame.draw.line(screen, (255, 255, 255), (cubes[2]), (cubes[8][0], cubes[8][1] + box_height))

        pygame.draw.line(screen, (255, 255, 255), (cubes[3]), (cubes[5][0] + box_width, cubes[5][1]))
        pygame.draw.line(screen, (255, 255, 255), (cubes[6]), (cubes[8][0] + box_width, cubes[8][1]))

        board = [
            [check_collision(cubes[0])], [check_collision(cubes[1])], [check_collision(cubes[2])],
            [check_collision(cubes[3])], [check_collision(cubes[4])], [check_collision(cubes[5])],
            [check_collision(cubes[6])], [check_collision(cubes[7])], [check_collision(cubes[8])],
        ]

        for i in range(len(board)):
            if board[i] == [True]:
                if board_layout[i] == None:
                    cross = Shape(cubes[i], i)
                    shape_group.add(cross)

        shape_group.update()
        shape_group.draw(screen)

    if win_check(board_layout, 'X'):

        draw_text(f"Congratulations! X have won the Game", 135, 500, (255, 255, 255), 35)
        red_button.restart = True

    elif win_check(board_layout, '0'):

        draw_text(f"Congratulations! 0 have won the Game", 135, 500, (255, 255, 255), 35)
        red_button.restart = True

    elif None not in board_layout:

        draw_text(f"It's a Draw", 300, 500, (255, 255, 255), 35)
        red_button.restart = True

    pygame.display.update()
