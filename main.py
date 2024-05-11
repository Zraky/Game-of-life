import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
gen_life_cooldown = 100
probability_of_spawn = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
last_gen = pygame.time.get_ticks()
run = True
pygame.display.set_caption("Jeux de la vie")


def spawn(grid, proba):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if random.randint(0, 100) <= proba:
                grid[x][y] = 1
            else:
                grid[x][y] = 0
    return grid


class Life_map():

    def __init__(self, column_number=100, line_number=100, prob_of_spawn=probability_of_spawn, line_color=(100, 100, 100), life_color=(100, 100, 100)):
        self.screen_size_w = round(SCREEN_WIDTH * 3/4)
        self.screen_size_h = SCREEN_HEIGHT

        self.column_size = round(self.screen_size_w / column_number)
        self.line_size = round(self.screen_size_h / line_number)
        self.line_color = line_color
        self.life_color = life_color

        self.grid = [[0 for _ in range(column_number)] for _ in range(line_number)]
        self.copy_grid = [[0 for _ in range(column_number)] for _ in range(line_number)]

        self.grid = spawn(self.grid, prob_of_spawn)

    def draw(self):
        for x in range(len(self.grid)):
            pygame.draw.line(screen, self.line_color, (x * self.column_size, 0),
                             (x * self.column_size, self.screen_size_h), 1)
            for y in range(len(self.grid[x])):
                pygame.draw.line(screen, self.line_color, (0, y * self.line_size),
                                 (self.screen_size_w, y * self.line_size), 1)
                if self.grid[x][y] == 1:
                    pygame.draw.rect(screen, self.life_color,
                                     (x * self.column_size, y * self.line_size, self.column_size, self.line_size))

    def next_gen(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                stack_grid = 0

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        nx, ny = x + i, y + j
                        if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[x]):
                            stack_grid += self.grid[nx][ny]

                if self.grid[x][y] == 1:
                    if stack_grid == 2 or stack_grid == 3:
                        self.copy_grid[x][y] = 1
                    else:
                        self.copy_grid[x][y] = 0
                else:
                    if stack_grid == 3:
                        self.copy_grid[x][y] = 1
                    else:
                        self.copy_grid[x][y] = 0

        self.grid, self.copy_grid = self.copy_grid, self.grid


life_map = Life_map()


class Menu():
    def __init__(self, color_1=(100, 100, 100), color_2=(150, 150, 150)):
        self.screen_size_w = round(SCREEN_WIDTH * 1 / 4)
        self.screen_size_h = SCREEN_HEIGHT
        self.color = color_1
        self.police = pygame.font.SysFont(str(None), 30)
        self.living_cell = 0
        self.previous_living_cell = []
        self.gen = 0

        self.button_re_start = pygame.Rect(self.screen_size_w * 3.1, self.screen_size_h * 1 / 3, self.screen_size_w * 0.8,self.screen_size_h * 1 / 10)
        self.button_re_start_color = color_1
        self.button_start = pygame.Rect(self.screen_size_w * 3.1, self.screen_size_h * 1 / 2, self.screen_size_w * 0.8, self.screen_size_h * 1/10)
        self.button_start_color = color_1
        self.button_stop = pygame.Rect(self.screen_size_w * 3.1, self.screen_size_h * 10 / 15, self.screen_size_w * 0.8, self.screen_size_h * 1/10)
        self.button_stop_color = color_1
        self.button_quit = pygame.Rect(self.screen_size_w * 3.1, self.screen_size_h * 10 / 12, self.screen_size_w * 0.8, self.screen_size_h * 1 / 10)
        self.button_quit_color = color_1
        self.button_color_1 = color_1
        self.button_color_2 = color_2
        self.police_button = pygame.font.SysFont(str(None), 50)

        self.continue_run = True

    def button_click(self, mouse_1, mouse_pos):
        if self.button_re_start.collidepoint(mouse_pos):
            self.button_re_start_color = self.button_color_2
            if mouse_1:
                global life_map
                life_map = Life_map()
                self.gen = 0
        else:
            self.button_re_start_color = self.button_color_1

        if self.button_start.collidepoint(mouse_pos):
            self.button_start_color = self.button_color_2
            if mouse_1:
                self.continue_run = True
        else:
            self.button_start_color = self.button_color_1

        if self.button_stop.collidepoint(mouse_pos):
            self.button_stop_color = self.button_color_2
            if mouse_1:
                self.continue_run = False
        else:
            self.button_stop_color = self.button_color_1

        if self.button_quit.collidepoint(mouse_pos):
            self.button_quit_color = self.button_color_2
            if mouse_1:
                global run
                run = False
        else:
            self.button_quit_color = self.button_color_1

    def number_cell(self, grid):
        self.gen += 1
        self.living_cell = 0
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == 1:
                    self.living_cell += 1

    def draw(self):
        dt = clock.tick(60) / 1000

        pygame.draw.rect(screen, (self.color), (self.screen_size_w * 3, 0, SCREEN_WIDTH, self.screen_size_h), 5, 0)

        screen.blit((self.police.render(f"Gen n°{self.gen}", 1, self.color)),(self.screen_size_w * 3.1, self.screen_size_h * 1/98))
        screen.blit((self.police.render(f"Living cell : {self.living_cell}", 1, self.color)), (self.screen_size_w * 3.1, self.screen_size_h * 1/20))
        screen.blit((self.police.render(f"Spawn : {probability_of_spawn}%", 1, self.color)), (self.screen_size_w * 3.1, self.screen_size_h * 1 / 12))
        screen.blit((self.police.render(f"Time : {int(round(pygame.time.get_ticks() / 1000, 0))}s", 1, self.color)), (self.screen_size_w * 3.1, self.screen_size_h * 1 / 8))
        screen.blit((self.police.render(f"FPS : {round(1 / dt, 2)}", 1, self.color)), (self.screen_size_w * 3.1, self.screen_size_h * 1 / 6))


        pygame.draw.rect(screen, self.button_re_start_color, self.button_re_start, 10, 4)
        screen.blit((self.police_button.render("restart", 1, self.button_re_start_color)),(self.button_re_start.x * 1.045, self.button_re_start.y * 1.05))

        pygame.draw.rect(screen, self.button_start_color, self.button_start, 10, 4)
        screen.blit((self.police_button.render("start", 1, self.button_start_color)), (self.button_start.x * 1.06, self.button_start.y * 1.05))

        pygame.draw.rect(screen, self.button_stop_color, self.button_stop, 10, 4)
        screen.blit((self.police_button.render("stop", 1, self.button_stop_color)), (self.button_stop.x * 1.07, self.button_stop.y * 1.03))

        pygame.draw.rect(screen, self.button_quit_color, self.button_quit, 10, 4)
        screen.blit((self.police_button.render("exit", 1, self.button_quit_color)), (self.button_quit.x * 1.08, self.button_quit.y * 1.025))


menu = Menu()

while run:
    screen.fill("#000000")
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()
    mouse_clic_0 = pygame.mouse.get_pressed()[0]
    mouse_clic_2 = pygame.mouse.get_pressed()[2]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #update
    menu.button_click(mouse_clic_0, mouse_pos)
    current_time = pygame.time.get_ticks()
    if current_time - last_gen > gen_life_cooldown and menu.continue_run:
        last_gen = current_time
        life_map.next_gen()
        menu.number_cell(life_map.grid)

    #draw
    menu.draw()
    life_map.draw()

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()