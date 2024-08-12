import pygame as pg
from monster import Monster
from pyautogui import size


class App:
    def __init__(self):
        self.size = self.width, self.height = tuple(size())
        self.sc = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.just_show = True

        self.monsters = tuple(Monster(self, self.just_show) for _ in range(3))

    def run(self):
        pg.init()

        while True:
            self.clock.tick(self.fps)
            [exit() for event in pg.event.get() if event.type == pg.QUIT]

            self.sc.fill((0, 0, 0))

            [monster.update() for monster in self.monsters]

            pg.display.flip()
            pg.display.set_caption(f"FPS: {self.clock.get_fps()}")


if __name__ == '__main__':
    App().run()
