# Credit to https://github.com/phouse512

import enum
import os
import time


@enum.unique
class Button(enum.Enum):
    A = 'a'
    B = 'b'
    X = 'x'
    Y = 'y'
    Z = 'z'
    START = 'start'
    L = 'l'
    R = 'r'
    D_UP = 'd_up'
    D_DOWN = 'd_down'
    D_LEFT = 'd_left'
    D_RIGHT = 'd_right'


@enum.unique
class Trigger(enum.Enum):
    L = 'l'
    R = 'r'

@enum.unique
class Stick(enum.Enum):
    MAIN = 'main'
    C = 'c'

@enum.unique
class Direction(enum.Enum):
    DOWN = (.5, 1)
    UP = (.5, 0)
    LEFT = (0, .5)
    RIGHT = (1, .5)
    DOWN_LEFT = (0, 1)
    DOWN_RIGHT = (1, 1)
    UP_LEFT = (0, 0)
    UP_RIGHT = (1, 0)
    NEUTRAL = (.5, .5)

class Controller:
    """ Writes controller inputs to pipe """

    def __init__(self, path):
        """ opens the fifo """
        self.pipe = None
        try:
            os.mkfifo(path)
        except OSError:
            print("failure")
            pass
        self.pipe = open(path, 'w', buffering=1)

    def __del__(self):
        if self.pipe:
            self.pipe.close()

    def _press_button(self, button):
        """ press a button, here button is the Button enum """
        assert button in Button
        self.pipe.write('PRESS {}\n'.format(button.name))

    def _release_button(self, button):
        """ release button, button is the Button enum """
        assert button in Button
        self.pipe.write('RELEASE {}\n'.format(button.name))

    def _tilt_stick(self, stick, x, y):
        assert stick in Stick
        assert 0 <= x <= 1 and 0 <= y <= 1
        self.pipe.write('SET {} {:.2f} {:.2f}\n'.format(stick.name, x, y))

    def tilt_control(self, stick, direction):
        assert stick in Stick
        assert direction in Direction
        self._tilt_stick(stick, direction.value[0], direction.value[1])
        time.sleep(.3)
        self._tilt_stick(stick, Direction.NEUTRAL.value[0], Direction.NEUTRAL.value[1])

    def tilt_attack(self, stick, direction, button):
        assert stick in Stick
        assert direction in Direction
        assert button in Button
        self._tilt_stick(stick, direction.value[0], direction.value[1])
        self._press_button(button)
        time.sleep(.1)
        self._tilt_stick(stick, Direction.NEUTRAL.value[0], Direction.NEUTRAL.value[1])
        self._release_button(button)

    def smash_attack(self, direction):
        assert direction in Direction
        self._tilt_stick(Stick.MAIN, direction.value[0], direction.value[1])
        self._press_button(Button.A)
        time.sleep(.3)
        self._tilt_stick(Stick.MAIN, Direction.NEUTRAL.value[0], Direction.NEUTRAL.value[1])
        self._release_button(Button.A)

    def hit_button(self, button):
        print("hitting %s" % button.value)
        self._press_button(button)
        time.sleep(.25)
        self._release_button(button)

    def performCommand(self, message):
        if message == 'a':
            self.hit_button(Button.A)
        elif message == 'b':
            self.hit_button(Button.B)
        elif message == 'grab':
            self.hit_button(Button.Z)
        elif message == 'left':
            self.tilt_control(Stick.MAIN, Direction.LEFT)
        elif message == 'right':
            self.tilt_control(Stick.MAIN, Direction.RIGHT)
        elif message == 'crouch':
            self.tilt_control(Stick.MAIN, Direction.DOWN)
        elif message == 'jump':
            self.hit_button(Button.X)
        elif message == 'doublejump':
            self.hit_button(Button.X)
            self.hit_button(Button.X)
        elif message == 'tiltup':
            self.tilt_attack(Stick.MAIN, Direction.UP, Button.A)
        elif message == 'tiltdown':
            self.tilt_attack(Stick.MAIN, Direction.DOWN, Button.A)
        elif message == 'tiltleft':
            self.tilt_attack(Stick.MAIN, Direction.LEFT, Button.A)
        elif message == 'tiltright':
            self.tilt_attack(Stick.MAIN, Direction.RIGHT, Button.A)
        elif message == 'specialup':
            self.tilt_attack(Stick.MAIN, Direction.UP, Button.B)
        elif message == 'specialdown':
            self.tilt_attack(Stick.MAIN, Direction.DOWN, Button.B)
        elif message == 'specialleft':
            self.tilt_attack(Stick.MAIN, Direction.LEFT, Button.B)
        elif message == 'specialright':
            self.tilt_attack(Stick.MAIN, Direction.RIGHT, Button.B)
        elif message == 'airup':
            self.hit_button(Button.X)
            self.tilt_attack(Stick.MAIN, Direction.UP, Button.A)
        elif message == 'airdown':
            self.hit_button(Button.X)
            self.tilt_attack(Stick.MAIN, Direction.DOWN, Button.A)
        elif message == 'airleft':
            self.hit_button(Button.X)
            self.tilt_attack(Stick.MAIN, Direction.LEFT, Button.A)
        elif message == 'airright':
            self.hit_button(Button.X)
            self.tilt_attack(Stick.MAIN, Direction.RIGHT, Button.A)
        elif message == 'smashup':
            self.smash_attack(Direction.UP)
        elif message == 'smashdown':
            self.smash_attack(Direction.DOWN)
        elif message == 'smashleft':
            self.smash_attack(Direction.LEFT)
        elif message == 'smashright':
            self.smash_attack(Direction.RIGHT)
