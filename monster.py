import pygame as pg
from pyautogui import size
from random import randint
from typing import Literal
import math


class Leg:
    def __init__(self, part: 'Part', monster: 'Monster', app, type_: Literal["right", "left"]):
        self.app = app
        self.part = part
        self.monster = monster
        self.s_pos: list[float] = self.part.pos.copy()
        self.type = type_
        self.c_pos = self.s_pos.copy()  # center pos
        self.l_pos = [10, 10] # last pos

        self.c_rad = self.part.rad * 2 / 3
        self.l_rad = self.c_rad * 2 / 3
        self.change = False

    def set_l_pos(self):
        distance = math.sqrt(sum((self.l_pos[i] - self.s_pos[i]) ** 2 for i in range(2)))

        if distance < (self.c_rad + self.l_rad) * 10:
            return

        last = self.monster.points[self.part.index - 1]
        vector = list(last.pos[i] - self.part.pos[i] for i in range(2))

        rand_vec = [randint(int(self.c_rad) * 5, int(self.c_rad) * 10) *
                    (1 if self.type == "right" else -1)
                    for _ in range(2)]

        self.l_pos = [vector[i] - rand_vec[i] + self.s_pos[i] for i in range(2)]

    def set_s_pos(self):
        self.s_pos = self.part.pos

    def set_c_pos(self):
        cen = [((self.s_pos[i] - self.l_pos[i]) / 2) + self.l_pos[i] for i in range(2)]

        # l_dis = math.sqrt(sum((self.c_pos[i] - self.l_pos[i]) ** 2 for i in range(2)))
        # s_dis = math.sqrt(sum((self.c_pos[i] - self.s_pos[i]) ** 2 for i in range(2)))

        for i in range(2):
            self.c_pos[i] += (cen[i] - self.c_pos[i]) * self.monster.smooth * 1.5

    def get_pos(self) -> list[float]:
        return self.monster.pos

    def draw(self):
        pg.draw.line(
            self.app.sc,
            self.part.color,
            self.s_pos,
            self.c_pos,
            int(self.c_rad)
        )

        pg.draw.line(
            self.app.sc,
            self.part.color,
            self.c_pos,
            self.l_pos,
            int(self.l_rad)
        )

        pg.draw.circle(
            self.app.sc,
            self.part.color,
            self.c_pos,
            self.c_rad
        )

        pg.draw.circle(
            self.app.sc,
            self.part.color,
            self.l_pos,
            self.c_rad
        )

        # if self.part.index != 1:
        #     pg.draw.line(
        #         self.app.sc,
        #         self.part.color,
        #         self.l_pos,
        #         self.s_pos,
        #         int(self.l_rad)
        #     )

        ...

    def update(self):
        self.set_s_pos()
        self.set_l_pos()
        self.set_c_pos()

        self.draw()


class Part:
    def __init__(self, monster: 'Monster', app, index, type_: Literal["t", "p"]):
        self.monster = monster
        self.index = index
        self.app = app
        self.pos: list[float] = [randint(0, self.app.size[i]) for i in range(2)]
        self.color = 255, 255, 255
        self.rad = self.monster.rad / (self.monster.point_count / (self.monster.point_count - self.index + 1))
        self.type = type_

        if self.type == "p" and self.index != 1:
            self.legs = tuple(Leg(self, self.monster, self.app, type__) for type__ in ("right", "left"))
        else:
            self.legs = tuple()

    def draw(self):
        pass

    def key_update(self):
        last = self.monster.points[self.index - 1]
        all_dis = math.sqrt(sum((self.pos[i] - last.pos[i]) ** 2 for i in range(2)))

        if all_dis <= self.rad + last.rad + 10:
            return True

        for i in range(2):
            distance = self.pos[i] - last.pos[i]
            self.pos[i] -= self.monster.smooth * distance

        if all_dis > (self.rad + self.monster.points[self.index - 1].rad) * 2 + 2 and self.index != 1:
            self.key_update()

    def update(self):
        self.key_update()
        [leg.update() for leg in self.legs]

        pg.draw.circle(self.app.sc, self.color, self.pos, self.rad)

        if self.index != 1:
            pg.draw.line(
                self.app.sc,
                self.color,
                self.pos,
                self.monster.points[self.index - 1].get_pos(),
                width=int(self.rad / 2) + 1
            )

    def set_pos(self, pos: list[float]):
        self.pos = pos

    def get_pos(self):
        return self.pos


class Monster:
    def __init__(self, app, just_show: bool):
        self.just_show = just_show
        self.app = app
        self.smooth = 0.08 if self.just_show else 0.1
        self.mouse_pos: list[float, float] = list(pg.mouse.get_pos())
        self.pos: list[float] = [float(randint(0, self.app.size[i])) for i in range(2)]
        self.point_count = 35
        self.tail_index = 15
        self.rad = 10
        self.points: tuple[Part, ...] = tuple(Part(self, self.app, i, "p" if i < self.tail_index else "t")
                                              for i in range(self.point_count + 1))

    def set_mouse_pos(self):
        if self.just_show:

            distance = math.sqrt(sum((self.mouse_pos[i] - self.points[1].pos[i]) ** 2 for i in range(2)))
            if distance <= self.rad * 5:
                self.mouse_pos = [randint(0, self.app.size[i]) for i in range(2)]
            return

        self.mouse_pos = list(pg.mouse.get_pos())

    def update(self):
        self.set_mouse_pos()
        self.points[0].set_pos(self.mouse_pos)

        for point in self.points[1:]:
            point.update()
            point.draw()
