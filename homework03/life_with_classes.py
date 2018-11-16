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
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_cell_list(self, cell_list: "CellList") -> None:
        x = 0
        y = 0
        for cell in cell_list:
            if cell.is_alive():
                pygame.draw.rect(self.screen, pygame.Color('green'), [x, y, self.cell_size, self.cell_size])
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'), [x, y, self.cell_size, self.cell_size])
            x += self.cell_size
            if x >= self.width:
                y += self.cell_size
                x = 0

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        cell_list = CellList(self.cell_height, self.cell_width, randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(cell_list)
            cell_list.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row: int, col: int, state=False) -> None:
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize=False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.grid = []
        for st in range(nrows):
            line = []
            for elem in range(ncols):
                if randomize:
                    line.append(Cell(st, elem, random.randint(0, 1)))
                else:
                    line.append(Cell(st, elem, False))
            self.grid.append(line)

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        col, row = cell.col, cell.row
        for st in range(row - 1, row + 2):
            for elem in range(col - 1, col + 2):
                if st in range(0, self.nrows) and elem in range(0, self.ncols) and (elem != col or st != row):
                    neighbours.append(self.grid[st][elem])
        return neighbours

    def update(self):
        new_clist = copy.deepcopy(self.grid)
        for cell in self:
            neigh = sum(i.is_alive() for i in self.get_neighbours(cell))
            if neigh != 2 and neigh != 3:
                new_clist[cell.row][cell.col].state = False
            elif neigh == 3:
                new_clist[cell.row][cell.col].state = True
        self.grid = new_clist
        return self

    def __iter__(self):
        self.st, self.elem = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.st < self.nrows:
            cell = self.grid[self.st][self.elem]
            self.elem += 1
            if self.elem == self.ncols:
                self.st += 1
                self.elem = 0
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        str = ''
        str1 = ''
        for st in range(self.nrows, 0):
            for col in range(self.ncols, 0):
                if self.grid[st][col].state:
                    str += '1'
                else:
                    str += '0'
            str1 += str[::-1]
            str1 += '\n'
        return str1

    @classmethod
    def from_file(cls, filename: str) -> "CellList":
        with open(filename, 'r') as file:
            grid = []
            row = 0
            col = 0
            ncol = 0
            for st in file:
                line = []
                for c in st:
                    if c == '0':
                        line.append(Cell(row, col, False))
                    if c == '1':
                        line.append(Cell(row, col, True))
                    col += 1
                ncol = col
                col = 0
                grid.append(line)
            for line in grid:
                for cell in line:
                    cell.row = row
                row += 1

            cell_list = CellList(row, ncol, False)
            cell_list.grid = grid
            return cell_list


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
