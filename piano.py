import pygame

from button import Button, ButtonTypes


class Piano:

    KEYBOARD = [
        (pygame.K_z, ButtonTypes.WHITE_LEFT),
        (pygame.K_s, ButtonTypes.BLACK),
        (pygame.K_x, ButtonTypes.WHITE_CENTER),
        (pygame.K_d, ButtonTypes.BLACK),
        (pygame.K_c, ButtonTypes.WHITE_RIGHT),
        (pygame.K_v, ButtonTypes.WHITE_LEFT),
        (pygame.K_g, ButtonTypes.BLACK),
        (pygame.K_b, ButtonTypes.WHITE_CENTER),
        (pygame.K_h, ButtonTypes.BLACK),
        (pygame.K_n, ButtonTypes.WHITE_CENTER),
        (pygame.K_j, ButtonTypes.BLACK),
        (pygame.K_m, ButtonTypes.WHITE_RIGHT),
        (pygame.K_q, ButtonTypes.WHITE_LEFT),
        (pygame.K_2, ButtonTypes.BLACK),
        (pygame.K_w, ButtonTypes.WHITE_CENTER),
        (pygame.K_3, ButtonTypes.BLACK),
        (pygame.K_e, ButtonTypes.WHITE_RIGHT),
        (pygame.K_r, ButtonTypes.WHITE_LEFT),
        (pygame.K_5, ButtonTypes.BLACK),
        (pygame.K_t, ButtonTypes.WHITE_CENTER),
        (pygame.K_6, ButtonTypes.BLACK),
        (pygame.K_y, ButtonTypes.WHITE_CENTER),
        (pygame.K_7, ButtonTypes.BLACK),
        (pygame.K_u, ButtonTypes.WHITE_RIGHT)
    ]

    def __init__(self, scale=1):
        self.buttons = dict()
        offset = 0
        for key, type_ in Piano.KEYBOARD:
            self.buttons[key] = Button(type_, offset, scale)
            offset += ButtonTypes.get_offset(type_)
        self._width = offset * scale
        self._height = max([max([y for _, y in button.get_polygon()]) for button in self.buttons.values()])

    def get_size(self):
        return self._width, self._height

    def set_position(self, position):
        for button in self.buttons.values():
            button.set_position(position)

    def press_key(self, key):
        if key in self.buttons:
            self.buttons[key].pressed = True

    def release_key(self, key):
        if key in self.buttons:
            self.buttons[key].pressed = False
