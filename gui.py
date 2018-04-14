import sys
import pygame
from time import time, sleep
from piano import Piano
from speaker import Speaker
from game import GameState, FailResult


class GUI:

    _FONT_SIZE = 15
    _FONT_NAME = 'Courier'

    def __init__(self, game, scale=1):
        self._game = game
        self._scale = scale
        self._sound = Speaker('samples/%d.wav')
        self._key_numbers = dict([(key, index) for index, (key, _) in enumerate(Piano.KEYBOARD)])
        pygame.init()
        pygame.display.init()
        if not pygame.display.get_init():
            raise Exception('Can not initialize a display')
        self._font = pygame.font.SysFont(GUI._FONT_NAME, int(GUI._FONT_SIZE * self._scale))
        pygame.mouse.set_visible(False)
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._width, self._height = self._screen.get_size()
        self._init_piano()
        self._showing_message = False

    def _init_piano(self):
        self._piano = Piano(self._scale)
        piano_width, piano_height = self._piano.get_size()
        piano_x = (self._width - piano_width) / 2
        piano_y = (self._height - piano_height) / 2
        self._piano.set_position((piano_x, piano_y))
        self._beat_position = (
            self._width / 2 - 3 * GUI._FONT_SIZE * self._scale,
            self._height / 2 + piano_height
        )

    def draw(self):
        self._draw_song_name()
        self._draw_piano()
        self._draw_beat()
        pygame.display.update()
        if self._showing_message:
            self._showing_message = False
            sleep(1.5)
        self._screen.fill((0, 0, 0))

    def _show_demo(self):
        showing = True
        for key, wait in self._game.song.keys:
            if wait == 0:
                wait = 1
            button = Piano.KEYBOARD[key][0]
            self._piano.press_key(button)
            self._sound.play(key)
            start = time()
            while time() - start < wait * self._game.song.tempo / 1000:
                self.draw()
                event = pygame.event.poll()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    showing = False
                    break
            self._piano.release_key(button)
            self._sound.stop(key)
            if not showing:
                break

    def _draw_piano(self):
        for key, button in self._piano.buttons.items():
            pygame.draw.polygon(self._screen, button.get_color(), button.get_polygon())
            x, y = button.get_position()
            width, height = button.get_size()
            letter = pygame.key.name(key).upper()
            pos_x = x + width / 2 - GUI._FONT_SIZE / 3 * self._scale
            pos_y = y + (-GUI._FONT_SIZE * self._scale if button.is_black() else height)
            self._draw_text([letter], (pos_x, pos_y))

    def _draw_text(self, lines, position, color=(255, 255, 255)):
        x, y = position
        for line in lines:
            label = self._font.render(line, True, color)
            self._screen.blit(label, (x, y))
            y += GUI._FONT_SIZE

    def _draw_beat(self):
        text = 'Beat: '
        if self._get_beat_state():
            text += '█'
        self._draw_text([text], self._beat_position)

    def _get_beat_state(self):
        value = self._game.song.tempo
        return (time() * 1000) % (8 * value) > 4 * value

    def _draw_song_name(self):
        piano_x, piano_y = self._piano.get_size()
        self._draw_text([self._game.song.name], (self._width / 2 - piano_x / 2, self._height / 2 - piano_y))

    def _show_game_message(self, info):
        if self._game.state == GameState.FAIL:
            type_, (actual, expected) = info
            text = 'FAILED: '
            if type_ == FailResult.WRONG_KEY:
                text += 'Wrong key!'
            elif type_ == FailResult.WRONG_DURATION:
                text += 'Wrong duration!'
                text += ' Expected = %d, Actual = %d.' % (expected, actual)
            color = (255, 0, 0)
        elif self._game.state == GameState.SUCCESS:
            text = 'SUCCESS!'
            color = (0, 255, 0)
        else:
            return
        beat_x, beat_y = self._beat_position
        piano_x, piano_y = self._piano.get_size()
        self._draw_text([text], (beat_x - piano_x / 3, beat_y + 2 * GUI._FONT_SIZE * self._scale), color)
        self._showing_message = True

    def mainloop(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT:
                self.draw()
            if self._game.state == GameState.SUCCESS:
                return True
            elif self._game.state == GameState.FAIL:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if event.key == pygame.K_SPACE:
                    self._show_demo()
                if event.key == pygame.K_BACKSPACE:
                    return True
                self._piano.press_key(event.key)
                if event.key in self._key_numbers:
                    number = self._key_numbers[event.key]
                    info = self._game.press_key(number)
                    self._show_game_message(info)
                    self._sound.play(number)
            elif event.type == pygame.KEYUP:
                self._piano.release_key(event.key)
                if event.key in self._key_numbers:
                    self._sound.stop(self._key_numbers[event.key])
            elif event.type == pygame.QUIT:
                break
