#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# nibbles like game. much more fun, moves on all directions and jump, can be played with mouse.

from math import cos, radians, sin
from random import choice
import os
import sys

import pygame
from pygame.locals import *
from pygame.colordict import THECOLORS

import data

EGG_RATIO = 5
MAX_EGGS = 2
SNAKE_WIDTH = 4
SNAKE_INITIAL_LENGTH = 10
SNAKE_INITIAL_HEADING = 90
SNAKE_INITIAL_SPEED = 10
SNAKE_INITIAL_POSITION = (200,200)
SNAKE_COLOR = THECOLORS['green']
INITIAL_GAME_SPEED = 5

WIDTH = 400
HEIGHT = 400
RESOLUTION = (WIDTH, HEIGHT)


class SnakeBodyPart(pygame.sprite.Sprite):
    """Snake body part."""
    def __init__(self, image, position, in_body_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.in_body_position = in_body_position


class Snake:
    """Player"""
    spacing = 5
    head_img = pygame.image.load(data.load(os.path.join('images', 'head.png')))
    tail_img = pygame.image.load(data.load(os.path.join('images', 'tail.png')))
    body_img = pygame.image.load(data.load(os.path.join('images', 'body.png')))

    def __init__(self, start, sections, heading, speed, color):
        self.body = [start]
        self.body.extend(
            [
                (
                    start[0] + sin(radians(360 - heading)) * self.spacing * i,
                    start[1] + cos(radians(360 - heading)) * self.spacing * i
                ) for i in range(sections)
            ]
        )
        self.sections = sections
        self.heading = heading
        self.speed = speed
        self.color = color
        self.older = False
        self.alive = True
        self.rects = []
        self.in_air = 0
        self.bodyparts = pygame.sprite.OrderedUpdates()
        self.create_bodyparts()

    @property
    def head(self):
        return self.bodyparts.sprites()[0].rect

    @property
    def head_point(self):
        """Return the closest to heading point of head's rect"""
        if 45 < self.heading < 135:
            return self.head.midright
        elif 135 < self.heading < 225:
            return self.head.midbottom
        elif 225 < self.heading < 315:
            return self.head.midleft
        else:
            return self.head.midtop
        
    def advance(self):
        head = self.body[0]

        if self.older:
            self.older -= 1
            tail = self.body[:]
        else:
            tail = self.body[:-1]

        xinc = sin(radians(self.heading)) * self.spacing
        yinc = cos(radians(self.heading)) * self.spacing

        head = (head[0] + xinc, head[1] + yinc)
        # check if run into snakes own body and die
        # why the split?, don't consider the beginning of the body, this make the snake die when turning
        for part in self.bodyparts.sprites()[10:]:
            if not self.in_air:
                if part.rect.colliderect(self.head):
                    self.die()
        # fell down from jump
        if self.in_air:
            self.in_air -= 1

        body = []
        body.append(head)
        body.extend(tail)
        self.body = body

        self.create_bodyparts()

        # put sprites in place
        for i in range(len(tail)):
            self.bodyparts.sprites()[i].rect.topleft = self.body[i]

    def create_bodyparts(self):
        self.bodyparts.empty()
        # first head
        self.bodyparts.add(SnakeBodyPart(self.head_img, self.body[0], 0))
        # then body 
        # minus head and tail
        for i in range(1, len(self.body) - 2):
            self.bodyparts.add(SnakeBodyPart(self.body_img, self.body[i], i))
        # finally tail
        self.bodyparts.add(SnakeBodyPart(self.tail_img, self.body[-1], len(self.body)))

    def die(self):
        self.alive = False

    def grow_up(self, sections=1):
        self.older += sections

    def jump(self):
        if not self.in_air:
            self.in_air += 10


class Egg(pygame.sprite.Sprite):
    """Eggs the player collect"""
    def __init__(self, position, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.position = position
        self.eaten = False
        self.drawed = False

    def die(self):
        self.drawed = False # Get redrawed
        self.eaten = True


class Main:
    def __init__(self):
        self.window = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(RESOLUTION)
        self.background.fill(THECOLORS['white'])
        self.screen = pygame.display.get_surface()
        self.screen.fill(THECOLORS['white'])

        self.s = Snake(SNAKE_INITIAL_POSITION, SNAKE_INITIAL_LENGTH , SNAKE_INITIAL_HEADING, SNAKE_INITIAL_SPEED, SNAKE_COLOR)
        self.s.bodyparts.clear(self.screen, self.background)
        self.s.bodyparts.draw(self.screen)

        self.pos = (0,0)
        self.eggs = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.game_speed = INITIAL_GAME_SPEED
        # TODO: Loader for eggs images
        self.egg_image = pygame.image.load('data/images/egg%s.png' % choice([0]))
        self.egg_size = self.egg_image.get_width(), self.egg_image.get_height()
        self.dead_egg = pygame.Surface(self.egg_size)
        self.dead_egg.fill(THECOLORS['white'])

    def run(self):
        while self.s.alive:
            # add eggs
            while len(self.eggs) < MAX_EGGS:
                invalid = True
                # Get egg position
                while invalid:
                    position = choice(range(self.egg_size[0], WIDTH - self.egg_size[0])), choice(range(self.egg_size[1], HEIGHT - self.egg_size[1]))
                    rect = pygame.Rect(position, self.egg_size)
                    # check against eggs
                    invalid = any([egg.rect.colliderect(rect) for egg in self.eggs])
                    # check against snake
                    if not invalid:
                        invalid = any([bp.rect.colliderect(rect) for bp in self.s.bodyparts.sprites()])

                self.eggs.add(Egg(position, self.egg_image))

            # eat eggs.
            for egg in self.eggs.sprites():
                if egg.rect.colliderect(self.s.head):
                    egg.die()
                    self.s.grow_up(5)
                    self.game_speed += 1

                if not egg.drawed:
                    self.screen.blit(egg.image, egg.rect)
                    egg.drawed = True

                if egg.eaten:
                    self.screen.blit(self.dead_egg, egg.rect)
                    self.eggs.remove(egg)

            self.input(pygame.event.get())
            self.s.bodyparts.clear(self.screen, self.background)
            self.s.bodyparts.draw(self.screen)
            pygame.display.flip()

            self.s.advance()

            # fall out of screen
            if not self.screen.get_rect().collidepoint(self.s.head_point):
                self.s.die()

            self.clock.tick(self.game_speed)

    def input(self, events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == MOUSEMOTION:
                if event.pos[0] < self.pos[0]:
                    self.s.heading += 1
                else:
                    self.s.heading -= 1
                self.pos = event.pos
            elif event.type in (KEYUP, KEYDOWN):
                if event.key == K_SPACE:
                    self.s.jump()
                elif event.key == K_ESCAPE:
                    sys.exit(0)


def main():
    pygame.init()
    game = Main()
    game.run()
