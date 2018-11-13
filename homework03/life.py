import pygame
from pygame.locals import *
import random
import copy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) -> list:
        self.clist = []
        self.clist = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for st in range(self.cell_height):
                for element in range(self.cell_width):
                    self.clist[st][element] = random.randint(0, 1)
        return self.clist

    def draw_cell_list(self, clist: list) -> None:
        x = 0
        y = 0
        for col in range(self.cell_height):
            for row in range(self.cell_width):
                if clist[col][row] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), [x, y, self.cell_size, self.cell_size])
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), [x, y, self.cell_size, self.cell_size])
                x += self.cell_size
            y += self.cell_size
            x = 0

    def get_neighbours(self, cell: tuple) -> list:
        neighbours = []
        row, col = cell
        for x in range(row - 1, row + 2):
            for y in range(col - 1, col + 2):
                if x in range(0, self.cell_height) and y in range(0, self.cell_width) and (x != row or y != col):
                    neighbours.append(self.clist[x][y])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        new_clist = copy.deepcopy(cell_list)
        for st in range(self.cell_height):
            for elem in range(self.cell_width):
                if sum(self.get_neighbours((st, elem))) != 2 and sum(self.get_neighbours((st, elem))) != 3:
                    new_clist[st][elem] = 0
                elif sum(self.get_neighbours((st, elem))) == 3:
                    new_clist[st][elem] = 1
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
