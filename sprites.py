import pygame as pg
from pygame.math import Vector2 as vec
from settings import *
import random

class Pacman():
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pixel_pos = self.get_pixel_pos()
        self.dir = vec(1,0)
        self.stored_dir = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2.5
        self.lives = 3

    def update(self):
        if self.able_to_move:
            self.pixel_pos += self.dir*self.speed
        if self.time_to_move():
            if self.stored_dir != None:
                self.dir = self.stored_dir
            self.able_to_move = self.can_move()

        # set grid position
        self.grid_pos[0] = (self.pixel_pos[0]-TOP_BOTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pixel_pos[1]-TOP_BOTTOM_BUFFER+self.app.cell_height//2)//self.app.cell_height+1

        if self.on_coin():
            self.eat_coin()

    def move(self, dir):
        self.stored_dir = dir


    def draw(self):
        # drawing pacman
        pg.draw.circle(self.app.screen, YELLOW, (int(self.pixel_pos.x), int(self.pixel_pos.y)), self.app.cell_width//2+2)
        # drawing lives
        for x in range(self.lives):
            pg.draw.circle(self.app.screen, YELLOW, (35 + 20*x, HEIGHT - 15), 8)
        # draw grid position rectangle
        #pg.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                    self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2,
        #                                    self.app.cell_width, self.app.cell_height), 1)

    def get_pixel_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                  (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        if int(self.pixel_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                return True
        if int(self.pixel_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.dir == vec(0,1) or self.dir == vec(0,-1) or self.dir == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.dir) == wall:
                return False
        return True

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pixel_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                    return True
            if int(self.pixel_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.dir == vec(0, 1) or self.dir == vec(0, -1) or self.dir == vec(0, 0):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1


class Ghosts():
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pixel_pos = self.get_pixel_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.color = self.set_color()
        self.dir = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pixel_pos += self.dir * self.speed
            if self.time_to_move():
                self.move()
        # set grid position
        self.grid_pos[0] = (self.pixel_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pixel_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self):
        pg.draw.circle(self.app.screen, self.color, (int(self.pixel_pos.x), int(self.pixel_pos.y)), self.radius)
    
    def get_pixel_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                  (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def set_color(self):
        if self.number == 0:
            return BLUE
        if self.number == 1:
            return PINK
        if self.number == 2:
            return RED
        if self.number == 3:
            return ORANGE

    def set_personality(self):
        if self.number == 0:
            return "blinky"
        elif self.number == 1:
            return "pinky"
        elif self.number == 2:
            return "clyde"
        else:
            return "inky"

    def set_target(self):
        if self.personality == "blinky" or self.personality == "inky":
            return self.app.pacman.grid_pos
        else:
            if self.app.pacman.grid_pos[0] > COLS//2 and self.app.pacman.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            if self.app.pacman.grid_pos[0] > COLS//2 and self.app.pacman.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.pacman.grid_pos[0] < COLS//2 and self.app.pacman.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

    def set_speed(self):
        if self.personality in ["blinky", "pinky"]:
            speed = 2
        else:
            speed = 1.5
        return speed

    def time_to_move(self):
        if int(self.pixel_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.dir == vec(1, 0) or self.dir == vec(-1, 0) or self.dir == vec(0, 0):
                return True
        if int(self.pixel_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.dir == vec(0, 1) or self.dir == vec(0, -1) or self.dir == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "blinky": # fast | chases pacman
            self.dir = self.get_path_direction(self.target)
        if self.personality == "pinky": # scared | runs from pacman
            self.dir = self.get_path_direction(self.target)
        if self.personality == "clyde": # random | moves randomly
            self.dir = self.get_clyde_dir()
        if self.personality == "inky": # slow | should try to ambush pacman, currently same as blinky, but slower
            self.dir = self.get_path_direction(self.target)

    # need to make clyde come out of the spawn area first, then move randomly
    def get_clyde_dir(self): # moves randomly
        while True:
            num = random.randint(-2, 1)
            if num == -2:
                x_dir, y_dir = 1,0
            elif num == -1:
                x_dir, y_dir = 0,1
            elif num == 0:
                x_dir, y_dir = -1,0
            else:
                x_dir, y_dir = 0,-1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vec(x_dir,y_dir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [int(target[0]), int(target[1])])
        return path[1]

    # need to change this to A* Search Algorithm
    # BFS = Breadth-First-Search Algorithm
    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)] # grid 28 wide, 30 high
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1 # set that grid to be not 0
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors = [[0, -1], [1, 0], [0, 1], [-1, 0]] # up, right, down, left neighbors
                for neighbor in neighbors:
                    # if next cell >= 0, and <= length of grid for x and y
                    if neighbor[0] + current[0] >= 0 and neighbor[0] + current[0] < len(grid[0]):
                        if neighbor[1] + current[1] >= 0 and neighbor[1] + current[1] < len(grid):
                            next_cell = [neighbor[0] + current[0], neighbor[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1: # if next cell is not a wall
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        # backtracking to find shortest path
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
