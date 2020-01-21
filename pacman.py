import pygame as pg
import sys
import copy
from settings import *
from sprites import *

pg.init()
vec = pg.math.Vector2
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pacman in Pygame")
clock = pg.time.Clock()

class Game(object):
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Pacman in Pygame")
        self.clock = pg.time.Clock()
        self.playing = True
        self.state = 'menu'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.pac_pos = None
        self.load()
        self.pacman = Pacman(self, vec(self.pac_pos))
        self.make_enemies()

    def run(self):
        while self.playing:
            if self.state == 'menu':
                self.menu_events()
                self.menu_update()
                self.menu_draw()
            elif self.state == 'game':
                self.game_events()
                self.game_update()
                self.game_draw()
            elif self.state == 'over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.playing = False
            self.clock.tick(FPS)
        pg.quit()
        sys.exit()

    def update(self):
        pass

    def draw_text(self, words, screen, pos, size, color, font, centered = False):
        font = pg.font.SysFont(MENU_FONT, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pg.image.load('maze.png')
        self.background = pg.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        # create list of walls
        with open('walls.txt', 'r') as file:
            for yindex, line in enumerate(file):
                for xindex, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xindex, yindex))
                    elif char == "C":
                        self.coins.append(vec(xindex, yindex))
                    elif char == "P":
                        self.pac_pos = [xindex, yindex]
                    elif char in ["2","3","4","5"]:
                        self.e_pos.append([xindex, yindex])
                    elif char == "B":
                        pg.draw.rect(self.background, BLACK, (xindex*self.cell_width, yindex*self.cell_height,
                                                              self.cell_width, self.cell_height))

    def make_enemies(self):
        for index, pos in enumerate(self.e_pos):
            self.enemies.append(Ghosts(self, vec(pos), index))

    def draw_grid(self):
        pass
        for x in range(WIDTH//self.cell_width):
            pg.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pg.draw.line(self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))
        # draw walls
        #for wall in self.walls:
        #    pg.draw.rect(self.background, GREEN, (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width, self.cell_height))
        #for coin in self.coins:
        #    pg.draw.rect(self.background, YELLOW, (coin.x*self.cell_width, coin.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.pacman.lives = 3
        self.pacman.current_score = 0
        self.pacman.grid_pos = vec(self.pacman.starting_pos)
        self.pacman.pixel_pos = self.pacman.get_pixel_pos()
        self.pacman.dir *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pixel_pos = enemy.get_pixel_pos()
            enemy.dir *= 0
        self.coins = []
        with open("walls.txt", 'r') as file:
            for yindex, line in enumerate(file):
                for xindex, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xindex, yindex))
        self.state = 'game'

    def menu_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                if event.key == pg.K_SPACE:
                    self.state = 'game'

    def menu_update(self):
        pass

    def menu_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACEBAR TO PLAY', self.screen, [WIDTH//2, HEIGHT//2-50], MENU_TEXT_SIZE, MENU_TEXT_COLOR, MENU_FONT, centered=True)
        self.draw_text('PUSH ESCAPE TO QUIT', self.screen, [WIDTH//2, HEIGHT//2+50], MENU_TEXT_SIZE, (44, 167, 198), MENU_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [4, 0], MENU_TEXT_SIZE, WHITE, MENU_FONT)
        pg.display.update()

    def game_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.pacman.move(vec(-1,0))
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.pacman.move(vec(1,0))
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.pacman.move(vec(0,-1))
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.pacman.move(vec(0,1))

    def game_update(self):
        self.pacman.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.pacman.grid_pos:
                self.remove_life()

    def game_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        #self.draw_grid()
        self.draw_text('CURRENT SCORE: {}'.format(self.pacman.current_score), self.screen, [60, 0], 18, WHITE, MENU_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2+60, 0], 18, WHITE, MENU_FONT)
        self.pacman.draw()
        for enemy in self.enemies:
            enemy.draw()
        pg.display.update()

    def draw_coins(self):
        if self.coins == []:
            with open("walls.txt", 'r') as file:
                for yindex, line in enumerate(file):
                    for xindex, char in enumerate(line):
                        if char == 'C':
                            self.coins.append(vec(xindex, yindex))
        for coin in self.coins:
            pg.draw.circle(self.screen, GOLD, (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def remove_life(self):
        self.pacman.lives -= 1
        if self.pacman.lives == 0:
            self.state = 'over'
        else:
            self.pacman.grid_pos = vec(self.pacman.starting_pos)
            self.pacman.pixel_pos = self.pacman.get_pixel_pos()
            self.pacman.dir *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pixel_pos = enemy.get_pixel_pos()
                enemy.dir *= 0

    def game_over_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                if event.key == pg.K_SPACE:
                    self.reset()

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER!", self.screen, [WIDTH//2, 100], 52, RED, "arial", centered=True)
        reset_text = "Press space to play again"
        quit_text = "or press escape to quit"
        self.draw_text(reset_text, self.screen, [WIDTH// 2, HEIGHT//2], 36, GREY, "arial", centered=True)
        self.draw_text(quit_text, self.screen, [WIDTH// 2, HEIGHT//1.5], 36, GREY, "arial", centered=True)
        pg.display.update()


g = Game()
g.run()