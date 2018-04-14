from time import time
from enum import Enum
from songs import Song


class GameState(Enum):

    NONE = 0
    RUNNING = 1
    SUCCESS = 2
    FAIL = 3


class FailResult(Enum):

    WRONG_KEY = 0
    WRONG_DURATION = 1


class Difficulty:

    def __init__(self, error_duration, miss_count):
        self.error_duration = error_duration
        self.miss_count = miss_count


class Game:

    def __init__(self, song, difficulty):
        self.state = GameState.NONE
        self.song = song
        self.difficulty = difficulty
        self._previous_time = None
        self._next_key_index = 0
        self._misses = 0

    def press_key(self, number):
        if self.state == GameState.NONE:
            expected_key, _ = self.song.keys[0]
            if number != expected_key:
                self.state = GameState.FAIL
                return FailResult.WRONG_KEY, (None, None)
            self._previous_time = time()
            self._next_key_index += 1
            self.state = GameState.RUNNING
            return
        if self.state != GameState.RUNNING:
            return

        current = time()
        player_time = (current - self._previous_time) * 1000
        self._previous_time = current
        expected_key, _ = self.song.keys[self._next_key_index]
        _, perfect_time = self.song.keys[self._next_key_index - 1]
        if expected_key != number:
            if self._misses >= self.difficulty.miss_count:
                self.state = GameState.FAIL
                return FailResult.WRONG_KEY, (None, None)
            self._misses += 1
        if abs(player_time - perfect_time * self.song.tempo) > self.difficulty.error_duration:
            self.state = GameState.FAIL
            return FailResult.WRONG_DURATION, (player_time, perfect_time * self.song.tempo)
        self._next_key_index += 1
        if self._next_key_index >= len(self.song.keys):
            self.state = GameState.SUCCESS


class FreeGame:
    def __init__(self):
        self.state = GameState.RUNNING
        self.difficulty = Difficulty(0, 0)
        self.song = Song('Free playing', [], 200)

    def press_key(self, number):
        return
