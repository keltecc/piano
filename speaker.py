import pygame


class Speaker:

    def __init__(self, path_mask):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        self._load_sounds(path_mask)

    def play(self, number):
        self._sounds[number].play()

    def stop(self, number):
        # self._sounds[number].stop()
        pass

    def _load_sounds(self, path_mask):
        self._sounds = []
        for i in range(24):
            sound = pygame.mixer.Sound(path_mask % i)
            sound.set_volume(0.5)
            self._sounds.append(sound)
